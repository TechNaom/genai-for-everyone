# Session 1.3: The GenAI Landscape

**Week:** 1 — Foundations of GenAI & LLMs
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes

---

## Why this chapter exists

By now you understand *what* generative AI is (Session 1.1) and roughly *how* it works under the hood (Session 1.2). This chapter answers a different, very practical question: **when you actually have to build something, which model do you reach for, and why?**

This matters because the GenAI landscape changes constantly — new models launch what feels like every few weeks, benchmarks shuffle, prices shift. If this chapter tried to hand you a definitive "best model" ranking, it would be wrong within months. So we're doing something more durable: teaching you the **categories, the trade-off dimensions, and the decision framework** that will still be useful long after today's specific model names have been replaced by their successors. A working professional doesn't need to memorize a leaderboard. They need to know *how to evaluate* whatever's on the leaderboard when they actually need to make a choice.

---

## Part 1: The Major Players — A Map, Not a Leaderboard

Rather than ranking models (which goes stale immediately), let's understand the *kinds* of organizations building them, because that tells you something durable about their incentives and strengths.

### The closed/proprietary API providers

These companies train large, frontier-capability models and make them available *only* through an API or a chatbot product — you can never download the actual model weights or run it yourself. The major names you'll hear constantly: **OpenAI** (GPT models, ChatGPT), **Anthropic** (Claude models), and **Google** (Gemini models).

What unites them: they pour enormous resources into training the largest, most capable models, and they monetize through API usage fees and consumer/enterprise subscriptions. You get convenience — no infrastructure to manage, frontier-level capability, regular improvements pushed automatically — in exchange for giving up control over how the model runs, where your data goes during processing, and the ability to customize the model's internals.

### The open-weight providers

These organizations release the actual trained model — its parameters, the literal "weights" — for anyone to download and run on their own hardware. **Meta** (the Llama family) is the most prominent example, alongside companies like **Mistral** and **DeepSeek**, which have both released highly capable open-weight models.

"Open" here is a specific, technical claim — it doesn't always mean "open source" in the traditional software sense (training data and training code are often still kept private), but it does mean you can self-host, fine-tune on your own data, and guarantee that your data never leaves your own infrastructure during inference. The cost: you (or your company) now own all the infrastructure complexity — GPUs, serving software, scaling, monitoring — that the closed providers handle invisibly for you.

### Why this split exists, and why it's not going away

This isn't a temporary market quirk — it reflects a genuine tension. Building frontier-capability models costs an enormous amount of money in compute and research talent, which pushes providers toward charging for access (closed). But many organizations — especially regulated industries like healthcare and finance, or anyone with strict data residency requirements — have a hard requirement that data never transits a third party's servers, which only open, self-hostable models satisfy. Expect both categories to keep existing, growing, and competing indefinitely, because they're solving for genuinely different constraints, not just competing on the same axis.

---

## Part 2: The Dimensions That Actually Matter for Choosing

Forget "which model is best" — that question is incomplete. The real question is always: **best *for what*, given *which* constraints?** Here are the dimensions that should drive any real decision.

### Capability

How well does the model handle complex reasoning, nuanced writing, coding, or multi-step problems? This is what most public benchmarks try to measure, and it's genuinely important — but it's also the dimension most likely to change month to month, and the dimension most overweighted by people new to this field. A model that's 2% better on a benchmark is rarely worth a 5x cost increase for most real applications.

### Speed (latency)

How quickly does the model respond, measured in tokens generated per second, and how long before the *first* token appears? This matters enormously for real-time, user-facing applications (a chatbot a person is actively waiting on) and matters far less for batch or asynchronous workflows (generating overnight reports, processing a queue of documents). Smaller, lighter models within the same provider's lineup are almost always faster — this is why most providers offer a tiered lineup (a small/fast model, a mid-tier model, and a large/frontier model) rather than just one.

### Cost

Priced per million tokens, split into input cost and output cost (output is usually priced higher, since generating text is more computationally expensive than reading it). Costs vary by an order of magnitude or more between a provider's cheapest and most capable tiers, and self-hosting an open-weight model trades per-token fees for fixed infrastructure costs (GPUs), which only becomes economical at high, predictable volume. We'll build an actual cost calculator for this in Week 6.

### Context length

How much text can the model consider in a single request? This has grown dramatically — models now commonly handle context windows in the hundreds of thousands to low millions of tokens. A huge context window matters enormously for tasks like analyzing an entire codebase or a large collection of legal documents in one pass, and matters far less for short, simple conversational tasks.

### Specialization

Some models or model variants are specifically tuned for certain tasks — strong coding performance, strong multilingual handling, dedicated "reasoning" modes that spend more computation deliberating before answering. A model that's a generalist powerhouse isn't automatically the best choice for a narrow, specialized task where a smaller, tuned model might do just as well for a fraction of the cost.

### Compliance and data handling

For regulated industries — healthcare, finance, government — this can be the *deciding* factor above all others, overriding capability comparisons entirely. Questions like "does this provider offer a signed compliance agreement for handling sensitive health data?" or "where geographically is my data processed and stored?" can eliminate otherwise-excellent options immediately. Always verify compliance commitments directly with a provider's enterprise sales channel — documentation pages lag reality and policies change.

---

## Part 3: A Practical Decision Framework

Here's a framework you can actually apply, regardless of which specific models exist when you're reading this.

**Step 1: Start with a strong, well-known general-purpose model for development and evaluation.** Don't optimize prematurely. Build your first working version with whichever capable, well-documented model is easiest to get started with. Get the actual application logic right first.

**Step 2: Once it works, ask whether you need that much capability for production.** Many tasks that *feel* like they need the most powerful model available actually work fine on a smaller, faster, cheaper tier from the same provider. Test this explicitly — don't assume.

**Step 3: Check for hard constraints that override pure capability comparison.** Does this involve regulated data? Does the use case require self-hosting for data residency? Is there a fixed, predictable high volume that would make self-hosting an open-weight model cheaper than ongoing API fees? These constraints can eliminate "the best model" entirely in favor of "the only compliant model."

**Step 4: Re-evaluate periodically, not constantly.** The landscape moves fast, but re-architecting your application every time a new model launches is its own kind of waste. Pick a reasonable cadence (quarterly is common in industry) to reassess whether a newer or cheaper option now fits better.

---

## Part 4: A Worked Comparison Exercise

Let's make the trade-offs concrete with a simple thought experiment. Imagine three different applications, and notice how the "right" model choice differs sharply for each, even though all three are technically just "calling an LLM":

**Application A: A customer-facing live chat widget on an e-commerce site.** Priority: speed (users won't wait), moderate capability (most questions are simple), cost matters at high volume since every visitor might trigger a call. → A fast, cheap, smaller-tier model from a closed provider is usually the right fit. Frontier capability is wasted here; latency is what users actually feel.

**Application B: An internal tool that summarizes lengthy legal contracts overnight in a batch job.** Priority: capability and context length (contracts can be long and the cost of a missed clause is high), speed barely matters (it runs overnight, unattended), cost matters less per-call since volume is lower. → A frontier-capability, large-context model is worth the cost here, even if it's slower and pricier per call.

**Application C: A healthcare provider's internal clinical documentation assistant, handling protected patient data.** Priority: compliance and data handling come first, full stop — capability and cost are secondary considerations that only get evaluated *among* the options that already satisfy the compliance requirement. → The decision starts by filtering to providers with confirmed compliance agreements for sensitive health data, and only then comparing capability and cost among that filtered set.

Notice the pattern: **none of these three applications would make the same model choice**, and none of them are simply "pick whichever model wins the benchmark this month." That's the actual skill this chapter is teaching.

---

## Points to Remember

- **The GenAI landscape splits into closed/proprietary providers** (frontier capability, no infrastructure burden, but you don't control the model or guarantee where data goes) **and open-weight providers** (self-hostable, customizable, data stays in your infrastructure, but you own all the operational complexity).
- **"Best model" is an incomplete question.** The real question is always "best for what task, under which constraints (speed, cost, context length, compliance)?"
- **Capability is the most talked-about dimension and the most overweighted one.** Speed, cost, and compliance often matter more in practice than a small benchmark edge.
- **Compliance and data-handling requirements can override every other consideration** for regulated industries — always verify directly with a provider's enterprise team rather than trusting documentation alone.
- **Different applications within the same company can reasonably use entirely different models** — there's no single "house model" requirement, and matching the model to the specific task's constraints is the actual skill.

---

## Quick Check: Fill in the Blanks

1. Closed/proprietary providers give you frontier capability without infrastructure burden, but you don't control the model or always know where your __________ goes during processing.
2. Open-weight models can be __________, meaning you can run them on your own hardware and guarantee data never leaves your infrastructure.
3. The question "which model is best" is incomplete — the better question is "best for __________, given which __________?"
4. For regulated industries like healthcare and finance, __________ requirements can override capability and cost comparisons entirely.
5. A fast, real-time, user-facing chat widget typically prioritizes __________ over raw capability, while an overnight batch summarization job typically prioritizes __________ instead.

**Answers:** 1. data — 2. self-hosted (or self-hostable) — 3. what task, constraints — 4. compliance (or data-handling) — 5. speed, capability (or context length)

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-01/session-1.3-quiz.md`](../../assessments/quizzes/week-01/session-1.3-quiz.md) · Answer key: [`assessments/answer-keys/week-01/session-1.3-quiz-answers.md`](../../assessments/answer-keys/week-01/session-1.3-quiz-answers.md)

Interview-style questions for this topic:

1. *"How would you choose between an open-weight model and a closed/proprietary API for a new project?"*
2. *"A startup wants to use the most powerful model available for every single feature, regardless of cost. What would you push back on, and why?"*
3. *"What's the difference between a model's capability and its speed, and can you give an example of a use case where speed matters more than capability?"*
4. *"How would you evaluate model options for a healthcare application handling patient data?"*
5. *"Why might a single company reasonably use three different models across three different features, instead of standardizing on one?"*

---

## Core path — guided activity

**Comparison Matrix.** You'll run the same realistic task (e.g., summarizing a short document, or answering a multi-step question) across multiple models available to you, and build a comparison table covering observed speed, output quality, and — where pricing is published — relative cost. Full instructions: [`codebase/exercises/week-01/session-1.3/`](../../codebase/exercises/week-01/session-1.3/).

## Pro path — extended challenge

You're given three short, realistic application briefs (similar in spirit to Part 4's worked examples, but new ones). For each, you'll write a one-paragraph model-selection recommendation, explicitly naming which dimensions (capability, speed, cost, context length, compliance) drove your decision — and defend why a *different* choice would be wrong for that specific brief.

## What's next

Session 1.4 — **Your First GenAI Application** — moves from comparing models to actually calling one: system/user/assistant roles, and building a working CLI chatbot in Python.
