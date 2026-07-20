# Session 3.4 Exercise — Building a RAG Pipeline

## Goal

Complete the pipeline from Session 3.3: take retrieved chunks, format
them into citeable context, build a grounded prompt, generate an answer
with a real LLM call, and extract which chunks the model actually cited.

## This one needs a real API key

Sessions 3.1–3.3 were designed to run fully offline. This session is
different: generating a grounded answer is the actual point of today's
exercise, and there's no meaningful toy substitute for "call an LLM and
get a real answer." To run the full pipeline:

```bash
export ANTHROPIC_API_KEY=your-key-here
pip install anthropic pdfplumber numpy --break-system-packages
python3 starter.py
```

If you don't have a key yet, you can still do most of the real work
offline — `format_context()` and `extract_citations()` are pure logic
with no API dependency, and the starter file includes `offline_test()`,
which validates both without needing any API access. Get those two
functions right first; they're most of what this session is actually
teaching.

## Instructions

1. Open `starter.py`.
2. Fill in the TODOs, in order:
   - `format_context()` — turn `(chunk_text, score)` tuples into clean,
     numbered context (no similarity scores in the output).
   - `build_rag_prompt()` — fill in `RAG_PROMPT_TEMPLATE`'s variables.
   - `extract_citations()` — pull out cited chunk numbers like `[1]`,
     `[2]` from the model's answer text.
   - `answer_question()` — tie the full retrieve → augment → generate →
     extract-citations pipeline together.
3. Run `python3 starter.py`. This runs `offline_test()` first (no API
   key needed), then attempts the full pipeline against three real test
   questions (API key required for this part).

## Core path

Get `offline_test()` passing first. Then, if you have an API key, get
the full pipeline running against the three test questions.

Look closely at the third test question — "Does the company offer
dental insurance?" — which is deliberately **not** answerable from the
handbook (`sample_handbook.pdf`, included in this folder). Check: does
your system say so honestly, or does it generate a plausible-sounding
answer anyway? This is the exact behavior the session's prompt template
is designed to produce, and it's worth verifying directly rather than
assuming the instruction worked.

## Pro path — extended challenge

1. **Verify a citation by hand.** Pick one test question, find which
   chunk number the model cited, and manually check the actual chunk
   text in `result["retrieved_chunks"]` — does that chunk genuinely
   support the claim the model attached the citation to? Write 2-3
   sentences on what you found.
2. **Break the grounding instruction on purpose.** Make a copy of
   `RAG_PROMPT_TEMPLATE` with the first paragraph (the "ONLY the
   information in the provided context" instruction) removed entirely,
   and rerun the dental insurance question through it. Does the model's
   behavior change? This directly demonstrates why that instruction is
   doing real work, not just adding boilerplate.
3. **Test a chunk-size mismatch.** Build the store with a deliberately
   poor chunk size (try `chunk_size=20` or `chunk_size=400`) and rerun
   one of the real test questions. Does a weaker retrieval step produce
   a visibly weaker grounded answer, or does the model's phrasing paper
   over the gap? Compare what you see here to Session 3.3's honest
   results table.

For a fuller version of this extended challenge — including exactly how
to check whether a genuinely unanswerable question gets an honest
non-answer, and how to separate what you've directly verified from what
you're only assuming will work — see the [project](../project/index.html).

## What "done" looks like

- `offline_test()` passes with no assertion errors.
- If you have an API key: all three test questions return an answer with
  at least one citation attached, except the dental insurance question,
  which should honestly state the information isn't available rather
  than guessing.
- You've manually checked at least one citation against its actual chunk
  text.

## Stuck?

A fully worked reference solution, including the Pro path observations
written against a real API run, is in `solution.py` in this same folder.
Run it with `python3 solution.py`.
