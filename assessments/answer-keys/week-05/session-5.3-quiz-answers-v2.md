# Session 5.3 Quiz Answers (v2)

---

## Q1: The Core Difference
**Answer:** C) For RAG tools, the risk mostly lives in what gets
retrieved, often from ordinary questions with no malicious intent —
not just in crafted user input
- The wiki assistant's failures (salary leak, layoffs summary) both
  came from ordinary employees asking ordinary questions, not from
  anyone trying to trick the system.

---

## Q2: Technically Accessible vs. Appropriate
**Expected answer:** No — technical accessibility and appropriate use
are different questions. A document can pass access control (maybe
posted in a general space before formal controls were applied) while
still being clearly marked as sensitive by convention. The system
should check sensitivity signals independently of access control and
route such requests for review rather than auto-summarizing.

**Full credit:** States that access control passing doesn't mean the
content is appropriate to surface, with the reasoning.

---

## Q3: Where to Filter
**Answer:** B) Once content is in the model's context, it's harder to
guarantee it won't influence or be referenced in the response
- Filtering only at the final answer stage means the restricted content
  has already been "read" by the model — a much weaker guarantee than
  never including it in the first place.

---

## Q4: Indirect Injection
**Expected answer:** Anyone with EDIT access to a wiki page (not chat
access) can embed hidden instructions inside the document's text. Once
that page is indexed, it can be retrieved later for a completely
different user's unrelated query, and the model may treat the embedded
text as an instruction rather than as reference content.

**Full credit:** Identifies that the attacker only needs document edit
access, not chatbot interaction, and explains the delayed/indirect
mechanism.

---

## Q5: Index-Time vs. Query-Time Defense
**Answer:** B) It protects every future user from a poisoned document,
rather than relying on each individual query to defend against it
- Index-time scanning removes the threat once, for everyone. Query-time
  scanning has to work correctly every single time the document might
  be retrieved.

---

## Q6: Scenario — Context Accumulation

**Expected answer:** The risk is that the compensation document,
legitimately retrieved in turn 1 for the HR employee, may still be
sitting in the conversation's context when the "export everything"
request comes in turn 5 — meaning it gets bulk-exported and potentially
shared with people who were never authorized to see it (the employee's
"team," which may include non-HR staff). The system should re-check
relevance of previously retrieved documents against the CURRENT request
rather than assuming everything retrieved earlier in the session is
safe to include in a later, differently-scoped action like a bulk
export.

**Full credit (1 pt):** Identifies the risk (downstream sharing of
restricted content via the export) AND the fix (re-checking relevance/
scope rather than assuming persistence is safe).
**Partial credit (0.5 pts):** Identifies the risk only.

---

*Session 5.3 Answer Key (v2) | GenAI for Everyone | Week 5*
