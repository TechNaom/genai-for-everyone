# Session 4.4 Project: Multi-Reviewer System with Convergence Checking

The Pro-Path build for Session 4.4 — a sophisticated multi-reviewer system:

1. **Writer Agent** — creates or revises the essay
2. **Fact-Checker Agent** — reviews accuracy
3. **Style-Checker Agent** — reviews clarity
4. **Impact-Checker Agent** — reviews engagement

With **convergence checking**: the loop stops once feedback stops changing
(the reviewers are no longer surfacing new issues), instead of always running
a fixed number of revision rounds.

This is deliberately less scaffolded than the Core Path exercise. The writer
and all three reviewers are already implemented for you in `starter.py` — the
work here is running it, understanding how the pieces fit together, and then
extending it through the challenges below.

## What you'll build

Run `starter.py` as-is first, then work through:

- Changing `convergence_threshold` to `0.5` or `0.8` — do more or fewer
  revisions happen?
- Adding a 4th reviewer (e.g. an audience-relevance checker) — `solution.py`
  shows one worked version of this.
- Replacing `similarity_score()` (a crude word-overlap heuristic) with an
  LLM-based similarity check.

## Setup — this project makes real API calls

```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-..."
python starter.py
```

## Example run

```
Topic: The ethics of AI in hiring

=== Revision Round 1 ===
Fact-checking...
  → AI hiring systems have documented bias issues [sources needed]...

Checking style...
  → Strong opening, but paragraph 3 is dense...

Checking impact...
  → Good ethical framing, but missing a call-to-action...

Convergence score: 0.42
Writer revising...

=== Revision Round 2 ===
[More feedback, higher convergence...]

Convergence score: 0.68
Feedback converged (> 0.65). Stopping.

RESULTS SUMMARY
Topic: The ethics of AI in hiring
Total revisions: 2
Stopped because: convergence
```

## How convergence checking works

`similarity_score()` compares the current round's combined reviewer feedback
against the previous round's, using simple word overlap (intersection over
union of the two feedback strings' word sets). When that score crosses
`convergence_threshold`, the loop treats the feedback as having stabilized —
reviewers are largely repeating the same points rather than surfacing new
ones — and stops, even if `max_revisions` hasn't been reached yet. This is
the same "define your stopping condition before building" idea from Part 6 of
the lesson, applied concretely.

Note that convergence here is a placeholder heuristic, not a rigorous
similarity measure — word overlap can be fooled by paraphrased feedback that
means the same thing in different words. The third challenge above
(replacing it with an LLM-based similarity check) is exactly this
limitation, made explicit.

## Key learning

- How to coordinate multiple specialized reviewers running independently
- Feedback aggregation: combining several reviewers' input into one writer
  revision prompt
- Convergence detection as a stopping condition, distinct from simply
  "agents agree" — it means the *feedback pattern* has stabilized
- The trade-off made concrete: more reviewers catch more, but each one is
  another API call and another few seconds of latency

## Extensions

- **Orchestrator pattern:** instead of writer + reviewers, try an
  orchestrator agent that assigns "researcher, find data" tasks to a
  researcher agent, then hands the results to a writer agent to synthesize.
- **Debate pattern:** implement competing viewpoints — a pro agent argues for
  a position, a con agent argues against it, and a moderator agent
  synthesizes the two.
- **Persistence:** save drafts and feedback history to JSON with
  `json.dump(result, f, indent=2)` so a run can be inspected after the fact.
- **Feedback scoring:** have the writer rank which piece of feedback across
  all reviewers was most important to address first.

## Solution

See `solution.py` in this folder for a version with the 4th
audience-relevance reviewer already added, as a worked example of the first
extension challenge.
