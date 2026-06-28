# Week 2 Written Exam

_Deeper, scenario-based exam covering all of Week 2's sessions (2.1–2.6): prompt anatomy, few-shot/zero-shot/role prompting, chain-of-thought and self-consistency, structured outputs, prompt systems, and applied integration._

**Format:** 8 short-answer questions + 4 scenario-analysis questions
**Suggested time:** 45–60 minutes
**Open book:** Yes — this tests understanding and application, not memorization

---

## Section A — Short Answer

**A1.** A prompt that gets inconsistent results across runs is often missing one of the four core ingredients from "Anatomy of a Great Prompt." Name the four ingredients (clarity, context, constraints, format specification) and, for each one, give a one-sentence example of what's missing when a prompt fails because of it.

**A2.** What is the difference between zero-shot and few-shot prompting? Describe one situation where adding examples (few-shot) would clearly improve output quality over a zero-shot prompt, and one situation where zero-shot is good enough and few-shot would just waste tokens.

**A3.** "Role prompting" means assigning the model a persona or expertise framing (e.g., "You are a senior tax accountant"). Explain *why* this technique tends to improve output quality — what is it actually doing to the model's behavior — and name one risk of relying on role prompting too heavily.

**A4.** Chain-of-thought (CoT) prompting asks a model to reason step-by-step before answering. Give an example of a task where CoT meaningfully improves accuracy, and an example of a task where CoT adds little value or actively hurts (e.g., latency, cost, or overthinking a simple lookup).

**A5.** What is "step-back prompting," and how is it different from chain-of-thought? Use a concrete example (not from the lesson) to illustrate.

**A6.** Self-consistency prompting involves generating multiple reasoning paths and selecting the most common answer. Explain why this can catch errors that a single chain-of-thought pass would miss, and identify the main cost trade-off of using it.

**A7.** When asking a model to "return JSON," outputs can still fail to parse reliably. Name two concrete techniques covered in Session 2.4 for improving structured-output reliability, and explain what failure mode each one is designed to prevent.

**A8.** What is a "prompt template," and what's the practical benefit of using variables/placeholders in a template instead of writing a fresh prompt every time? Give one example of a variable you'd parameterize in a prompt template for a real business task.

---

## Section B — Scenario Analysis

**B1. The inconsistent classifier**
A teammate built a prompt that classifies incoming support tickets into "Billing," "Technical," or "Other." It works well on simple tickets but misclassifies anything with mixed signals (e.g., a billing question that also mentions a bug). The teammate's prompt is:

> "Classify this ticket: {ticket_text}"

Diagnose what's missing using concepts from Sessions 2.1 and 2.2, and rewrite the prompt to fix it. Your answer should address: (a) what's structurally weak about the original prompt, (b) whether and how few-shot examples would help here, and (c) how you'd constrain the output format so it's safe to parse downstream.

**B2. The resume parser that "mostly" works**
You're building a resume parser that extracts name, years of experience, and top 3 skills as JSON, to feed into an applicant-tracking system. In testing, the model returns valid JSON about 90% of the time, but occasionally:
- wraps the JSON in a sentence ("Here is the extracted data: {...}")
- invents a "skills" field with 5 items instead of 3
- returns years of experience as a string ("5 years") instead of a number

Using ideas from Session 2.4 (Structured Outputs), explain three specific changes you'd make to the prompt/system design to drive that 90% toward something closer to 100%, and explain why each change addresses one of the three failure modes above.

**B3. The reasoning task that needs a second opinion**
Your company wants an LLM to help triage which support tickets are likely to churn-risk customers, based on tone and account history described in free text. This is a judgment call, not a lookup — different reasonable people might disagree on borderline cases. A junior team member proposes a single chain-of-thought prompt and calling it done.

Using Sessions 2.3 and 2.5, argue for or against augmenting this with self-consistency, and explain how you'd turn this into a reusable *prompt system* (not just a one-off prompt) — covering at minimum: what would be templated/parameterized, and whether/how you'd chain multiple prompt steps.

**B4. The tone-control build (ties to the Week 2 Lab)**
You're extending the customer-support reply generator from the Week 2 Lab (Session 2.6) to support three tone settings — "empathetic," "formal," and "concise" — selectable per-customer. A teammate suggests just writing three completely separate prompts, one hardcoded for each tone.
Explain why a templated prompt-system approach (Session 2.5) is preferable here, what you would parameterize besides tone, and how you'd handle a customer message that requires a structured output (e.g., a JSON object with `reply_text` and `escalate: true/false`) on top of the tone control. Your answer should integrate at least three distinct concepts from across Week 2 (not just Session 2.5).

---

## Answer Key

### Section A

**A1.** The four ingredients: **clarity** (an unambiguous task description — missing clarity looks like a vague verb, e.g. "improve this text" without saying improve *how*), **context** (background the model needs to make a good judgment — missing context looks like asking for a "professional" tone without saying for what audience or purpose), **constraints** (explicit boundaries — missing constraints looks like no length, scope, or content limits, so output length/style varies wildly run to run), **format specification** (the exact shape of the expected output — missing format looks like asking for "a list" without specifying numbered, bulleted, JSON, etc., so downstream parsing breaks). Inconsistent results across runs are a classic symptom of missing constraints and/or format specification, since the model is free to choose structure each time.

**A2.** Zero-shot gives the model only an instruction; few-shot gives the model the instruction plus example input/output pairs. Few-shot helps when the *desired output style or labeling convention is idiosyncratic or non-obvious* — e.g., classifying tickets into custom categories the model hasn't seen defined anywhere, or matching a specific tone/format unique to your brand. Zero-shot is sufficient for *well-known, general tasks* the model has strong priors on — e.g., summarizing a paragraph or translating a sentence — where examples add tokens/cost without changing behavior.

**A3.** Role prompting works by conditioning the model's implicit "persona" — it shifts the distribution of likely outputs toward the vocabulary, assumptions, and conventions associated with that role in the model's training data (a "senior tax accountant" persona nudges toward precise, hedge-appropriate, jargon-correct language). The risk: a role label is not a substitute for actual domain constraints or verification — the model can produce confident-sounding output "in character" that is still wrong, and over-reliance on persona framing can mask the need for real fact-checking or guardrails (especially in regulated domains like tax, legal, or medical).

**A4.** CoT helps on tasks with **multiple dependent reasoning steps** — e.g., a multi-step word problem, or a business decision that requires weighing several factors before concluding. CoT adds little value (or hurts) on **simple lookups or single-step tasks** — e.g., "what is the capital of France?" — where forcing step-by-step reasoning only adds latency and token cost without changing the (already-correct) answer, and can occasionally cause the model to "talk itself into" an unnecessary tangent.

**A5.** Step-back prompting asks the model to first articulate the *general principle or higher-level question* behind a specific problem before solving the specific instance, whereas CoT reasons forward through the specific steps of the problem itself. Example: instead of immediately answering "Why did my Q3 marketing campaign underperform?", a step-back prompt would first ask the model to consider "What are the general factors that cause marketing campaigns to underperform?" and only then apply that general framework to the specific Q3 case — this tends to surface considerations a direct forward-chained answer might skip.

**A6.** A single CoT pass can land on a plausible-looking but wrong reasoning chain, especially on ambiguous or multi-path problems — there's no internal check. Self-consistency runs the same prompt multiple times (often with some sampling randomness), and if the majority of independent reasoning paths converge on the same answer, that answer is more likely correct, while a single bad chain becomes a visible outlier rather than the only answer. The main trade-off is **cost and latency** — running N completions instead of 1 multiplies token spend and response time, so it's reserved for cases where correctness matters more than speed/cost.

**A7.** Two concrete techniques: (1) **explicit schema specification** — providing the exact JSON keys, types, and structure expected (or using a JSON-mode/schema-constrained API feature) prevents the "almost-right-shape" failure mode where the model invents extra fields or wrong types. (2) **instructing "JSON only, no surrounding text"** (and/or stripping/validating output programmatically) prevents the failure mode where the model wraps valid JSON in conversational preamble ("Here's the data: {...}"), which breaks naive `json.loads()` parsing.

**A8.** A prompt template is a reusable prompt skeleton with placeholders (variables) for the parts that change between uses, while the surrounding instruction/structure stays fixed. The practical benefit is **consistency and maintainability** — you write and refine the prompt logic once, then swap in different inputs without re-deriving the wording each time, which also makes it easy to update the prompt in one place and have every use case benefit. Example variable: `{customer_tier}` in a support-reply template, so the same template produces appropriately different tone/detail for a free-tier vs. enterprise customer.

### Section B

**B1.** The original prompt is structurally weak because it has **no context** (no definition of what distinguishes the three categories), **no constraints** (nothing stopping the model from picking a category based on whichever keyword appears first), and **no format specification** (the model could return "Billing", "billing ticket", "This is billing", etc. — all different strings to a downstream parser). Few-shot examples would help significantly here because the categories are business-specific and the boundary cases (mixed-signal tickets) are exactly what examples are good at disambiguating — 3–5 examples showing how a mixed billing+bug ticket should be classified (e.g., by primary intent) would anchor the model's judgment. Output format should be constrained to one of exactly three fixed string values (or an enum/JSON field), with an explicit instruction like "respond with exactly one of: BILLING, TECHNICAL, OTHER — no other text," making downstream parsing safe.

**B2.** Three changes: (1) **Add an explicit schema** (key names, types, and exact array length — "skills must be an array of exactly 3 strings") so the model has no ambiguity about shape, directly preventing the "5 items instead of 3" failure. (2) **Instruct (and/or enforce via API JSON mode) that the response must be JSON only, with no surrounding text** — this directly prevents the "wrapped in a sentence" failure, since the instruction removes the model's default conversational instinct to introduce its answer. (3) **Specify types explicitly per field, e.g. "years_of_experience must be a JSON number, not a string"** — this directly targets the type-coercion failure ("5 years" vs. `5`), since without an explicit type constraint the model defaults to whatever's most natural in prose. A strong answer may also mention validating/coercing output programmatically as a safety net regardless of prompt quality.

**B3.** This is a good candidate for self-consistency (Session 2.3) *because* the task is explicitly judgment-based with reasonable disagreement on borderline cases — exactly the situation where a single CoT pass risks landing on one plausible-but-not-most-defensible answer, and where majority-vote across multiple reasoning paths adds real signal rather than just cost. The trade-off to flag: self-consistency multiplies cost/latency, so it should likely be applied selectively (e.g., only on cases near a decision threshold, not on every ticket). To turn this into a prompt *system* rather than a one-off prompt (Session 2.5): template the account-history and ticket-text as variables, parameterize things like risk-threshold or tone of explanation, and chain steps — e.g., a first prompt step extracts structured signals (sentiment, mentioned issues, tenure) and a second prompt step reasons over those structured signals to produce a churn-risk judgment, rather than asking one prompt to do extraction and judgment simultaneously. A strong answer notes that chaining also makes each step independently testable/evaluable.

**B4.** A templated approach is preferable because hardcoding three separate prompts means **the underlying logic (what the reply must cover, escalation rules, structured-output requirements) has to be duplicated and kept in sync three times** — any future fix or business-rule change requires editing three places instead of one, which is exactly the maintainability problem prompt systems are designed to solve (Session 2.5). Beyond tone, you'd likely also parameterize: customer name/context, the original message, and any relevant account/order details. To layer structured output (Session 2.4) on top of tone control, the template's *fixed* instruction block should specify the output schema (`{"reply_text": string, "escalate": boolean}`) and format constraints ("JSON only"), while only the `{tone}` variable and tone-specific guidance change between calls — this way structured-output reliability isn't re-solved per tone, it's solved once in the shared template. A strong answer explicitly names at least three Week 2 concepts in combination: prompt templating/variables (2.5), structured output schema constraints (2.4), and either role/instruction framing for tone (2.1/2.2) or chaining if escalation logic is treated as a separate reasoning step.

---

## Grading Guidance

- **Section A (8 × 2.5 pts = 20 pts):** Award full credit for answers that correctly name the concept *and* give a relevant example/justification. Half credit for correct concept with a weak or missing example.
- **Section B (4 × 7.5 pts = 30 pts):** These should be graded holistically against the answer key's *reasoning*, not matched word-for-word. Award credit for: correctly diagnosing the underlying issue, proposing a fix grounded in the right Week 2 concept(s), and (for B3/B4) successfully integrating multiple concepts rather than just one.
- **Total: 50 pts.** Suggested cutoffs: 45+ = excellent, 35–44 = solid, 25–34 = needs review of specific sessions (see which question clusters were missed), <25 = recommend revisiting Week 2 sessions before Week 3.
