# Session 5.1 Project: Regression Testing (Pro Path)

## Overview

The Pro-path build for this session: a **regression testing framework** that compares two prompt versions on the same golden dataset, so you can see trade-offs explicitly instead of trusting a gut feel.

(Looking for the Core Path golden-dataset build first? See `../exercises/README.md`.)

---

## Pro Path: Regression Testing

**Files:** `starter.py`, `solution.py`

Note: as with the Core Path, `starter.py` and `solution.py` in this repo are identical — this is a fully working reference implementation, not a fill-in-the-blank stub. Trace how it works, then use it as a framework for testing your own prompt changes.

### What you'll build

A **regression test suite** that compares two prompt versions:

1. **Baseline (v1):** Test on golden dataset, record scores
2. **Improved (v2):** Test on same dataset, record new scores
3. **Compare:** Show improvements, regressions, net change
4. **Decide:** Is v2 better?

### How it works

```
Golden Dataset (5 examples, multiple criteria)
  ↓
Test Prompt V1
  Relevance: 85%, Accuracy: 90%, Helpfulness: 75% → Overall: 83%
  ↓
Test Prompt V2
  Relevance: 90%, Accuracy: 88%, Helpfulness: 85% → Overall: 88%
  ↓
Compare:
  Relevance: +5% (improved)
  Accuracy: -2% (regression)
  Helpfulness: +10% (improved)
  Overall: +5% (net improvement)
  ↓
Decision: Promote V2 to production
```

### Run it

```bash
python starter.py
```

### Expected output

```
Testing PROMPT V1 (Baseline)...
Testing PROMPT V2 (Improved)...

======================================================================
REGRESSION TEST: Prompt V1 (Basic) vs Prompt V2 (Helpful)
======================================================================

Metric               v1 Score        v2 Score        Change          Status
----------------------------------------------------------------------
Relevance            85.0            90.0           +5.0%           Improved
Accuracy             90.0            88.0           -2.0%           Regressed
Helpfulness          75.0            85.0          +10.0%           Improved
Overall              83.3            87.7           +4.4%           Improved
======================================================================

DECISION:
  Improvements: 2
  Regressions: 1
  Overall change: +4.4%

V2 is better overall. Recommend promoting to production.
```

### Key learning

- Regression testing prevents breaking existing functionality
- Trade-offs are explicit (see all metrics)
- Data-driven decisions (not gut feel)
- Version management (track prompt changes like code)

---

## A deliberately weak proxy — read this before you trust the numbers

Look closely at `score_response` in `starter.py`:

```python
elif criterion == "Accuracy":
    # For this mock, assume accuracy is based on response length (poor proxy!)
    scores[criterion] = min(len(actual) / 100, 1.0)
```

The comment isn't decoration — this is a genuinely fragile stand-in for "Accuracy," and it's worth understanding exactly why before you reuse this pattern anywhere real.

**Why it's fragile:** "Accuracy" should mean "is the information in the response correct." Instead, this scores accuracy purely on how many characters the response contains, capped at 100. That means:

- A response that is longer but padded with irrelevant filler scores *higher* on "Accuracy" than a short response that is factually perfect. Prompt v2's responses are longer than v1's largely because they're more verbose (more instructions, more sign-off text), not because they contain more correct facts.
- A response could be 100+ characters of confident, fluent, completely wrong information and still score a perfect 1.0 on this metric.
- Nothing here checks the response against `expected_output` at all for this criterion — compare that to the `Relevance` criterion just above it, which at least does a substring check against `expected`.

**Why it's a good debugging exercise:** in the sample run above, `Accuracy` goes from 90.0 (v1) to 88.0 (v2) — a "regression." But look at what actually happened: v1's canned response for "reset password" is `"You can reset your password."` (29 characters → scores low on this length proxy) and v2's is a longer, more helpful, and *also correct* response. If the length proxy happened to reward v1's shorter responses on this run, that "regression" isn't telling you v2 got less accurate — it's telling you v2's responses have a different length profile. A real regression in *correctness* would look completely different from a regression in *length*, but this metric can't tell them apart.

**The fix, if you were building this for real:** don't score Accuracy by proxy at all. Compare the actual claims in the response against a verified expected answer — by hand (as the Core Path's rubric does, which is why the exercises path avoids this proxy), with an LLM-as-judge prompt that's shown the expected answer and asked whether the response contradicts it (Session 5.2 covers this), or with automatic checks for specific hallucination patterns (invented URLs, invented policy details, wrong numbers). The general lesson: any time a metric substitutes an easy-to-compute proxy (length, keyword presence, sentiment) for the thing you actually care about (correctness, safety, relevance), that gap is exactly where a regression test can tell you the opposite of the truth.

---

## What to build if you're extending this

1. **Add your own examples** — same five in `starter.py` are a starting point, not a ceiling. Add more, and make sure they include cases where a length-based Accuracy proxy would clearly mislead you (a long, wrong answer vs. a short, correct one).
2. **Replace the Accuracy proxy** — write a version of `score_response` that actually compares `actual` against `expected` for correctness rather than length. Even a stricter keyword-overlap check would be an improvement over character count.
3. **Trace a regression to its cause** — for any metric that regresses when you swap in your own prompt versions, don't just report the percentage change. Look at the actual example outputs and explain *why* the number moved, the same way this chapter's lesson traced the accuracy/safety trade-off back to specific examples (Part 3 of the lesson).

## Debugging Tips

### "My scores are all 0"
- Check the mock prompt responses
- Are your expected outputs realistic?
- Is your scoring logic too strict?

### "I'm getting inconsistent scores"
- Scoring should be deterministic (same input = same score)
- If using manual scoring, create a detailed rubric
- Consider using an LLM for consistency

### "Everything looks like an improvement"
- Double check whether your metric is actually measuring what you think it's measuring — see the Accuracy proxy discussion above
- A metric that trends the same direction as an unrelated variable (like response length) will look like consistent improvement even when nothing meaningful changed

---

## Production Checklist

Before shipping, ensure:

- Golden dataset covers happy path + edge cases + boundaries + security
- Rubric is explicit (not "good" vs "bad") and each criterion actually measures what its name claims
- Scoring is reproducible (same test, same results)
- You've documented what fails and why
- Regression tests pass (no unexplained degradation from the previous version)
- Minimum accuracy threshold met (e.g., 85%+ on golden dataset)
- Failure modes are understood and documented

---

## Further Reading

- **Session 5.1:** Eval mindset (this session)
- **Session 5.2:** Evaluation methods (rubric grading, LLM-as-judge, metrics)
- **Session 5.3:** Safety fundamentals (prompt injection, jailbreaks)

---

*Session 5.1 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
