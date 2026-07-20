# Session 3.4 Project — Verifying an Honest "I Don't Know"

The Pro path extended challenge for this session: take the completed RAG
pipeline from the exercises and push it on the exact question the lesson
raises — not "does retrieval find a weak match," but "when a fact is
genuinely absent from the entire document set, does the system say so
honestly, or does it produce a fluent, confident-sounding guess anyway?"

## What you'll build

`starter.py` reproduces the completed pipeline from the Session 3.4
exercises (chunking, embedding, `VectorStore`, `format_context()`,
`build_rag_prompt()`, `call_llm()`, `extract_citations()`,
`answer_question()`) so this file is self-contained. Two new pieces to
write:

1. **`is_grounded_refusal()`** — pure logic, no API call. Given the
   model's raw answer text, detect whether it honestly says the context
   doesn't contain enough information, using a substring check against
   `REFUSAL_PHRASES`.
2. **`run_verification_challenge()`** — run each question in
   `UNANSWERABLE_QUESTIONS` through the full pipeline, check whether
   `is_grounded_refusal()` agrees the system refused honestly, and print
   a clear PASS/FAIL verdict alongside the model's actual answer text.

## This one needs a real API key for the live part

Same situation as the exercises: there's no meaningful toy substitute for
"generate a real answer and check whether it's honest." To run the full
challenge:

```bash
export ANTHROPIC_API_KEY=your-key-here
pip install anthropic pdfplumber numpy --break-system-packages
python3 starter.py
```

## No key yet? The offline path still teaches the core lesson

`is_grounded_refusal()` is pure string logic with no API dependency, and
`offline_test()` validates it against fake answer text — an honest
refusal, a fabricated-but-confident answer, and a normal grounded answer
— with no network access required at all. Running `python3 starter.py`
always runs `offline_test()` first, regardless of whether a key is set.

## Why `tuition reimbursement` and `bereavement leave`

`UNANSWERABLE_QUESTIONS` asks about tuition reimbursement/continuing
education and bereavement leave. Neither is a weak retrieval match —
they're facts that simply never appear anywhere in `sample_handbook.pdf`
(same PDF as the exercises: PTO, sick leave, remote work, expense
reimbursement, health/retirement benefits, parental leave — six sections,
none of them tuition, education, degree programs, or bereavement). No
amount of retrieval tuning could surface a chunk that legitimately
supports an answer to either question, which is exactly what makes this a
clean test of the grounding instruction rather than of retrieval quality.

## Instructions

1. Open `starter.py`.
2. Fill in `is_grounded_refusal()` first — it's the pure-logic piece and
   doesn't need a key.
3. Run `python3 starter.py` and confirm `offline_test()` passes with no
   assertion errors.
4. Fill in `run_verification_challenge()`.
5. With a key set, run `python3 starter.py` again and read the actual
   printed answers for both unanswerable questions — not just the
   PASS/FAIL line.

## What "done" looks like

- `offline_test()` passes with no assertion errors.
- If you have an API key: `run_verification_challenge()` runs both
  unanswerable questions through the real pipeline and prints a verdict
  for each.
- You've personally read the model's actual answer text for at least one
  question, not just trusted the automated PASS/FAIL classification.
  `is_grounded_refusal()` only detects refusal *language* — it can't tell
  you whether a non-refusal answer is actually true, so a human read is
  still the real check.
- You can say, in your own words, which parts of your result you verified
  by direct execution (retrieval, the fact-absence check, the offline
  logic tests) versus which parts you're only trusting the model got
  right on this particular run (the live generated wording).

## Stuck?

A fully worked reference solution — including `VERIFICATION_NOTES`, which
explicitly separates what was checked by direct execution from what
requires your own live API key to verify — is in `solution.py`. Run it
with `python3 solution.py`. Note: the live model-generated wording in
`VERIFICATION_NOTES` was **not** run in the environment that wrote this
solution (no API key was available there) — run it yourself to see your
own live output, and read the printed answers yourself rather than
trusting the automated verdict alone.
