# Session 5.2 Quiz (v2): Evaluation Methods

**6 questions. MC, short answer, and scenario.**

---

## Q1: Semantic Similarity's Blind Spot

A contract clause summary omits a class-action waiver but correctly
describes the arbitration requirement. Why might semantic similarity
still score it 0.75-0.85 instead of much lower?

A) Semantic similarity always returns high scores regardless of content
B) The summary still captures most of the clause's overall meaning;
   similarity has no concept of which specific detail is most important
C) The embedding model was trained incorrectly
D) 0.75-0.85 is actually a low score on this scale

**Answer:** B

---

## Q2: LLM-as-Judge Generosity

Why would an ungrounded LLM-judge prompt ("is this summary accurate?")
tend to rate an incomplete-but-true summary too highly?

**Short answer:** (2-3 sentences)

---

## Q3: The Partial-Failure Cap

What does explicitly telling an LLM-judge to "cap the score at 5 if a
legally significant detail is omitted" actually fix?

A) It makes the LLM judge run faster
B) It counters the LLM-judge's tendency to rate partial truths
   generously, by defining in advance what counts as a capped failure
C) It removes the need for semantic similarity entirely
D) It guarantees the LLM-judge will never make a mistake

**Answer:** B

---

## Q4: Routing Logic

Why does flagging based on the MIDDLE band of semantic similarity
(0.70-0.85) catch more real failures than flagging only low scores
(<0.5) for this specific task?

**Short answer:** (2-3 sentences)

---

## Q5: Picking a "Winner" Variant

Variant B scores higher than Variant C on LLM-judge average, but a
manual check of Variant C's flagged cases shows the lower score
reflects casual tone, not missing information. Should the team
prefer Variant B over Variant C based on the average score alone?

**Short answer:** (2-3 sentences)

---

## Q6: Scenario — Design a Routing Rule

You're evaluating an AI tool that summarizes medical visit notes for
patients. A "deceptive middle band" failure here might be a summary
that captures the diagnosis correctly but omits a follow-up
instruction (e.g., "take this medication on an empty stomach"). Design
a routing rule (in plain English, no code needed) for when this should
be flagged for a nurse to review, using the same structure as the
chapter's arbitration example.

**Short answer:** (write your routing rule)

---

*Session 5.2 Quiz (v2) | GenAI for Everyone | Week 5*
