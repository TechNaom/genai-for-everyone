# Answer Key — Session 2.5 Quiz

**1.** B — A prompt system differs in kind, not just scale: it adds reusable templates with variables, some notion of versioning, consistent testing, and often chaining multiple prompts together.

**2.** Even well-written prompts become hard to find, review, and modify when buried in application code — there's no centralized place to see what prompts exist, no clear history of what changed, and anyone (including the original author) has to dig through unrelated business logic to locate and understand a given prompt. This makes maintenance, debugging, and onboarding new team members significantly harder over time.

**3.** C — Since exact-match testing is unrealistic for naturally-varying LLM output, lightweight tests should check for specific, verifiable characteristics (required content, length limits, absence of forbidden content) rather than requiring identical text every time.

**4. **Chaining is the right choice when a task has genuinely distinct sub-problems that benefit from being handled separately and tested independently (e.g., classify, then extract, then draft) — it adds latency and complexity, so it's not appropriate for simple tasks that don't actually have that kind of internal structure.

**5.** Likely problems: duplicate or near-duplicate prompts get written because nobody can find the existing one; nobody knows what a given prompt's expected inputs are without reading through the calling code; there's no way to tell what changed if a prompt's behavior shifts; and onboarding a new team member becomes much slower since there's no organized place to learn what prompts the system actually uses.

**6.** The trade-off: chaining adds latency (multiple API calls) and complexity (managing handoffs between steps), in exchange for each step being simpler, more testable in isolation, and easier to debug independently. The decision should weigh whether the task genuinely has distinct sub-problems worth separating, against the added cost and complexity of managing a multi-step pipeline.
