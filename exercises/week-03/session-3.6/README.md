# Session 3.6 — Week 3 Lab: Company Policy Q&A Bot

## What you're building

A Q&A bot that answers employee questions by retrieving from **four
separate company policy documents** instead of one handbook:

- `remote_work_policy.pdf`
- `expense_policy.pdf`
- `leave_policy.pdf`
- `it_security_policy.pdf`

This is the integration lab for everything in Week 3. You'll use:

| Week 3 session | What you're reusing here |
|---|---|
| 3.2 Embeddings | `tokenize()`, `vectorize()`, `cosine_sim()` |
| 3.3 Vector stores | Chunking + a searchable `PolicyVectorStore` |
| 3.4 RAG pipeline | `format_context()`, `build_rag_prompt()`, `extract_citations()` |
| 3.5 Failure modes | Diagnosing and fixing a real chunking bug (Part 4) |

## Files

- `exercise.py` — your starter file. Every `TODO` needs filling in.
- `solution.py` — the reference answer key. Don't open it until you've
  given Part 1–4 a real attempt.
- `policy_docs/` — the four source PDFs (already generated, don't edit).

## How to work through it

1. **Parts 1–3**: fill in `load_documents`, `chunk_text`,
   `build_corpus_chunks`, `PolicyVectorStore`, `format_context`,
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
   AssertionError: Your section-aware chunking should fix this retrieval...
   ```
   That's expected — `chunk_text_by_section()` is still a stub. But
   before you fill it in, go diagnose *why* the bot gets this question
   wrong using your Part 1 chunker:

   > "What is the home office equipment stipend amount?"

   It should come from `remote_work_policy.pdf`, but with blank-line
   chunking it pulls from `expense_policy.pdf` instead. Investigate:
   - Print out the chunks for `remote_work_policy.pdf`. How many are
     there? How big is the biggest one?
   - Try changing `target_words` in `chunk_text()` to 80, then 50, then
     25. Does the chunk boundary move at all?
   - Print `repr(text[:300])` for one loaded document and look closely
     at where the actual newlines are.

   Once you understand *why* it's broken, write
   `chunk_text_by_section()` to split on numbered section headers
   instead of blank lines, and confirm the bug is fixed.

3. **Optional — live model answers.** Set `ANTHROPIC_API_KEY` in your
   environment and try the full pipeline end-to-end with real generated
   answers (the questions in `DEMO_QUESTIONS` inside `solution.py`
   include one that's genuinely unanswerable from the corpus — watch
   what an honest, well-grounded RAG system says when it can't find the
   answer, instead of guessing).

## A note on the Part 4 bug

This bug isn't a contrived classroom example — it's a real failure mode
you'll hit with PDF-sourced documents in production. PDF text extraction
libraries (here, `pypdf`) generally do **not** preserve the blank lines
that separated sections in the original layout. A chunker that assumes
"blank line = paragraph break" — which is a completely reasonable
assumption for clean markdown or plain text — can silently collapse an
entire multi-section PDF into a single oversized chunk, no matter what
`target_words` is set to. The fix isn't a magic number; it's matching
your chunking strategy to the actual structure of your source documents.

## Pro path

If you finish early: add a second source document type (try a `.txt`
file alongside the PDFs) and confirm your pipeline handles a mixed
corpus without any changes to `PolicyVectorStore` — that's the payoff of
keeping retrieval and document-loading cleanly separated.
