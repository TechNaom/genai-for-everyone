# Session 3.5 Exercise — Debug a Broken RAG Pipeline

## Goal

Diagnose three real, planted failure modes in a working-but-broken RAG
pipeline, using direct inspection of retrieved chunks — not guesswork,
and not judging by how confident any output sounds.

## This is a diagnostic exercise, not a coding exercise

`broken_pipeline.py` is **given to you broken on purpose** — do not fix
the bugs in it. Each of its three test cases has exactly one planted
failure mode from today's session: a chunking error, a retrieval miss,
or context stuffing. Your actual work happens in
`diagnosis_worksheet.py`.

## Instructions

1. Run the broken pipeline first, and read its output carefully:

   ```bash
   python3 broken_pipeline.py
   ```

   For each of the three cases, look at: the pipeline configuration
   used, the question asked, and the actual chunks retrieved (with
   their similarity scores).

2. Open `diagnosis_worksheet.py` and fill in, for each case:
   - `diagnosis` — which of the three failure modes is responsible
   - `evidence` — specific details from the actual printed output that
     support your diagnosis (exact similarity scores, exact chunk text,
     where a sentence got cut off) — not a generic definition restated
   - `proposed_fix` — what you'd actually change in the configuration

3. Run your worksheet:

   ```bash
   python3 diagnosis_worksheet.py
   ```

## Core path

Diagnose all three cases. Resist the urge to pattern-match on the case
number matching the order failure modes were introduced in the lesson —
read the actual evidence for each case independently.

## Pro path — extended challenge

1. **Find the exact orphaned word.** For Case 1, look at the chunking
   configuration (`chunk_size=15, overlap=0`) and manually compute (or
   print, by editing a scratch copy — not `broken_pipeline.py` itself)
   which two consecutive chunks the key sentence about sick leave
   carryover got split across. Identify the specific word or phrase that
   ends up missing from both halves.
2. **Propose a re-ranking fix for Case 2.** Case 2 is a retrieval miss
   caused by vocabulary mismatch ("telecommute" vs. "remote work"). A
   larger k alone doesn't fully fix a vocabulary mismatch problem the
   way it might help with a narrowly-missed near-match — explain in 2-3
   sentences why, and what a re-ranking step would need to actually
   evaluate to recover from this kind of miss.
3. **Quantify Case 3's dilution.** For Case 3, calculate what fraction
   of the 10 retrieved chunks have a similarity score below 0.15 (a
   reasonable "probably not actually relevant" threshold for this toy
   embedding). What does that fraction tell you about where a more
   conservative k value should have been set instead?

## What "done" looks like

- All three cases have a diagnosis, evidence, and proposed fix filled in.
- Your evidence cites something specific and checkable from the actual
  output — a similarity score, an exact chunk boundary, a missing word —
  not just a restatement of "this is what a [failure mode] looks like."
- You can explain, for at least one case, why the OTHER two diagnoses
  don't fit as well as the one you chose.

## Stuck?

A fully worked answer key with reasoning for all three cases, plus the
Pro path answers, is in `codebase/solutions/week-03/session-3.5/`. Try
your own diagnosis first — this is a genuinely useful skill to practice
under your own steam before checking against someone else's reasoning.
