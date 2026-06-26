# Session 3.1 Exercise — "RAG or Not?" Decision Worksheet

## Goal

Build the judgment to tell, *before* writing any retrieval infrastructure,
whether a problem actually needs RAG — or whether it needs something
simpler (a better prompt), something different (a tool call, a database
lookup), or nothing at all (the model already knows this reliably).

This is a reasoning exercise, not a coding exercise — but it's still
structured as a Python file you fill in and run, so you get the same
self-check loop as every other session this program.

## Instructions

1. Open `rag_or_not.py`.
2. For each of the six scenarios in the `SCENARIOS` list, fill in:
   - `decision`: `"RAG"`, `"Not RAG"`, or `"Something else"`
   - `reasoning`: 2-4 sentences applying the framework from the session
     (training-data gap, source traceability, time-sensitivity — versus
     reasoning/timeless-knowledge/prompting-problem)
   - `actual_fix`: if not RAG, name the real fix. Leave as `None` if your
     decision is `"RAG"`.
3. Run the script:

   ```bash
   python3 rag_or_not.py
   ```

   It prints your answers back in a readable format and flags any
   scenario you haven't filled in yet.

## Core path

Work through all six scenarios using the framework above. Don't aim for
the "expected" answer — argue your case. A couple of these are
deliberately close calls.

## Pro path — extended challenge

For scenario 4 (the HR chatbot), go one level deeper: even once you've
correctly identified that this needs *some* form of retrieval, is
semantic/vector-based RAG (the kind you'll build in 3.2–3.4) actually the
right retrieval mechanism here — or does a question like "how many sick
days do I have left" call for a direct, structured database lookup
instead, with the LLM only used to phrase the final answer naturally?
Write 3-4 sentences on the distinction. This previews a real distinction
you'll need in production: not all "give the model real data" problems are
solved by *vector search* specifically.

## What "done" looks like

- All six scenarios have a decision, reasoning, and (where relevant) an
  actual fix filled in.
- Your reasoning explicitly references at least one of the three RAG
  criteria (training-data gap, traceability, time-sensitivity) or one of
  the three non-RAG signals (reasoning task, timeless knowledge, prompting
  problem) — not just a gut-feel decision.
- Running `python3 rag_or_not.py` shows no "[NOT FILLED IN YET]" scenarios.

## Stuck, or want to check your reasoning?

A fully worked answer key with reasoning for all six scenarios (plus the
Pro path question) is in `codebase/solutions/week-03/session-3.1/`. Try
your own reasoning first — disagreeing with the key on a close call is
fine, as long as you can articulate why using the same framework.
