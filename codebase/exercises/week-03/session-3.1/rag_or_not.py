"""
Session 3.1 Exercise — The "RAG or Not?" Decision Worksheet

For each of the six scenarios below, decide whether the problem genuinely
needs Retrieval-Augmented Generation (RAG), or whether there's a simpler
or better fix.

For each scenario, fill in:
  - decision:    "RAG", "Not RAG", or "Something else" (be specific in
                 your reasoning about what "something else" is)
  - reasoning:   2-4 sentences, using the framework from the session:
                   * Is the needed info outside the model's training data
                     (private, post-cutoff, or just unreliable to memorize)?
                   * Does the answer need to be traceable to a real source?
                   * Does the underlying info change over time?
                   ...or is this actually a reasoning/writing/transformation
                   task, a timeless-knowledge task, or a prompting problem
                   in disguise?
  - actual_fix:  if decision is "Not RAG" or "Something else", name the
                 real fix (e.g. "better prompting", "the model already
                 knows this reliably", "this needs a tool call to a
                 calculator/API, not retrieval", "this needs a database
                 lookup, not semantic search"). Leave as None if decision
                 is "RAG".

Then run this file: python3 rag_or_not.py
It will print your answers in a readable format and flag any scenario
you haven't filled in yet.
"""

SCENARIOS = [
    {
        "id": 1,
        "scenario": (
            "A legal tech startup wants their AI assistant to answer "
            "questions like 'What does Section 4.2 of our standard NDA "
            "template say about confidentiality duration?' by quoting the "
            "exact clause."
        ),
        "decision": None,    # TODO: "RAG" / "Not RAG" / "Something else"
        "reasoning": None,   # TODO
        "actual_fix": None,  # TODO (or leave None if decision is "RAG")
    },
    {
        "id": 2,
        "scenario": (
            "A user asks a general-purpose chatbot: 'Can you explain how "
            "binary search works, and then write me a Python "
            "implementation?'"
        ),
        "decision": None,
        "reasoning": None,
        "actual_fix": None,
    },
    {
        "id": 3,
        "scenario": (
            "A news summarization tool needs to answer: 'What were the "
            "three biggest headlines in financial markets today?'"
        ),
        "decision": None,
        "reasoning": None,
        "actual_fix": None,
    },
    {
        "id": 4,
        "scenario": (
            "An internal HR chatbot needs to answer employee questions "
            "like 'How many paid sick days do I have left this year?' "
            "where the answer is different for every employee and stored "
            "in the company's HR system."
        ),
        "decision": None,
        "reasoning": None,
        "actual_fix": None,
    },
    {
        "id": 5,
        "scenario": (
            "A user pastes in a 3-paragraph email they wrote and asks: "
            "'Can you make this sound more professional and fix any "
            "grammar issues?'"
        ),
        "decision": None,
        "reasoning": None,
        "actual_fix": None,
    },
    {
        "id": 6,
        "scenario": (
            "A customer support tool keeps giving customers slightly "
            "different -- and sometimes contradictory -- answers about "
            "the company's current return policy, because the model is "
            "answering from training data instead of the company's "
            "actual, occasionally-updated policy page."
        ),
        "decision": None,
        "reasoning": None,
        "actual_fix": None,
    },
]


def print_worksheet(scenarios):
    incomplete = []

    for s in scenarios:
        print(f"\n{'=' * 70}")
        print(f"Scenario {s['id']}: {s['scenario']}")
        print(f"{'-' * 70}")

        if s["decision"] is None:
            incomplete.append(s["id"])
            print("  Decision:   [NOT FILLED IN YET]")
            continue

        print(f"  Decision:   {s['decision']}")
        print(f"  Reasoning:  {s['reasoning']}")
        if s["decision"] != "RAG":
            print(f"  Actual fix: {s['actual_fix']}")

    print(f"\n{'=' * 70}")
    if incomplete:
        print(f"Still need to fill in scenario(s): {incomplete}")
    else:
        print("All six scenarios filled in. Check your reasoning against")
        print("the answer key in codebase/solutions/week-03/session-3.1/")


if __name__ == "__main__":
    print_worksheet(SCENARIOS)
