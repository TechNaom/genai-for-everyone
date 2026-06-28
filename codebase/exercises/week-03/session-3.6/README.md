# Session 3.6 — Week 3 Lab: Campus Student Services Q&A Bot

## What you're building

A Q&A bot that answers student questions by retrieving from **four
separate campus documents** instead of one handbook:

- `registration_guide.pdf`
- `financial_aid_handbook.pdf`
- `academic_standing_policy.pdf`
- `housing_handbook.pdf`

This is the integration lab for everything in Week 3. You'll use:

| Week 3 session | What you're reusing here |
|---|---|
| 3.2 Embeddings | `tokenize()`, `vectorize()`, `cosine_sim()` |
| 3.3 Vector stores | Chunking + a searchable `CampusVectorStore` |
| 3.4 RAG pipeline | `format_context()`, `build_rag_prompt()`, `extract_citations()` |
| 3.5 Failure modes | Diagnosing and fixing a real chunking bug (Part 4) |

## Files

- `exercise.py` — your starter file. Every `TODO` needs filling in.
- `solution.py` — the reference answer key. Don't open it until you've
  given Part 1–4 a real attempt.
- `campus_docs/` — the four source PDFs (already generated, don't edit).

## How to work through it

1. **Parts 1–3**: fill in `load_documents`, `chunk_text`,
   `build_corpus_chunks`, `CampusVectorStore`, `format_context`,
   `build_rag_prompt`, `extract_citations`, and `answer_question`.
   Run:
   ```
   python3 exercise.py
   ```
   Keep going until everything through "Part 3" passes. None of this
   needs an API key.

2. **Part 4 — this is the real lesson of the lab.** Once Parts 1–3
   pass, the Part 4 check will almost certainly **fail**:
   ```
   AssertionError: Your caps-header chunking should fix this retrieval...
   ```
   That's expected — `chunk_text_by_caps_header()` is still a stub.
   Before filling it in, diagnose why the bot gets these questions
   wrong with your Part 1 chunker:

   > "What is the maximum course load for a student on probation?"
   > "What happens if I drop below full-time enrollment while living in a dorm?"

   Both should come from `academic_standing_policy.pdf` and
   `housing_handbook.pdf` respectively — but with blank-line chunking,
   both incorrectly pull from `registration_guide.pdf` instead, because
   that document's one giant merged chunk happens to mention "course
   load" and "full-time" in passing, even though it isn't the right
   answer to either question.

   Investigate:
   - Print out the chunks for `registration_guide.pdf`. How many are
     there? How big is the biggest one?
   - Try changing `target_words` in `chunk_text()` to 80, then 50, then
     25. Does the chunk boundary move at all?
   - Print `repr(text[:300])` for one loaded document and look at how
     the section headers are actually written in the extracted text —
     are they numbered? Something else?

   Once you understand *why* it's broken, write
   `chunk_text_by_caps_header()` to split on this corpus's actual
   header style, and confirm the bug is fixed for both questions.

3. **Optional — live model answers.** Set `ANTHROPIC_API_KEY` and try
   the full pipeline end-to-end (the `DEMO_QUESTIONS` in `solution.py`
   include one that's genuinely unanswerable from this corpus — watch
   what an honest, well-grounded RAG system says when it can't find the
   answer).

## A note on the Part 4 bug

This is a different chunking bug than you may have seen elsewhere in
this course, on purpose. The underlying cause is the same general
problem — PDF text extraction doesn't reliably preserve blank lines
between sections — but the *fix* is genuinely different, because this
corpus's documents use a different section-header style (ALL CAPS on
their own line, not numbered headers). A fix that worked for a numbered
document wouldn't catch a single header here. The actual lesson isn't
"split on caps headers" as a universal rule — it's that you have to
look at how *your specific documents* are actually structured before
choosing a splitting strategy, every time, for every new document type
you bring into a RAG system.

## Pro path

If you finish early: write a quick script that runs every test question
in `offline_test()` against BOTH the baseline and fixed chunkers, and
report how many of the 8 questions each gets right. Confirm the fixed
chunker doesn't just fix the two known bugs — check whether it changes
the result on any of the other six questions too, and if so, whether
that's an improvement or a regression.
