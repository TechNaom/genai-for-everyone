# Quiz — Session 6.3: Choosing & Switching Models

_5-8 questions, mixed format. Answer key in `assessments/answer-keys/`._

1. Name two concrete reasons a team might move from a closed API to a self-hosted open model, beyond "it's cheaper."
2. What problem does an adapter layer (e.g., `call_model(prompt, provider=...)`) solve that calling each provider's SDK directly in your business logic doesn't?
3. True or False: Most teams should start with a self-hosted open model to avoid vendor lock-in from day one.
4. **Scenario:** Your primary model provider has a 20-minute outage. Requests are timing out and failing for users. What are two different fallback strategies you could use, and how do they differ?
5. What is a "circuit breaker" pattern, and why is it better than retrying a failing provider on every single request?
6. Why might a company with strict data-residency requirements choose self-hosting even if the closed API model is higher quality?
7. Your codebase calls `anthropic.Anthropic().messages.create(...)` directly in 40 different files. What's the risk this creates, and what's the fix?
