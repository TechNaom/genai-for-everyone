"""
Session 3.1 — Reference Solution
"RAG or Not?" Decision Worksheet

Try the exercise yourself first -- the value is in practicing the
judgment call, not reading someone else's answer.

Note: Scenarios 1, 3, 4, and 6 are clear "RAG" cases for different reasons
(source traceability, time-sensitivity, training-data gap, time-sensitivity
+ traceability respectively). Scenarios 2 and 5 are deliberately NOT RAG --
they're reasoning/transformation tasks where the model doesn't need to
retrieve anything; it needs to think or rewrite. If you reasoned your way to
something different on a close call, that's fine as long as your argument
genuinely engages with the framework rather than guessing.

Run it: python3 solution.py
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
        "decision": "RAG",
        "reasoning": (
            "This needs source traceability above all else -- a legal "
            "answer that can't be pointed back to the exact clause it "
            "came from is close to useless, and arguably dangerous, in a "
            "legal context. The NDA template text is also specific, "
            "private company content that was never going to be reliably "
            "memorized by a general-purpose model's training data. "
            "Retrieving the actual Section 4.2 text and grounding the "
            "answer in it directly addresses both needs at once."
        ),
        "actual_fix": None,
    },
    {
        "id": 2,
        "scenario": (
            "A user asks a general-purpose chatbot: 'Can you explain how "
            "binary search works, and then write me a Python "
            "implementation?'"
        ),
        "decision": "Not RAG",
        "reasoning": (
            "Binary search is a timeless, extremely well-established "
            "computer science concept that any capable model already "
            "knows reliably -- there's no training-data gap, no private "
            "or post-cutoff information involved, and no need for source "
            "traceability. This is purely a reasoning/explanation/code-"
            "generation task. Adding retrieval here would add complexity "
            "and latency for zero accuracy benefit."
        ),
        "actual_fix": (
            "Nothing needed -- this is squarely within what the model "
            "already does well. If anything, a clear, well-structured "
            "prompt (Session 2.1) is all that's required."
        ),
    },
    {
        "id": 3,
        "scenario": (
            "A news summarization tool needs to answer: 'What were the "
            "three biggest headlines in financial markets today?'"
        ),
        "decision": "RAG",
        "reasoning": (
            "This is the clearest possible time-sensitivity case: 'today' "
            "is, by definition, after the model's training cutoff, no "
            "matter how recently the model was trained. The model cannot "
            "have reliably memorized headlines from today because they "
            "didn't exist yet when training happened. This needs live "
            "retrieval from a current news source, not model memory."
        ),
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
        "decision": "RAG",
        "reasoning": (
            "Clear training-data gap: this is private, per-employee data "
            "that was never going to be in any general-purpose model's "
            "training set, no matter how recent. It also changes over "
            "time (sick days get used throughout the year) and benefits "
            "from traceability (the employee should trust the number "
            "came from the real HR record, not a guess). The information "
            "needs to be retrieved and handed to the model at answer "
            "time."
        ),
        "actual_fix": None,
    },
    {
        "id": 5,
        "scenario": (
            "A user pastes in a 3-paragraph email they wrote and asks: "
            "'Can you make this sound more professional and fix any "
            "grammar issues?'"
        ),
        "decision": "Not RAG",
        "reasoning": (
            "All the information the model needs is already sitting "
            "directly in the prompt -- the user pasted the email "
            "themselves. There's no training-data gap to fill, nothing "
            "external to retrieve, and no time-sensitivity. This is "
            "purely a rewriting/transformation task, the same category as "
            "the binary-search example: the model needs to think and "
            "rewrite, not look anything up."
        ),
        "actual_fix": (
            "Nothing needed beyond a clear prompt -- the content to work "
            "with is already provided in context."
        ),
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
        "decision": "RAG",
        "reasoning": (
            "This is almost a textbook description of the exact failure "
            "mode the session covered: a model answering from memorized "
            "(and possibly stale or simply hallucinated) training "
            "patterns about 'a' return policy in general, instead of THE "
            "company's actual, specific, occasionally-changing policy. "
            "It needs both time-sensitivity (the policy updates "
            "occasionally) and traceability (customers should get an "
            "answer grounded in the real current policy page, not a "
            "plausible-sounding guess) -- retrieving the actual policy "
            "text before answering directly fixes the inconsistency "
            "described."
        ),
        "actual_fix": None,
    },
]


# ---------------------------------------------------------------------------
# Pro path — extended challenge answer
# ---------------------------------------------------------------------------

PRO_PATH_ANSWER = """
Pro path -- Scenario 4, one level deeper:

Correctly identifying that scenario 4 needs *some* form of retrieval is
the first-level answer -- but the specific mechanism matters. The
semantic/vector-based RAG you'll build in Sessions 3.2-3.4 is designed for
finding the most *relevant* passages out of a large, somewhat unstructured
body of text, when the question can be phrased many different ways and
you don't know in advance exactly which document or field holds the
answer.

"How many sick days do I have left" is not that kind of problem. It's a
precise, structured lookup against a specific field for a specific
employee ID -- exactly the kind of thing a direct database/API query
answers deterministically and correctly every time, with none of the
approximate-similarity uncertainty that vector search introduces. Using
vector search here would be using a more expensive, less precise tool for
a job a simple lookup already solves perfectly.

The better architecture: query the HR system's database directly for that
employee's remaining sick-day count (a tool call / function call, which
you'll formalize in Week 4), then hand that exact number to the model only
to phrase the final natural-language answer. The model's job here is
*language*, not *retrieval* -- the retrieval, in this case, is a precise
lookup, not a semantic search.

The broader lesson: "the model needs real external data" does not
automatically mean "the model needs vector-based RAG." Sometimes it means
a structured database query, sometimes a live API call, sometimes a
calculator. Vector-based RAG -- what the rest of this week focuses on --
is specifically the right tool when the relevant information lives in
unstructured or semi-structured text and you need to find the most
relevant passages among many candidates.
"""


def print_worksheet(scenarios):
    for s in scenarios:
        print(f"\n{'=' * 70}")
        print(f"Scenario {s['id']}: {s['scenario']}")
        print(f"{'-' * 70}")
        print(f"  Decision:   {s['decision']}")
        print(f"  Reasoning:  {s['reasoning']}")
        if s["decision"] != "RAG":
            print(f"  Actual fix: {s['actual_fix']}")

    print(f"\n{'=' * 70}")
    print(PRO_PATH_ANSWER)


if __name__ == "__main__":
    print_worksheet(SCENARIOS)
