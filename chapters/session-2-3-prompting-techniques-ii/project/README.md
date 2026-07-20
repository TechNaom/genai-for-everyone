# Session 2.3 Project: Self-Consistency Checker

The Pro path build for this session &mdash; a small, reusable tool that
implements the self-consistency technique for real: ask a model the same
question several independent times, extract a comparable short answer from
each response, and detect whether the answers converge or diverge.

## What you'll build

Given a question and a number of runs, the checker:

1. Calls the model `N` times on the exact same prompt, with sampling
   randomness enabled (`temperature=1.0`) so the runs are genuinely
   independent attempts rather than identical copies.
2. Extracts a short, comparable answer from each response (the model is
   asked to end with a `Final answer: <answer>` line to make this parseable).
3. Tallies the answers and computes a convergence ratio &mdash; what fraction
   of runs agreed with the majority answer.
4. Prints a plain-language interpretation: high convergence means treat the
   answer as reasonably reliable; low convergence means this is a genuinely
   hard case and no single run should be trusted at face value.

You'll test it on two questions with very different expected behavior:

- **An easy question** ("What is 12 times 4?") &mdash; expect high convergence.
- **A tricky question** (the classic "bat and ball" cognitive-reflection
  puzzle, where the intuitive answer is wrong) &mdash; expect more divergence,
  since models sometimes get pulled toward the intuitive-but-wrong answer on
  some runs and the correct one on others.

## How to run it

```bash
pip install anthropic python-dotenv
export ANTHROPIC_API_KEY="your-key-here"
python starter.py
```

Fill in the three `# TODO` sections in `starter.py`:

- **TODO 1** &mdash; `query_n_times`: call the model `n` independent times on
  the same prompt and collect the raw response strings.
- **TODO 2** &mdash; `extract_answer`: parse the `Final answer: ...` line out
  of a response, returning `"UNPARSEABLE"` if the model didn't follow the
  format (don't let a malformed response crash the whole run).
- **TODO 3** &mdash; `check_convergence`: tally the extracted answers with
  `collections.Counter`, find the majority answer, and compute what fraction
  of runs agreed with it.

Want to see one finished version first? Run `python solution.py`.

## Ideas to make it your own (optional stretch goals)

- Swap in your own genuinely ambiguous question and see how the convergence
  ratio behaves.
- Print the full text of any response that disagreed with the majority, so
  you can actually read where its reasoning diverged.
- Add a cost estimate: `RUNS_PER_QUESTION` calls instead of 1 is exactly the
  "honest cost" trade-off from this session — try computing how much a
  5-run self-consistency check costs versus a single call, using Session
  1.3's per-token pricing framing.

## Why this project matters

This is self-consistency exactly as described in this session, minus the
hand-waving: real independent calls, a real extraction step, and a real
convergence number you can act on. It's also a small, honest demonstration
of the technique's cost — running this file makes ten actual API calls (five
per question) instead of two, which is precisely the trade-off Session 2.3
asks you to reason about before reaching for this technique in production.
