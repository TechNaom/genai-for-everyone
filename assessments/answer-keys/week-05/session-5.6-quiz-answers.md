# Session 5.6 Quiz Answers and Grading Guide

---

## Question 1: Report vs. Demo

**Answer:** Missing: any systematic coverage (edge cases, adversarial inputs), any objective scoring, and any written record. "It worked 5 times" is anecdotal and cherry-picked. Ask for a golden dataset with scored results and a written report instead.

**Full credit (1 pt):** Names at least two of (systematic coverage, objective scoring, written artifact) and asks for a report/golden dataset.
**No credit:** Accepts the anecdotal claim as sufficient.

---

## Question 2: Golden Dataset Design

**Answer:** B) A question where the correct answer requires a specific number from the policy document

**Grading:**
- **Full credit (1 pt):** Answer is B
- **No credit:** Any other answer

**Explanation:** Numeric, document-grounded facts are exactly where RAG hallucination shows up (Session 3.5). Adding a tenth easy happy-path question adds little new signal.

---

## Question 3: Red-Teaming Your Own System

**Answer:** B) Your attacks weren't aggressive or creative enough

**Grading:**
- **Full credit (1 pt):** Answer is B
- **No credit:** Any other answer

**Explanation:** Systems rarely defend perfectly against a genuinely adversarial red-team pass. A 5/5 clean result on the first try is far more likely to reflect soft attacks than a hardened system.

---

## Question 4: Injection via Retrieved Content

**Full credit (1 pt):** Explains that retrieved content is usually trusted/unfiltered by default, and that the attacker doesn't need direct access to the chat interface — just a way to get text into any document the system might retrieve.
**Partial credit (0.5 pts):** Notes it's "harder to detect" without explaining why (trust boundary, attack surface).
**No credit:** Treats the two injection vectors as equivalent.

---

## Question 5: Bias Check Design

**Answer:** B) Ask the same underlying question multiple ways, varying only the demographic/framing detail, and compare answers

**Full credit (1 pt):** Answer is B
**No credit:** Any other answer

**Why:** Bias is comparative, not absolute — a single output can't reveal unequal treatment.

---

## Question 6: Guardrails and Residual Risk

**Full credit (2 pts):** Explains that keyword-based filters are inherently brittle and bypassable by rephrasing, that this doesn't make the guardrail worthless (it still blocks the literal case), and that the report must document the bypass as an open risk rather than treat the filter as a complete fix.
**Partial credit (1 pt):** Says the guardrail "isn't perfect" without connecting it to keyword-filter brittleness or without mentioning honest documentation.
**No credit:** Treats it as either a total failure or fully solved.

---

## Question 7: Choosing What to Ship

**Full credit (2 pts):** Takes a clear position (ship with monitoring / ship to a limited rollout / don't ship yet) and ties the justification to the actual numbers given — e.g., MEDIUM-severity partial red-team successes may be acceptable for a low-stakes internal tool but not for anything customer-facing or handling sensitive data; an unresolved bias gap is a harder blocker if it touches a protected characteristic.
**Partial credit (1 pt):** Gives a position with generic reasoning not grounded in the specific severities/rates given.
**No credit:** No clear position, or ignores the findings.

---

## Grading Summary

| Question | Type | Points |
|----------|------|--------|
| 1 | Short | 1 |
| 2 | MC | 1 |
| 3 | MC | 1 |
| 4 | Short | 1 |
| 5 | MC | 1 |
| 6 | Scenario | 2 |
| 7 | Scenario | 2 |
| **Total** | | **9** |

---

## Common Misconceptions

1. **"5 clean red-team attempts means it's safe"** — No, it more often means the attacks were too weak.
2. **"A keyword filter that catches the literal case is a complete fix"** — No, it's one layer; rephrasing bypasses it easily.
3. **"Bias checks just need one test on a sensitive topic"** — No, bias requires a controlled comparison across framings.
4. **"90% pass rate is automatically good enough to ship"** — No, whether it's acceptable depends entirely on what the remaining 10% of failures look like and who they affect.

---

*Session 5.6 Answer Key | GenAI for Everyone | Week 5 Lab*
