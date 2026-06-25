# Session 1.5: Limitations, Hallucination & Bias

**Week:** 1 — Foundations of GenAI & LLMs
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes

---

## Why this chapter exists

You've now built a real, working GenAI application. It runs. It responds. It feels like magic. This chapter exists to make sure that feeling doesn't turn into misplaced trust — because the same mechanism that makes these models so capable also makes them capable of being confidently, fluently, convincingly wrong.

This isn't a chapter about being afraid of GenAI. It's a chapter about respecting what it actually is, so you can build things that account for its real failure modes instead of getting blindsided by them after launch. Every serious GenAI practitioner — and every serious interview for a GenAI role — assumes you understand this material cold. Let's make sure you do.

---

## Part 1: Hallucination — Confident, Fluent, and Wrong

### Defining the term precisely

**Hallucination**, in the GenAI sense, means the model generates content that is factually incorrect, fabricated, or unsupported — while presenting it with the same fluent confidence as accurate content. The word is a little dramatic (the model isn't "seeing things"), but it's stuck because it captures something real: the output isn't hedged, isn't uncertain-sounding, isn't flagged in any way as potentially wrong. It just... is wrong, delivered with total conversational ease.

### Why this happens — connecting back to Session 1.1 and 1.2

We've actually already built the explanation for this, piece by piece, over the last four sessions. Let's assemble it explicitly:

From Session 1.1: an LLM generates the most statistically plausible next token, given everything before it — it does not retrieve verified facts from a database unless explicitly given a tool to do so.

From Session 1.2: the model's "knowledge" lives in the patterns learned across its training data, compressed into the relationships between tokens and embeddings — not as a lookup table of discrete, verifiable facts with sources attached.

Put these together, and hallucination stops being mysterious: **when you ask a model something where the most statistically plausible continuation happens to be false** — perhaps because the true answer was rare or contradictory in training data, perhaps because the question nudges the model toward a plausible-sounding but incorrect pattern — **the model has no internal mechanism that flags this and says "wait, I'm not sure."** Fluency and accuracy are two separate properties of the output, and nothing about how the model works guarantees they travel together.

### A concrete, common example

Ask a model to cite the specific page number of a quote from a real book it's only seen a handful of times in training, or to provide a citation for a very specific, obscure statistic. A model will often produce something that *looks* exactly like a real citation — a plausible author name, a plausible-sounding journal, a specific page number — entirely fabricated, because "a citation-shaped piece of text" is precisely the most statistically plausible continuation in that context, even though no such specific source exists. This is one of the most consequential and well-documented hallucination patterns in real-world GenAI deployments, especially in legal and academic contexts.

### Hallucination is not a bug that will simply be "fixed" by the next model version

This matters enough to state directly: while later, larger models do generally hallucinate less often than earlier ones on many tasks, **hallucination is not a temporary engineering bug awaiting a patch.** It's a structural consequence of how these models generate text at all. Newer models reduce the *frequency*, not the fundamental *possibility*. Any system design that assumes "the next model release will solve this" is building on a false premise. The actual mitigations — grounding outputs in retrieved, verifiable documents (Week 3's entire subject), rigorous evaluation (Week 5), and appropriate guardrails (also Week 5) — are about managing this reality, not eliminating it.

---

## Part 2: Where Bias Enters the Pipeline

### Bias is not a single point of failure

A common misconception is that "AI bias" means one thing: biased training data, full stop. The reality is messier and more important to understand: **bias can enter a GenAI system at multiple distinct points**, and addressing only one of them while ignoring the others leaves real problems unsolved.

**Training data bias.** If the text a model learned from over- or under-represents certain perspectives, demographics, languages, or viewpoints, the model's outputs will tend to reflect those same imbalances. This is the bias source most people have heard of, but it's far from the only one.

**Prompt-level bias.** The way a question is phrased can shift a model's output in a biased direction, even with identical underlying facts. Asking "why do many people distrust [group]" presupposes something different than "what are perspectives on [group]," and the model's response will often reflect the framing baked into the question itself.

**Few-shot example bias.** When you give a model example input/output pairs to guide its behavior (a technique you'll formalize in Week 2), the specific examples you choose can introduce skew. If every example of "a successful entrepreneur" you provide happens to share certain characteristics, the model may implicitly learn to associate success with those characteristics, regardless of your actual intent.

**Evaluation bias.** Even the process of checking whether a model's output is "good" can encode bias — if the criteria or the human reviewers judging quality share a narrow set of assumptions, outputs that diverge from those assumptions may get unfairly penalized regardless of their actual merit. We'll dig into this properly in Week 5, but it's worth knowing now that evaluation isn't a neutral, bias-free step just because it happens after generation.

### Why this multi-point view matters practically

If your organization's response to "is our AI biased?" is solely "we checked the training data," you've addressed exactly one of at least four entry points. A genuinely careful practitioner asks the question at every stage: how was this prompted, what examples (if any) shaped its behavior, and how is "good output" being judged — not just where the underlying model came from.

---

## Part 3: Other Real Limitations Worth Knowing Cold

Beyond hallucination and bias, a few other limitations come up constantly in real GenAI work and in interviews.

**Knowledge cutoffs.** Every model has a point in time after which it has no training data at all — it simply has never seen anything that happened after that date. Ask about something genuinely recent, and the model either says so honestly, or — more concerning — may hallucinate a plausible-sounding but fabricated answer rather than admitting uncertainty. This is precisely the problem Week 3's Retrieval-Augmented Generation exists to solve.

**Inconsistency across runs.** Ask a model the exact same question twice, and you may get meaningfully different answers, especially for open-ended or creative tasks. This isn't necessarily a flaw — some randomness is often intentional and adjustable (a concept called "temperature," which affects how much variation is injected into the token-selection process) — but it does mean you can't always assume perfect reproducibility, which has real implications for testing and evaluation.

**Struggles with precise counting and certain logical structures.** We touched on this in Session 1.2 — letter-counting and similar tasks are awkward for token-based models because the units they process don't map cleanly onto the units the task actually requires. Similarly, models can struggle with deeply nested logical conditions or very long chains of precise arithmetic, even while excelling at tasks that "feel" much harder, like writing nuanced prose. Capability isn't evenly distributed across task types in the way human intuition might expect.

**Sensitivity to phrasing.** The same underlying question, asked two slightly different ways, can sometimes produce meaningfully different quality of response. This isn't a flaw to be embarrassed about as a user — it's a real property of how these systems work, and it's the entire reason prompt engineering (all of Week 2) exists as a discipline.

---

## Part 4: A Realistic Scenario, Worked Through

**The setup:** Your company just launched an AI feature that answers customer questions about your product. Three days in, a customer posts on social media that the bot confidently told them your product supports a feature it does not actually have. Your product manager is panicking and asks you to explain what happened and what you're going to do about it.

**The calm, accurate explanation:** The model wasn't being deceptive or malicious. It generated the most statistically plausible-sounding answer to a question about your product's features, based on patterns from its training data — likely including general knowledge about what similar products in your category typically offer — rather than a verified, grounded fact about *your specific* product. Without being connected to your actual, current product documentation, the model has no way to distinguish between "what's generally true of products like this" and "what's specifically true of this exact product." This is hallucination, exactly as described in Part 1 — not a one-off glitch, but an expected behavior of an ungrounded model answering a specific factual question.

**The honest, non-defensive framing for your PM:** No current LLM eliminates this risk entirely. What reduces it dramatically is *grounding* the model's answers in your actual product documentation — having it retrieve and cite real, current information rather than generating from general patterns. That's RAG, the entire subject of Week 3, and it's the direct, structural fix for exactly this kind of failure — not a vague promise that "the next model update will be smarter."

**What NOT to do:** Don't promise this will "never happen again" — that promise can't be honestly made about any current GenAI system. Do commit to specific mitigations: grounding answers in verified documentation, adding evaluation before launch (Week 5), and adding guardrails for especially high-stakes claims (also Week 5).

---

## Points to Remember

- **Hallucination is confident, fluent, fabricated content** — a structural consequence of how LLMs generate text (predicting plausible continuations, not retrieving verified facts), not a temporary bug awaiting a future patch.
- **Bias can enter at multiple points**: training data, prompt phrasing, few-shot example selection, and even the evaluation process itself — addressing only one point leaves the others unexamined.
- **Knowledge cutoffs, run-to-run inconsistency, awkward counting/logic, and phrasing sensitivity** are all real, well-documented limitations worth knowing cold, separate from hallucination and bias specifically.
- **The honest, professional response to an AI failure** is calm, mechanism-based explanation plus concrete mitigation — never a promise that it will "never happen again."
- **Grounding (RAG, Week 3), evaluation (Week 5), and guardrails (Week 5)** are the real, structural mitigations for these limitations — not "wait for a smarter model."

---

## Quick Check: Fill in the Blanks

1. Hallucination means the model generates fabricated content while presenting it with the same __________ as accurate content.
2. Hallucination happens because the model predicts the most statistically __________ continuation, with no internal mechanism to flag __________.
3. Bias can enter through training data, __________ phrasing, __________ example selection, and even the evaluation process itself.
4. A model's __________ __________ means it has no training data at all after a certain point in time.
5. The real, structural mitigation for hallucination on factual questions about a specific product is __________ the model's answers in actual, current documentation.

**Answers:** 1. fluency/confidence — 2. plausible, uncertainty — 3. prompt, few-shot — 4. knowledge cutoff — 5. grounding

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-01/session-1.5-quiz.md`](../../assessments/quizzes/week-01/session-1.5-quiz.md) · Answer key: [`assessments/answer-keys/week-01/session-1.5-quiz-answers.md`](../../assessments/answer-keys/week-01/session-1.5-quiz-answers.md)

Interview-style questions for this topic:

1. *"How would you explain hallucination to a product manager who is panicking after seeing a wrong answer from your company's new AI feature?"*
2. *"Is hallucination a bug that will eventually be fixed by a smarter model? Why or why not?"*
3. *"Name three distinct points in a GenAI pipeline where bias can enter, beyond just training data."*
4. *"What is a knowledge cutoff, and what's the structural fix for questions that fall after it?"*
5. *"A model gives different answers to the exact same question on two different runs. Is this necessarily a bug? Explain."*

---

## Core path — guided activity

**Hallucination Detection Exercise.** You'll be given a set of model-generated answers to factual questions, some accurate and some subtly fabricated, and practice spotting the fabricated ones — paying attention to confidence and fluency as poor signals, and learning what *does* serve as a better signal (specificity that can't be verified, suspiciously convenient details). Full instructions: [`codebase/exercises/week-01/session-1.5/`](../../codebase/exercises/week-01/session-1.5/).

## Pro path — extended challenge

You'll design a short "red flag checklist" for spotting likely hallucinations in a specific domain of your choosing (e.g., legal citations, medical claims, historical dates), then test your checklist against a new set of examples to see how well it actually performs — including checking for false positives, where your checklist flags something true as suspicious.

## What's next

Session 1.6 — **Week 1 Lab: Mini Build Day** — integrates everything from this week into a single build: an "explain it to me simply" tool that adapts its explanation to different audiences.
