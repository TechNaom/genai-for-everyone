"""
Session 3.5 — Reference Solution
Diagnosis Worksheet (completed)
===========================================================================

Try the exercise yourself first -- the value is in practicing the
diagnostic process, not reading someone else's diagnosis.

All evidence below was obtained by actually running broken_pipeline.py
and inspecting its real, reproducible output -- nothing here is a
hypothetical or idealized example.
"""

CASE_1 = {
    "question": "How many sick days do employees get and do they roll over?",
    "diagnosis": "chunking error",
    "evidence": (
        "With chunk_size=15 and overlap=0, the source sentence about sick "
        "leave gets split across two separate chunks with nothing shared "
        "between them: one chunk ends with '...Sick days do not carry' and "
        "the very next chunk begins with 'over to the following year...'. "
        "Neither chunk alone contains the complete fact. The top-3 results "
        "do surface fragments related to sick leave (sim=0.311, 0.234, "
        "0.234), but the single most specific fact -- that sick days do "
        "NOT carry over -- is the exact phrase that got orphaned by the "
        "zero-overlap cut."
    ),
    "proposed_fix": (
        "Increase overlap so that consecutive chunks share enough words "
        "that an idea spanning a chunk boundary is fully contained in at "
        "least one of the two chunks -- e.g. overlap=5 or more at this "
        "chunk size, following the session's general guidance of roughly "
        "10-20% overlap relative to chunk size."
    ),
}

CASE_2 = {
    "question": "Can I telecommute instead of going to the office?",
    "diagnosis": "retrieval miss",
    "evidence": (
        "The actual Remote Work Policy section of the handbook (which "
        "directly answers this question -- 'up to three days per week "
        "without prior approval') does not appear anywhere in the top-3 "
        "results. The top match (sim=0.436) is about 401(k) and health "
        "plan tiers -- entirely unrelated. The second match (sim=0.434) "
        "does contain the word 'remote' but is actually about the home-"
        "office equipment reimbursement allowance, not the remote work "
        "policy itself -- a different section that happens to share one "
        "word with the query. The third match (sim=0.384) is about "
        "parental leave -- also unrelated. This happens because the query "
        "uses 'telecommute' and 'office', and 'telecommute' in particular "
        "appears nowhere in the handbook's actual text (which says "
        "'remote', 'remotely', 'hybrid'), so the word-count embedding "
        "can't connect the query to the section that actually answers it, "
        "and instead surfaces chunks that share a few incidental words "
        "instead."
    ),
    "proposed_fix": (
        "A larger k alone would not reliably fix this -- the correct "
        "chunk isn't a near-miss sitting just outside the top-3, it's "
        "fundamentally not similar under this embedding's vocabulary-"
        "overlap logic. The more targeted fix is a better embedding model "
        "(a real, trained embedding model would recognize 'telecommute' "
        "and 'remote work' as closely related concepts even with no "
        "shared letters) or, short of that, a re-ranking step using a "
        "method that evaluates semantic relevance more directly than raw "
        "word-count cosine similarity."
    ),
}

CASE_3 = {
    "question": "How many PTO days do employees get per year?",
    "diagnosis": "context stuffing",
    "evidence": (
        "At k=10 against an 11-chunk document, the system retrieves "
        "nearly the entire handbook for one specific question. The "
        "similarity scores show a clear quality cliff: the top 5 results "
        "(0.359, 0.345, 0.299, 0.262, 0.243) are plausibly relevant, but "
        "results 6 through 10 drop to 0.153, 0.148, 0.147, 0.053, and "
        "0.025 -- the last two are close to or at zero similarity, meaning "
        "they share almost no vocabulary with the query at all. Of the 10 "
        "chunks retrieved, 4 (40%) score below 0.15, well into "
        "'essentially unrelated' territory, yet all 10 would be handed to "
        "the model as if equally worth considering."
    ),
    "proposed_fix": (
        "Lower k substantially -- the genuinely relevant signal is "
        "concentrated in the top 3-5 results here, and there's a visible "
        "score cliff after rank 5 that a more conservative k (e.g. k=3 or "
        "k=5) would respect. If retrieval still feels unreliable at a "
        "lower k on harder questions, the fix is re-ranking over a wider "
        "initial candidate pool, not simply raising k and handing "
        "everything to the model regardless of relevance."
    ),
}

ALL_CASES = [("Case 1", CASE_1), ("Case 2", CASE_2), ("Case 3", CASE_3)]


PRO_PATH_NOTES = """
Pro path answers:

1. Exact orphaned word/phrase (Case 1): running chunk_text() on the
   handbook text at chunk_size=15, overlap=0 and inspecting chunks 15
   and 16 directly shows:
     chunk[15] = "...available in full starting January 1st rather
                   than accruing monthly. Sick days do not carry"
     chunk[16] = "over to the following year and are not paid out
                   upon separation from the company..."
   The orphaned phrase is "carry over" -- split exactly across the verb
   phrase itself, with "carry" stranded at the end of one chunk and
   "over" stranded at the start of the next. Neither chunk alone
   contains the complete, searchable phrase "carry over," which is the
   single most important phrase for answering this specific question.

2. Why k alone doesn't fix Case 2, and what re-ranking needs to do
   instead: increasing k helps when the correct chunk is a near-miss --
   sitting just below the cutoff but still reasonably similar under the
   same similarity measure. Case 2 isn't that: the correct chunk has
   genuinely low word-count similarity to the query, because "telecommute"
   and "office" share no vocabulary with "remote," "remotely," or
   "hybrid" at all. Pulling in more chunks via a higher k doesn't change
   the underlying similarity scores -- the correct chunk could still rank
   low even among 20 or 50 candidates. A re-ranking step would need to
   evaluate actual semantic relevance between the query and each
   candidate -- recognizing that "telecommute" and "remote work" describe
   the same real-world concept -- rather than just re-sorting by the same
   word-overlap signal that caused the miss in the first place.

   (The project for this session digs into this case further: it turns
   out the correct chunk isn't buried arbitrarily deep -- it sits just
   outside the top-3 cutoff. See project/index.html for what actually
   pushed the wrong chunks above it.)

3. Quantifying Case 3's dilution: of the 10 chunks retrieved at k=10,
   4 (40%) score below 0.15 -- a reasonable "probably not actually
   relevant" threshold for this toy embedding. Looking at the actual
   score sequence (0.359, 0.345, 0.299, 0.262, 0.243, then a drop to
   0.153, 0.148, 0.147, 0.053, 0.025), there's a visible cliff after
   rank 5: the gap from rank 5 (0.243) to rank 6 (0.153) is larger than
   any gap among the top 5, and ranks 9-10 are barely above zero
   similarity. This suggests a more conservative k of around 5 -- or
   even 3 -- would have captured the genuinely relevant signal without
   diluting it with several chunks that share almost no real connection
   to the query.
"""


def print_diagnosis():
    for name, case in ALL_CASES:
        print(f"\n{'=' * 70}")
        print(f"{name}: {case['question']}")
        print(f"{'-' * 70}")
        print(f"  Diagnosis:    {case['diagnosis']}")
        print(f"  Evidence:     {case['evidence']}")
        print(f"  Proposed fix: {case['proposed_fix']}")

    print(f"\n{'=' * 70}")
    print(PRO_PATH_NOTES)


if __name__ == "__main__":
    print_diagnosis()
