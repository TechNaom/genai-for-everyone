"""
Exercise — Session 2.6: Week 2 Lab — Mini Build Day

Customer-Support Reply Generator with Tone Control (SCAFFOLD — fill in the TODOs).

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
1. TONE_EXAMPLES            -- few-shot example replies, one per tone.
2. REASONING_INSTRUCTIONS   -- internal chain-of-thought instructions.
3. build_prompt()           -- validates the tone, fills the template's variables.
4. call_llm()                -- already provided (offline stub or real API call).
5. parse_reply()             -- defensively parses + validates the model's JSON.
6. generate_reply()           -- ties it all together: build -> call -> parse -> return.

Run this file directly to test against the sample tickets at the bottom:
  python3 starter.py

With the provided stub call_llm(), this tests your parsing and validation
logic against a deliberately messy model response (wrapped in markdown code
fences) without needing API access. To test against a real model, set
USE_REAL_LLM=1 and complete the optional TODO(4) with your own API call.
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
# TODO(1): Fill in TONE_EXAMPLES with one short few-shot example reply per
#          tone (empathetic, professional, concise), for a sample ticket of
#          your choosing. Write these yourself -- they're the anchor the
#          model will copy the *style* of, not the content.
#
# TODO(2): Fill in REASONING_INSTRUCTIONS. It should ask the model to
#          privately think through: what the customer actually wants,
#          whether the ticket gives enough information to resolve it, and
#          whether the issue involves money/data loss/repeated complaints
#          (which should push toward escalation) -- WITHOUT including that
#          reasoning in the final output.

TONE_EXAMPLES = None  # TODO(1): a multi-line string with one example reply per tone

REASONING_INSTRUCTIONS = None  # TODO(2): internal reasoning steps, excluded from output

PROMPT_TEMPLATE = """You are a customer support reply assistant for a software company.
You write clear, accurate replies. You never invent policy details, refund
amounts, or timelines that are not stated in the ticket.

A customer has submitted the following support ticket:

Subject: {ticket_subject}
Body: {ticket_body}

Write a reply in a {tone} tone, where:
- "empathetic" means lead with acknowledging the customer's frustration or
  situation before addressing the issue.
- "professional" means clear, courteous, and businesslike, with no casual
  language.
- "concise" means the shortest reply that fully resolves the issue, with no
  pleasantries.

{tone_examples}

{reasoning_instructions}

Rules:
- Only state details you can see directly in the ticket. Never invent
  specific policies, refund amounts, or timelines.
- If the ticket does not contain enough information to resolve the issue,
  do not guess -- set "escalate" to true and explain why in
  "escalation_reason".
- Return ONLY a JSON object. No markdown formatting, no commentary, no
  code fences.

Return your answer as JSON matching exactly this schema:
{schema}
"""


def build_prompt(ticket_subject: str, ticket_body: str, tone: str) -> str:
    """
    Fill in the template's variables.

    TODO(3): Validate that `tone` is one of VALID_TONES before building the
    prompt. Raise a ValueError with a clear message if it isn't -- this is
    a cheap guard that catches a bug before it ever reaches the model. Then
    return PROMPT_TEMPLATE.format(...) with all variables filled in.
    """
    raise NotImplementedError("Fill in build_prompt()")


# ---------------------------------------------------------------------------
# Step 3: Calling the model (provided)
# ---------------------------------------------------------------------------

def call_llm(prompt: str) -> str:
    """
    Calls the LLM and returns its raw text response.

    A stub is provided so you can test the parsing/validation logic without
    API access. Replace the stub with a real call (e.g. the Anthropic API)
    when you're ready to test end-to-end.
    """
    if os.environ.get("USE_REAL_LLM") == "1":
        # TODO(4, optional): wire up a real API call here if you have a key.
        #   import anthropic
        #   client = anthropic.Anthropic()
        #   response = client.messages.create(
        #       model="claude-sonnet-4-6", max_tokens=500,
        #       messages=[{"role": "user", "content": prompt}],
        #   )
        #   return response.content[0].text
        raise NotImplementedError("Real LLM call not wired up.")

    # --- Stub behavior for offline testing ---
    # Returns a deliberately imperfect response so your parser has
    # something real to defend against. Don't "fix" this stub --
    # parse_reply() should handle it as-is. It does pick a tone-appropriate
    # canned response by reading the {tone} variable back out of the
    # prompt, so you can still see tone genuinely affecting the output.
    tone_match = re.search(r"Write a reply in a (\w+) tone", prompt)
    tone = tone_match.group(1) if tone_match else "professional"

    canned = {
        "empathetic": (
            "Thank you for reaching out. I understand this is frustrating, "
            "and I want to help resolve it as quickly as possible.",
            "medium", "false", "null",
        ),
        "professional": (
            "Thank you for your message. I will look into this and follow "
            "up with the relevant details shortly.",
            "low", "true",
            '"Ticket does not contain enough detail to resolve without guessing."',
        ),
        "concise": (
            "Looking into this now -- will follow up shortly.",
            "high", "false", "null",
        ),
    }
    body, confidence, escalate, escalation_reason = canned.get(
        tone, canned["professional"]
    )

    return f"""Here is the reply:
```json
{{
  "reply_body": "{body}",
  "tone_applied": "{tone}",
  "confidence": "{confidence}",
  "escalate": {escalate},
  "escalation_reason": {escalation_reason}
}}
```"""


# ---------------------------------------------------------------------------
# Step 4: Defensive parsing + validation (Session 2.4)
# ---------------------------------------------------------------------------

def parse_reply(raw_output: str) -> SupportReply:
    """
    Defensively parse the model's raw text into a validated SupportReply.

    TODO(5): Implement this. It must:
      a) Strip any wrapper text/markdown code fences around the JSON
         (the stub above deliberately includes some).
      b) Attempt to parse the cleaned text as JSON. If parsing fails,
         raise a ValueError with a clear message -- don't let a bad
         parse silently produce a broken dict.
      c) Validate the parsed object:
         - all five keys are present
         - "tone_applied" is one of VALID_TONES
         - "confidence" is one of VALID_CONFIDENCE
         - "escalate" is a bool
         - "reply_body" is a non-empty string
         - if "escalate" is True, "escalation_reason" must be a non-empty
           string (a schema-valid but logically inconsistent case a plain
           schema check alone won't catch)
         If any check fails, raise a ValueError describing exactly what's
         wrong (this is what makes debugging a bad prompt change fast).
      d) Return the validated dict.

    Hint: write a small helper that extracts the first {...} JSON object
    from a string, in case the model wraps it in code fences or commentary
    despite being told not to.
    """
    raise NotImplementedError("Fill in parse_reply()")


# ---------------------------------------------------------------------------
# Step 5: Tie it together
# ---------------------------------------------------------------------------

def generate_reply(ticket_subject: str, ticket_body: str, tone: str) -> SupportReply:
    """
    Full pipeline: build the prompt, call the model, parse and validate
    the result. If parsing/validation fails, fall back to a safe escalation
    response rather than letting a broken reply reach a customer.
    """
    prompt = build_prompt(ticket_subject, ticket_body, tone)
    raw_output = call_llm(prompt)

    try:
        return parse_reply(raw_output)
    except ValueError as e:
        # TODO(6): Build and return a fallback SupportReply here:
        #   - escalate should be True
        #   - escalation_reason should mention that the reply could not
        #     be generated automatically (include the str(e) for debugging)
        #   - confidence should be "low"
        #   - reply_body can be a short, generic holding message
        #   - tone_applied should still reflect the requested tone
        raise NotImplementedError("Fill in the fallback path in generate_reply()")


# ---------------------------------------------------------------------------
# Test tickets -- run this file directly to try your implementation
# ---------------------------------------------------------------------------

SAMPLE_TICKETS = [
    {
        "subject": "Can't export my data",
        "body": "I've tried exporting my project as CSV three times today and it just spins forever. This is for a client deadline tomorrow morning.",
        "tone": "empathetic",
    },
    {
        "subject": "Billing question",
        "body": "I was charged $49 but I thought I was on the $29 plan. Can you explain the difference?",
        "tone": "professional",
    },
    {
        "subject": "How do I change my email address?",
        "body": "Want to update the email tied to my account.",
        "tone": "concise",
    },
]


if __name__ == "__main__":
    for i, ticket in enumerate(SAMPLE_TICKETS, start=1):
        print(f"\n--- Ticket {i}: {ticket['subject']} ---")
        try:
            result = generate_reply(ticket["subject"], ticket["body"], ticket["tone"])
            print(json.dumps(result, indent=2))
        except NotImplementedError as e:
            print(f"[Not implemented yet] {e}")
