"""
Session 3.1 Project — reference solution.
The Wrong-Direction Failure Report

Note: the exact wording isn't the point -- what matters is that your version
names a concrete, realistic failure, not just "it would be wrong."

Run it: python3 solution.py
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
        "wrong_call": (
            "Someone writes a well-crafted prompt asking the model to "
            "'quote Section 4.2 of our standard NDA template' and ships it "
            "without ever giving the model the actual template text."
        ),
        "failure_mode": (
            "The model has never seen this company's specific NDA template "
            "-- it's private content, not public training data -- so it "
            "generates a plausible-sounding clause that resembles a typical "
            "confidentiality-duration clause but isn't the real one. Because "
            "it's phrased with total confidence and legal-sounding language, "
            "a user (or worse, a lawyer relying on the assistant) has no way "
            "to tell it's fabricated just by reading it."
        ),
        "cost_of_the_mistake": (
            "A real legal/compliance risk -- someone could act on a quoted "
            "clause that was never actually in the contract."
        ),
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
        "wrong_call": (
            "An engineer builds a retrieval step that embeds the question, "
            "searches a vector store of programming documentation, and "
            "stuffs the top-k matching chunks into the prompt before "
            "generation."
        ),
        "failure_mode": (
            "Binary search is timeless, well-established knowledge the "
            "model already explains reliably on its own -- so the retrieval "
            "step adds a search request, network latency, and a chunk of "
            "documentation text the model didn't need, with no improvement "
            "in answer quality. Worse, if the retrieved chunks are a "
            "slightly different framing than the user's question, they can "
            "actually crowd out the model's own clean explanation and make "
            "the answer more disjointed, not less."
        ),
        "cost_of_the_mistake": (
            "Wasted engineering effort and unnecessary latency on every "
            "request, for zero accuracy gain."
        ),
    },
    {
        "id": 3,
        "scenario": (
            "A news summarization tool needs to answer: 'What were the "
            "three biggest headlines in financial markets today?'"
        ),
        "correct_call": "RAG",
        "wrong_direction": "handled with prompting alone, no retrieval",
        "wrong_call": (
            "The prompt is engineered carefully -- 'you are a financial "
            "news expert, list today's three biggest market headlines' -- "
            "but the model is never given any actual current news text to "
            "work from."
        ),
        "failure_mode": (
            "'Today' is by definition after the model's training cutoff, so "
            "it has no reliable memory of it at all. It will confidently "
            "produce three headlines anyway -- either recycled from "
            "whatever was newsworthy near its cutoff date, or invented "
            "outright -- and present them with the same fluent, "
            "authoritative tone as if they were real and current."
        ),
        "cost_of_the_mistake": (
            "Users trust stale or fabricated headlines as today's real "
            "market news, which can directly misinform financial decisions."
        ),
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
        "wrong_call": (
            "The chatbot is prompted with generic company policy text "
            "('employees get 10 sick days per year') and asked to answer "
            "the employee's question directly, without ever looking up "
            "that specific employee's actual remaining balance."
        ),
        "failure_mode": (
            "This data is per-employee, private, and constantly changing -- "
            "it was never in the model's training data and can't be, no "
            "matter how the prompt is worded. The model will either guess a "
            "generic number based on the stated policy (ignoring the days "
            "the employee has already used) or, without any policy text "
            "either, invent a plausible-sounding figure -- and an employee "
            "who trusts a wrong number may plan time off around it."
        ),
        "cost_of_the_mistake": (
            "A concrete, personal wrong answer that an employee can act on "
            "-- and a support/HR escalation when reality doesn't match what "
            "the bot said."
        ),
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
        "wrong_call": (
            "The product embeds the pasted email, retrieves 'similar' "
            "documents from a style guide or writing-tips knowledge base, "
            "and injects those retrieved snippets into the rewrite prompt "
            "alongside the user's email."
        ),
        "failure_mode": (
            "Everything the model needs -- the actual email text -- is "
            "already sitting directly in the prompt; there's nothing to "
            "retrieve. Injecting unrelated 'similar' style-guide snippets "
            "can actually pull the rewrite away from the user's own voice "
            "and content, producing an edited email that sounds more like "
            "generic advice than the user's original message, tuned up."
        ),
        "cost_of_the_mistake": (
            "Added latency and infrastructure cost for a task that was "
            "already solved by the prompt alone, plus a real risk of worse "
            "output quality."
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
        "correct_call": "RAG",
        "wrong_direction": "handled with prompting alone, no retrieval",
        "wrong_call": (
            "The team 'fixes' the inconsistency by tightening the system "
            "prompt -- 'always state our return policy accurately and "
            "consistently' -- without ever giving the model the actual, "
            "current policy text to answer from."
        ),
        "failure_mode": (
            "Telling the model to 'be accurate' does nothing to change what "
            "it actually knows -- it's still answering from a generic, "
            "possibly stale memory of 'a' return policy rather than THIS "
            "company's specific, occasionally-changing one. The answers may "
            "even become more consistent with each other while being "
            "consistently wrong, which is arguably worse: uniform wrong "
            "answers are more likely to be trusted and repeated by "
            "customers than obviously random ones."
        ),
        "cost_of_the_mistake": (
            "Customers act on an incorrect return policy, creating support "
            "disputes and potential real financial/compliance exposure when "
            "the company has to honor -- or fails to honor -- what the bot "
            "told them."
        ),
    },
]


def run_report():
    for case in CASES:
        print(f"\n{'=' * 70}")
        print(f"Scenario {case['id']}: {case['scenario']}")
        print(f"Correct call: {case['correct_call']}")
        print(f"Wrong-direction mistake: {case['wrong_direction']}")
        print(f"{'-' * 70}")
        print(f"  What the wrong call looks like: {case['wrong_call']}")
        print(f"  Failure mode:                   {case['failure_mode']}")
        print(f"  Cost of the mistake:            {case['cost_of_the_mistake']}")


if __name__ == "__main__":
    run_report()
