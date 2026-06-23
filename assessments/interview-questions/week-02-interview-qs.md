# Week 2 Interview Questions — Prompt Engineering & Application Design

_Prompt engineering is consistently described by hiring managers as the single most "immediately testable" GenAI skill — interviewers often ask candidates to write or critique an actual prompt live, not just describe techniques abstractly. These questions reflect that pattern: expect to be asked to DO prompt engineering, not just define it._

---

## Section A — Anatomy of a Great Prompt (Session 2.1)

**1. "Here's a vague prompt: 'Write something about our product.' What's wrong with it, and how would you fix it?"**
*What a strong answer includes:* naming the missing elements specifically — no audience, no format, no length, no tone, no constraints — and then rewriting it with those elements added. Interviewers want to see the rewrite, not just the critique.

**2. "What's the difference between giving a model context and giving it constraints? Why do you need both?"**
*What a strong answer includes:* context = background information the model needs to give a relevant answer (who the audience is, what the business does); constraints = boundaries on the output itself (length, format, tone, what to avoid). Missing either one tends to produce technically-correct-but-useless output.

---

## Section B — Prompting Techniques I & II (Sessions 2.2–2.3)

**3. "Explain the difference between zero-shot, few-shot, and role prompting, with a one-line example of each."**
*What a strong answer includes:* zero-shot = no examples given, just the instruction; few-shot = 2-3 example input/output pairs included to show the pattern; role prompting = assigning the model a persona or expertise framing ("You are a senior tax accountant..."). A strong answer gives a quick example of each rather than just defining them.

**4. "When would you use few-shot prompting instead of just writing clearer instructions?"**
*What a strong answer includes:* few-shot is especially useful when the desired output format or style is hard to describe in words but easy to demonstrate — e.g., a very specific JSON structure, a particular tone, or a classification scheme with edge cases that are easier to show than explain.

**5. "What is chain-of-thought prompting, and what's a risk of relying on it too heavily?"**
*What a strong answer includes:* asking the model to reason step-by-step before giving a final answer, which often improves accuracy on multi-step problems — but the risk is that a confident, well-structured chain of reasoning can still arrive at a wrong conclusion, so the reasoning text itself isn't proof of correctness (this connects directly back to Week 1's myths).

**6. "What is self-consistency prompting, and when is it worth the extra cost?"**
*What a strong answer includes:* running the same prompt multiple times (often with some randomness) and taking the most common answer, or otherwise comparing multiple reasoning paths — worth it for high-stakes or ambiguous problems where a single pass might land on a brittle answer, but adds real latency and token cost, so it's not a default for every request.

---

## Section C — Structured Outputs (Session 2.4)

**7. "Why is getting reliable JSON output from an LLM harder than it sounds, and how do you make it more reliable?"**
*What a strong answer includes:* models can add explanatory text around the JSON, use inconsistent field names, or produce malformed syntax under certain prompts. Mitigations: explicit schema definition in the prompt, asking for JSON-only output with no preamble, using a model's structured-output/JSON mode if available, and validating/parsing defensively in code rather than trusting the output blindly.

**8. "You're building a resume parser that returns structured JSON. What happens if the LLM returns a field with the wrong data type, and how do you guard against that breaking your application?"**
*What a strong answer includes:* validating the parsed JSON against an expected schema before using it downstream (not just trying to `json.loads()` and hoping), having a defined fallback or error-handling path when validation fails, and not assuming 100% compliance even with a good prompt.

---

## Section D — Prompt Systems & Application Design (Session 2.5)

**9. "What's the difference between 'a good prompt' and 'a good prompt system,' and why does that distinction matter for a real product?"**
*What a strong answer includes:* a single good prompt solves one specific case; a prompt system involves reusable templates with variables, version control, consistent testing across many real-world inputs, and often chaining multiple prompts together — the difference between a one-off script and something you'd actually ship and maintain.

**10. "How would you organize a library of prompt templates for a team building several different AI features?"**
*What a strong answer includes:* some notion of separating prompts from application code (not hardcoding strings everywhere), naming/versioning conventions, documenting what each template expects as input variables, and ideally some lightweight testing so a prompt edit doesn't silently break a feature — this previews Week 6's prompt CI/versioning topic.

---

## Section E — Scenario-Based (Synthesizing the whole week)

**11. "A teammate writes a customer-support reply generator prompt that works great in testing but produces inconsistent tone in production. What would you investigate?"**
*What a strong answer includes:* checking whether the test examples covered a narrow range of inputs while production sees much more variety, whether the prompt gives explicit tone constraints or relies on the model "figuring it out," and whether few-shot examples could tighten consistency — diagnosing a prompt robustness gap, not just re-writing blindly.

**12. "Live exercise: Take this prompt — '[vague prompt provided by interviewer]' — and improve it out loud, explaining each change as you make it."**
*What a strong answer includes:* this is the most common live-coding-equivalent for prompt engineering roles. Narrate your reasoning as you add context, constraints, format specification, and (if relevant) examples — interviewers are evaluating your process, not just your final prompt.

---

### How to use this set

- **Practice the live-prompt-rewrite format specifically (Q12)** — this exact format shows up often in real interviews, and it's the one most people under-practice because it feels less "studyable" than definitions.
- **Pair with Week 1's questions** for a more realistic mixed-topic mock interview by Week 7.
