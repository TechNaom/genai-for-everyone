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

## Answer Key

### Section A

**A1.** An LLM generates text by predicting the next most statistically plausible token given everything before it, one piece at a time — it isn't looking anything up or fact-checking as it goes. Fluency comes from having learned the patterns of grammatical, well-formed language extremely well; truth is a completely separate property the model has no built-in mechanism to verify. A sentence can be perfectly fluent and confidently stated while being entirely fabricated, because the generation process optimizes for "what plausibly comes next," not "what is verifiably true."

**A2.** The flaw is treating capability as the only relevant variable, ignoring cost, latency, and the fact that many tasks don't need the strongest model to be handled well (e.g., simple classification or short replies). The decision should be driven by the specific task's requirements — accuracy needs, response-time constraints, and budget — matched against the cheapest/fastest model that reliably meets them, reserving the most capable (and expensive) model for genuinely hard cases.

**A3.** The context window is the amount of text (measured in tokens) the model can process in a single request — it's a hard technical limit on one call. "Memory" of a past conversation is not automatic; the model is stateless between API calls, so any sense of remembering previous turns only exists because the application resends the full prior conversation as part of each new request, within the context window's limit. This matters for a real chatbot because if you don't explicitly resend prior messages, the model has no memory at all — and if the conversation grows long enough, you can exceed the context window and have to decide what to drop.

**A4.** Any two of: (1) **Data collection/labeling** — even if raw text data is topically balanced, the humans or processes that label/curate it can introduce systematic skew; (2) **Prompt design** — how a request is phrased can activate stereotypical associations or framings even from a model trained on balanced data; (3) **Deployment/application logic** — how outputs are used or filtered downstream (e.g., which outputs get flagged for review) can introduce disparate impact regardless of the model's training. Each shows that "balanced training data" alone doesn't guarantee a bias-free outcome — bias can enter at multiple points in the full pipeline.

---

### Section B

**B1.** At least three distinct projects: (1) an AI that pre-screens/ranks resumes against job criteria — predictive (selecting/scoring from existing candidates); (2) an AI that drafts personalized outreach or rejection emails to candidates — generative (produces new text); (3) an AI that predicts which candidates are likely to accept an offer or stay long-term — predictive (a risk/likelihood score). The clarifying question: "When you say 'use AI to improve hiring,' do you mean helping us screen candidates faster, communicate with them better, or predict outcomes like retention — these are different projects with different data and timelines."

**B2.** (a) The model isn't looking up the actual policy in real time — unless it was explicitly given retrieval access to the current policy document, it generated the most statistically plausible-sounding answer based on patterns in its training data, which may reflect a common industry norm (60 days) rather than this company's actual policy (30 days). (b) This is hallucination — a confidently stated, fluent, factually incorrect claim. (c) A structural fix: connect the assistant to the actual, current policy document via retrieval (RAG) so answers are grounded in the real source rather than generated from general training patterns — this is the direction Week 3 builds toward.

**B3.** The likely cause is tokenization differences between languages: Japanese text (using a different script, often without whitespace-delimited words the way English does) can require substantially more tokens per unit of meaning than English or Spanish, since the model's tokenizer was optimized on a training mix where some scripts split into more/smaller tokens than others. Since API pricing and processing cost scale with token count, a similarly-lengthed and equally-complex Japanese conversation can cost more simply because it decomposes into more tokens, before the model ever generates a single word of response.

**B4.** (1) The FAQ chat widget: **latency** should drive model selection most heavily — users expect a fast real-time reply, so a smaller/faster model is likely the right choice; raw capability matters less since FAQ answers are typically simple and don't require the strongest available reasoning. (2) The overnight batch summarization job: **cost** should drive selection most heavily, since it runs on a large volume of tickets on a schedule with no real-time latency requirement — using the cheapest model that produces acceptable summaries at that scale matters far more than shaving off response time nobody is waiting for. (3) The clinical notes tool: **accuracy/safety** should drive selection most heavily, given patient data and the real-world stakes of an incorrect clinical note — cost and latency matter far less here than minimizing the risk of a clinically significant error.

---

### Section C

**C1.** The path: the user types a message → it gets tokenized (broken into the model's vocabulary units) → it's sent as part of an API request, which must include the *entire* conversation history so far, not just the new message → the model generates a response token by token → the response is displayed to the user. For the next message to be handled correctly, the application must append both the user's new message and the model's own reply to the stored conversation history, then resend that full updated history with the next request — the model itself retains nothing between calls. The single most common point of failure for a first chatbot: forgetting to append the model's own reply to the history (only saving the user's messages), so the model appears to "forget" its own previous answers on the very next turn.

**C2.** Sample answer (grade for content, not exact wording): "Our AI feature generates responses by predicting likely-sounding text based on patterns it learned, rather than looking up guaranteed facts every time, which means it can occasionally state something confidently that isn't actually true. We've seen this happen in a small number of cases, and we're actively working on grounding its answers in our real, current documentation so it's checking against verified facts rather than relying on general patterns alone. In the meantime, we're monitoring outputs and adding review steps for the highest-stakes answers so a mistake doesn't reach a customer unchecked."

**C3.** No single correct answer — evaluate for genuine connection-making. Common strong answers: (a) "fluency isn't the same as accuracy" connects directly to prompt engineering, since a well-crafted prompt in Week 2 can't fix an underlying hallucination risk, only reduce it; (b) the token-prediction mechanism explains why *how* you phrase a prompt (Week 2's entire subject) changes which patterns the model draws on; (c) the context-window/memory distinction previews why prompt *systems* (Week 2.5) — not just single prompts — matter once you're managing multi-turn state. Full credit for any answer that draws a real, specific link rather than restating a Week 1 concept in isolation.

---

## Grading Guidance (for instructors / self-grading)

This exam is intentionally not multiple choice. Strong answers demonstrate:
- **Mechanism-based reasoning** (referencing tokens, embeddings, context, statelessness) rather than vague restatement ("AI can be wrong sometimes")
- **Recognition of trade-offs** rather than one-size-fits-all answers (especially in B4 and A2)
- **Calm, non-defensive professional communication** in scenario answers involving a real failure (B2, C2) — panicked or overconfident answers should be flagged for discussion even if technically correct
- **Genuine synthesis in C3** — answers that connect concepts across sessions, not just repeat one session's content

A reasonable passing bar: solid mechanism-based answers in Section A, correct classification and a real clarifying question in B1, and a calm, accurate explanation in B2 and C2. Section C3 is best used as a discussion prompt rather than strictly graded.

**Suggested scoring (optional, if a numeric score is wanted):** Section A (4 × 3 pts = 12), Section B (4 × 6 pts = 24), Section C (3 × 6 pts = 18). Total: 54 pts. Cutoffs: 48+ = excellent, 38–47 = solid, 27–37 = needs review, <27 = recommend revisiting Week 1 before Week 2.
