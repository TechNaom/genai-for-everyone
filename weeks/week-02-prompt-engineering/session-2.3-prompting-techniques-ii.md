# Session 2.3: Prompting Techniques II

**Week:** 2 — Prompt Engineering & Application Design
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes

---

## Why this chapter exists

Session 2.2's techniques — zero-shot, few-shot, role prompting — shape *what pattern* the model follows. This chapter's techniques shape *how the model reasons* on its way to an answer, which matters enormously once a task involves more than one step of thinking. A model asked to directly produce the answer to a multi-step problem will sometimes skip steps, make an early mistake that cascades, or simply guess at a plausible-looking final answer without genuinely working through the logic. The techniques in this chapter exist specifically to counteract that.

This is also where Session 1.5's central warning becomes operationally important rather than just conceptually true: these techniques can dramatically *improve* reasoning quality, but none of them eliminate the core risk that a fluent, well-structured wrong answer is still possible. Keep that tension in mind throughout this chapter — it's not a contradiction, it's the honest reality of working with these tools.

---

## Part 1: Chain-of-Thought Prompting — Show the Work

### What it is

Chain-of-thought prompting means explicitly instructing the model to reason step-by-step *before* giving a final answer, rather than jumping straight to a conclusion. The simplest version is often just appending a phrase like "think step by step" or "explain your reasoning before giving your final answer" to a prompt.

### Why it works

Recall Session 1.1's core mechanism: the model predicts the next token based on everything currently in its context. If the model's own intermediate reasoning steps become part of that context as they're generated, each subsequent token gets predicted with the benefit of that visible reasoning trail — rather than having to implicitly do all that work in a single, opaque leap to a final answer. Writing out "Step 1: identify the two numbers being compared, Step 2: ..." literally gives the model more relevant context to draw on for predicting Step 3, in exactly the sense established back in Session 1.2.

### A concrete demonstration

**Without chain-of-thought:** "A store had 142 items. They sold 38% on Monday and 25 more on Tuesday. How many are left?" → A direct prompt risks the model jumping to an answer that skips or garbles one of the two operations.

**With chain-of-thought:** "A store had 142 items. They sold 38% on Monday and 25 more on Tuesday. How many are left? Think through this step by step before giving your final answer." → The model is far more likely to explicitly compute 38% of 142, subtract that, then subtract the additional 25, showing each intermediate result — and each correct intermediate step makes the next step more likely to also be correct.

### The honest limit, restated from Session 1.1 and 1.5

A beautifully formatted, step-by-step chain of reasoning can still arrive at a wrong conclusion. The *presence* of visible reasoning is not proof of *correct* reasoning — it's a mechanism that tends to improve accuracy on many tasks, not a guarantee. For anything genuinely high-stakes, the chain of reasoning itself is something worth actually reading and checking, not just trusting because it looks thorough.

---

## Part 2: Step-Back Prompting — Zoom Out Before Zooming In

### What it is

Step-back prompting means asking the model to first articulate the general principle, concept, or strategy relevant to a problem, *before* applying that principle to the specific question at hand. Instead of diving straight into specifics, the model is prompted to "step back" to the more abstract level first.

### A concrete demonstration

**Direct approach:** "Should we use a relational database or a document database for storing user session data that expires after 24 hours?"

**Step-back approach:** "What are the general factors that determine whether relational or document databases are better suited to a given use case? Then, applying those factors, should we use a relational database or a document database for storing user session data that expires after 24 hours?"

The step-back version forces the model to first lay out the relevant general framework (data structure, query patterns, consistency needs, lifespan/expiry handling) *before* committing to a specific recommendation — which tends to produce a more grounded, better-justified answer than jumping straight to "use X" without first establishing why that general category of answer makes sense here.

### Why this helps, mechanically

This connects to the same context-shaping mechanism as chain-of-thought: by generating the general principle first, that principle becomes part of the context the model draws on when it then addresses the specific question — rather than answering the specific question using whatever generic pattern is statistically closest, with no explicit grounding step in between.

### When step-back is worth the extra step

Step-back prompting is most valuable for problems that have a real underlying decision framework or principle — comparisons, recommendations, and "should we do X or Y" questions especially. It's less necessary for simple factual lookups or straightforward generation tasks where there isn't really a "general principle" layer to surface first.

---

## Part 3: Self-Consistency — Don't Trust Just One Attempt

### What it is

Self-consistency means generating multiple independent responses to the same prompt (often with some randomness enabled) and then comparing them — taking the most common answer, or otherwise examining where the different attempts agree and disagree — rather than accepting a single response at face value.

### Why this matters

A single response represents one path through the model's possible outputs for a given prompt. For ambiguous or genuinely difficult problems, that single path might land on a brittle, lucky-or-unlucky answer that wouldn't reproduce reliably. Running the same prompt multiple times and looking for *agreement* across runs is a practical, simple way to catch cases where the model is genuinely uncertain (and the answers diverge) versus confidently consistent (and the answers converge).

### A concrete demonstration

Imagine asking a model to solve a tricky logic puzzle once, and getting an answer. Now imagine running that same prompt five times. If four out of five runs converge on the same answer, that convergence is meaningful evidence (not proof) that the answer is likely correct. If the five runs produce five different answers, that divergence is a strong signal that this is a genuinely hard case for the model — exactly the kind of case where you should NOT trust a single confident-sounding response, connecting directly back to Session 1.5's warning that confidence and correctness are separate properties.

### The honest cost

Self-consistency isn't free — it multiplies your token cost and latency by however many times you run the prompt, directly engaging with Session 1.3's cost/speed trade-off thinking. It's a tool for genuinely high-stakes or ambiguous cases, not a default you'd apply to every single request in a production system. Knowing *when* the extra cost is justified is as much a part of this skill as knowing the technique exists.

---

## Part 4: Choosing the Right Tool for the Job

With five techniques now in your toolkit across Sessions 2.2 and 2.3 (zero-shot, few-shot, role prompting, chain-of-thought, step-back, self-consistency — six, technically), the real skill is matching technique to situation, not applying all of them reflexively to every prompt.

**A simple, well-defined factual question:** zero-shot is usually fine. Adding chain-of-thought to "what's the capital of France" is unnecessary overhead.

**A company-specific classification task:** few-shot, as covered in 2.2.

**A multi-step word problem or logical puzzle:** chain-of-thought, since intermediate steps genuinely help.

**A "should we do X or Y" recommendation with an underlying framework:** step-back, to ground the recommendation in the right general principle first.

**A genuinely ambiguous, high-stakes decision where being wrong is costly:** self-consistency, accepting the extra cost for the added confidence signal.

**A task needing both a specific persona AND demonstrated pattern:** role prompting combined with few-shot, as shown in Session 2.2's content-moderation example.

Notice that none of these techniques are about making the prompt "fancier" for its own sake — each one earns its place by solving a specific failure mode that a plainer prompt would risk.

---

## Points to Remember

- **Chain-of-thought**: explicitly asking the model to reason step-by-step before answering, which gives each subsequent step more relevant context to draw on. Improves accuracy on multi-step tasks but doesn't guarantee a correct conclusion.
- **Step-back prompting**: asking the model to articulate the general principle before applying it to the specific question — most valuable for comparisons, recommendations, and "X or Y" decisions with a real underlying framework.
- **Self-consistency**: running the same prompt multiple times and checking for agreement, which is a practical signal (not proof) of reliability — costs extra tokens and latency, so reserve it for genuinely ambiguous or high-stakes cases.
- **None of these techniques eliminate the core risk from Session 1.5** — a fluent, well-structured, confident response can still be wrong. These techniques improve odds, not certainty.
- **Match the technique to the failure mode you're actually worried about**, rather than applying every technique to every prompt by default.

---

## Quick Check: Fill in the Blanks

1. Chain-of-thought prompting works because intermediate reasoning steps become part of the __________ that subsequent tokens are predicted from.
2. Step-back prompting asks the model to articulate a general __________ before applying it to the specific question.
3. Self-consistency means running the same prompt __________ times and checking for __________ across the results.
4. Divergent answers across multiple self-consistency runs are a signal that the model is genuinely __________ on that case.
5. None of the techniques in this chapter eliminate the core risk from Session __________: a fluent, confident response can still be __________.

**Answers:** 1. context — 2. principle (or framework) — 3. multiple, agreement — 4. uncertain — 5. 1.5, wrong

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-02/session-2.3-quiz.md`](../../assessments/quizzes/week-02/session-2.3-quiz.md) · Answer key: [`assessments/answer-keys/week-02/session-2.3-quiz-answers.md`](../../assessments/answer-keys/week-02/session-2.3-quiz-answers.md)

Interview-style questions for this topic:

1. *"What is chain-of-thought prompting, and what's a risk of relying on it too heavily?"*
2. *"When would step-back prompting help more than just asking the question directly?"*
3. *"What is self-consistency prompting, and when is it worth the extra cost?"*
4. *"How would you decide which prompting technique to apply to a new task you've never seen before?"*

---

## Core path — guided activity

**Multi-Step Reasoning Prompt.** You'll take a real multi-step business problem (e.g., a pricing or staffing calculation), write both a direct prompt and a chain-of-thought version, run both, and compare the results for accuracy and whether the reasoning trail actually holds up to scrutiny. Full instructions: [`codebase/exercises/week-02/session-2.3/`](../../codebase/exercises/week-02/session-2.3/).

## Pro path — extended challenge

You'll implement a basic self-consistency check: run the same ambiguous prompt multiple times programmatically, collect the responses, and write logic to detect whether the answers converge or diverge — then test it on both an easy question (expect convergence) and a genuinely hard or ambiguous one (expect more divergence), demonstrating the signal actually behaves as this chapter predicts.

## What's next

Session 2.4 — **Structured Outputs** — moves from reasoning quality to output reliability: getting consistent, parseable JSON and other structured formats out of an LLM.
