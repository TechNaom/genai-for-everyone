# Week 1 Written Exam — Foundations of GenAI & LLMs

**Format:** Open-book, scenario-based. This exam tests whether you can apply Week 1's concepts to situations you haven't seen before — not whether you've memorized definitions. Take your time; depth of reasoning matters more than speed.

**Sections:** A (Short Answer, conceptual) · B (Scenario Analysis, applied) · C (Synthesis, cross-session)

---

## Section A — Short Answer

**A1.** Explain, in your own words, why a large language model can produce a fluent, grammatically perfect, and completely false sentence. Your answer should reference the actual generation mechanism, not just say "it makes mistakes."

**A2.** A teammate says: "We should always use the most capable model available for every feature, since more capability can only help." Identify the flaw in this reasoning and explain what should actually drive the decision instead.

**A3.** What is the difference between a model's context window and its memory of a past conversation? Why does this distinction matter when building a real chatbot?

**A4.** Name two distinct points in a GenAI pipeline where bias can enter, beyond training data, and explain how each one could produce a biased outcome even with perfectly balanced training data.

---

## Section B — Scenario Analysis

**B1. The Ambiguous Request.**
Your VP says: "Let's use AI to improve our hiring process." Identify at least three meaningfully different projects this could refer to, classify each as predictive or generative, and write the single clarifying question you'd ask before starting any work.

**B2. The Confident Wrong Answer.**
A user asks your company's AI assistant, "What's your return policy for international orders?" The assistant confidently states a 60-day return window. Your actual policy is 30 days for international orders. Walk through: (a) why this likely happened, referencing the actual generation mechanism, (b) what category of failure this is, and (c) one structural change (not "use a smarter model") that would reduce this risk going forward.

**B3. The Cost Surprise.**
Your company's AI-powered translation feature, which works fine for English-to-Spanish, is costing significantly more per conversation when used for English-to-Japanese, even though the conversations are similar in length and complexity. Explain the likely cause, referencing what you learned about how text gets processed before a model ever generates a response.

**B4. The Model Selection Brief.**
You're building three features for the same company: (1) a real-time chat widget answering simple FAQ questions, (2) an overnight batch job summarizing thousands of support tickets for a weekly report, (3) a tool that drafts clinical notes for a healthcare provider, handling patient data. For each, identify the dimension that should drive model selection most heavily, and justify why a different dimension matters less for that specific case.

---

## Section C — Synthesis

**C1.** Trace the full path of a single user message through a chatbot you might build: from the moment the user types their message, through tokenization, through the API request, to the moment a response is displayed — and then explain specifically what has to happen for the *next* message in that same conversation to be handled correctly. Identify the single most common point of failure in this entire path for someone building their first chatbot.

**C2.** A non-technical executive asks you to summarize, in three sentences total, why your company's new AI feature might occasionally "make things up," and what your team is doing about it. Write those three sentences as you actually would say them in that meeting — calm, accurate, and free of unnecessary jargon, but not dishonestly reassuring.

**C3.** Looking back across all of Week 1: which single concept do you think will matter most in Week 2 (Prompt Engineering) and why? There's no single correct answer here — this question is assessing whether you can see how this week's foundation connects forward, not testing recall.

---

## Grading Guidance (for instructors / self-grading)

This exam is intentionally not multiple choice. Strong answers demonstrate:
- **Mechanism-based reasoning** (referencing tokens, embeddings, context, statelessness) rather than vague restatement ("AI can be wrong sometimes")
- **Recognition of trade-offs** rather than one-size-fits-all answers (especially in B4 and A2)
- **Calm, non-defensive professional communication** in scenario answers involving a real failure (B2, C2) — panicked or overconfident answers should be flagged for discussion even if technically correct
- **Genuine synthesis in C3** — answers that connect concepts across sessions, not just repeat one session's content

A reasonable passing bar: solid mechanism-based answers in Section A, correct classification and a real clarifying question in B1, and a calm, accurate explanation in B2 and C2. Section C3 is best used as a discussion prompt rather than strictly graded.
