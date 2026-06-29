# Session 5.3 Quiz (v2): Safety Fundamentals for Internal RAG Tools

**6 questions. MC and short answer.**

---

## Q1: The Core Difference

How does the main safety risk for an internal RAG tool differ from a
customer-facing chatbot's main safety risk?

A) There's no real difference; the same defenses apply identically
B) RAG tools have no safety risks since they're internal-only
C) For RAG tools, the risk mostly lives in what gets retrieved, often
   from ordinary questions with no malicious intent — not just in
   crafted user input
D) RAG tools are only vulnerable to jailbreaks, never injection

**Answer:** C

---

## Q2: Technically Accessible vs. Appropriate

A document passes formal access control for a given user, but its
title says "CONFIDENTIAL — Do Not Distribute." Should it be
automatically summarized on request?

**Short answer:** (2-3 sentences)

---

## Q3: Where to Filter

Why does the chapter insist permission filtering happen BEFORE
documents enter the model's prompt context, rather than only at the
final answer stage?

A) It's faster computationally
B) Once content is in the model's context, it's harder to guarantee
   it won't influence or be referenced in the response
C) The model can't read context anyway
D) There's no real difference in where you filter

**Answer:** B

---

## Q4: Indirect Injection

How can a wiki page be used to attack a RAG system WITHOUT the
attacker ever interacting with the chatbot?

**Short answer:** (2-3 sentences)

---

## Q5: Index-Time vs. Query-Time Defense

Why is scanning for injected instructions at INDEX time better than
only scanning at QUERY time?

A) Index-time scanning is the only option available
B) It protects every future user from a poisoned document, rather
   than relying on each individual query to defend against it
C) Query-time scanning is always more accurate
D) There's no meaningful difference

**Answer:** B

---

## Q6: Scenario — Context Accumulation

An HR employee legitimately retrieves a compensation document in turn
1 of a conversation, then in turn 5 asks the assistant to "export this
whole conversation as a summary for my team." What's the risk here,
and what should the system do differently?

**Short answer:** (2-4 sentences)

---

*Session 5.3 Quiz (v2) | GenAI for Everyone | Week 5*
