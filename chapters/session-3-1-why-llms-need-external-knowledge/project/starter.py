"""
Session 3.1 Project: The Wrong-Direction Failure Report
See README.md in this folder for the full brief and an example run.

This is the Pro path build for Session 3.1. The exercises/ worksheet asked
you to make the right call on six "RAG or Not?" scenarios. This project asks
a sharper question: what actually goes wrong when someone makes the WRONG
call on each one -- in the opposite direction from the mistake you'd expect?

  - For the four scenarios that genuinely need RAG (1, 3, 4, 6), the wrong
    call is handling them with prompting alone -- no retrieval, just asking
    the model and hoping.
  - For the two scenarios that don't need RAG (2, 5), the wrong call is
    building a full RAG pipeline anyway -- retrieval infrastructure for a
    problem that never needed it.

Each CASE below reuses the same six scenarios from the exercises worksheet,
plus the correct decision. For each, fill in:
  - wrong_call:        what the opposite-direction mistake looks like in
                        practice (one sentence: what someone actually builds
                        or does instead of the right call)
  - failure_mode:       2-3 sentences on what concretely breaks -- who
                        notices, how, and why it's bad (not just "it's
                        wrong" -- the specific, realistic consequence)
  - cost_of_the_mistake: one sentence naming the type of cost (wasted
                        engineering time, latency, a wrong answer shipped to
                        a user, a compliance risk, etc.)

No API calls needed -- this is a pure diagnostic-reasoning exercise, plain
Python, runs anywhere.
"""

CASES = [
    {
        "id": 1,
        "scenario": (
            "A legal tech startup wants their AI assistant to answer "
            "questions like 'What does Section 4.2 of our standard NDA "
            "template say about confidentiality duration?' by quoting the "
            "exact clause."
        ),
        "correct_call": "RAG",
        "wrong_direction": "handled with prompting alone, no retrieval",
        "wrong_call": None,          # TODO
        "failure_mode": None,        # TODO
        "cost_of_the_mistake": None,  # TODO
    },
    {
        "id": 2,
        "scenario": (
            "A user asks a general-purpose chatbot: 'Can you explain how "
            "binary search works, and then write me a Python "
            "implementation?'"
        ),
        "correct_call": "Not RAG",
        "wrong_direction": "given a full RAG pipeline anyway",
        "wrong_call": None,
        "failure_mode": None,
        "cost_of_the_mistake": None,
    },
    {
        "id": 3,
        "scenario": (
            "A news summarization tool needs to answer: 'What were the "
            "three biggest headlines in financial markets today?'"
        ),
        "correct_call": "RAG",
        "wrong_direction": "handled with prompting alone, no retrieval",
        "wrong_call": None,
        "failure_mode": None,
        "cost_of_the_mistake": None,
    },
    {
        "id": 4,
        "scenario": (
            "An internal HR chatbot needs to answer employee questions "
            "like 'How many paid sick days do I have left this year?' "
            "where the answer is different for every employee and stored "
            "in the company's HR system."
        ),
        "correct_call": "RAG",
        "wrong_direction": "handled with prompting alone, no retrieval",
        "wrong_call": None,
        "failure_mode": None,
        "cost_of_the_mistake": None,
    },
    {
        "id": 5,
        "scenario": (
            "A user pastes in a 3-paragraph email they wrote and asks: "
            "'Can you make this sound more professional and fix any "
            "grammar issues?'"
        ),
        "correct_call": "Not RAG",
        "wrong_direction": "given a full RAG pipeline anyway",
        "wrong_call": None,
        "failure_mode": None,
        "cost_of_the_mistake": None,
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
        "correct_call": "RAG",
        "wrong_direction": "handled with prompting alone, no retrieval",
        "wrong_call": None,
        "failure_mode": None,
        "cost_of_the_mistake": None,
    },
]


def run_report():
    incomplete = 0
    for case in CASES:
        print(f"\n{'=' * 70}")
        print(f"Scenario {case['id']}: {case['scenario']}")
        print(f"Correct call: {case['correct_call']}")
        print(f"Wrong-direction mistake: {case['wrong_direction']}")
        print(f"{'-' * 70}")

        if (
            case["wrong_call"] is None
            or case["failure_mode"] is None
            or case["cost_of_the_mistake"] is None
        ):
            incomplete += 1
            print("  (not yet analyzed)")
            continue

        print(f"  What the wrong call looks like: {case['wrong_call']}")
        print(f"  Failure mode:                   {case['failure_mode']}")
        print(f"  Cost of the mistake:            {case['cost_of_the_mistake']}")

    print(f"\n{'=' * 70}")
    if incomplete:
        print(f"{incomplete} of {len(CASES)} scenario(s) not yet analyzed.")
    else:
        print(f"All {len(CASES)} scenarios analyzed. Compare against solution.py")


if __name__ == "__main__":
    run_report()
