"""
Exercise — Session 1.1: What GenAI Actually Is (and Isn't)

The AI Capability Map.

For each scenario below, fill in:
  - category:        "predictive" or "generative"
  - io_description:   one sentence describing input -> output
  - example_tool:      a real tool/product that does this

Then run this file:  python starter.py
"""

SCENARIOS = [
    {
        "scenario": "Flagging a credit card transaction as fraudulent",
        "category": None,          # TODO: "predictive" or "generative"
        "io_description": None,    # TODO
        "example_tool": None,      # TODO
    },
    {
        "scenario": "Writing a product description from a list of bullet-point features",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
    {
        "scenario": "Recommending which show to watch next on a streaming platform",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
    {
        "scenario": "Generating a product photo from a text description",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
    {
        "scenario": "Predicting whether a customer will cancel their subscription this month",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
    {
        "scenario": "Summarizing a 40-message customer support thread into 3 bullet points",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
    {
        "scenario": "Sorting incoming emails into 'urgent', 'normal', 'spam'",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
    {
        "scenario": "Writing working Python code from a plain-English description of what it should do",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
    {
        "scenario": "Estimating the resale value of a used car from its mileage, age, and condition",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
    {
        "scenario": "Translating a paragraph from English to Japanese",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
    {
        "scenario": "Detecting whether a chest X-ray shows signs of pneumonia",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
    {
        "scenario": "Drafting a personalized reply to a customer's angry support email",
        "category": None,
        "io_description": None,
        "example_tool": None,
    },
]


def validate_and_print():
    incomplete = []
    print(f"{'Scenario':<60} {'Category':<12} {'Example Tool':<20}")
    print("-" * 95)

    for item in SCENARIOS:
        if item["category"] is None or item["io_description"] is None or item["example_tool"] is None:
            incomplete.append(item["scenario"])
            continue

        category = item["category"].strip().lower()
        if category not in ("predictive", "generative"):
            print(f"WARNING: '{item['scenario']}' has an invalid category: {item['category']!r}")
            continue

        print(f"{item['scenario']:<60} {category:<12} {item['example_tool']:<20}")

    if incomplete:
        print("\nNot yet filled in:")
        for s in incomplete:
            print(f"  - {s}")
        print(f"\n{len(incomplete)} of {len(SCENARIOS)} scenarios remaining.")
    else:
        print(f"\nAll {len(SCENARIOS)} scenarios classified. Compare your reasoning with a classmate or the solution file.")


if __name__ == "__main__":
    validate_and_print()
