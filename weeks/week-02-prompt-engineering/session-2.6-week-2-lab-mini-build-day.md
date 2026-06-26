# Session 2.6 — Week 2 Lab: Mini Build Day

## Building the Customer-Support Reply Generator

---

### Where you've been

Five sessions ago, you couldn't reliably get an LLM to do what you wanted. Now look at what's actually in your toolbox.

You learned that a prompt is made of four pillars — clarity, context, constraints, and format — and that vague prompts get vague answers because the model is filling gaps with guesses, not magic. You learned that *how* you ask matters as much as *what* you ask: zero-shot for things the model already knows how to do, few-shot when you need to pin down a specific style or edge case the model wouldn't guess on its own, and role prompting to put the model in the right "mode" before it starts generating. You learned that for anything requiring more than one logical step, asking the model to think before it answers — chain-of-thought — turns a confident wrong answer into a careful right one, and that step-back prompting and self-consistency give you ways to catch the cases where even careful thinking goes sideways. You learned that getting clean output isn't the same as getting *usable* output, and that structured outputs — JSON mode, schemas, and defensive parsing — are what separate a cool demo from something another piece of software can actually depend on. And most recently, you learned that real applications don't run one prompt — they run a *system* of prompts: templates with variables, organized into a library, versioned and tested like the rest of your codebase.

Here's the thing nobody tells you about learning this way, one technique at a time: it can start to feel like five separate party tricks. Few-shot prompting is its own little skill. JSON parsing is its own little skill. They sit in your head as five answers to five different quiz questions.

Today that ends. Today you build one real thing, and every single technique from this week earns its place in it — not because the instructions say so, but because the problem genuinely needs it.

---

### The problem: a support inbox that's drowning

Picture a small software company. Twelve hundred support tickets a week, four support agents, and a backlog that never quite gets to zero. The tickets aren't exotic — "my export isn't working," "how do I change my billing plan," "this is the third time I've reported this bug and I'm furious" — but each reply has to be *written*, and writing takes time the team doesn't have.

The naive fix is "just have an LLM write the replies." And if you tried that with a single bare prompt — `"Reply to this support ticket: {ticket}"` — you'd get something that mostly works and occasionally embarrasses the company. A frustrated customer gets a chirpy reply that sounds like it didn't read the complaint. A billing question gets answered with made-up policy details. A bug report gets a reply that doesn't actually acknowledge what's broken. None of these are exotic LLM failures — they're exactly the failure modes you've spent five sessions learning to prevent.

So the real spec for this build is more interesting than "write a reply." It's:

> Given a support ticket and a target tone, generate a reply that addresses the customer's actual issue, matches the requested tone *consistently*, and returns in a structured format the support team's ticketing software can actually consume — with no invented policy details.

Read that spec again and notice how it maps onto the week:

- **"addresses the customer's actual issue"** → this needs context and constraints (2.1), and for anything beyond a one-line question, a bit of reasoning before writing (2.3).
- **"matches the requested tone *consistently*"** → tone is exactly the kind of thing models drift on without anchoring — this is what few-shot examples and role prompting are for (2.2).
- **"structured format the ticketing software can consume"** → this is session 2.4, full stop. JSON mode, a schema, defensive parsing.
- **"no invented policy details"** → a constraint you enforce *in the prompt*, and a thing your eval/spot-checks need to watch for.
- **"given a support ticket and a target tone"** → this is a template with variables, not a one-off prompt — which means it belongs in your prompt library, versioned, with documented inputs (2.5).

You're not learning a sixth technique today. You're learning how the five you have compose into a system bigger than any one of them.

---

### Step 1 — Design before you prompt

The instinct when you're excited to build is to open the editor and start writing prompt strings immediately. Resist it for five minutes. Production prompt systems are designed the same way production code is: decide the interface first.

What goes **in**? A ticket has a subject, a body, and (for this build) a customer-supplied tone preference — say, one of `"empathetic"`, `"professional"`, or `"concise"`. What comes **out**? Not free text — a JSON object the ticketing system can route, log, and display: a `reply_body`, the `tone_applied`, a `confidence` flag for whether the model thinks it actually has enough information to resolve the issue, and an `escalate` boolean for tickets that need a human.

Notice that last field. A genuinely well-designed support-reply system doesn't try to answer everything — it knows when *not* to answer. That's not a stretch goal bolted onto this exercise for the sake of difficulty. It's what separates a toy generator from one a real support team would actually trust enough to use. You'll see this exact theme again in Week 5 when we cover evaluation and guardrails: a system that knows its own limits is safer than one that always sounds confident.

This is the schema you're designing toward:

```json
{
  "reply_body": "string",
  "tone_applied": "empathetic | professional | concise",
  "confidence": "high | medium | low",
  "escalate": true | false,
  "escalation_reason": "string or null"
}
```

Design the contract first. The prompt exists to satisfy the contract — not the other way around.

---

### Step 2 — Build the template, not the instance

If you were solving one ticket, you'd write one prompt. You're solving a *category* of tickets, so you write a template — the session 2.5 move. Two variables drive everything: the ticket content and the tone setting. Everything else in the prompt is fixed scaffolding that should behave the same way every time it runs.

A first-draft template skeleton looks like this:

```
You are a customer support reply assistant for a software company.

A customer has submitted the following support ticket:

Subject: {ticket_subject}
Body: {ticket_body}

Write a reply in a {tone} tone, where:
- "empathetic" means lead with acknowledging the customer's frustration or situation before addressing the issue
- "professional" means clear, courteous, and businesslike, with no casual language
- "concise" means the shortest reply that fully resolves the issue, no pleasantries

Rules:
- Only state policy or product details you can see directly in the ticket. Never invent specific policies, refund amounts, or timelines.
- If the ticket doesn't contain enough information to resolve the issue, do not guess — set escalate to true and explain why in escalation_reason.

Return your answer as JSON matching exactly this schema:
{schema}
```

Stop and notice what's already in there from earlier sessions even before you've run it once: explicit format specification and constraints (2.1), a hard rule against fabricating policy details — directly addressing the hallucination risk from Week 1 that this whole program keeps spiraling back to — and a JSON schema contract (2.4) with an explicit "don't guess, escalate instead" instruction.

What's *missing* is tone consistency. Notice the prompt currently just *describes* each tone in one clause and trusts the model to nail it. Try this in isolation and you'll likely get tone drift: "empathetic" tickets that are warm on easy issues and oddly flat on hard ones, or "concise" replies that creep back toward chatty once the issue gets complicated. Description alone under-constrains style — this is precisely the gap few-shot examples exist to close.

---

### Step 3 — Pin down tone with few-shot examples

Pick one short example reply for each tone — written once, by you, as the gold standard — and fold them into the template as few-shot demonstrations rather than just adjective descriptions:

```
Here is an example of the "empathetic" tone for a different ticket:

Ticket: "I've been charged twice this month and no one has responded to my last two emails."
Reply: "I completely understand the frustration here — being charged twice and then not hearing back only makes it worse. I've looked into your account and I can see the duplicate charge. I'm flagging this for an immediate refund and will personally confirm once it's processed within 24 hours."

[similarly for "professional" and "concise"]
```

This is role prompting and few-shot prompting working together, not separately: the system message establishes *who* the model is being asked to be, and the worked examples establish *what that identity sounds like on the page*. One sets the frame; the other anchors the execution inside it. That pairing is worth remembering — in production prompt systems, role and few-shot are almost always used together rather than as alternatives.

---

### Step 4 — Add reasoning for the cases that need it

For a simple ticket — "how do I export my data as CSV" — the model doesn't need to deliberate. It knows the answer or it doesn't. But for a ticket like "your app deleted three days of my work and I want to know why before I decide whether to cancel," jumping straight to a reply risks missing something: Is this actually a known bug? Does the situation genuinely warrant escalation? Is there a risk of promising something the company can't actually deliver?

This is where session 2.3's chain-of-thought earns its place — but notice the discipline it requires. You don't want the model's reasoning showing up in the customer-facing reply. So you ask it to reason *internally*, as a step before producing the final structured answer, and your schema only surfaces the *output* of that reasoning — the `escalate` flag and `confidence` rating — not the reasoning text itself.

```
Before writing the reply, privately reason through:
1. What specifically is the customer asking for or upset about?
2. Do I have enough information in the ticket to resolve this, or am I missing something I'd have to guess?
3. Does this involve money, data loss, or a repeated complaint? If so, lean toward escalation.

Then write only the final JSON object — do not include your reasoning in the output.
```

This is a subtle but important pattern: chain-of-thought doesn't always mean "show your work to the user." Often it means "think carefully, then show the user only the conclusion." The reasoning step improves the *quality* of the escalate/confidence decision without leaking scratch-work into a customer's inbox.

---

### Step 5 — Parse defensively, exactly like 2.4 taught you

You already know not to trust that the model's output is clean JSON on the first try, every try. The same defensive parsing logic from the resume-parser exercise applies here without modification: strip wrapper text if the model adds any despite instructions, attempt to parse, validate the result against your schema (right field names, right types, `tone_applied` is actually one of your three allowed values, `confidence` is one of your three allowed values), and have a defined fallback — flagging the ticket for manual handling — rather than letting malformed output silently break the pipeline.

This is the unglamorous 20% of the build that makes the other 80% trustworthy. A prompt that works on your ten test tickets but has no parsing safety net is a demo. The same prompt with validation and a fallback path is a system you could actually hand to a real support team.

---

### Step 6 — This is a template library entry, not a one-off

Once it works, don't leave it as a loose script. Following the convention from 2.5, this prompt belongs in your template library with:

- a name (`support_reply_v1`)
- documented input variables (`ticket_subject`, `ticket_body`, `tone`)
- the schema it returns
- a version number, so that when you improve the tone examples next month, you're not silently breaking whatever already depends on `v1`

This is a small thing to do for one prompt and an essential thing to do for a team running dozens of them. You're previewing Week 6 here — when we get to prompt CI and versioning, this exact discipline is what a regression suite checks against.

---

### What today actually proved

Step back and look at what you just built: a single feature with one clear job, that nonetheless needed format specification, constraints, role framing, few-shot anchoring, conditional reasoning, structured output with a schema, defensive parsing, and a place in a versioned library to be considered done. Nobody handed you a single trick that did all of that. You combined five separate things you already knew, in service of one spec you wrote yourself.

That's the actual skill this week was teaching, underneath the named techniques: not "how do I use chain-of-thought" but "given a real problem, which of my tools does it actually need, and in what order." Every production GenAI feature you'll ever build starts from that same question. The techniques are just the vocabulary — this is the grammar.

Week 3 turns to a different kind of gap entirely: what happens when the model doesn't just need better instructions, but needs information it was never trained on in the first place. That's where retrieval comes in.
