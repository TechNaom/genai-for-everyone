# Answer Key — Session 6.3 Quiz

**1.** Any two of: data residency/compliance requirements that prohibit sending data to a third party; extremely high steady-state volume where fixed infrastructure cost becomes cheaper than per-token pricing; needing guarantees (uptime, latency, customization) a third-party API can't offer; wanting full control over model behavior/fine-tuning.

**2.** It isolates provider-specific request/response shapes in one place, so business logic calls a single consistent function (`call_model(...)`) regardless of provider. Without it, switching or adding a provider means finding and rewriting every call site that used that provider's SDK directly.

**3.** False. Most teams should start with a closed API because setup cost is near zero, and move to self-hosting only when a specific driver (data residency, extreme steady volume, etc.) appears — self-hosting from day one adds real infrastructure burden most projects don't need yet.

**4.** (1) Hard fallback: automatically retry the same request against a secondary provider when the primary fails/times out. (2) Quality-tiered fallback: try the best model first, and on failure fall back to a faster/cheaper model rather than failing the request outright. They differ in what they optimize for — (1) tries to preserve the same quality via a different provider, (2) accepts a quality trade-off to guarantee *some* response.

**5.** A circuit breaker stops sending requests to a provider after N consecutive failures, waiting out a cooldown period before trying again — instead of retrying (and adding latency/cost) on every single request during an outage. It's better because repeatedly hitting a provider that's clearly down wastes time and resources on requests very likely to fail anyway.

**6.** Because data residency/compliance requirements can be a hard legal constraint, not a quality trade-off — if regulations or contracts prohibit data leaving a company's own infrastructure, a lower-quality self-hosted model may be the only compliant option, regardless of how good the closed API is.

**7.** The risk is that switching providers, adding a fallback, or even upgrading the SDK requires finding and changing 40 separate places, which is slow and error-prone (easy to miss one). The fix is introducing an adapter layer — a single function or module that wraps all provider calls — so the other 40 files call that one function instead of the provider SDK directly.
