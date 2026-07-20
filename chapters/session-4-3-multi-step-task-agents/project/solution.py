"""
Session 4.3: Fact-Checking Agent - Reference Solution (Pro Path)

A complete, working implementation of a fact-checking agent that:
- Plans searches to verify a claim (explicit planning)
- Gathers evidence via a tool-calling loop, logging every raw result
- Asks the model for a single structured JSON judgment at the end, letting it
  split the evidence into supporting / contradicting / conflicting -- since by
  that point it has the full context of every search result, which we don't
- Parses that judgment into a FactCheckResult dataclass

Setup:
    pip install anthropic
    export ANTHROPIC_API_KEY="your-api-key-here"
"""

from anthropic import Anthropic
from dataclasses import dataclass, field
import json

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

TOOLS = [
    {
        "name": "search_web",
        "description": "Search for information to verify a claim.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    }
]

# Simulated sources with conflicting info
SOURCES = {
    "gpt-4 release date": [
        "OpenAI released GPT-4 on March 14, 2023.",
        "GPT-4 launched March 2023.",
        "Some sources claim GPT-4 early access was February 2023."
    ],
    "python most popular language 2024": [
        "Python is the most popular programming language according to TIOBE index (2024).",
        "Some rankings show JavaScript more popular in web development.",
        "Python leads in data science and AI, JavaScript in web apps."
    ],
    "ai model training cost": [
        "Training GPT-4 cost an estimated $100M.",
        "Some estimates put it at $50-100M.",
        "Exact costs are proprietary and not publicly confirmed."
    ]
}

def search_web(query: str) -> str:
    """Simulate a search that returns multiple sources (some of which disagree)."""
    query_lower = query.lower()
    for topic, sources in SOURCES.items():
        if any(word in query_lower for word in topic.split()):
            return "\n".join([f"- {source}" for source in sources])
    return f"No sources found for '{query}'."

def process_tool_call(tool_name: str, tool_input: dict) -> str:
    if tool_name == "search_web":
        return search_web(tool_input["query"])
    return f"Unknown tool: {tool_name}"

@dataclass
class FactCheckResult:
    """Structured result from fact-checking."""
    claim: str
    veracity_score: int  # 0-100
    confidence: int  # 0-100
    supporting_evidence: list = field(default_factory=list)
    contradicting_evidence: list = field(default_factory=list)
    conflicting_sources: list = field(default_factory=list)
    reasoning: str = ""

def _extract_json(text: str) -> dict:
    """
    Pull the first {...} JSON object out of a model response and parse it.
    Models occasionally wrap JSON in a sentence or a code fence even when
    told not to -- this is a defensive extraction, not a strict parser.
    """
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        return {}
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError:
        return {}

def run_fact_checker(claim: str, max_iterations: int = 8) -> FactCheckResult:
    """
    Run a fact-checking agent on a claim.

    Phase 1 (plan): the agent breaks the claim into verifiable parts and
    plans searches -- without executing any yet.
    Phase 2 (execute): a standard tool-calling loop, logging every raw
    {query, result} pair. We deliberately do NOT try to categorize evidence
    as supporting/contradicting while it comes in -- a single search result
    can contain both, and the model is in a far better position to make that
    call once it has seen everything.
    Phase 3 (judge): a final, tools-off call asking for one structured JSON
    verdict, which we parse into a FactCheckResult.
    """

    messages = []
    evidence_log = []  # raw, uncategorized: [{"query": ..., "result": ...}, ...]

    # PHASE 1: Planning
    plan_prompt = f"""You are a fact-checking agent. A claim has been submitted for verification:

"{claim}"

Break the claim down into its verifiable parts. Then plan the searches you will
run to find both supporting evidence and contradicting evidence -- include at
least one search phrased in a way likely to surface disagreement between
sources. Do NOT search yet -- just plan."""

    messages.append({"role": "user", "content": plan_prompt})
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        tools=TOOLS,
        messages=messages
    )

    plan_text = "".join([block.text for block in response.content if hasattr(block, "text")])
    print(f"Fact-check plan:\n{plan_text}\n")
    messages.append({"role": "assistant", "content": response.content})

    # PHASE 2: Evidence gathering
    execution_prompt = """Now execute your plan. Use the search_web tool to gather evidence -- both
supporting and contradicting -- for the claim. Search from multiple angles.
Stop calling tools once you have enough evidence (supporting, contradicting,
or clearly conflicting) to make a confident judgment."""
    messages.append({"role": "user", "content": execution_prompt})

    stopped_naturally = False
    for iteration in range(max_iterations):
        print(f"--- Iteration {iteration + 1} ---")

        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=2048,
            tools=TOOLS,
            messages=messages
        )

        tool_calls = [block for block in response.content if hasattr(block, "type") and block.type == "tool_use"]

        if not tool_calls:
            print("Evidence-gathering complete (agent stopped calling tools).")
            stopped_naturally = True
            break

        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for tool_call in tool_calls:
            query = tool_call.input.get("query", "")
            result = process_tool_call(tool_call.name, tool_call.input)
            evidence_log.append({"query": query, "result": result})
            print(f"  Search: {query}")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result
            })

        messages.append({"role": "user", "content": tool_results})

    if not stopped_naturally:
        print("Max iterations reached -- proceeding to judgment with the evidence gathered so far.")

    # PHASE 3: Final structured judgment
    judgment_prompt = """Based on all the evidence you've gathered, output your final fact-check
judgment as a single JSON object with exactly these keys and nothing else
(no prose before or after it):

{
  "veracity_score": <int 0-100, how true the claim appears to be>,
  "confidence": <int 0-100, how confident you are in that score given the evidence>,
  "supporting_evidence": ["short strings summarizing evidence that supports the claim"],
  "contradicting_evidence": ["short strings summarizing evidence against the claim"],
  "conflicts": ["short strings describing any sources that disagreed with each other"],
  "reasoning": "two or three sentences explaining the score"
}"""
    messages.append({"role": "user", "content": judgment_prompt})

    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        messages=messages
    )

    judgment_text = "".join([block.text for block in response.content if hasattr(block, "text")])
    print(f"\nJudgment:\n{judgment_text}")

    parsed = _extract_json(judgment_text)

    return FactCheckResult(
        claim=claim,
        veracity_score=int(parsed.get("veracity_score", 50)),
        confidence=int(parsed.get("confidence", 0)),
        supporting_evidence=parsed.get("supporting_evidence", []),
        contradicting_evidence=parsed.get("contradicting_evidence", []),
        conflicting_sources=parsed.get("conflicts", []),
        reasoning=parsed.get("reasoning", "Could not parse a structured judgment from the model's output."),
    )

def print_result(result: FactCheckResult) -> None:
    print("\n" + "=" * 70)
    print("FACT-CHECK RESULT")
    print("=" * 70)
    print(f"Claim:      {result.claim}")
    print(f"Veracity:   {result.veracity_score}/100")
    print(f"Confidence: {result.confidence}/100")
    print(f"\nSupporting evidence:")
    for item in result.supporting_evidence:
        print(f"  + {item}")
    print(f"\nContradicting evidence:")
    for item in result.contradicting_evidence:
        print(f"  - {item}")
    if result.conflicting_sources:
        print(f"\nConflicts between sources:")
        for item in result.conflicting_sources:
            print(f"  ! {item}")
    print(f"\nReasoning: {result.reasoning}")
    print("=" * 70)

# Test
if __name__ == "__main__":
    claims = [
        "GPT-4 was released in March 2023",
        "Python is the most popular programming language",
        "AI model training is free"
    ]

    for claim in claims:
        print(f"\n{'='*60}")
        print(f"Fact-checking: {claim}")
        print('='*60)
        result = run_fact_checker(claim)
        print_result(result)
