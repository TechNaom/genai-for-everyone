# Answer Key — Session 6.1 Quiz

**1.** (1) An entry point that handles a request each time it's called, instead of running once and exiting. (2) Configuration (model name, tunable values) read from environment variables/config instead of hard-coded. (3) Secrets read from the environment, never committed to source control or printed in logs.

**2.** B — Environment variables let the same deployed code point at different models, rate limits, or staging/production credentials without any code change or redeploy.

**3.** It should return a proper 4xx response (e.g., `400 Bad Request`) with a clear error message like `{"error": "question is required"}`, not crash with an unhandled exception. A raw stack trace can also leak internal implementation details to the caller.

**4.** False. The GenAI logic (`call_llm()` or equivalent) stays exactly the same — only the *invocation* changes, from being called once at the bottom of a script to being called inside a request handler.

**5.** Logs are often stored, searched, and shared far more widely than people expect (monitoring dashboards, third-party log aggregators, support tickets that include log snippets) — a printed API key can leak to anyone with log access, effectively as bad as committing it to source control. Log that a key was loaded/valid, never the key's value.

**6.** The better failure mode is failing fast and clearly at startup — check for required environment variables when the process boots and exit immediately with a message like `"Missing required env var: ANTHROPIC_API_KEY"`, rather than letting the first real user request hit an unhandled `KeyError` deep in the code. A startup check surfaces the problem to whoever is deploying, immediately and unambiguously.

**7.** A `/health` endpoint gives infrastructure (load balancers, uptime monitors, container orchestrators) a fast, cheap way to check "is this process alive and able to respond" without exercising the full (and often expensive/slow) LLM-calling logic. Functional endpoints can be down for reasons unrelated to basic process health (e.g., a downstream API outage), so keeping the two checks separate gives clearer signal about what's actually broken.
