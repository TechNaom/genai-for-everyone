"""
Reference solution — Session 1.1: What GenAI Actually Is (and Isn't)

Note: a few of these are genuinely debatable at the edges (e.g. recommendation
systems sometimes blend predictive scoring with generative explanation text).
The goal isn't perfect agreement with this file — it's being able to defend
your classification with the input->output framing.
"""

SCENARIOS = [
    {
        "scenario": "Flagging a credit card transaction as fraudulent",
        "category": "predictive",
        "io_description": "Input: transaction features (amount, location, time, history). Output: a fraud probability score or yes/no flag.",
        "example_tool": "Stripe Radar",
    },
    {
        "scenario": "Writing a product description from a list of bullet-point features",
        "category": "generative",
        "io_description": "Input: bullet points. Output: newly generated marketing copy/prose.",
        "example_tool": "Claude / ChatGPT / Jasper",
    },
    {
        "scenario": "Recommending which show to watch next on a streaming platform",
        "category": "predictive",
        "io_description": "Input: watch history + similar users' behavior. Output: a ranked list of existing titles (it doesn't invent new shows).",
        "example_tool": "Netflix recommendation engine",
    },
    {
        "scenario": "Generating a product photo from a text description",
        "category": "generative",
        "io_description": "Input: text prompt. Output: a newly created image that didn't exist before.",
        "example_tool": "Midjourney / DALL-E",
    },
    {
        "scenario": "Predicting whether a customer will cancel their subscription this month",
        "category": "predictive",
        "io_description": "Input: usage/billing history. Output: a churn-risk score or probability.",
        "example_tool": "Internal churn models (common at most SaaS companies)",
    },
    {
        "scenario": "Summarizing a 40-message customer support thread into 3 bullet points",
        "category": "generative",
        "io_description": "Input: full thread text. Output: newly generated condensed text.",
        "example_tool": "Claude / GPT-4 summarization",
    },
    {
        "scenario": "Sorting incoming emails into 'urgent', 'normal', 'spam'",
        "category": "predictive",
        "io_description": "Input: email content/metadata. Output: one of a fixed set of category labels.",
        "example_tool": "Gmail's spam/priority filters",
    },
    {
        "scenario": "Writing working Python code from a plain-English description of what it should do",
        "category": "generative",
        "io_description": "Input: natural-language description. Output: newly generated code.",
        "example_tool": "GitHub Copilot / Claude Code",
    },
    {
        "scenario": "Estimating the resale value of a used car from its mileage, age, and condition",
        "category": "predictive",
        "io_description": "Input: car attributes. Output: a continuous numeric price estimate.",
        "example_tool": "Kelley Blue Book online estimator",
    },
    {
        "scenario": "Translating a paragraph from English to Japanese",
        "category": "generative",
        "io_description": "Input: source text. Output: newly generated text in the target language (not a lookup).",
        "example_tool": "Google Translate (modern neural version) / DeepL",
    },
    {
        "scenario": "Detecting whether a chest X-ray shows signs of pneumonia",
        "category": "predictive",
        "io_description": "Input: medical image. Output: a diagnosis classification/probability.",
        "example_tool": "FDA-cleared radiology AI tools (e.g. Aidoc)",
    },
    {
        "scenario": "Drafting a personalized reply to a customer's angry support email",
        "category": "generative",
        "io_description": "Input: customer's email + context. Output: newly generated reply text.",
        "example_tool": "Intercom Fin / Zendesk AI",
    },
]


def print_solution():
    for item in SCENARIOS:
        print(f"\n{item['scenario']}")
        print(f"  Category: {item['category']}")
        print(f"  I/O: {item['io_description']}")
        print(f"  Example: {item['example_tool']}")


if __name__ == "__main__":
    print_solution()
