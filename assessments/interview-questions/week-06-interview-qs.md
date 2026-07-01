# Week 6 Interview Questions: Deployment, Cost, Scaling & MLOps-for-GenAI

**Topic:** Deploying Services, Cost/Latency Engineering, Model Switching, Monitoring, CI/CD for Prompts
**Format:** Open-ended technical questions designed for real interviews
**Difficulty:** Intermediate-Advanced (assumes understanding of Sessions 6.1–6.6)

---

## Question 1: Notebook to Application

**The Question:**
"Walk me through what actually changes when you take a working GenAI script and turn it into a deployable service. Does the AI logic itself change?"

**What a strong answer includes:**
- ✅ No, the underlying GenAI logic (the function that calls the model) stays the same
- ✅ What changes: an entry point that handles requests as they arrive (not run-once-and-exit), configuration read from environment variables instead of hard-coded, secrets read from the environment and never logged/committed
- ✅ Mentions the practical benefit: the same code can run in different environments (local, staging, production) with different config/secrets, with zero code changes

**Red flags in weak answers:**
- Thinks deployment requires rewriting the GenAI logic
- No mention of environment-based configuration
- Doesn't distinguish "runs once" from "handles ongoing requests"

**Follow-up if they nail it:**
"What's the risk of hard-coding an API key directly in the script, beyond it being visible in source control?"

---

## Question 2: Token Economics

**The Question:**
"Why are output tokens usually priced higher than input tokens, and how does that change how you'd prompt a model when cost matters?"

**What a strong answer includes:**
- ✅ Generating output requires a full forward pass per token, more compute-intensive than processing given input tokens
- ✅ Practical implication: constraining requested output length (e.g., "answer in 2 sentences") is a direct, high-leverage cost lever
- ✅ Bonus: mentions that model routing (cheap model for simple requests) and prompt caching (for repeated large prefixes) are other major levers

**Red flags in weak answers:**
- Doesn't know input/output are priced differently at all
- No concrete prompting implication offered
- Suggests "just use a cheaper model everywhere" without nuance

**Follow-up if they nail it:**
"When would prompt caching not actually help reduce cost?"

---

## Question 3: Closed API vs. Self-Hosted

**The Question:**
"When would you recommend self-hosting an open-weight model instead of using a closed API, given that the closed API is probably higher quality?"

**What a strong answer includes:**
- ✅ Data residency/compliance requirements that prohibit sending data to a third party
- ✅ Extremely high, steady-state volume where fixed infrastructure cost undercuts per-token pricing
- ✅ Acknowledges the trade-off: self-hosting adds real operational burden (uptime, scaling, staying current with new releases) most projects don't need on day one
- ✅ Notes that most teams should default to a closed API and move only when a specific driver appears

**Red flags in weak answers:**
- "Self-hosting is always cheaper" (ignores infrastructure/operational cost)
- No mention of compliance/data-residency as a real driver
- Treats this as a purely technical decision with no business context

**Follow-up if they nail it:**
"Your self-hosted model needs to be updated to a newer open-weight release. What does that process look like compared to a closed API's automatic updates?"

---

## Question 4: The Adapter Layer

**The Question:**
"Your codebase calls a specific provider's SDK directly in 40 different files. What's the risk, and how would you fix it?"

**What a strong answer includes:**
- ✅ Risk: switching providers, adding a fallback, or upgrading the SDK requires finding and changing all 40 call sites — slow and error-prone
- ✅ Fix: introduce an adapter layer — a single function/module wrapping provider calls — so business logic calls one consistent interface regardless of provider
- ✅ Bonus: mentions this is what makes adding a fallback strategy cheap later

**Red flags in weak answers:**
- Doesn't identify the maintainability risk clearly
- Proposes rewriting all 40 files as the "fix" rather than introducing an abstraction
- No mention of how this affects fallback design

**Follow-up if they nail it:**
"Design the function signature for that adapter layer."

---

## Question 5: Fallback Strategy Design

**The Question:**
"You've built a fallback: if the primary provider times out, retry against a secondary model. In production, you discover the primary is experiencing intermittent slowness (not full outages), and 15% of requests are triggering the fallback unnecessarily. What's wrong, and how would you fix it?"

**What a strong answer includes:**
- ✅ Diagnoses that the fallback's trigger condition (timeout) is too sensitive to transient slowness, not just genuine failures
- ✅ Proposes a fix: a more tolerant timeout, or a circuit-breaker pattern that only engages the fallback after sustained failures rather than per-request
- ✅ Recognizes the trade-off: falling back too eagerly serves users a weaker model unnecessarily often

**Red flags in weak answers:**
- "The fallback is working as designed, no issue" (misses the real problem)
- No concrete fix proposed
- Doesn't distinguish transient slowness from genuine outages

**Follow-up if they nail it:**
"How would a circuit breaker specifically prevent this compared to a per-request timeout retry?"

---

## Question 6: Drift and Monitoring

**The Question:**
"A RAG-based support bot's underlying policy documents get updated, but nobody rebuilds the vector index. Three weeks later, customers are complaining about wrong answers. What went wrong, and what should have caught it sooner?"

**What a strong answer includes:**
- ✅ Identifies this as retrieval/data drift: the source of truth changed while the system (retrieval logic, index) stayed the same
- ✅ What should have caught it: periodic re-scoring of a golden dataset against the live system, or a feedback mechanism (thumbs up/down) surfacing real failures quickly
- ✅ Notes this isn't a code bug — the system worked exactly as built, the world around it changed

**Red flags in weak answers:**
- Treats this as a bug in the retrieval code
- No mention of ongoing monitoring or periodic re-evaluation
- Doesn't distinguish drift from a one-time launch-quality problem

**Follow-up if they nail it:**
"Design a lightweight process for keeping a RAG index's freshness in check going forward."

---

## Question 7: CI Regression Gates for Prompts

**The Question:**
"Why should a CI regression check for a prompt change compare the new score to a baseline, rather than just checking it against a fixed absolute threshold?"

**What a strong answer includes:**
- ✅ A fixed threshold alone can't detect a regression — a new version could clear the bar while still being meaningfully worse than what it's replacing
- ✅ Comparing to the last known-good baseline specifically catches relative degradation, which is the actual thing the gate needs to prevent
- ✅ Mentions that both the prompt and the golden dataset should be versioned together so baseline comparisons stay meaningful

**Red flags in weak answers:**
- Doesn't see the difference between an absolute threshold and a baseline comparison
- No mention of versioning the golden dataset alongside prompts

**Follow-up if they nail it:**
"A prompt change passes the CI gate but a real production issue shows up two weeks later on a case the golden dataset didn't cover. Whose fault is that, and what should happen next?"

---

## Question 8: Startup-Time vs. CI-Time Gates

**The Question:**
"What's the difference between a regression check that runs in CI and one that runs at service startup? What does the startup check catch that CI alone would miss?"

**What a strong answer includes:**
- ✅ CI-time checks only fire when a change goes through the normal pull-request pipeline
- ✅ Startup-time checks run every time the service process boots, regardless of how it got into that state
- ✅ Concrete example: a manual deploy that skips CI, or an environment variable/prompt version set incorrectly at the infrastructure level — both invisible to CI but caught at boot

**Red flags in weak answers:**
- Treats the two as redundant/equivalent
- Can't give a concrete scenario where only the startup check would catch the problem

**Follow-up if they nail it:**
"What should the service do if the startup regression check fails — and why is refusing to start better than starting anyway with a warning?"

---

## Question 9: Bonus — Real-World: The Surprise Bill

**The Question:**
"A support chatbot handled 500 conversations in week one with no cost concerns. By month two, at 50,000 conversations, finance is asking about a $12,000 bill. What should have been modeled before launch, and why didn't the problem show up in week one?"

**What a strong answer includes:**
- ✅ Cost modeling at expected production scale (not just pilot scale) should have happened before launch — per-request inefficiencies (oversized prompts, no model routing) were always present, just invisible at low volume
- ✅ Concrete levers: model routing (cheap model for simple requests), prompt/context trimming, prompt caching for repeated prefixes
- ✅ Recognizes that the "surprise" wasn't really sudden — it was a pre-existing inefficiency multiplied by volume

**Red flags in weak answers:**
- "There's no way to have predicted this" (misses that cost modeling at scale is a standard practice)
- Only proposes one lever (e.g., "just use a cheaper model") without broader analysis

**Follow-up if they nail it:**
"Design a cost dashboard you'd want in place from day one to avoid being surprised like this again."

---

## Rapid-Fire Technical Q&A

Quick checks during interviews:

1. **"What three properties make a service 'deployable,' independent of hosting provider?"**
   → Answer: One-command startup with environment-based config, logging of every request, and graceful degradation (fallback) when a dependency fails.

2. **"Why is a `/health` endpoint useful, separate from the actual functional endpoint?"**
   → Answer: It lets infrastructure check basic process aliveness cheaply, without exercising the full (often expensive/slow) model-calling logic.

3. **"What's the main cost lever for reducing output token spend?"**
   → Answer: Constraining requested output length explicitly in the prompt.

4. **"What does an adapter layer decouple your business logic from?"**
   → Answer: Any single provider's specific SDK/request-response shape.

5. **"What's 'drift' in one sentence?"**
   → Answer: Quality degradation in production caused by the real world changing (input patterns, provider models, underlying data) without any code change.

6. **"Why version the golden dataset alongside prompts, not just the prompts themselves?"**
   → Answer: Because the dataset itself evolves as new production failures are found, and a baseline score is only meaningful relative to the dataset version that produced it.

7. **"What's the safest response when a startup regression check fails?"**
   → Answer: Refuse to start and exit with a clear error, rather than starting anyway in a possibly-broken state.

---

## Interview Strategy Tips

1. **Listen for provider-independence:** Strong candidates describe "production-ready" as a set of properties, not a specific cloud host.
2. **Probe cost reasoning:** Do they think in terms of concrete levers (routing, trimming, caching) rather than vague "optimize it" answers?
3. **Check for monitoring instinct:** Do they mention logging/feedback loops unprompted when discussing anything shipped to production?
4. **Watch for gate design nuance:** Baseline comparison vs. fixed threshold is a good signal of real CI/eval experience.
5. **Real-world grounding:** Ask for a specific number (a real latency, a real cost figure) from something they've actually measured, not just theory.

---

*Week 6 Interview Questions | GenAI for Everyone | Deployment, Cost, Scaling & MLOps-for-GenAI*
