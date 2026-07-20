"""
Session 2.6 — Reference Solution
Customer Support Reply Generator with Tone Control
===========================================================================

This is the worked solution. Try the exercise yourself first --
the value is in building the defensive parsing logic, not reading it.

This solution combines every technique from Week 2:
  - 2.1 Clarity, context, constraints, format specification
  - 2.2 Few-shot examples + role prompting for tone consistency
  - 2.3 Internal chain-of-thought reasoning, kept out of the final output
  - 2.4 Schema-constrained JSON output + defensive parsing
  - 2.5 A documented, versioned, reusable prompt template
"""

import json
import os
import re
from typing import Optional, TypedDict


# ---------------------------------------------------------------------------
# Step 1: The structured output contract
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
# Step 2: The prompt template
#   Template name: support_reply_v1
#   Variables: ticket_subject, ticket_body, tone
#   Returns: JSON matching SupportReply
# ---------------------------------------------------------------------------

TONE_EXAMPLES = """Here are example replies showing each tone, for a different ticket
("I've been charged twice this month and no one has responded to my last
two emails."):

[empathetic]: "I completely understand the frustration here -- being
charged twice and then not hearing back only makes it worse. I've looked
into your account and can see the duplicate charge. I'm flagging this for
an immediate refund and will confirm once it's processed."

[professional]: "Thank you for bringing this to our attention. I have
reviewed your account and confirmed a duplicate charge was applied this
month. I am processing a refund for the duplicate amount and will follow
up with confirmation."

[concise]: "Confirmed duplicate charge on your account. Refund is being
processed now. You'll get a confirmation once it completes."

Match the style and length of the example for the requested tone -- not
its specific content."""

REASONING_INSTRUCTIONS = """Before writing the reply, privately reason through the following (do not
include this reasoning in your output):
1. What specifically is the customer asking for or upset about?
2. Does the ticket give enough information to actually resolve this, or
   would resolving it require guessing at details not stated here?
3. Does this involve money, data loss, or signs of a repeated/escalating
   complaint? If so, lean toward escalation rather than a confident reply.
Then write only the final JSON object -- no reasoning, no commentary."""

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
    """Fill in the template's variables, after validating the tone."""
    if tone not in VALID_TONES:
        raise ValueError(
            f"Invalid tone '{tone}'. Must be one of: {', '.join(VALID_TONES)}"
        )

    return PROMPT_TEMPLATE.format(
        ticket_subject=ticket_subject,
        ticket_body=ticket_body,
        tone=tone,
        tone_examples=TONE_EXAMPLES,
        reasoning_instructions=REASONING_INSTRUCTIONS,
        schema=REPLY_SCHEMA_DESCRIPTION,
    )


# ---------------------------------------------------------------------------
# Step 3: Calling the model
# ---------------------------------------------------------------------------

def call_llm(prompt: str) -> str:
    """
    Calls the LLM and returns its raw text response.

    Stub mode (default): returns a deliberately imperfect response --
    wrapped in markdown code fences with leading commentary -- so the
    parser below has something realistic to defend against.

    Real mode: set USE_REAL_LLM=1 and provide ANTHROPIC_API_KEY to call
    the actual Anthropic API instead.
    """
    if os.environ.get("USE_REAL_LLM") == "1":
        import anthropic  # import here so the stub path has no hard dependency

        client = anthropic.Anthropic()
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    # --- Stub behavior for offline testing ---
    # A real LLM reads the actual ticket and tone out of the prompt and
    # responds accordingly. This stub can't do that, but it picks a
    # tone-appropriate canned response by reading the {tone} variable back
    # out of the prompt, so the demo still shows tone genuinely changing
    # the output -- rather than returning one fixed answer for every input.
    tone_match = re.search(r"Write a reply in a (\w+) tone", prompt)
    tone = tone_match.group(1) if tone_match else "professional"

    canned_responses = {
        "empathetic": {
            "reply_body": (
                "I completely understand how stressful this is with a "
                "deadline tomorrow morning. I've checked and there's a "
                "known issue affecting CSV exports today, which is why "
                "it's spinning. Our engineering team is on it. In the "
                "meantime, you can export as JSON instead, which is not "
                "affected, and I'll follow up the moment CSV export is "
                "back online."
            ),
            "confidence": "medium",
            "escalate": "false",
            "escalation_reason": "null",
        },
        "professional": {
            "reply_body": (
                "Thank you for reaching out. I am unable to confirm which "
                "billing plan your account is currently set to from this "
                "ticket alone, so I am escalating this to verify your "
                "exact plan details before providing billing specifics."
            ),
            "confidence": "low",
            "escalate": "true",
            "escalation_reason": (
                '"Ticket does not state which billing plan the customer is '
                "currently on, so the price difference cannot be confirmed "
                'without guessing."'
            ),
        },
        "concise": {
            "reply_body": (
                "Go to Account Settings, Profile, Email, enter the new "
                "address, and confirm via the verification link sent to it."
            ),
            "confidence": "high",
            "escalate": "false",
            "escalation_reason": "null",
        },
    }
    chosen = canned_responses.get(tone, canned_responses["professional"])

    return f"""Here is the reply:
```json
{{
  "reply_body": "{chosen['reply_body']}",
  "tone_applied": "{tone}",
  "confidence": "{chosen['confidence']}",
  "escalate": {chosen['escalate']},
  "escalation_reason": {chosen['escalation_reason']}
}}
```"""


# ---------------------------------------------------------------------------
# Step 4: Defensive parsing + validation
# ---------------------------------------------------------------------------

def _extract_json_object(text: str) -> str:
    """
    Pull the first {...} JSON object out of a string that may contain
    wrapper text or markdown code fences around it.
    """
    # Try to find a fenced code block first (```json ... ``` or ``` ... ```)
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence_match:
        return fence_match.group(1)

    # Fall back to the first {...} span in the text (handles nested braces
    # reasonably well for a single flat JSON object like ours).
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("No JSON object found in model output.")
    return text[start : end + 1]


def parse_reply(raw_output: str) -> SupportReply:
    """
    Defensively parse the model's raw text into a validated SupportReply.

    Raises ValueError with a specific, debuggable message on any failure --
    never returns a partially-valid or silently-wrong result.
    """
    json_str = _extract_json_object(raw_output)

    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model output was not valid JSON: {e}")

    if not isinstance(parsed, dict):
        raise ValueError(f"Expected a JSON object, got {type(parsed).__name__}.")

    required_keys = {
        "reply_body",
        "tone_applied",
        "confidence",
        "escalate",
        "escalation_reason",
    }
    missing = required_keys - parsed.keys()
    if missing:
        raise ValueError(f"Missing required field(s): {', '.join(sorted(missing))}")

    if not isinstance(parsed["reply_body"], str) or not parsed["reply_body"].strip():
        raise ValueError("'reply_body' must be a non-empty string.")

    if parsed["tone_applied"] not in VALID_TONES:
        raise ValueError(
            f"'tone_applied' must be one of {VALID_TONES}, got "
            f"{parsed['tone_applied']!r}."
        )

    if parsed["confidence"] not in VALID_CONFIDENCE:
        raise ValueError(
            f"'confidence' must be one of {VALID_CONFIDENCE}, got "
            f"{parsed['confidence']!r}."
        )

    if not isinstance(parsed["escalate"], bool):
        raise ValueError(
            f"'escalate' must be a boolean, got {type(parsed['escalate']).__name__}."
        )

    if parsed["escalation_reason"] is not None and not isinstance(
        parsed["escalation_reason"], str
    ):
        raise ValueError("'escalation_reason' must be a string or null.")

    # Cross-field check: a schema-valid reply can still be logically
    # inconsistent. An escalate=True reply with no stated reason isn't
    # actionable for whoever receives it -- no per-field type check alone
    # catches this, so it needs its own explicit rule.
    if parsed["escalate"] and not (
        isinstance(parsed["escalation_reason"], str)
        and parsed["escalation_reason"].strip()
    ):
        raise ValueError(
            "'escalate' is true but 'escalation_reason' is missing or empty -- "
            "an escalation must always state why."
        )

    return SupportReply(
        reply_body=parsed["reply_body"],
        tone_applied=parsed["tone_applied"],
        confidence=parsed["confidence"],
        escalate=parsed["escalate"],
        escalation_reason=parsed["escalation_reason"],
    )


# ---------------------------------------------------------------------------
# Step 5: Tie it together
# ---------------------------------------------------------------------------

def generate_reply(ticket_subject: str, ticket_body: str, tone: str) -> SupportReply:
    """
    Full pipeline: build the prompt, call the model, parse and validate
    the result. Falls back to a safe escalation response if parsing or
    validation fails, rather than letting a broken reply reach a customer.
    """
    prompt = build_prompt(ticket_subject, ticket_body, tone)
    raw_output = call_llm(prompt)

    try:
        return parse_reply(raw_output)
    except ValueError as e:
        return SupportReply(
            reply_body=(
                "Thanks for reaching out -- we've received your message and "
                "a member of our support team will follow up shortly."
            ),
            tone_applied=tone,
            confidence="low",
            escalate=True,
            escalation_reason=f"Automatic reply generation failed validation: {e}",
        )


# ---------------------------------------------------------------------------
# Test tickets -- run this file directly to see it work
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
        print(f"\n--- Ticket {i}: {ticket['subject']} ({ticket['tone']}) ---")
        result = generate_reply(ticket["subject"], ticket["body"], ticket["tone"])
        print(json.dumps(result, indent=2))

    # --- Demonstrate the invalid-tone guard ---
    print("\n--- Invalid tone guard ---")
    try:
        build_prompt("Test", "Test body", "sarcastic")
    except ValueError as e:
        print(f"Correctly rejected: {e}")

    # --- Demonstrate the fallback path on broken model output ---
    print("\n--- Fallback path on broken output ---")
    broken_outputs = [
        "Sorry, I can't help with that.",  # no JSON at all
        '{"reply_body": "Hi"}',  # missing required fields
        '{"reply_body": "Hi", "tone_applied": "rude", "confidence": "high", "escalate": false, "escalation_reason": null}',  # invalid tone value
        '{"reply_body": "Hi", "tone_applied": "professional", "confidence": "low", "escalate": true, "escalation_reason": null}',  # escalate/reason mismatch
    ]
    for broken in broken_outputs:
        try:
            parse_reply(broken)
            print("Unexpectedly parsed without error -- check test case.")
        except ValueError as e:
            print(f"Correctly caught: {e}")
