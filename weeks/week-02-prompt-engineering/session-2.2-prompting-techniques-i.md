# Session 2.2: Prompting Techniques I

**Week:** 2 — Prompt Engineering & Application Design
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes

---

## Why this chapter exists

Session 2.1 gave you a framework — clarity, context, constraints, format — for diagnosing what's *missing* from a weak prompt. This chapter gives you something different: three specific, named *techniques* for actually shaping how a model approaches a task, each suited to different situations. These aren't competing approaches where you pick a favorite; they're tools in a kit, and knowing which one fits which job is the actual skill.

These three techniques — zero-shot, few-shot, and role prompting — are also, not coincidentally, the three terms you'll hear most often in any real conversation about prompting, in interviews, in documentation, in casual conversation among practitioners. Today you'll understand exactly what each one means, when to reach for it, and what it actually changes about the model's output.

---

## Part 1: Zero-Shot Prompting — Just the Instruction

### What it is

Zero-shot prompting means giving the model an instruction with **no examples** of what the output should look like — just the task itself, relying on the model's general training to produce something reasonable. Almost everything you've written so far in this program, including the worked rewrite from Session 2.1, has been zero-shot.

**Example:** "Classify this customer review as positive, negative, or neutral: 'The shipping took forever but the product itself works great.'"

You haven't shown the model a single example of what a "positive" or "negative" classification looks like — you're trusting that the model's training already encodes a strong enough understanding of these everyday categories to apply them correctly. For well-known, common-sense tasks like this one, zero-shot is usually perfectly sufficient, and it's the right default to reach for first.

### When zero-shot is the right choice

Zero-shot works well when the task is conceptually clear from the instruction alone, the categories or format you want are common and unambiguous, and there isn't a subtle, hard-to-describe pattern you need the model to pick up on. Most everyday tasks — summarization, straightforward classification, translation, simple drafting — work fine zero-shot, especially once you've applied Session 2.1's four pillars properly.

### When zero-shot starts to struggle

Zero-shot tends to break down when the task has a specific, non-obvious format you need followed exactly, when the categories or rules are unusual or company-specific (not something the model would have a strong default sense of), or when you need consistent edge-case handling that's hard to describe in words but easy to demonstrate. This is exactly the gap few-shot prompting fills.

---

## Part 2: Few-Shot Prompting — Show, Don't Just Tell

### What it is

Few-shot prompting means including a small number of example input/output pairs *within the prompt itself*, demonstrating the exact pattern you want the model to follow, before giving it the real input to handle. The model isn't being "trained" in any permanent sense — these examples live only in this one request's context window (recall Session 1.2) — but they powerfully steer what a good response looks like for *this specific call*.

### A worked example

Suppose you're classifying support tickets into categories specific to your company — categories a general model wouldn't have any standard sense of. Zero-shot might fail here, because "Tier 2 Escalation" or "Billing Dispute - Resolved" aren't universal concepts the model already understands consistently.

**Few-shot version:**

```
Classify the following support ticket into one of: Billing, Technical, Account Access, Other.

Ticket: "I was charged twice for my subscription this month."
Category: Billing

Ticket: "The app crashes every time I try to upload a photo."
Category: Technical

Ticket: "I can't log in, it says my password is wrong even after I reset it."
Category: Account Access

Ticket: "Can you tell me when paddle boarding season starts?"
Category: Other

Ticket: "My invoice shows a fee I don't recognize from last week."
Category:
```

Notice what those four examples accomplish: they don't just state the categories (a zero-shot prompt could do that too) — they demonstrate the *boundary cases*. The model can now infer that "billing" means money/charges-related, "technical" means app malfunction, "account access" means login/credential issues, and crucially, that genuinely unrelated questions get "Other" rather than being forced into one of the real categories. That last example is doing real work — it's teaching the model what *doesn't* belong, which is often harder to convey through instruction alone.

### Why few-shot works: connecting back to Session 1.2

Recall that an LLM predicts the next token based on patterns in everything currently in its context window. Few-shot examples are a direct, powerful way to shape that context — instead of describing a pattern abstractly, you're handing the model several worked instances of the pattern, and it continues that pattern, the same fundamental mechanism from Session 1.1 and 1.2, just deliberately engineered.

### How many examples is "few"

Typically 2–5 examples is enough to establish a clear pattern; more isn't automatically better; past a certain point you're consuming context window space (Session 1.2's "lost in the middle" risk applies here too) without meaningfully improving pattern recognition. Choose examples that cover the real range of cases you expect, including at least one boundary or edge case if one exists — examples that are too similar to each other don't teach the model much beyond the first one.

---

## Part 3: Role Prompting — Assigning a Persona or Expertise Frame

### What it is

Role prompting means instructing the model to adopt a specific persona, professional identity, or expertise frame — "You are a senior tax accountant," "You are a patient, encouraging math tutor," "You are a skeptical code reviewer looking for security vulnerabilities." This shapes the *style*, *vocabulary*, *priorities*, and sometimes the *focus* of the response, without necessarily changing the underlying task instruction.

### Why this works, mechanically

A role assignment shifts what's most statistically plausible to generate next, because "tax accountant" language patterns and "math tutor" language patterns look meaningfully different in the training data the model learned from. Assigning a role is, in effect, telling the model which region of its learned patterns to draw from — similar in spirit to how Session 1.4's system prompt let you set persistent behavioral instructions, but specifically focused on *identity and expertise framing* rather than task mechanics.

### A concrete before/after

**Without role prompting:** "Review this code for issues." → A generic, broad review touching on style, naming, maybe a few bugs.

**With role prompting:** "You are a security-focused code reviewer. Review this code specifically for injection vulnerabilities, unsafe input handling, and authentication weaknesses. Ignore style issues entirely." → A narrower, more specialized review, because the role plus explicit scope steers attention toward a specific lens rather than a generic pass.

### The honest limit of role prompting

Role prompting shapes *style and focus* — it does not grant the model genuinely new capabilities it didn't already have. Telling a model "you are a board-certified cardiologist" doesn't give it medical knowledge it lacked before; it shifts *how* it presents and frames whatever it already knows, drawing on patterns associated with that kind of expert voice in its training data. This distinction matters enormously for anything high-stakes: role prompting is a genuinely useful tool for tone, focus, and framing, but it is not a substitute for actual verification, actual domain expertise, or — circling back to Session 1.5 — actual grounding in verified facts. Don't mistake a confident expert *voice* for verified expert *accuracy*.

---

## Part 4: Combining the Techniques

These three techniques aren't mutually exclusive — real prompts often combine them. A role-prompted, few-shot classification task is entirely reasonable:

```
You are a meticulous content moderator for a children's education platform.

Classify each comment as Approve or Flag for review.

Comment: "This video really helped me understand fractions!"
Classification: Approve

Comment: "lol this is so easy a baby could do it, what a waste of time"
Classification: Flag

Comment: "Can someone explain the third example again?"
Classification:
```

Here, the role ("meticulous content moderator for a children's platform") sets the lens and sensitivity level, while the few-shot examples demonstrate exactly where the line falls between borderline-rude-but-fine and actually-flag-worthy. Neither technique alone would do as much work as the combination.

---

## Points to Remember

- **Zero-shot**: instruction only, no examples. The right default for clear, common-sense tasks.
- **Few-shot**: 2–5 example input/output pairs included in the prompt, demonstrating the exact pattern — especially powerful for company-specific categories, unusual formats, or conveying boundary cases that are hard to describe in words.
- **Role prompting**: assigning a persona or expertise frame, which shifts style, vocabulary, and focus — but does NOT grant new capabilities the model didn't already have. A confident expert voice is not the same as verified expert accuracy.
- **These techniques combine.** A role-prompted few-shot prompt is often stronger than either technique used alone.
- **More few-shot examples isn't automatically better** — 2–5 well-chosen examples, including boundary cases, typically outperforms a longer list of similar ones.

---

## Quick Check: Fill in the Blanks

1. Zero-shot prompting gives the model an instruction with __________ examples.
2. Few-shot examples are especially useful for conveying __________ cases that are hard to describe in words but easy to demonstrate.
3. Few-shot examples work by shaping what's in the model's __________, the same mechanism from Session 1.2.
4. Role prompting shifts __________ and __________, but does not grant the model new __________ it didn't already have.
5. A reasonable number of few-shot examples is typically __________, including at least one __________ case if one exists.

**Answers:** 1. no (or zero) — 2. boundary (or edge) — 3. context window — 4. style, focus, capabilities — 5. 2–5, boundary/edge

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-02/session-2.2-quiz.md`](../../assessments/quizzes/week-02/session-2.2-quiz.md) · Answer key: [`assessments/answer-keys/week-02/session-2.2-quiz-answers.md`](../../assessments/answer-keys/week-02/session-2.2-quiz-answers.md)

Interview-style questions for this topic:

1. *"Explain the difference between zero-shot, few-shot, and role prompting, with a one-line example of each."*
2. *"When would you use few-shot prompting instead of just writing clearer instructions?"*
3. *"Does role prompting actually give a model new expertise? Explain what it does and doesn't change."*
4. *"How would you design few-shot examples for a classification task with a tricky 'none of the above' category?"*

---

## Core path — guided activity

**Few-Shot Classifier Prompt.** You'll build a working few-shot prompt for a classification task of your choosing (or use the support-ticket example), including at least one boundary case, and test it against several new inputs to see whether the pattern actually holds. Full instructions: [`codebase/exercises/week-02/session-2.2/`](../../codebase/exercises/week-02/session-2.2/).

## Pro path — extended challenge

You'll be given a zero-shot prompt that fails inconsistently on a company-specific classification task. You'll diagnose why (the categories are too specific/unusual for zero-shot to handle reliably), convert it to a few-shot prompt with well-chosen boundary-case examples, and verify the failure mode is actually fixed — not just hidden by easier test cases.

## What's next

Session 2.3 — **Prompting Techniques II** — continues with chain-of-thought, step-back prompting, and self-consistency: techniques for improving reasoning on multi-step problems.
