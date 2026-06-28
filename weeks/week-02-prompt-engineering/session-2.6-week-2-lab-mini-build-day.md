# Session 2.6 — Week 2 Lab: Mini Build Day

## Building the Customer-Support Reply Generator

**Week:** 2 — Prompt Engineering & Application Design
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes

---

## Why this chapter exists

Five sessions ago, you couldn't reliably get an LLM to do what you wanted. Now look at what's actually in your toolbox.

You learned that a prompt is made of four pillars — clarity, context, constraints, and format — and that vague prompts get vague answers because the model is filling gaps with guesses, not magic. You learned that *how* you ask matters as much as *what* you ask: zero-shot for things the model already knows how to do, few-shot when you need to pin down a specific style or edge case the model wouldn't guess on its own, and role prompting to put the model in the right "mode" before it starts generating. You learned that for anything requiring more than one logical step, asking the model to think before it answers — chain-of-thought — turns a confident wrong answer into a careful right one, and that step-back prompting and self-consistency give you ways to catch the cases where even careful thinking goes sideways. You learned that getting clean output isn't the same as getting *usable* output, and that structured outputs — JSON mode, schemas, and defensive parsing — are what separate a cool demo from something another piece of software can actually depend on. And most recently, you learned that real applications don't run one prompt — they run a *system* of prompts: templates with variables, organized into a library, versioned and tested like the rest of your codebase.

Here's the thing nobody tells you about learning this way, one technique at a time: it can start to feel like five separate party tricks. Few-shot prompting is its own little skill. JSON parsing is its own little skill. They sit in your head as five answers to five different quiz questions.

Today that ends. Today you build one real thing, and every single technique from this week earns its place in it — not because the instructions say so, but because the problem genuinely needs it.

---

## Part 1: The Problem — A Support Inbox That's Drowning

### The scenario

Picture a small software company. Twelve hundred support tickets a week, four support agents, and a backlog that never quite gets to zero. Most tickets are routine — a password reset, a billing question, a "how do I export my data" — but each one still needs a reply that's accurate, on-brand, and doesn't read like it was copy-pasted from a template that ignores what the customer actually asked.

The company doesn't want to fully automate support away. They want a tool that drafts a strong first-pass reply for every incoming ticket, in a tone that fits the situation, which a human agent can review, lightly edit, and send — instead of writing every reply from a blank page. That's the artifact you're building today: **a customer-support reply generator with tone control.**

### Why this needs every technique from the week, not just one

It would be easy to write a single, reasonably good prompt for this and call it done — and that's exactly the trap. A single ad-hoc prompt might handle one ticket well and quietly fail on the next one, with no way to tell which is which until a customer complains. Look at what the real requirements actually demand:

- **The reply needs the right tone** — an angry billing dispute and a casual feature question shouldn't get the same voice. That's few-shot and role prompting (2.2).
- **The model needs to reason about severity before it writes** — should this ticket be escalated to a human immediately, or is a standard reply fine? That's chain-of-thought (2.3).
- **The output needs to be machine-checkable**, not just a paragraph of text, because a real support tool needs to log the tone used, flag escalations, and route tickets — that's structured output with a schema (2.4).
- **The prompt itself needs to be a maintainable, documented template** — not a string improvised fresh for this exercise — because in six months someone will need to add a fourth tone option without reading through application code to find where the prompt lives. That's prompt systems (2.5).
- **And the whole thing still needs to follow the four pillars** from session 2.1, because none of the above matters if the prompt itself is vague about what "good" looks like.

This is the real lesson of a lab day: production prompting work is rarely "pick the one right technique." It's combining several techniques, each solving a different sub-problem, into one coherent system.

---

## Part 2: Designing the Output Contract First

### Why contract-first, not prompt-first

A natural instinct is to start by writing the prompt and see what comes back. For this build, it's better to start at the other end: **decide exactly what a finished reply needs to contain, as a schema, before writing a single word of the prompt.** This mirrors the discipline from Session 2.4 — the schema is the actual deliverable; the prompt is just the mechanism that produces it.

For this tool, every generated reply needs:

```json
{
  "reply_body": "string",
  "tone_applied": "empathetic | professional | concise",
  "confidence": "high | medium | low",
  "escalate": true | false,
  "escalation_reason": "string or null"
}
```

Notice what this schema is doing beyond just holding the reply text. `confidence` lets a human reviewer triage their workload — a "low confidence" reply gets a closer read before sending. `escalate` and `escalation_reason` mean the model isn't just drafting replies blindly; it's making (and explaining) a judgment call about whether this ticket actually needs a human, which is a chain-of-thought decision baked directly into the contract.

### The three tones, defined concretely

"Tone control" is a vague phrase until you pin it down with **examples**, not adjectives. Telling a model "be empathetic" is far weaker than showing it one short example of what empathetic actually sounds like in this context — which is exactly the lesson from few-shot prompting in Session 2.2. For this build, three tones are defined:

- **Empathetic** — for frustrated, upset, or anxious customers. Leads with acknowledgment before any explanation or solution.
- **Professional** — the default for routine, neutral requests. Clear, polite, efficient, no unnecessary warmth or formality.
- **Concise** — for customers who clearly want a fast, no-fluff answer (short tickets, direct questions). Shortest replies of the three, with no preamble.

---

## Part 3: Building the Prompt as a Documented Template

### Following the 2.5 convention

Per Session 2.5's lesson, this prompt doesn't live as a one-off string improvised inline — it's built as a named, documented template with placeholders, stored separately from the calling code:

```python
SUPPORT_REPLY_TEMPLATE = """You are a customer support assistant for a
software company. Read the ticket below, decide on the right tone, reason
through whether this needs human escalation, then draft a reply.

Tone examples:
{tone_examples}

Before answering, think step by step about: (1) what the customer is
actually asking, (2) how urgent or sensitive this is, (3) whether a
standard reply is sufficient or this needs escalation. Do this reasoning
internally — do not include it in your final output.

Respond with ONLY valid JSON matching this schema:
{schema}

Ticket:
{ticket_text}
"""
```

`{tone_examples}` carries the few-shot anchors (2.2). The "think step by step... do this internally" instruction is chain-of-thought (2.3), deliberately kept out of the visible output — the model still reasons, but the reply stays clean for the schema. `{schema}` is the structured-output contract from Part 2 (2.4). And the whole thing is a named, reusable `SUPPORT_REPLY_TEMPLATE`, not a string buried inside a function (2.5).

### Why the reasoning has to stay invisible to the customer

A subtlety worth naming explicitly: chain-of-thought reasoning is genuinely useful for getting a better-quality decision out of the model, but a customer should never see "Let me think about whether this needs escalation..." in their actual support reply. The instruction to reason "internally" and exclude it from the final output is what keeps the *benefit* of chain-of-thought (a more careful decision) without its *cost* (a confusing, unprofessional-looking reply). This is a detail easy to miss if you've only practiced chain-of-thought in isolation, where the visible reasoning was the point.

---

## Part 4: Defensive Parsing, Again — Because It's Never One-and-Done

### The lesson that doesn't go away

Session 2.4 introduced defensive parsing: never trust that the model's JSON is well-formed, never trust that an enum field actually contains one of the allowed values, always validate before your application logic touches the data. It would be tempting to think of that as "the 2.4 lesson," already learned, checked off. It isn't. Every session from here forward that touches model output needs this same discipline, because the underlying risk — a model that's *usually* well-behaved but not *guaranteed* to be — never goes away.

For this build, `parse_reply()` needs to handle, at minimum: JSON that fails to parse at all (the model added a sentence of preamble before the `{`), a `tone_applied` value that isn't one of the three defined tones, and an `escalate: true` response with a missing or empty `escalation_reason` — which is a logically inconsistent output the schema doesn't prevent on its own, but your validation code should catch.

### Why this matters more here, not less

In earlier single-technique exercises, a malformed response was an inconvenience you'd notice immediately while testing. In a tool meant to run continuously over a live ticket queue, an unhandled malformed response is the difference between "the system flags one ticket for manual review" and "the system silently sends a customer a JSON parsing error instead of a reply." The stakes of defensive parsing scale with how close a tool is to something real — and this lab is deliberately the closest thing to "real" you've built so far.

---

## Points to Remember

- **A lab/build day isn't about learning something new — it's about discovering that the week's separate techniques were never actually separate.** A real prompting problem usually needs several techniques combined, each solving a distinct sub-problem.
- **Design the output contract (schema) before writing the prompt.** The schema is the actual deliverable; the prompt is the mechanism that produces it.
- **Tone control is concrete only when backed by few-shot examples**, not adjectives alone — "be empathetic" is far weaker than showing what empathetic sounds like.
- **Chain-of-thought reasoning should often stay invisible to the end user** — instruct the model to reason internally and exclude that reasoning from the final output, especially in customer-facing tools.
- **Defensive parsing is not a one-time lesson from Session 2.4** — every exercise that touches model output needs it, and the stakes increase as a tool gets closer to running on real, continuous data.
- **Prompts belong in named, documented templates**, not inline strings, from the very first version of a tool — not retrofitted later once it's "important enough."

---

## Quick Check: Fill in the Blanks

1. Before writing the prompt for this build, you should first design the __________ — exactly what fields a finished reply needs to contain.
2. Tone control becomes concrete when backed by __________ examples, rather than relying on adjectives alone.
3. Chain-of-thought reasoning in a customer-facing tool should generally stay __________ to the end user, even though the model still benefits from doing it.
4. An `escalate: true` response with a missing `escalation_reason` is an example of a __________ inconsistent output that schema validation alone won't catch.
5. The stakes of defensive parsing __________ as a tool moves from a single test run to something running continuously over real data.

**Answers:** 1. output contract / schema — 2. few-shot — 3. invisible / hidden — 4. logically — 5. increase / scale up

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-02/session-2.6-quiz.md`](../../assessments/quizzes/week-02/session-2.6-quiz.md) · Answer key: [`assessments/answer-keys/week-02/session-2.6-quiz-answers.md`](../../assessments/answer-keys/week-02/session-2.6-quiz-answers.md)

Interview-style questions for this topic:

1. *"You're asked to build a tool that drafts customer support replies. Walk me through how you'd combine prompting techniques to handle tone, reasoning, and reliable output all at once."*
2. *"Why might you want a model to reason step-by-step internally but hide that reasoning from the final user-facing output?"*
3. *"What's a logically inconsistent output that a JSON schema alone wouldn't catch, and how would you validate against it?"*
4. *"How would you decide which support tickets a tool like this should auto-escalate to a human, versus reply to automatically?"*

---

## Core path — guided activity

**Customer-Support Reply Generator with Tone Control.** You'll build `generate_reply()`, wiring together a documented prompt template (`build_prompt()`), the schema-validated call to the model, and defensive parsing (`parse_reply()`) that catches malformed JSON, invalid tone values, and the escalate/escalation_reason inconsistency. Full instructions: [`codebase/exercises/week-02/session-2.6/`](../../codebase/exercises/week-02/session-2.6/).

## Pro path — extended challenge

Extend the generator to log every generated reply (ticket, tone applied, confidence, escalation decision) to a simple structured log, then write a small script that reports the escalation rate and tone distribution across a batch of tickets — a first, lightweight taste of the monitoring and observability work formalized in Week 6.

## What's next

Week 2 is complete. Next: **Week 3 — Working with Data: Embeddings & RAG**, starting with Session 3.1, **Why LLMs Need External Knowledge** — knowledge cutoffs, hallucination on facts, and when retrieval-augmented generation is (and isn't) the right tool.
