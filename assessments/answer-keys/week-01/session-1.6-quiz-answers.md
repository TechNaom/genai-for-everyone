# Answer Key — Session 1.6 Quiz

**1.** A version that "runs without errors" might send a generic prompt like "explain X for a Y" and print whatever comes back, producing outputs that differ mainly in length rather than substance. A well-built version uses system prompts with concrete behavioral instructions per level (specific vocabulary rules, required or forbidden analogy types, assumed background knowledge), producing genuinely differentiated explanations — not just shorter/longer versions of the same content.

**2.** B — Explaining a topic at a given audience level is a well-scoped task that doesn't require frontier-level reasoning capability; per Session 1.3's framework, paying for a larger, more expensive tier here would likely add cost and latency without meaningfully improving the actual output for this specific use case.

**3.** Most likely wrong: the system prompts aren't specific enough — they probably say something like "explain simply" without concrete instructions on vocabulary, analogy type, or assumed background. The fix is in the system prompt design (Part 2 of this chapter), not in the surrounding code — this is a prompt-engineering problem, which Week 2 formalizes further.

**4.** Apply Session 1.5's lesson: don't treat the specific year and named figure as verified just because the explanation sounds confident and fluent. Independently check those specific factual details (the date, the person's name and role) against a reliable source before relying on or repeating them — exactly the kind of specific, checkable claim that's most at risk of being a hallucination, even inside an otherwise reasonable explanation.
