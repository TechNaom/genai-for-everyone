"""
Session 3.5 Exercise — Diagnosis Worksheet

Run broken_pipeline.py first and read its output carefully. For each of
the three cases, you'll see a question, a pipeline configuration, and
the actual chunks that got retrieved.

Your job: diagnose WHICH of today's three failure modes is responsible
for each case, and WHY -- using direct evidence from the printed output,
not a guess.

The three possible diagnoses (you may use each at most once, or more
than once if you genuinely believe two cases share a cause -- argue
your case either way):
    - "chunking error"     (an idea got orphaned/diluted by bad chunk
                             boundaries or size)
    - "retrieval miss"      (the right chunk exists in the document but
                             didn't make it into the top-k results,
                             typically due to vocabulary mismatch)
    - "context stuffing"    (too many low-relevance chunks retrieved,
                             diluting the genuinely useful ones)

For each case, fill in:
    diagnosis:        one of the three strings above
    evidence:         2-4 sentences citing SPECIFIC details from the
                       actual printed output (similarity scores, exact
                       chunk text, chunk boundaries) -- not a generic
                       restatement of the failure mode's definition
    proposed_fix:      1-3 sentences on what you'd actually change in
                       the pipeline configuration to address it

Then run this file: python3 diagnosis_worksheet.py
It will print your answers and flag any case you haven't filled in yet.
"""

CASE_1 = {
    "question": "How many sick days do employees get and do they roll over?",
    "diagnosis": None,      # TODO: "chunking error" / "retrieval miss" / "context stuffing"
    "evidence": None,       # TODO
    "proposed_fix": None,   # TODO
}

CASE_2 = {
    "question": "Can I telecommute instead of going to the office?",
    "diagnosis": None,
    "evidence": None,
    "proposed_fix": None,
}

CASE_3 = {
    "question": "How many PTO days do employees get per year?",
    "diagnosis": None,
    "evidence": None,
    "proposed_fix": None,
}

ALL_CASES = [("Case 1", CASE_1), ("Case 2", CASE_2), ("Case 3", CASE_3)]


def print_diagnosis():
    incomplete = []

    for name, case in ALL_CASES:
        print(f"\n{'=' * 70}")
        print(f"{name}: {case['question']}")
        print(f"{'-' * 70}")

        if case["diagnosis"] is None:
            incomplete.append(name)
            print("  [NOT FILLED IN YET]")
            continue

        print(f"  Diagnosis:    {case['diagnosis']}")
        print(f"  Evidence:     {case['evidence']}")
        print(f"  Proposed fix: {case['proposed_fix']}")

    print(f"\n{'=' * 70}")
    if incomplete:
        print(f"Still need to diagnose: {incomplete}")
    else:
        print("All three cases diagnosed. Check your reasoning against")
        print("the answer key in codebase/solutions/week-03/session-3.5/")


if __name__ == "__main__":
    print_diagnosis()
