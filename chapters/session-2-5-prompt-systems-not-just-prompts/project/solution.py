"""
Session 2.5 Project: Three-Step Prompt Chain — reference solution.

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
    """Step 1: classify the email into a fixed category."""
    prompt = CLASSIFY_TEMPLATE.format(email_text=email_text)
    if verbose:
        print("--- Step 1: classify -- prompt ---")
        print(prompt)

    # Stand-in for a real model call: simple keyword rules, since
    # simulate_model() doesn't actually reason about the text.
    lowered = email_text.lower()
    if "ship" in lowered or "deliver" in lowered:
        category = "shipping"
    elif "refund" in lowered or "charge" in lowered:
        category = "billing"
    elif "return" in lowered:
        category = "returns"
    else:
        category = "other"

    if verbose:
        print(f"--- Step 1: classify -- output: {category} ---\n")
    return category


def extract_step(email_text, verbose=False):
    """Step 2: extract order numbers (and dates, if present) as structured data."""
    prompt = EXTRACT_TEMPLATE.format(email_text=email_text)
    if verbose:
        print("--- Step 2: extract -- prompt ---")
        print(prompt)

    order_numbers = []
    for raw_token in email_text.split():
        token = raw_token.strip(".,!?;:()")
        if token.upper().startswith("ORD-"):
            order_numbers.append(token)

    extracted = {"order_numbers": order_numbers, "dates": []}

    if verbose:
        print(f"--- Step 2: extract -- output: {extracted} ---\n")
    return extracted


def draft_step(email_text, category, extracted, verbose=False):
    """Step 3: draft a reply using the category and extracted data from steps 1-2."""
    prompt = DRAFT_REPLY_TEMPLATE.format(
        category=category,
        order_numbers=extracted["order_numbers"],
        dates=extracted["dates"],
        email_text=email_text,
    )
    if verbose:
        print("--- Step 3: draft reply -- prompt ---")
        print(prompt)

    if extracted["order_numbers"]:
        order_ref = f" regarding order {extracted['order_numbers'][0]}"
    else:
        order_ref = ""

    reply = (
        f"Thanks for reaching out{order_ref}. We've logged this as a "
        f"{category} request and a member of our team will follow up shortly "
        f"with an update. We appreciate your patience."
    )

    if verbose:
        print(f"--- Step 3: draft reply -- output ---\n{reply}\n")
    return reply


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
    print("=== Chain result ===")
    print(f"Category:  {result['category']}")
    print(f"Extracted: {result['extracted']}")
    print(f"Reply:     {result['reply']}")
