"""
Reference solution — Session 2.5: Prompt Systems, Not Just Prompts

A complete 5-template library with lightweight, non-exact-match tests.
"""

FOLLOW_UP_TEMPLATE = """Write a polite follow-up email to {customer_name} about
their unpaid invoice from {invoice_date}, mentioning a {late_fee_pct}% late fee.
Keep it under 100 words."""
# Expects: customer_name (str), invoice_date (str), late_fee_pct (number)

REFUND_APOLOGY_TEMPLATE = """Write an apologetic email to {customer_name} approving
a refund of ${refund_amount} for their {product_name}. Offer a {discount_pct}%
discount on their next order as goodwill. Keep it under 120 words."""
# Expects: customer_name (str), refund_amount (number), product_name (str), discount_pct (number)

SHIPPING_DELAY_TEMPLATE = """Write a brief, honest notification to {customer_name}
about a delay on order #{order_number}. The new estimated delivery date is
{new_estimated_date}. Apologize once, do not over-apologize, and offer no
discount unless explicitly instructed to. Keep it under 80 words."""
# Expects: customer_name (str), order_number (str), new_estimated_date (str)

ACCOUNT_REACTIVATION_TEMPLATE = """Write a welcoming email to {customer_name}, a
returning customer reactivating their account after {months_inactive} months away.
Mention that their {saved_items_count} previously saved items are still in their
cart. Friendly, not pushy. Keep it under 90 words."""
# Expects: customer_name (str), months_inactive (number), saved_items_count (number)

FEATURE_ANNOUNCEMENT_TEMPLATE = """Write a short product announcement to
{customer_name} about a new feature: {feature_name}. Explain in one sentence
what it does, using this description as a basis: {feature_description}.
Enthusiastic but not over-the-top. Keep it under 70 words."""
# Expects: customer_name (str), feature_name (str), feature_description (str)


def contains_customer_name(prompt: str, customer_name: str) -> bool:
    return customer_name.lower() in prompt.lower()


def under_word_limit(prompt: str, limit: int) -> bool:
    return str(limit) in prompt


def contains_value(prompt: str, value) -> bool:
    return str(value) in prompt


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
            lambda p: contains_value(p, 49.99),
        ],
    },
    {
        "template": SHIPPING_DELAY_TEMPLATE,
        "variables": {"customer_name": "Amara Okafor", "order_number": "ORD-88213", "new_estimated_date": "June 30th"},
        "checks": [
            lambda p: contains_customer_name(p, "Amara Okafor"),
            lambda p: contains_value(p, "ORD-88213"),
            lambda p: contains_value(p, "June 30th"),
        ],
    },
    {
        "template": ACCOUNT_REACTIVATION_TEMPLATE,
        "variables": {"customer_name": "Devon Brooks", "months_inactive": 8, "saved_items_count": 3},
        "checks": [
            lambda p: contains_customer_name(p, "Devon Brooks"),
            lambda p: contains_value(p, 8),
            lambda p: contains_value(p, 3),
        ],
    },
    {
        "template": FEATURE_ANNOUNCEMENT_TEMPLATE,
        "variables": {
            "customer_name": "Priya Nair",
            "feature_name": "Dark Mode",
            "feature_description": "switches the interface to a low-light color scheme",
        },
        "checks": [
            lambda p: contains_customer_name(p, "Priya Nair"),
            lambda p: contains_value(p, "Dark Mode"),
        ],
    },
]


def run_tests():
    passed = 0
    failed = 0
    for i, case in enumerate(TEST_CASES, 1):
        formatted = case["template"].format(**case["variables"])
        all_passed = all(check(formatted) for check in case["checks"])
        if all_passed:
            passed += 1
            print(f"Test {i}: PASSED")
        else:
            failed += 1
            print(f"Test {i}: FAILED")
            print(f"  Formatted prompt: {formatted[:100]}...")

    print(f"\n{passed} passed, {failed} failed (out of {len(TEST_CASES)} total).")
    print(
        "\nNote: these checks verify TEMPLATE STRUCTURE — that variables substitute "
        "correctly and key facts appear in the formatted prompt. They do NOT verify "
        "live model output quality, which would need actual API calls and the kind "
        "of evaluation practices formalized in Week 5."
    )


if __name__ == "__main__":
    run_tests()
