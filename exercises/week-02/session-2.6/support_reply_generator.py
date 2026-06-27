"""
Session 2.6 Exercise — Customer Support Reply Generator with Tone Control
===========================================================================

Your task: build a function that takes a support ticket and a desired tone,
and returns a structured, validated reply using everything from Week 2.

This exercise pulls together:
  - Session 2.1: clarity, context, constraints, format specification
  - Session 2.2: few-shot examples + role prompting for tone consistency
  - Session 2.3: internal reasoning before answering (kept out of the output)
  - Session 2.4: schema-constrained JSON output + defensive parsing
  - Session 2.5: a documented, reusable prompt template

WHAT YOU NEED TO BUILD
-----------------------
1. SUPPORT_REPLY_TEMPLATE — fill in the {tone_examples} and
                             {reasoning_instructions} sections. (TODOs 1-2)
2. build_prompt()         — validates the tone, fills in the template's
                             variables. (TODO 3)
3. call_llm()              — already provided as a stub for offline testing.
                             Optionally wire up a real call. (TODO 4, optional)
4. parse_reply()           — defensively parses + validates the model's
                             JSON. (TODO 5)
5. generate_reply()        — ties it all together, with a safe fallback
                             to escalation on parse failure. (TODO 6)

Run this file directly to test against the sample tickets at the bottom:
    python3 support_reply_generator.py

With the provided stub call_llm(), this tests your parsing and validation
logic against a deliberately messy model response (wrapped in markdown
code fences) without needing API access.
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
#
# TODO(1): Fill in the {tone_examples} section with one short few-shot
#          example reply per tone (empathetic, professional, concise).
#          Write these yourself -- they're the anchor the model will copy
#          the *style* of, not the content. Keep each example to 1-2
#          sentences; you're demonstrating voice, not writing the final copy.
#
# TODO(2): Fill in the {reasoning_instructions} section. Ask the model to
#          think step by step about: (a) what the customer is actually
#          asking, (b) how urgent or sensitive the situation is, (c)
#          whether a standard reply is enough or this needs escalation --
#          and explicitly instruct it to do this internally, without
#          including the reasoning in the final output.

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
    """
    TODO(3):
      1. Validate that `tone` is one of VALID_TONES. If not, raise a
         ValueError with a clear message (don't let an invalid tone
         silently reach the model).
      2. Fill in SUPPORT_REPLY_TEMPLATE's variables:
         - tone_examples: your three few-shot examples from TODO(1)
         - reasoning_instructions: your instructions from TODO(2)
         - schema: REPLY_SCHEMA_DESCRIPTION
         - ticket_text: the ticket_text argument
      3. Return the filled-in prompt string.

    Note: this function always includes all three tone examples regardless
    of which tone was requested -- the model still benefits from seeing
    the contrast between tones, not just the one it's being asked to use.
    """
    raise NotImplementedError("Fill in build_prompt()")


# ---------------------------------------------------------------------------
# Step 3: Calling the model
# ---------------------------------------------------------------------------

def call_llm(prompt: str) -> str:
    """
    Stub implementation for offline testing -- returns a deliberately
    messy response (wrapped in markdown code fences, like real models
    sometimes do even when asked for "ONLY valid JSON") so you can build
    and test parse_reply() without needing API access.

    TODO(4) [OPTIONAL]: if you have ANTHROPIC_API_KEY set and want to see
    real model output, set the environment variable USE_REAL_LLM=1 and
    replace the stub body below with a real call, e.g.:

        import anthropic
        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    The stub is fine to leave as-is if you don't have API access --
    everything through TODO(6) is fully testable without it.
    """
    if os.environ.get("USE_REAL_LLM") == "1":
        raise NotImplementedError(
            "Fill in the real API call here if USE_REAL_LLM=1 is set."
        )

    # Deliberately messy stub response: wrapped in markdown fences, the
    # way real models sometimes respond even when told "ONLY valid JSON."
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
    """
    TODO(5): Defensively parse and validate the model's response.

    Steps:
      1. Strip markdown code fences if present (models sometimes wrap
         JSON in ```json ... ``` even when told not to). A simple
         approach: use a regex to extract content between ``` markers
         if they're present, otherwise use the raw text as-is.
      2. Parse the result as JSON. If parsing fails, raise a ValueError
         with a clear message (don't let a JSONDecodeError leak out
         unhandled).
      3. Validate every field is present and has the right shape:
         - reply_body: non-empty string
         - tone_applied: must be one of VALID_TONES
         - confidence: must be one of VALID_CONFIDENCE
         - escalate: must be a bool
         - escalation_reason: string or None
      4. Validate the logical consistency rule: if escalate is True,
         escalation_reason must be a non-empty string (you can't
         escalate without saying why). Raise a ValueError if this rule
         is violated.
      5. Return a SupportReply dict.

    Raise ValueError (not a bare assertion or generic Exception) for
    every validation failure, with a message specific enough to debug
    from -- "tone_applied was 'happy', expected one of ('empathetic',
    'professional', 'concise')" is far more useful than "invalid input."
    """
    raise NotImplementedError("Fill in parse_reply()")


# ---------------------------------------------------------------------------
# Step 5: Wiring it together, with a safe fallback
# ---------------------------------------------------------------------------

def generate_reply(ticket_text: str, tone: str) -> SupportReply:
    """
    TODO(6):
      1. prompt = build_prompt(ticket_text, tone)
      2. raw = call_llm(prompt)
      3. Try parse_reply(raw). If it raises ValueError, DO NOT crash --
         catch it and return a safe fallback SupportReply instead:
            {
              "reply_body": "",
              "tone_applied": tone,
              "confidence": "low",
              "escalate": True,
              "escalation_reason": "Automated reply generation failed "
                                    "validation; needs human review.",
            }
         (You can include the original error message somewhere in your
         own logging/printing if you want, but the returned dict should
         match this shape.)
      4. If parsing succeeds, return the parsed SupportReply as-is.

    This fallback is the point of the exercise: a parsing failure should
    turn into a safe escalation, never an unhandled crash that takes down
    whatever system is calling this function.
    """
    raise NotImplementedError("Fill in generate_reply()")


# ---------------------------------------------------------------------------
# Offline tests (no API key required) -- get these passing first
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
        "tone_applied": "happy",  # not a valid tone
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
        "escalation_reason": None,  # inconsistent!
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
    # Monkey-patch call_llm to return garbage, confirm generate_reply()
    # falls back to a safe escalation instead of crashing.
    import builtins
    original_call_llm = globals()["call_llm"]
    globals()["call_llm"] = lambda prompt: "not valid json at all"
    try:
        fallback_result = generate_reply("some ticket", "professional")
        assert fallback_result["escalate"] is True
        assert fallback_result["confidence"] == "low"
        print(f"Fallback path correctly triggered: {fallback_result}\n")
    finally:
        globals()["call_llm"] = original_call_llm

    print("All offline tests passed!")


if __name__ == "__main__":
    offline_test()
