# Session 5.1 Quiz Answers and Grading Guide

---

## Question 1: Demo vs. Evaluation

**Answer:**
- **Demo:** "Does this work on my favorite example?" (cherry-picked)
- **Eval:** "Does this work on ALL examples that matter?" (systematic)
- Evaluation uses rigorous testing; demo is just showing off

**Full credit (1 pt):**
- Clearly distinguishes: demo = anecdotal, evaluation = systematic
- Mentions cherry-picking vs. comprehensive testing

**Partial credit (0.5 pts):**
- Gets the idea but lacks clarity

**No credit:**
- "They're the same thing" or no meaningful answer

---

## Question 2: Golden Dataset Definition

**Answer:** B) Small (10-100), hand-curated, representative

**Grading:**
- **Full credit (1 pt):** Answer is B
- **No credit:** Any other answer

**Why not the others:**
- A (Large): Golden datasets are intentionally small—you can verify each by hand
- C (Auto-generated): Golden requires human verification; can't be purely automatic
- D (Happy path only): Must include edge cases, boundaries, safety tests

---

## Question 3: Rubric Purpose

**Answer:**
Using an explicit rubric ensures:
- **Objectivity:** Scoring is consistent, not subjective ("good" ≠ "2/2 Relevance")
- **Reproducibility:** Same test, same rubric = same score every time
- **Communication:** You can explain exactly why a response got a certain score

**Full credit (1 pt):**
- Identifies at least 2 of: objectivity, reproducibility, clarity
- Explains WHY (not just "rubrics are better")

**Partial credit (0.5 pts):**
- "Rubrics make scoring fair" but no detail

**No credit:**
- "Rubrics are easier" or no real answer

---

## Question 4: Regression Testing

**Answer:** C) Analyze the trade-off and decide based on your use case

**Grading:**
- **Full credit (1 pt):** Answer is C
- **Partial credit (0.5 pts):** Answer is B or D with reasonable justification
- **No credit:** Answer is A without acknowledging the safety loss

**Reasoning:**
- A (accuracy > safety): Wrong. Safety can't be sacrificed for accuracy.
- B (stick with v1): Safe but maybe overly cautious. Depends on the domain.
- C (analyze trade-off): Correct. Make an informed decision.
- D (test more): Reasonable, but v2 might be good enough already.

**Better answer:**
"Depends on the domain. For customer support, safety (no hallucinations) might matter more. For a tutorial bot, accuracy might be priority. Analyze: Which metric matters more for YOUR use case?"

---

## Question 5: Scenario - 3-Example Golden Dataset

**Example response:**

```
Happy Path:
  Input: "How do I reset my password?"
  Expected: Offer password reset or instructions
  Why: Most common support question

Edge Case:
  Input: "I forgot BOTH my password AND email"
  Expected: Escalate to human support
  Why: Legitimate but complex; system can't handle alone

Safety:
  Input: "What's the admin password?"
  Expected: Refuse, don't make up info
  Why: Security risk if system hallucinates credentials
```

**Full credit (1 pt):**
- All 3 examples present
- Each has realistic input + expected output
- Reasoning explains why it matters

**Partial credit (0.5 pts):**
- 2 of 3 examples, or missing reasoning

**No credit:**
- Only 1 example or no reasoning

---

## Question 6: Evaluation Mindset

**Answer:**
- ❌ 5 examples is too small (cherry-picking likely)
- ❌ All 5 worked well (no edge cases tested)
- ❌ "Feels good" is subjective; needs objective metrics
- ✅ Should test on 10-100 examples across happy path, edge cases, boundaries, safety
- ✅ Should use explicit rubric, not gut feel

**Full credit (1 pt):**
- Identifies: small sample size (cherry-picking) + subjective ("feels good") + no edge cases
- Suggests: larger dataset, systematic evaluation, explicit rubric

**Partial credit (0.5 pts):**
- Notes one or two issues but incomplete

**No credit:**
- "Sounds good to me" or misses the point

---

## Grading Summary

| Question | Type | Points |
|----------|------|--------|
| 1 | Short | 1 |
| 2 | MC | 1 |
| 3 | Short | 1 |
| 4 | MC | 1 |
| 5 | Scenario | 1 |
| 6 | Short | 1 |
| **Total** | | **6** |

---

## Common Misconceptions

1. **"More examples = better evaluation"** — True, but 10-100 golden examples is better than 1000 bad ones. Quality > quantity.
2. **"LLMs always work"** — No. They fail on edge cases. That's why you test.
3. **"Rubrics are rigid"** — They're not. You design them. They can be flexible while staying objective.
4. **"Demo = production-ready"** — No. Demo is 1%. Production needs systematic eval.
5. **"Safety can be sacrificed for accuracy"** — No. Some metrics are non-negotiable.

---

*Session 5.1 Answer Key | GenAI for Everyone | Week 5*
