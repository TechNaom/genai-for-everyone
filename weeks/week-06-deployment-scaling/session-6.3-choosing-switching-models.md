# Session 6.3: Choosing & Switching Models

**Week:** 6 (Deployment Scaling)
**Format:** Live session + self-paced exercise + quiz

## Learning objective

Choose a model deliberately for a given task (open vs. closed, self-hosted vs. API), and design a system that can switch models — including a fallback when your primary provider is unavailable — without a rewrite.

## Concept (shared by everyone)

By Week 6 you've used at least two or three different models across this program (Session 1.3's comparison matrix, whichever provider your exercises defaulted to). Model choice isn't a one-time decision made at project kickoff — it's a recurring engineering decision, because the landscape changes constantly (new models ship, prices shift, a provider has an outage) and requirements change too (a prototype's "good enough" model is rarely the right choice at scale).

### Closed (API) vs. open (self-hosted), the real trade-off

| | Closed API (Claude, GPT, Gemini) | Open-weight, self-hosted (Llama, Mistral, etc.) |
|---|---|---|
| **Setup cost** | Near zero — API key and you're calling it | Real infrastructure work: hosting, serving framework, scaling |
| **Per-request cost** | Pay per token, scales with usage | Fixed infrastructure cost regardless of usage (can be cheaper at very high, steady volume) |
| **Quality ceiling** | Usually the strongest available models | Competitive, but typically a step behind the best closed models |
| **Data control** | Data leaves your infrastructure (subject to provider's policies) | Full control — critical for some regulated/sensitive workloads |
| **Operational burden** | Provider handles uptime, scaling, updates | You own uptime, scaling, and keeping up with new model releases |

Most teams start on a closed API because the setup cost is near zero, and only move to self-hosting when a specific driver appears: data residency requirements, extremely high steady-state volume where the economics flip, or a need for guarantees a third-party API can't offer.

### Designing for switchability

The mistake that makes switching painful later is baking a specific provider's API shape directly into your business logic. The fix is a thin adapter layer:

```python
def call_model(prompt: str, provider: str = "anthropic") -> str:
    if provider == "anthropic":
        return _call_anthropic(prompt)
    elif provider == "openai":
        return _call_openai(prompt)
    raise ValueError(f"Unknown provider: {provider}")
```

Your application code calls `call_model(prompt)` and never touches provider-specific request/response shapes directly. Adding a new provider, or falling back to one, means adding a function — not rewriting every call site.

### Fallback strategies

A production system that depends on a single provider with no fallback has a single point of failure it didn't need to have. Common patterns:
- **Hard fallback:** primary provider fails or times out → retry against a secondary provider automatically
- **Quality-tiered fallback:** try the best model first; if it errors or times out, fall back to a faster/cheaper model rather than failing the request entirely
- **Circuit breaker:** after N consecutive failures from a provider, stop trying it for a cooldown period instead of adding latency to every request with a doomed retry

## Core path — guided activity

Run the same task (e.g., summarizing a document, or a question from your Week 3 policy bot) across at least 2 model providers/tiers using the adapter pattern above, and produce a comparison table of cost, latency, and a subjective quality note for each. Full instructions: [`codebase/exercises/week-06/session-6.3/`](../../codebase/exercises/week-06/session-6.3/).

## Pro path — extended challenge

Implement a fallback wrapper: `call_model_with_fallback(prompt, primary, fallback)` that calls the primary provider, catches a simulated failure (the exercise mocks a provider outage), and automatically retries against the fallback — logging which path was actually used so you can measure how often the fallback fires.

## Real-world scenario

Your team built a feature entirely around one provider's specific API. Six months later, that provider raises prices sharply, and switching means touching 40 call sites across the codebase because provider-specific code is scattered everywhere. A thin adapter layer, decided on in Week 6 rather than discovered the hard way in month 7, would have made that a one-function change.

## Key takeaways

- Closed APIs win on setup speed; self-hosted open models win on data control and cost at very high steady volume — most projects start closed and switch only when a specific driver appears.
- An adapter layer between your business logic and any specific provider's API is what makes switching (or adding a fallback) cheap later.
- A single-provider system without a fallback has an avoidable single point of failure.
- Model choice isn't a one-time decision — revisit it as the landscape and your requirements both change.

## Quiz

See [`assessments/quizzes/week-06/session-6.3-quiz.md`](../../assessments/quizzes/week-06/session-6.3-quiz.md)

## Slide deck

See `assets/slides/week-06/session-6.3.pptx`
