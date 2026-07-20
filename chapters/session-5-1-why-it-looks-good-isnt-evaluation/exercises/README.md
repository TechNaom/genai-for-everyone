# Session 5.1 Exercises: Golden Dataset (Core Path)

## Overview

Master the **eval mindset**: systematic, rigorous testing instead of cherry-picking examples.

This is the Core Path exercise: build a 10-example golden dataset for a customer support chatbot. It teaches you to think like an evaluator, not a demoer.

(Looking for the harder regression-testing build? That's the Pro Path — see `../project/README.md`.)

---

## Core Path: Golden Dataset

**Files:** `starter.py`, `solution.py`

Note: in this repo, `starter.py` and `solution.py` are identical — every TODO below is already filled in. Don't go looking for blanks to fill; instead, trace *how* each TODO was implemented, then use the six-step process (below) to extend the dataset with your own examples for a system of your own.

### What you'll build

A **10-example golden dataset** for a customer support chatbot:
- 3 happy path examples (common questions)
- 3 edge case examples (unusual but real)
- 2 boundary case examples (where expertise ends)
- 2 safety/security examples (what NOT to do)

For each example:
1. Write the user input
2. Define expected output
3. Explain why it matters
4. Test your chatbot on it
5. Score using a rubric

### How to trace it

1. Open `starter.py`.
2. Find **TODO 1** (`score_response`): scoring logic that scores each response on Relevance, Accuracy, Tone, Safety, then calculates total points and percentage.
3. Find **TODO 2** (`add_example`): stores examples in the dataset.
4. Find **TODO 3** (`test_example`): runs the mock chatbot on an example, scores the response, and records the result.
5. Find **TODO 4** (the `if __name__ == "__main__":` block): builds the full 10-example dataset across all four categories.
6. Run: `python starter.py`

### Expected output

```
============================================================
GOLDEN DATASET: Customer Support Chatbot
============================================================

Example 1: HAPPY PATH
  Input: How do I reset my password?
  Expected: Offer password reset link or instructions
  Actual: I can help you reset your password. Go to Settings > Account > Reset Password.
  Why it matters: Most common user question
  Scores: {'Relevance': 2, 'Accuracy': 2, 'Tone': 1, 'Safety': 2}
  Result: 7/7 (100.0%)

Example 2: HAPPY PATH
  ...

============================================================
OVERALL SCORE: 95.0%
============================================================
```

### Key learning

- Golden datasets are ground truth
- Rubrics make scoring objective
- You're testing YOUR system, not the LLM
- Coverage matters (edge cases catch bugs)

---

## Understanding the Rubric

### Criteria explained

**Relevance (0-2 points)**
- 0: Response doesn't address question
- 1: Partially addresses
- 2: Directly answers question

**Accuracy (0-2 points)**
- 0: Contains false information
- 1: Mostly accurate but minor errors
- 2: Completely accurate

**Tone (0-1 point)**
- 0: Inappropriate (rude, too casual, wrong register)
- 1: Professional and friendly

**Safety (0-2 points)**
- 0: Violates safety (hallucinates, reveals secrets)
- 1: Minor overreach but caught itself
- 2: Completely safe

### Scoring example

```
User: "I can't log in"
Expected: "Offer password reset or troubleshooting"
Actual: "Try resetting your password in Settings."

Relevance: 2 (directly answers)
Accuracy: 2 (password reset is correct step)
Tone: 1 (professional)
Safety: 2 (safe advice)
Total: 7/7 = 100%
```

---

## Extending the dataset yourself

Once you've traced how `starter.py` works, extend it for a system of your own:

1. **Pick your system** (e.g., your own chatbot, or a different domain entirely).
2. **Identify categories** — happy path, edge cases, boundary cases, safety/security. Use the same four buckets as your checklist.
3. **Write 10+ examples**, each with: input, expected output, and a one-line "why this matters."
4. **Test your system** on all of them.
5. **Score using the rubric** above (or your own).
6. **Document failures** — what broke and why?

### Other extensions

**Add more criteria** — beyond Relevance/Accuracy/Tone/Safety, consider:
- **Conciseness** (is the response too long?)
- **Action items** (does the user know what to do next?)
- **Empathy** (is the tone appropriate to the user's emotion?)

**Weight criteria differently** — not all criteria matter equally:
```python
weighted_score = (Relevance * 0.4 +
                 Accuracy * 0.4 +
                 Tone * 0.1 +
                 Safety * 0.1)
```

**Test on real data** — replace the mock chatbot's canned responses with real user queries from support logs.

---

## Debugging Tips

### "My scores are all 0"
- Check the mock chatbot responses
- Are your expected outputs realistic?
- Is your scoring logic too strict?

### "I'm getting inconsistent scores"
- Scoring should be deterministic (same input = same score)
- If using manual scoring, create a detailed rubric
- Consider using an LLM for consistency (see Session 5.2)

### "Dataset is too small"
- 10 examples is okay for starting
- Add more as you find edge cases
- Aim for 50-100 for production

### "All examples pass"
- Either your system is perfect (unlikely) or your tests are too easy
- Add harder examples: edge cases, boundary cases, adversarial inputs

---

## Production Checklist

Before shipping, ensure:

- Golden dataset covers happy path + edge cases + boundaries + security
- Rubric is explicit (not "good" vs "bad")
- Scoring is reproducible (same test, same results)
- You've documented what fails and why
- Minimum accuracy threshold met (e.g., 85%+ on golden dataset)
- Failure modes are understood and documented

---

## Further Reading

- **Session 5.1:** Eval mindset (this session)
- **Session 5.2:** Evaluation methods (rubric grading, LLM-as-judge, metrics)
- **Session 5.3:** Safety fundamentals (prompt injection, jailbreaks)

---

*Session 5.1 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
