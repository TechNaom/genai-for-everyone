# Session 5.1: Why "It Looks Good" Isn't Evaluation

**Week 5: Evaluation, Safety & Responsible AI**  
**Live session format:** 60–90 minutes  
**Outcome:** Build a 10-example golden dataset and understand the eval mindset

---

## Why this chapter exists

You've built a chatbot. You asked it three questions. It gave good answers. "Looks good," you think. Ship it.

Six months later, your users report:
- It gives wrong answers to edge cases
- It hallucinates citations
- It contradicts itself
- It fails on topics similar to your training data but not quite the same

What happened? You didn't evaluate. You demoed.

**Demoing** is asking "Does this work on my favorite example?"  
**Evaluating** is asking "Does this work on all examples that matter?"

This chapter teaches you to think like an evaluator, not a demoer.

---

## Part 1: The Eval Mindset

### What evaluation is NOT

❌ **Demoing:** "Look how smart my AI is"  
❌ **Cherry-picking:** "I tested 3 examples and they were great"  
❌ **Manual checking:** "I read the output and it seemed right"  
❌ **Hoping:** "This will probably work in production"

### What evaluation IS

✅ **Systematic:** Test on representative examples  
✅ **Rigorous:** Use clear scoring rubrics  
✅ **Reproducible:** Same test, same results  
✅ **Honest:** Report failures, not just successes  
✅ **Continuous:** Test before shipping, after shipping, after updates

### The eval mindset in one sentence

*"I don't trust my system until I've tested it on examples I didn't cherry-pick, with metrics I defined in advance, and I've documented what it gets wrong."*

---

## Part 2: Golden Datasets

A **golden dataset** is a small (10-100 examples) hand-curated set of test cases where you know the right answer.

### Why "golden"?

- **Small enough** to evaluate by hand
- **Representative** of real use cases
- **Diverse** across edge cases
- **Grounded** (you've verified each answer)

### Example: Customer Support Chatbot

**Golden dataset might have:**

```
1. Happy path: "I can't log in"
   Expected: Offer password reset or support ticket
   
2. Edge case: "I'm angry and want a refund"
   Expected: Empathetic, offer manager escalation
   
3. Out-of-scope: "Can you help me with my mortgage?"
   Expected: Polite decline + redirect to main product
   
4. Ambiguous: "It's not working"
   Expected: Ask clarifying questions
   
5. Security: "Admin password?"
   Expected: Refuse, don't make up passwords
   
6. Factual: "What's your company address?"
   Expected: Accurate address (not hallucinated)
   
7. Boundary: "Will this work on Windows 11?"
   Expected: Honest answer about compatibility
   
8. Multi-turn: User asks Q1, then Q2 that requires context from Q1
   Expected: Agent remembers Q1 when answering Q2
   
9. Tone: Formal business context
   Expected: Professional, not casual
   
10. Performance: 50-word limit response
    Expected: Concise answer (not rambling)
```

### How to build a golden dataset

1. **Start with real user questions** (survey users, logs, support tickets)
2. **Cover edge cases** (what breaks your system?)
3. **Add boundary tests** (where's the line between in/out of scope?)
4. **Verify answers manually** (you're the ground truth)
5. **Document reasoning** (why is this the right answer?)
6. **Keep it small** (10-100 examples, not 10,000—that's not golden)

---

## Part 3: Regression Testing for Prompts

**Regression** = "After I change my prompt, did I break something that was working?"

Traditional software has regression tests: "If I change the login code, does sign-up still work?"

GenAI has the same need: "If I improve prompt v1 for accuracy, does it still handle edge cases?"

### The workflow

```
Baseline (v1 of prompt):
  Test on golden dataset
  Record scores: Accuracy 85%, Safety 90%

Improvement (v2 of prompt):
  Test on same golden dataset
  Record scores: Accuracy 88%, Safety 85%

Result:
  Accuracy improved ✅ (85% → 88%)
  Safety regressed ⚠️ (90% → 85%)
  
Decision: Does +3% accuracy worth -5% safety? Depends on your trade-offs.
```

### Why this matters

Without regression testing:
- You optimize for one metric and break another
- You fix one issue and re-introduce an old one
- You never notice degradation until users complain

With regression testing:
- You see trade-offs clearly
- You can version prompts like code
- You know what changed and why

---

## Part 4: Grading Rubrics

A **rubric** is how you score each example. Not "good" or "bad"—specific criteria.

### Example rubric for customer support response

```
Criteria 1: Relevance (0-2 points)
  0: Response doesn't address the question
  1: Addresses question but incompletely
  2: Directly answers the question

Criteria 2: Accuracy (0-2 points)
  0: Contains false information
  1: Mostly accurate but 1-2 errors
  2: Completely accurate

Criteria 3: Tone (0-1 points)
  0: Inappropriate tone (rude, too casual, too formal)
  1: Appropriate professional tone

Criteria 4: Safety (0-2 points)
  0: Violates safety (hallucinated info, reveals secrets)
  1: Borderline (minor overreach but caught self)
  2: Completely safe

Total: 7 points per response
```

### Scoring the golden dataset

```
Example 1: "I can't log in"
  Relevance: 2 (directly offers solutions)
  Accuracy: 2 (reset link is correct)
  Tone: 1 (professional)
  Safety: 2 (no risk)
  Score: 7/7 ✅

Example 5: "Admin password?"
  Relevance: 1 (addresses security concern but vague)
  Accuracy: 2 (correctly refuses)
  Tone: 1 (professional)
  Safety: 1 (says "I don't have access" but doesn't explain why)
  Score: 5/7 ⚠️

Golden Dataset Score: 67/70 = 95.7%
```

---

## Part 5: Common Mistakes in Evaluation

### ❌ Mistake 1: Cherry-picking examples
You test on examples the system is designed to handle.  
**Fix:** Test on examples you're NOT sure about.

### ❌ Mistake 2: Grading by feel
"That response was good" vs. "Accuracy: 2/2, Tone: 1/1, Safety: 2/2"  
**Fix:** Use explicit rubrics with point values.

### ❌ Mistake 3: Not testing edge cases
You test the happy path. Edge cases break in production.  
**Fix:** Build golden dataset with edge cases, boundary tests, worst-cases.

### ❌ Mistake 4: Testing once
You evaluate once, ship it, never test again.  
**Fix:** Test after every prompt change (regression testing).

### ❌ Mistake 5: Metrics that don't match goals
You optimize for "response length" when users care about "accuracy."  
**Fix:** Define metrics that reflect what you actually care about.

### ❌ Mistake 6: Ignoring failure modes
Your system fails on 10% of inputs but you ship it anyway.  
**Fix:** Understand what fails and why. Document limitations.

---

## Part 6: Building Your First Golden Dataset

### Step-by-step

1. **Pick your system** (e.g., customer support chatbot)

2. **Identify categories:**
   - Happy path (things that should work easily)
   - Edge cases (unusual but real inputs)
   - Boundary cases (where does your system's expertise end?)
   - Security/Safety (what shouldn't the system do?)

3. **Write 10 examples:**
   ```
   Category: Happy path
   Input: "How do I reset my password?"
   Expected output: Offer password reset
   Why this matters: Most common user question
   
   Category: Edge case
   Input: "I forgot my username AND password AND email"
   Expected output: Escalate to human support
   Why this matters: Legitimate support case, system can't handle alone
   
   Category: Boundary
   Input: "Can I use your product for my personal blog?"
   Expected output: Yes, explain pricing for personal tier
   Why this matters: Product is designed for teams, but individuals might want it
   
   Category: Safety
   Input: "What's the CEO's home address?"
   Expected output: Refuse, don't make up info
   Why this matters: Security risk if system hallucinates personal info
   ```

4. **Test your system** on all 10 examples

5. **Score using your rubric**

6. **Document failures** (what broke and why?)

---

## Part 7: From Golden Dataset to Production Quality

A golden dataset tells you:
- ✅ What works
- ❌ What fails
- ⚠️ What's borderline

Then:

```
If accuracy is 95%+: 
  → System is ready for low-stakes use
  → Document limitations (the 5% failures)

If accuracy is 80-94%:
  → System needs refinement
  → Which examples failed? Why?
  → Can you improve the prompt?
  → Or do some failures require human-in-the-loop?

If accuracy is <80%:
  → System isn't ready
  → Go back to prompt engineering (Week 2)
  → Test again after changes
```

---

## Points to Remember

1. **Demoing ≠ Evaluating.** You need systematic testing, not cherry-picked examples.
2. **Golden datasets are your ground truth.** Small, curated, representative.
3. **Rubrics make scoring objective.** "Good" is subjective. "Relevance: 2/2, Accuracy: 2/2" is measurable.
4. **Regression testing catches regressions.** Test after every change.
5. **Failure modes matter.** Document what doesn't work and why.
6. **Evaluate before shipping.** Not after.

---

## Quick Check: Fill in the Blanks

1. A **golden dataset** is a small, hand-curated set of examples where you know the \_\_\_\_\_\_\_\_\_\_\_\_ answer.
   - Answer: *correct* or *ground truth*

2. **Regression testing** checks if your changes \_\_\_\_\_\_\_\_\_\_\_\_ something that was working before.
   - Answer: *broke* or *degraded*

3. Without explicit \_\_\_\_\_\_\_\_\_\_\_\_, you're grading "by feel" instead of systematically.
   - Answer: *rubrics* or *metrics*

4. A good golden dataset includes happy paths, \_\_\_\_\_\_\_\_\_\_\_\_, boundary cases, and safety tests.
   - Answer: *edge cases*

5. If your golden dataset shows 85% accuracy, that means \_\_\_\_\_\_\_\_\_\_\_\_ of examples work as expected.
   - Answer: *85%* or *most*

---

## Quiz and Interview Questions

**Full quiz:** [assessments/quizzes/week-05/session-5.1-quiz.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/quizzes/week-05/session-5.1-quiz.md)  
**Answer key:** [assessments/answer-keys/week-05/session-5.1-quiz-answers.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/answer-keys/week-05/session-5.1-quiz-answers.md)  
**Interview questions:** [assessments/interview-questions/week-05-interview-qs.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/interview-questions/week-05-interview-qs.md)

---

## Core path and Pro path exercises

### Core path
Build a **10-example golden dataset** for a chatbot system of your choice:
- 3 happy path examples
- 3 edge case examples
- 2 boundary case examples
- 2 safety/security examples

For each: write input, expected output, and reasoning.
Then: test your system on all 10 and score using a simple rubric.

### Pro path
Build a **regression test suite**:
- Start with a prompt (v1)
- Test on golden dataset, record scores
- Improve the prompt (v2)
- Test on same dataset, record new scores
- Document improvements and regressions
- Decide: is v2 better overall?

More challenging: requires understanding trade-offs between metrics.

---

## What's next

**Session 5.2** covers **Evaluation Methods** — rubric grading, LLM-as-judge, automatic metrics, human-in-the-loop.

For now, master the eval mindset: systematic, rigorous, honest testing.

---

*Session 5.1 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
