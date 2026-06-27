"""
Session 2.6 Exercise — Customer Support Reply Generator with Tone Control
(REFERENCE SOLUTION)

This is the answer key. Look at support_reply_generator.py first and try
it yourself before reading this file.

WHAT THIS BUILD INTEGRATES FROM THE WEEK:
  - 2.1: clarity, context, constraints, format specification baked into
         one cohesive prompt
  - 2.2: few-shot tone examples + role prompting ("You are a customer
         support assistant...")
  - 2.3: chain-of-thought reasoning, deliberately kept invisible to the
         end user in the final output
  - 2.4: a strict JSON schema contract + defensive parsing of the result
  - 2.5: the prompt lives as a named, documented, reusable template
"""

import json
import os
import re
from typing import Optional, TypedDict


# ---------------------------------------------------------------------------
# Step 1: The structured output contract (Session 2.4)
# ---------------------------------------------------------------------------

VALID_TONES = ("empathetic", "professional", "concise")
VALID_CONFIDENCE = ("high", "medium", "low")


class SupportReply(TypedDict):
    reply_body: str
    tone_applied: str
    confidence: str
    escalate: bool
    escalation_reason: Optional[str]


REPLY_SCHEMA_DESCRIPTION = """{
  "reply_body": "string",
  "tone_applied": "empathetic | professional | concise",
  "confidence": "high | medium | low",
  "escalate": true | false,
  "escalation_reason": "string or null"
}"""


# ---------------------------------------------------------------------------
# Step 2: The prompt template (Sessions 2.1, 2.2, 2.3, 2.5)
# ---------------------------------------------------------------------------

TONE_EXAMPLES = """- Empathetic: "I completely understand how frustrating this must be, and I'm sorry for the trouble this has caused."
- Professional: "Thank you for reaching out. I've reviewed your account and can confirm the following."
- Concise: "Here's how to do that: go to Settings > Export > CSV."
"""

REASONING_INSTRUCTIONS = """Before answering, think step by step about:
(1) what the customer is actually asking for,
(2) how urgent or sensitive this situation is,
(3) whether a standard reply is sufficient, or this needs human escalation.
Do this reasoning internally -- do NOT include your step-by-step reasoning
in the final output. Only the final JSON should be visible in your response."""

SUPPORT_REPLY_TEMPLATE = """You are a customer support assistant for a
software company. Read the ticket below, decide on the right tone, reason
through whether this needs human escalation, then draft a reply.

Tone examples:
{tone_examples}

{reasoning_instructions}

Respond with ONLY valid JSON matching this schema, and nothing else:
{schema}

Ticket:
{ticket_text}
"""


def build_prompt(ticket_text: str, tone: str) -> str:
    if tone not in VALID_TONES:
        raise ValueError(
            f"Invalid tone '{tone}'. Expected one of {VALID_TONES}."
        )
    return SUPPORT_REPLY_TEMPLATE.format(
        tone_examples=TONE_EXAMPLES,
        reasoning_instructions=REASONING_INSTRUCTIONS,
        schema=REPLY_SCHEMA_DESCRIPTION,
        ticket_text=ticket_text,
    )


# ---------------------------------------------------------------------------
# Step 3: Calling the model
# ---------------------------------------------------------------------------

def call_llm(prompt: str) -> str:
    """Requires ANTHROPIC_API_KEY and USE_REAL_LLM=1 to call the real API."""
    if os.environ.get("USE_REAL_LLM") == "1":
        import anthropic

        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    # Offline stub: deliberately messy (markdown-fenced) response, the way
    # real models sometimes respond even when told "ONLY valid JSON."
    return """```json
{
  "reply_body": "I completely understand how frustrating this must be, and I'm sorry for the trouble. I've checked your account and the duplicate charge will be refunded within 3-5 business days.",
  "tone_applied": "empathetic",
  "confidence": "high",
  "escalate": false,
  "escalation_reason": null
}
```"""


# ---------------------------------------------------------------------------
# Step 4: Defensive parsing (Session 2.4, applied again)
# ---------------------------------------------------------------------------

def parse_reply(raw_response: str) -> SupportReply:
    # 1. Strip markdown code fences if present.
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", raw_response, re.DOTALL)
    json_text = fence_match.group(1) if fence_match else raw_response.strip()

    # 2. Parse as JSON.
    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Could not parse model response as JSON: {e}")

    if not isinstance(data, dict):
        raise ValueError(f"Expected a JSON object, got {type(data).__name__}")

    # 3. Validate every field.
    reply_body = data.get("reply_body")
    if not isinstance(reply_body, str) or not reply_body.strip():
        raise ValueError("reply_body must be a non-empty string")

    tone_applied = data.get("tone_applied")
    if tone_applied not in VALID_TONES:
        raise ValueError(
            f"tone_applied was {tone_applied!r}, expected one of {VALID_TONES}"
        )

    confidence = data.get("confidence")
    if confidence not in VALID_CONFIDENCE:
        raise ValueError(
            f"confidence was {confidence!r}, expected one of {VALID_CONFIDENCE}"
        )

    escalate = data.get("escalate")
    if not isinstance(escalate, bool):
        raise ValueError(f"escalate must be a bool, got {type(escalate).__name__}")

    escalation_reason = data.get("escalation_reason")
    if escalation_reason is not None and not isinstance(escalation_reason, str):
        raise ValueError("escalation_reason must be a string or null")

    # 4. Logical consistency: escalate=True requires a real reason.
    if escalate and not (escalation_reason and escalation_reason.strip()):
        raise ValueError(
            "escalate is True but escalation_reason is missing or empty -- "
            "an escalation must always include a reason"
        )

    return SupportReply(
        reply_body=reply_body,
        tone_applied=tone_applied,
        confidence=confidence,
        escalate=escalate,
        escalation_reason=escalation_reason,
    )


# ---------------------------------------------------------------------------
# Step 5: Wiring it together, with a safe fallback
# ---------------------------------------------------------------------------

def generate_reply(ticket_text: str, tone: str) -> SupportReply:
    prompt = build_prompt(ticket_text, tone)
    raw = call_llm(prompt)
    try:
        return parse_reply(raw)
    except ValueError as e:
        print(f"[generate_reply] Falling back to escalation due to: {e}")
        return SupportReply(
            reply_body="",
            tone_applied=tone,
            confidence="low",
            escalate=True,
            escalation_reason=(
                "Automated reply generation failed validation; "
                "needs human review."
            ),
        )


# ---------------------------------------------------------------------------
# Offline tests (no API key required)
# ---------------------------------------------------------------------------

SAMPLE_TICKETS = [
    {
        "ticket_text": "I was charged twice for my subscription this month and I'm really annoyed, this is the second time this has happened!",
        "tone": "empathetic",
    },
    {
        "ticket_text": "How do I export my project data as a CSV file?",
        "tone": "concise",
    },
    {
        "ticket_text": "Could you clarify your data retention policy for deleted accounts? I need this for a compliance review.",
        "tone": "professional",
    },
]


def offline_test():
    print("=== Testing build_prompt() ===")
    prompt = build_prompt(SAMPLE_TICKETS[0]["ticket_text"], "empathetic")
    assert SAMPLE_TICKETS[0]["ticket_text"] in prompt
    assert "empathetic" in prompt.lower()
    print("build_prompt() produced a prompt containing the ticket text.\n")

    print("=== Testing build_prompt() tone validation ===")
    try:
        build_prompt("some ticket", "angry")
        raise AssertionError("Expected build_prompt() to reject an invalid tone")
    except ValueError:
        print("Correctly raised ValueError for an invalid tone.\n")

    print("=== Testing parse_reply() on a well-formed (but fenced) response ===")
    fenced_response = """```json
{
  "reply_body": "Thanks for reaching out -- here's how to export your data.",
  "tone_applied": "concise",
  "confidence": "high",
  "escalate": false,
  "escalation_reason": null
}
```"""
    parsed = parse_reply(fenced_response)
    assert parsed["tone_applied"] == "concise"
    assert parsed["escalate"] is False
    print("Correctly parsed a markdown-fenced JSON response.\n")

    print("=== Testing parse_reply() rejects an invalid tone value ===")
    bad_tone_response = json.dumps({
        "reply_body": "Some reply.",
        "tone_applied": "happy",
        "confidence": "high",
        "escalate": False,
        "escalation_reason": None,
    })
    try:
        parse_reply(bad_tone_response)
        raise AssertionError("Expected parse_reply() to reject an invalid tone_applied")
    except ValueError:
        print("Correctly raised ValueError for an invalid tone_applied value.\n")

    print("=== Testing parse_reply() rejects escalate=True with no reason ===")
    inconsistent_response = json.dumps({
        "reply_body": "Some reply.",
        "tone_applied": "professional",
        "confidence": "low",
        "escalate": True,
        "escalation_reason": None,
    })
    try:
        parse_reply(inconsistent_response)
        raise AssertionError("Expected parse_reply() to reject escalate=True with no reason")
    except ValueError:
        print("Correctly raised ValueError for the escalate/escalation_reason inconsistency.\n")

    print("=== Testing parse_reply() rejects malformed JSON ===")
    try:
        parse_reply("This is not JSON at all.")
        raise AssertionError("Expected parse_reply() to reject non-JSON text")
    except ValueError:
        print("Correctly raised ValueError for unparseable text.\n")

    print("=== Testing generate_reply() end-to-end (with the stub LLM) ===")
    result = generate_reply(SAMPLE_TICKETS[0]["ticket_text"], "empathetic")
    assert result["tone_applied"] == "empathetic"
    assert result["escalate"] is False
    print(f"generate_reply() returned: {result}\n")

    print("=== Testing generate_reply()'s fallback path ===")
    global call_llm
    original_call_llm = call_llm
    globals()["call_llm"] = lambda prompt: "not valid json at all"
    try:
        fallback_result = generate_reply("some ticket", "professional")
        assert fallback_result["escalate"] is True
        assert fallback_result["confidence"] == "low"
        print(f"Fallback path correctly triggered: {fallback_result}\n")
    finally:
        globals()["call_llm"] = original_call_llm

    print("All offline tests passed!")

    print("\n--- Demo: all three sample tickets, stub LLM ---")
    print("(Note: the offline stub always returns one fixed mock response")
    print(" regardless of the prompt -- that's why all three results look")
    print(" identical below. It exists only to test parsing/validation")
    print(" without API access. Set USE_REAL_LLM=1 with a real API key to")
    print(" see genuinely different, tone-appropriate replies per ticket.)")
    for sample in SAMPLE_TICKETS:
        result = generate_reply(sample["ticket_text"], sample["tone"])
        print(f"\nTicket: {sample['ticket_text'][:60]}...")
        print(f"Tone requested: {sample['tone']}")
        print(f"Result: {result}")


if __name__ == "__main__":
    offline_test()
