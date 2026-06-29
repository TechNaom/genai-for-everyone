# Session 5.5 Quiz Answers

---

## Q1: Guardrails vs. System Prompts
**Answer:** B) Guardrails enforce behavior with code; system prompts persuade the model

- Full credit: B
- A system prompt is a request to the model — it can still be argued with or bypassed.
  A guardrail is code that runs regardless of what the model decides.

---

## Q2: Defense Against Data Leakage
**Answer:** B) Never put the secret in the model's context in the first place

- Full credit: B
- Output filters (A) are a useful backstop but not the primary fix — if the secret
  is in context at all, something can eventually leak it. Removing it from context
  entirely is the real fix.

---

## Q3: Over-Blocking
**Answer:** B) A false positive

- A false positive = guardrail blocks something that was actually safe
- A false negative would be the opposite: an attack that got through

---

## Q4: Human Review Gates
**Answer:** B) User asks the bot to approve a $2,000 refund

- High financial stakes + irreversibility = good candidate for human review
- The other options are low-stakes, reversible, informational requests

---

## Q5: Refusal Design
**Answer:** B) Explaining exactly which detection pattern triggered the block

- Explaining your detection logic teaches attackers how to evade it next time
- Polite refusal + redirect (A, C, D) are all good practices

---

## Q6: Regression Testing Guardrails

**Expected answer:**
Re-running the same attacks verifies the fix actually works, instead of just assuming
it does. It also catches cases where a fix for one vulnerability accidentally
reintroduces or misses another — the same regression-testing principle from Session 5.1,
applied to security instead of accuracy.

**Full credit (1 pt):** Mentions verification of the fix AND regression/consistency checking
**Partial credit (0.5 pts):** Mentions only one of the two ideas

---

*Session 5.5 Answer Key | GenAI for Everyone | Week 5*
