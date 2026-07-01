# Session 6.5: CI/CD & Versioning for Prompts

**Week:** 6 (Deployment Scaling)
**Format:** Live session + self-paced exercise + quiz

## Learning objective

Treat prompts like code: version them, run a regression suite against them automatically, and gate merges on eval results instead of "it looked fine when I tried it."

## Concept (shared by everyone)

Session 5.1's regression testing (comparing prompt v1 vs. v2 on a golden dataset) was framed as something you'd do manually, once. This session makes it automatic and continuous — the same instinct that makes software teams run tests on every pull request, applied to prompts instead of code.

### Why prompts need version control discipline

A prompt is a specification for behavior, just like code — a one-word change ("Answer concisely" → "Answer in detail") can measurably shift accuracy, tone, cost, and latency all at once. Treating prompt edits as casual text changes, with no history and no test, means:
- You can't answer "what changed between the version that worked and the one that doesn't?"
- You can't roll back to a known-good version quickly when a change makes things worse
- Every teammate might be running a slightly different, un-tracked version of "the prompt"

The fix is the same one code already has: prompts live in version control (not scattered across notebooks or hard-coded strings duplicated in five files), and changes go through the same review process as code.

### The regression gate

Building on Session 5.1's `RegressionTestSuite`, a CI-integrated version looks like:

```
Pull request changes prompts/support_bot.txt
    ↓
CI pipeline runs: score new prompt against golden dataset
    ↓
Compare to the last known-good baseline score
    ↓
If score drops beyond an acceptable threshold → CI fails, PR is blocked
If score holds or improves → CI passes, safe to merge
```

This is not conceptually different from a unit test suite blocking a broken code change — it's the same gate, scoring behavior instead of asserting exact output equality (since LLM outputs aren't deterministic the way most unit-tested code is).

### Versioning strategy

- **Store prompts as their own files** (not inline strings scattered through code), so diffs are readable and history is meaningful.
- **Tag/name versions explicitly** (`support_bot_v3.txt`, or a version field in a prompt config) rather than silently overwriting — this is what let Session 5.1's "v1 vs v2" comparison work at all.
- **Keep the golden dataset in version control too**, and version it alongside the prompts it evaluates, since a golden dataset itself should evolve (as Session 6.4 covered — new failures found in production feed back into it).

### Rollback

When a regression is caught late (in production, not CI), the fastest safe response is reverting to the last known-good prompt version — exactly like reverting a bad code deploy — while you investigate the root cause without users experiencing the regression in the meantime.

## Core path — guided activity

Build a CI-style check function: given a new prompt version and a golden dataset, score it, compare against a stored baseline score, and return pass/fail with a clear message — the same shape as a real CI job's exit code. Full instructions: [`codebase/exercises/week-06/session-6.5/`](../../codebase/exercises/week-06/session-6.5/).

## Pro path — extended challenge

Extend the check into a small version history system: store each prompt version with its score and a timestamp, support "rollback to previous version," and produce a changelog-style report showing score trends across versions — enough to answer "when did this start getting worse, and what changed?"

## Real-world scenario

A teammate tweaks the support bot's system prompt to "sound friendlier" the night before a big product launch, and doesn't run the eval suite because "it's just a wording change." The friendlier prompt turns out to also make the bot less precise about refund policy, and it isn't caught until three days of wrong refund answers after launch. A CI gate that blocks merges below a score threshold would have caught this in the pull request, not in production.

## Key takeaways

- Prompts are specifications for behavior — version them, review changes to them, and test them exactly like code.
- A regression gate compares a new prompt's eval score to a known-good baseline and blocks the change if it drops too far, mirroring how a unit test suite blocks broken code.
- Store prompts as their own versioned files, and version the golden dataset alongside them.
- When a regression slips through to production, the fastest safe fix is rolling back to the last known-good prompt version while you investigate.

## Quiz

See [`assessments/quizzes/week-06/session-6.5-quiz.md`](../../assessments/quizzes/week-06/session-6.5-quiz.md)

## Slide deck

See `assets/slides/week-06/session-6.5.pptx`
