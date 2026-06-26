"""
Exercise — Session 2.5: Prompt Systems, Not Just Prompts

Reusable Prompt Template Library.

No API key needed — this exercise tests TEMPLATE STRUCTURE and your ability
to design lightweight, non-exact-match test checks. Run: python prompt_library.py
"""

# --- Templates (3 started, 2 for you to design) ---

FOLLOW_UP_TEMPLATE = """Write a polite follow-up email to {customer_name} about
their unpaid invoice from {invoice_date}, mentioning a {late_fee_pct}% late fee.
Keep it under 100 words."""
# Expects: customer_name (str), invoice_date (str), late_fee_pct (number)

REFUND_APOLOGY_TEMPLATE = """Write an apologetic email to {customer_name} approving
a refund of ${refund_amount} for their {product_name}. Offer a {discount_pct}%
discount on their next order as goodwill. Keep it under 120 words."""
# Expects: customer_name (str), refund_amount (number), product_name (str), discount_pct (number)

# TODO: design a third provided template — a "shipping delay notification" template.
# It should accept at least: customer_name, order_number, new_estimated_date.
SHIPPING_DELAY_TEMPLATE = None  # TODO

# TODO: design a fourth template of your own choosing (any customer-communication
# theme not already covered) with at least 2 named variables.
CUSTOM_TEMPLATE_1 = None  # TODO

# TODO: design a fifth template of your own choosing.
CUSTOM_TEMPLATE_2 = None  # TODO


# --- Test cases: lightweight checks, NOT exact-match ---
# Each test case provides sample variable values and a CHECK FUNCTION that
# takes the formatted prompt and returns True/False for some property it
# should have. This tests the TEMPLATE's structure, not live model output.

def contains_customer_name(prompt: str, customer_name: str) -> bool:
    return customer_name.lower() in prompt.lower()


def under_word_limit(prompt: str, limit: int) -> bool:
    # crude check: does the template ITSELF instruct a word limit at or under `limit`?
    return str(limit) in prompt


TEST_CASES = [
    {
        "template": FOLLOW_UP_TEMPLATE,
        "variables": {"customer_name": "Sarah Chen", "invoice_date": "March 15th", "late_fee_pct": 5},
        "checks": [
            lambda p: contains_customer_name(p, "Sarah Chen"),
            lambda p: under_word_limit(p, 100),
        ],
    },
    {
        "template": REFUND_APOLOGY_TEMPLATE,
        "variables": {"customer_name": "Wei Zhang", "refund_amount": 49.99, "product_name": "wireless mouse", "discount_pct": 15},
        "checks": [
            lambda p: contains_customer_name(p, "Wei Zhang"),
            lambda p: "49.99" in p,
        ],
    },
    # TODO: add a test case for SHIPPING_DELAY_TEMPLATE
    # TODO: add a test case for CUSTOM_TEMPLATE_1
    # TODO: add a test case for CUSTOM_TEMPLATE_2
]


def run_tests():
    incomplete = 0
    passed = 0
    failed = 0

    for i, case in enumerate(TEST_CASES, 1):
        if case["template"] is None:
            incomplete += 1
            print(f"Test {i}: SKIPPED (template not yet defined)")
            continue

        formatted = case["template"].format(**case["variables"])
        all_passed = all(check(formatted) for check in case["checks"])

        if all_passed:
            passed += 1
            print(f"Test {i}: PASSED")
        else:
            failed += 1
            print(f"Test {i}: FAILED")
            print(f"  Formatted prompt: {formatted[:100]}...")

    print(f"\n{passed} passed, {failed} failed, {incomplete} incomplete (out of {len(TEST_CASES)} total).")
    if incomplete:
        print("Fill in the remaining templates and test cases to complete this exercise.")


if __name__ == "__main__":
    run_tests()
