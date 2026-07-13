"""
Reference solution / worked example — Session 1.3: The GenAI Landscape

NOTE: the numbers below are ILLUSTRATIVE, not live measurements — exact
performance and pricing change constantly. Your own RESULTS will differ,
and that's expected. What matters is the comparison PROCESS and the
reasoning in the recommendation, not matching these exact figures.
"""

TASK_USED = "Explain photosynthesis to a 10-year-old in 3 sentences."

RESULTS = [
    {
        "model_name": "Smaller/faster tier",
        "provider": "Provider A",
        "response_time_seconds": 1.2,
        "quality_rating": 4,
        "cost_per_million_input": 0.25,
        "cost_per_million_output": 1.25,
        "notes": "Fast, simple explanation, slightly less vivid analogy than the larger model.",
    },
    {
        "model_name": "Larger/frontier tier",
        "provider": "Provider A",
        "response_time_seconds": 3.8,
        "quality_rating": 5,
        "cost_per_million_input": 3.00,
        "cost_per_million_output": 15.00,
        "notes": "Noticeably richer analogy, but ~3x slower and roughly 10x more expensive per output token for this simple task.",
    },
]


def print_solution():
    print(f"Task tested: {TASK_USED}\n")
    for r in RESULTS:
        print(f"{r['model_name']} ({r['provider']})")
        print(f"  Time: {r['response_time_seconds']}s | Quality: {r['quality_rating']}/5")
        print(f"  Cost: ${r['cost_per_million_input']}/M in, ${r['cost_per_million_output']}/M out")
        print(f"  Notes: {r['notes']}\n")

    print("--- Worked recommendation ---")
    print(
        "For a simple, well-defined task like explaining a basic concept, the smaller/faster "
        "tier is the better default: the quality gap (4 vs 5) is small relative to the cost gap "
        "(roughly 10x on output tokens) and the speed gap (3x faster). The larger tier would be "
        "worth it for a task where the EXTRA quality meaningfully matters — a customer-facing "
        "explanation that needs to be especially polished, or a more genuinely complex reasoning "
        "task where the smaller model's answers start breaking down. The lesson isn't 'always use "
        "the cheap model' or 'always use the best model' — it's that the gap between tiers is task-"
        "dependent, and testing your ACTUAL use case (like this exercise just did) beats assuming."
    )


if __name__ == "__main__":
    print_solution()
