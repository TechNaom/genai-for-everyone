# Week 6 Written Exam

_Deeper, scenario-based exam covering all of Week 6's sessions (6.1–6.6): from notebook to application, cost & latency engineering, choosing & switching models, monitoring & observability, CI/CD & versioning for prompts, and the deployment capstone._

**Format:** 7 short-answer questions + 3 scenario-analysis questions + 1 synthesis question
**Suggested time:** 60–75 minutes
**Open book:** Yes — this tests understanding and application, not memorization

---

## Section A — Short Answer

**A1.** Name the three changes that turn a one-off script into a deployable service, and explain why none of them require touching the underlying GenAI logic.

**A2.** Why are output tokens typically priced higher than input tokens, and what's the practical implication for how you should prompt a model when cost matters?

**A3.** Explain the trade-off between a closed API model and a self-hosted open-weight model — under what specific condition does self-hosting actually become the better choice?

**A4.** What does an adapter layer (e.g., `call_model(prompt, provider=...)`) protect you from that calling a provider's SDK directly in your business logic does not?

**A5.** Define "drift" in the context of a deployed GenAI system, and give one example that has nothing to do with the model itself changing.

**A6.** Why does a CI regression gate for prompts compare a new version's score to a *baseline*, rather than checking it against a fixed absolute threshold alone?

**A7.** What's the difference between a CI-time regression check and a startup-time regression check, and what specific failure mode does the startup-time check catch that CI alone would miss?

---

## Section B — Scenario Analysis

**B1. The Silent Cost Explosion**
A support chatbot handled 500 conversations in its first week with no complaints about cost. By month two, it's handling 50,000 conversations and finance is asking why the bill is $12,000. Identify at least two concrete levers (not "just use a cheaper model" alone) that should have been modeled *before* launch, and explain why cost modeling at 500 conversations/week didn't reveal the problem.

**B2. The Fallback That Fired Too Often**
You've deployed a provider adapter with automatic fallback: if the primary model errors or times out, requests silently retry against a cheaper, weaker secondary model. After a week in production, you notice quality complaints have risen, and investigation reveals the primary provider has been experiencing intermittent slowness (not full outages) that's triggering timeout-based fallbacks on roughly 15% of requests. Diagnose what's actually going wrong here, and explain why "the fallback is working as designed" doesn't fully address the real problem.

**B3. The Regression That Slipped Through**
A prompt change passes your CI regression gate (golden dataset score: 91%, baseline: 92%, within the 5-point threshold) and ships. Two weeks later, user complaints reveal the new prompt is subtly worse on a category of questions your golden dataset happened not to include. Explain why passing the CI gate didn't prevent this, and what mechanism (from a different Week 6 session) exists specifically to catch exactly this kind of gap.

---

## Section C — Synthesis

**C1.** A hiring manager asks you: "Walk me through what 'production-ready' actually means for a GenAI feature — not buzzwords, specifics." Write a 150–250 word answer, in plain language, that:
- Names at least three concrete properties (drawn from this week's sessions) that make a service production-ready, not just "it works when I test it"
- Explains why none of these require a specific cloud provider or expensive infrastructure
- Gives one honest example of what still isn't guaranteed even once all these properties are in place

---

## Answer Key

### Section A

**A1.** (1) An entry point that handles requests as they come in, rather than running once and exiting; (2) configuration (model name, tunable values) read from the environment instead of hard-coded; (3) secrets read from the environment, never committed or logged. None require touching the GenAI logic itself because they change *how the existing logic is invoked and configured*, not what it does — the same `call_llm()` function works identically whether it's called once at the bottom of a script or from inside a request handler.

**A2.** Output tokens are priced higher because generating each token requires a full model forward pass, which is more compute-intensive than processing tokens already provided as input. Practically, this means constraining requested output length (e.g., "answer in 2 sentences," "50 words max") is one of the most direct cost levers available, since it directly reduces the more expensive side of the token bill.

**A3.** Closed APIs require near-zero setup and access the strongest available models, but cost scales per token with usage and data leaves your infrastructure. Self-hosted open models require real infrastructure investment but offer full data control and can become cheaper at very high, steady-state volume. Self-hosting becomes the better choice specifically when a hard constraint exists — data residency/compliance requirements that prohibit third-party data handling, or usage volume high and steady enough that fixed infrastructure cost undercuts per-token API pricing.

**A4.** An adapter layer isolates provider-specific request/response shapes in one place, so switching providers, adding a fallback, or upgrading an SDK means changing one function instead of finding and rewriting every place in the codebase that called a provider's SDK directly.

**A5.** Drift is quality degradation in a deployed system that happens without any code change, because the world the system operates in shifted. An example unrelated to the model itself changing: the underlying documents in a RAG system's retrieval index become stale or are updated, so retrieval starts surfacing outdated information even though the retrieval logic and the model are both unchanged.

**A6.** Comparing to a fixed absolute threshold alone can't detect a *regression* — a new version could still clear a fixed bar while being meaningfully worse than the version it's replacing. Comparing to the last known-good baseline specifically catches drops in quality relative to what was already working, which is the actual thing a regression gate needs to prevent.

**A7.** A CI-time check only runs when a change goes through the normal pull-request pipeline. A startup-time check runs every time the service process boots, regardless of how it got into that state — catching configuration drift that never touched CI at all: a manual deploy that skipped the pipeline, an environment variable set incorrectly at the infrastructure level, or a stale/wrong prompt version loaded at runtime.

---

### Section B

**B1.** At least two levers: model routing (sending simpler requests to a cheaper/smaller model and reserving the expensive model for genuinely complex ones) and prompt/context trimming (reducing unnecessary input tokens per request, e.g., an oversized system prompt or excessive retrieved context). Cost modeling at 500 conversations/week didn't reveal the problem because the absolute dollar cost was small enough to go unnoticed at that volume — the per-request inefficiencies were always present, they just hadn't been multiplied by a volume large enough to become visible on a bill anyone was watching.

**B2.** The real problem is that the fallback's trigger condition (timeout) is firing on transient slowness, not just genuine outages, so a large fraction of requests are silently being served by the weaker secondary model even though the primary provider is technically still available and would likely have succeeded with a bit more patience. "The fallback is working as designed" doesn't address this because the *design* itself is flawed for this failure mode — a fallback tuned only for hard failures needs a more nuanced trigger (e.g., a slightly longer timeout, or a circuit-breaker pattern that only engages after sustained failures) rather than falling back on every individual slow response, which trades away quality more often than necessary.

**B3.** Passing the CI gate only confirms the new prompt didn't regress on the examples already in the golden dataset — it says nothing about a category of questions the dataset never included, and a genuinely new failure mode by definition isn't represented in an existing dataset. The mechanism that exists specifically to catch this gap is Session 6.4's monitoring and feedback loop: production monitoring and user feedback surface real-world failures the golden dataset didn't anticipate, which then get added back into the dataset so future CI gates catch this specific failure mode too.

---

### Section C

**C1.** Sample model answer (grade for content, not exact wording):

> "Production-ready" for a GenAI feature means a handful of concrete properties, not a specific hosting provider. First, it starts with one command and reads its configuration — model name, API keys — from the environment rather than hard-coded values, so the same code can run safely in different environments. Second, it logs every request (input, output, latency, cost) so we can actually investigate problems instead of guessing. Third, it degrades gracefully — if our primary model provider has an outage, it falls back to a secondary option rather than failing every request outright. Fourth, changes to it (especially to prompts) go through an automated check that compares new behavior against a known-good baseline before shipping. None of these require a specific cloud provider — they're properties of how the service is built and operated, and they'd apply whether it's running on a free-tier host or a major cloud platform. What's still not guaranteed even with all of this in place: correctness on situations we haven't seen or tested for yet — these properties make problems visible and recoverable, they don't make the system infallible.

**Full credit (15 pts):** Names at least 3 concrete properties correctly [6 pts], explains why they're provider-independent [4 pts], gives an honest example of what's still not guaranteed [5 pts].
**Partial credit:** Names properties but frames "production-ready" as tied to a specific host/provider, or omits the honest caveat.

---

## Grading Guidance

- **Section A (21 pts, 3 pts each):** Full credit requires the correct mechanism and the "why it matters" connection.
- **Section B (24 pts, 8 pts each):** Grade holistically — strong credit for correctly identifying the underlying issue (cost levers unmodeled at scale, fallback trigger design, or golden-dataset coverage gap) even with different specific wording, provided the reasoning holds.
- **Section C (15 pts):** See rubric above.
- **Total: 60 pts.** Suggested cutoffs: 54+ = excellent, 42–53 = solid, 30–41 = needs review (trace missed questions back to cost/latency/6.2, model switching/6.3, or CI/CD for prompts/6.5), <30 = recommend revisiting Week 6 sessions before Week 7.
