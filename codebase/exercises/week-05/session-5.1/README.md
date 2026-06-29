# Session 5.1 Exercises: Why "It Looks Good" Isn't Evaluation

## Overview

Master the **eval mindset**: systematic, rigorous testing instead of cherry-picking examples.

- **Core Path:** Build a 10-example golden dataset (scaffolded)
- **Pro Path:** Regression testing framework (compare two prompt versions)

Both teach you to think like an evaluator, not a demoer.

---

## Core Path: Golden Dataset (Scaffolded)

**File:** `core_path_starter.py`

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

### How to work through it

1. Open `core_path_starter.py`
2. Find **TODO 1**: Implement scoring logic
   - Score each response on Relevance, Accuracy, Tone, Safety
   - Calculate total points and percentage
3. Find **TODO 2**: Implement `add_example()`
   - Store examples in the dataset
4. Find **TODO 3**: Implement `test_example()`
   - Run chatbot on an example
   - Score the response
   - Record results
5. Find **TODO 4**: Build the 10-example dataset
   - Add all 10 examples (scaffolded starters provided)
6. Run: `python3 core_path_starter.py`

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

## Pro Path: Regression Testing (Challenge)

**File:** `pro_path_starter.py`

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
  Relevance: +5% ✅
  Accuracy: -2% ⚠️ (regression)
  Helpfulness: +10% ✅
  Overall: +5% (net improvement)
  ↓
Decision: Promote V2 to production
```

### Run it

```bash
python3 pro_path_starter.py
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
Relevance            85.0            90.0           +5.0%           📈 Improved
Accuracy             90.0            88.0           -2.0%           📉 Regressed
Helpfulness          75.0            85.0          +10.0%           📈 Improved
Overall              83.3            87.7           +4.4%           📈 Improved
======================================================================

DECISION:
  Improvements: 2
  Regressions: 1
  Overall change: +4.4%

✅ V2 is better overall. Recommend promoting to production.
```

### Key learning

- Regression testing prevents breaking existing functionality
- Trade-offs are explicit (see all metrics)
- Data-driven decisions (not gut feel)
- Version management (track prompt changes like code)

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

## Extensions

### 1. Add More Criteria
Beyond Relevance/Accuracy/Tone/Safety, add:
- **Conciseness** (is response too long?)
- **Action items** (does user know what to do next?)
- **Empathy** (is tone appropriate to user's emotion?)

### 2. Weight Criteria Differently
Not all criteria matter equally:
```python
weighted_score = (Relevance * 0.4 + 
                 Accuracy * 0.4 + 
                 Tone * 0.1 + 
                 Safety * 0.1)
```

### 3. Test on Real Data
Replace mock examples with real user queries from support logs.

### 4. Continuous Monitoring
After shipping, continuously test on new user queries.
Track: "Are we getting worse over time?"

### 5. LLM-as-Judge
Use an LLM to score responses instead of manual rubrics:
```python
def llm_score_response(user_input, actual, expected):
    prompt = f"""Score this response:
    User: {user_input}
    Expected: {expected}
    Actual: {actual}
    
    Is this response good? Rate 1-10."""
    
    response = llm.generate(prompt)
    return parse_score(response)
```

---

## Debugging Tips

### "My scores are all 0"
- Check the mock chatbot responses
- Are your expected outputs realistic?
- Is your scoring logic too strict?

### "I'm getting inconsistent scores"
- Scoring should be deterministic (same input = same score)
- If using manual scoring, create a detailed rubric
- Consider using LLM for consistency

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

- ✅ Golden dataset covers happy path + edge cases + boundaries + security
- ✅ Rubric is explicit (not "good" vs "bad")
- ✅ Scoring is reproducible (same test, same results)
- ✅ You've documented what fails and why
- ✅ Regression tests pass (no degradation from previous version)
- ✅ Minimum accuracy threshold met (e.g., 85%+ on golden dataset)
- ✅ Failure modes are understood and documented

---

## Further Reading

- **Session 5.1:** Eval mindset (this session)
- **Session 5.2:** Evaluation methods (rubric grading, LLM-as-judge, metrics)
- **Session 5.3:** Safety fundamentals (prompt injection, jailbreaks)

---

*Session 5.1 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
