"""
Exercise — Session 1.3: The GenAI Landscape

Comparison Matrix.

Run the SAME task across at least 2 different models you have access to,
then fill in your observations below. This works with free chat interfaces
(time yourself manually) or API calls if you have keys available.

Run this file once you've filled in RESULTS: python starter.py
"""

# Pick ONE of these (or write your own) as the task you'll run identically
# across every model you compare:
SUGGESTED_TASKS = [
    "Summarize this in 2 sentences: [paste a paragraph from a news article]",
    "Explain photosynthesis to a 10-year-old in 3 sentences.",
    "A train leaves City A at 60 mph. Another leaves City B (300 miles away) "
    "at 90 mph, heading toward City A, 1 hour later. When do they meet?",
]

# TODO 1: write the exact task text you tested everywhere
TASK_USED = None


# TODO 2: fill in one dictionary per model you tested.
# response_time_seconds: rough wall-clock time you observed (a stopwatch is fine)
# quality_rating: your own 1-5 subjective judgment of the output
# cost_per_million_input / output: published pricing if you found it, else None
RESULTS = [
    {
        "model_name": None,        # e.g. "Claude Haiku" or "GPT-4o-mini"
        "provider": None,          # e.g. "Anthropic"
        "response_time_seconds": None,
        "quality_rating": None,    # 1-5
        "cost_per_million_input": None,   # USD, or None if unknown
        "cost_per_million_output": None,  # USD, or None if unknown
        "notes": None,             # anything you observed worth flagging
    },
    {
        "model_name": None,
        "provider": None,
        "response_time_seconds": None,
        "quality_rating": None,
        "cost_per_million_input": None,
        "cost_per_million_output": None,
        "notes": None,
    },
]


def print_comparison():
    if not TASK_USED:
        print("Fill in TASK_USED with the exact task you tested before running this.")
        return

    print(f"Task tested across all models: {TASK_USED}\n")
    print(f"{'Model':<20} {'Provider':<14} {'Time (s)':<10} {'Quality':<9} {'$/M in':<10} {'$/M out':<10}")
    print("-" * 80)

    incomplete = 0
    for r in RESULTS:
        if r["model_name"] is None:
            incomplete += 1
            continue
        time_disp = str(r["response_time_seconds"]) if r["response_time_seconds"] is not None else "?"
        quality_disp = str(r["quality_rating"]) if r["quality_rating"] is not None else "?"
        cost_in_disp = f"${r['cost_per_million_input']}" if r["cost_per_million_input"] is not None else "n/a"
        cost_out_disp = f"${r['cost_per_million_output']}" if r["cost_per_million_output"] is not None else "n/a"
        print(f"{r['model_name']:<20} {r['provider']:<14} {time_disp:<10} {quality_disp:<9} {cost_in_disp:<10} {cost_out_disp:<10}")

    if incomplete:
        print(f"\n{incomplete} model(s) not yet filled in.")
        return

    # TODO 3: write a 2-3 sentence recommendation
    print("\n--- Your turn: write a 2-3 sentence recommendation below ---")
    print("Which model would you pick for a real-time customer-facing chat widget, and why?")
    print("Which would you pick for an overnight batch summarization job, and why?")


# --- OPTIONAL: paid-API path example (commented out) ---
# Requires: pip install anthropic   (or your provider's SDK)
# Requires: an API key set as an environment variable, never hardcoded here.
#
# import time
# import os
# from anthropic import Anthropic
#
# def call_model_and_time(prompt: str):
#     client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
#     start = time.time()
#     response = client.messages.create(
#         model="claude-haiku-4-5-20251001",
#         max_tokens=300,
#         messages=[{"role": "user", "content": prompt}],
#     )
#     elapsed = time.time() - start
#     return response.content[0].text, elapsed


if __name__ == "__main__":
    print_comparison()
