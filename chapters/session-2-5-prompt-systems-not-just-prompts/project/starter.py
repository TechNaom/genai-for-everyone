"""
Session 2.5 Project: Three-Step Prompt Chain
See README.md in this folder for the full brief and an example run.

Pro-path build: a classify -> extract -> draft-reply chain, where each step's
output feeds into the next, and every intermediate step can be inspected and
logged independently -- the debuggability advantage chaining provides over one
large combined prompt (Part 4 of the lesson).

No API key needed. `simulate_model()` stands in for a real LLM call so this
runs anywhere, offline, for free. Swap it for a real API call (same pattern as
Week 3's provider clients) once you want to see it work against a live model --
the CHAIN STRUCTURE below doesn't change either way.
"""

# --- Step prompt templates (each documents its own expected variables) ---

CLASSIFY_TEMPLATE = """Classify the category of this customer email as exactly
one of: "shipping", "billing", "returns", "other".

Email:
\"\"\"{email_text}\"\"\"

Respond with only the category word."""
# Expects: email_text (str)

EXTRACT_TEMPLATE = """Extract any order numbers and dates mentioned in this
customer email. Respond as JSON with keys "order_numbers" (list of strings)
and "dates" (list of strings). Use empty lists if none are present.

Email:
\"\"\"{email_text}\"\"\""""
# Expects: email_text (str)

DRAFT_REPLY_TEMPLATE = """Draft a short, polite reply to this customer email.
Category: {category}
Extracted order numbers: {order_numbers}
Extracted dates: {dates}

Original email:
\"\"\"{email_text}\"\"\"

Keep the reply under 80 words and reference the category and any extracted
order numbers or dates naturally."""
# Expects: category (str), order_numbers (list), dates (list), email_text (str)


def simulate_model(prompt: str) -> str:
    """
    Stand-in for a real LLM call so this exercise runs with no API key.
    A real version would call your provider's chat/completion endpoint with
    `prompt` and return the response text -- everything else in this file
    stays the same either way.
    """
    return "[simulated model output for prompt of length %d]" % len(prompt)


def classify_step(email_text, verbose=False):
    # TODO 1: format CLASSIFY_TEMPLATE with email_text, call simulate_model(),
    # and return a category string. For this offline exercise, since
    # simulate_model() doesn't do real classification, fall back to a simple
    # keyword rule: if "ship" or "deliver" is in the email (case-insensitive),
    # return "shipping"; if "refund" or "charge" is in it, return "billing";
    # if "return" is in it, return "returns"; otherwise return "other".
    # If verbose is True, print the formatted prompt before returning.
    pass


def extract_step(email_text, verbose=False):
    # TODO 2: format EXTRACT_TEMPLATE with email_text, and return a dict with
    # keys "order_numbers" and "dates". For this offline exercise, use a
    # simple rule: find tokens starting with "ORD-" for order numbers (split
    # the text on whitespace and strip punctuation), and leave "dates" as an
    # empty list (real extraction would use the model or a proper parser).
    # If verbose is True, print the formatted prompt before returning.
    pass


def draft_step(email_text, category, extracted, verbose=False):
    # TODO 3: format DRAFT_REPLY_TEMPLATE with category, extracted["order_numbers"],
    # extracted["dates"], and email_text, then return a short reply string.
    # For this offline exercise, build a simple templated reply by hand
    # (no need to call simulate_model() for real text -- the point of this
    # step is demonstrating the chain, not generating polished prose).
    # If verbose is True, print the formatted prompt before returning.
    pass


def run_chain(email_text, verbose=False):
    """Run all three steps in sequence, returning a dict with every
    intermediate output plus the final reply -- so each step can be
    inspected independently."""
    category = classify_step(email_text, verbose=verbose)
    extracted = extract_step(email_text, verbose=verbose)
    reply = draft_step(email_text, category, extracted, verbose=verbose)
    return {
        "category": category,
        "extracted": extracted,
        "reply": reply,
    }


SAMPLE_EMAIL = (
    "Hi, my order ORD-77410 was supposed to ship last week but I still don't "
    "have a tracking number. Can you tell me when it will actually deliver?"
)


if __name__ == "__main__":
    result = run_chain(SAMPLE_EMAIL, verbose=True)
    print("\n=== Chain result ===")
    print(f"Category:  {result['category']}")
    print(f"Extracted: {result['extracted']}")
    print(f"Reply:     {result['reply']}")
