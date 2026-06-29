"""
Session 4.3: Fact-Checking Agent (Pro Path Starter)

Build a fact-checking agent that:
1. Takes a claim as input
2. Researches supporting and contradicting evidence
3. Handles conflicting sources
4. Scores veracity (0-100%)
5. Returns a structured report

This is a harder version that requires handling ambiguity and evidence conflicts.
"""

from anthropic import Anthropic
from dataclasses import dataclass

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
    """Simulate a search that returns multiple sources."""
    query_lower = query.lower()
    for topic, sources in SOURCES.items():
        if any(word in query_lower for word in topic.split()):
            # Return all sources for this topic (simulating multiple results)
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
    supporting_evidence: list
    contradicting_evidence: list
    conflicting_sources: list
    reasoning: str
    confidence: int  # How confident are we? 0-100

def run_fact_checker(claim: str) -> FactCheckResult:
    """
    Run a fact-checking agent on a claim.
    
    TODO: Implement the agent loop that:
    1. Plans searches to verify the claim
    2. Searches for supporting evidence
    3. Searches for contradicting evidence
    4. Identifies conflicts
    5. Scores the claim's veracity
    6. Returns a structured FactCheckResult
    
    Hints:
    - The agent needs to understand the difference between "supporting" and "contradicting"
    - Build working memory to track evidence buckets
    - Implement stopping: when evidence is clear (or clearly conflicting), stop
    - Have the agent output a JSON-like summary at the end with:
      {"veracity_score": X, "confidence": Y, "key_findings": [...], "conflicts": [...]}
    """
    
    messages = []
    
    # TODO 1: Create a planning prompt for fact-checking
    # The agent should:
    #   1. Break down the claim into verifiable parts
    #   2. Plan searches for supporting evidence
    #   3. Plan searches for contradicting evidence
    #   4. Plan how to identify conflicts
    plan_prompt = f"""TODO: Create a planning prompt for fact-checking the claim: "{claim}"
Ask the agent to identify verifiable parts and plan searches."""
    
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
    
    # TODO 2: Implement the evidence-gathering loop
    # The agent should:
    #   - Search for supporting evidence
    #   - Search for contradicting evidence
    #   - Identify and flag conflicts
    #   - Stop when it has enough to make a judgment
    # TODO 2 START
    evidence = {
        "supporting": [],
        "contradicting": [],
        "conflicts": []
    }
    
    messages.append({"role": "user", "content": "TODO: Write a prompt to execute the fact-check plan"})
    
    max_iterations = 8
    for iteration in range(max_iterations):
        print(f"--- Iteration {iteration + 1} ---")
        
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=2048,
            tools=TOOLS,
            messages=messages
        )
        
        # TODO: Extract tool calls and text (same pattern as core path)
        tool_calls = []  # TODO: Implement
        text_blocks = []  # TODO: Implement
        
        if not tool_calls:
            print("Fact-checking complete.")
            break
        
        messages.append({"role": "assistant", "content": response.content})
        
        tool_results = []
        for tool_call in tool_calls:
            result = process_tool_call(tool_call.name, tool_call.input)
            print(f"  Search: {tool_call.input.get('query', 'N/A')}")
            # TODO: Categorize result as supporting/contradicting/conflict
            # For now, just collect it
            evidence["supporting"].append(result)
            
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result
            })
        
        messages.append({"role": "user", "content": tool_results})
    
    # TODO 2 END
    
    # TODO 3: Parse the agent's final judgment
    # Ask the agent to output a JSON-structured summary:
    # {
    #   "veracity_score": 0-100,
    #   "confidence": 0-100,
    #   "reasoning": "...",
    #   "conflicts_found": ["...", "..."]
    # }
    
    final_judgment_prompt = """TODO: Ask the agent to output its final fact-check judgment as structured JSON"""
    messages.append({"role": "user", "content": final_judgment_prompt})
    
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        messages=messages
    )
    
    judgment_text = "".join([block.text for block in response.content if hasattr(block, "text")])
    print(f"\nJudgment:\n{judgment_text}")
    
    # TODO 3 END: Parse judgment_text as JSON and create a FactCheckResult
    
    # For now, return a placeholder
    return FactCheckResult(
        claim=claim,
        veracity_score=50,
        supporting_evidence=evidence["supporting"],
        contradicting_evidence=evidence["contradicting"],
        conflicting_sources=evidence["conflicts"],
        reasoning="TODO: Parse from agent output",
        confidence=50
    )

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
        print(f"\nVeracity Score: {result.veracity_score}/100")
        print(f"Confidence: {result.confidence}/100")
