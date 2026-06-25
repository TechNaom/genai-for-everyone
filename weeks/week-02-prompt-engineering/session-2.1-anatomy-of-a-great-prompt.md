# Session 2.1: Anatomy of a Great Prompt

**Week:** 2 — Prompt Engineering & Application Design
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes

---

## Why this chapter exists

In Week 1's final session, you wrote system prompts without a formal framework — you relied on intuition about what a "beginner" explanation versus an "expert" explanation should contain. That intuition served you well, but intuition alone doesn't scale, doesn't transfer cleanly to new situations, and is hard to debug when something goes wrong.

This chapter gives you the formal framework. By the end, "write a better prompt" stops being a vague aspiration and becomes a checklist you can actually run through, every time, on any prompt, for any task. This is the single most immediately useful, immediately testable skill in this entire program — and it's exactly the skill real interviews probe hardest, often by handing you a bad prompt live and asking you to fix it on the spot.

---

## Part 1: Why "Just Ask Nicely" Isn't a Strategy

### The expectation gap

Here's a common, costly mistake: treating an LLM prompt like a Google search query — a few keywords, minimal structure, trust that "the AI is smart enough to figure out what I mean." This works *sometimes*, for simple, common requests where there's an obvious single interpretation. It fails constantly for anything with real ambiguity, and the failure is subtle: you don't get an error message, you get a confident, fluent, *wrong-for-your-purposes* answer, because the model genuinely couldn't have known what you actually wanted from the information you gave it.

### A concrete demonstration

Compare these two prompts:

**Prompt A:** "Write something about our product."

**Prompt B:** "Write a 100-word product description for our wireless noise-canceling headphones, targeting busy professionals who travel frequently. Emphasize battery life and comfort during long flights. Tone: confident but not salesy. Format: a single paragraph, no bullet points."

Both are grammatically valid English. Only one of them gives the model enough to work with to produce something actually useful on the first try. Prompt A isn't *wrong* — the model will produce *something* — but that something is essentially a guess, filling in every missing detail (which product? which audience? what tone? what length?) with whatever's statistically most generic, because nothing in the prompt steered it elsewhere.

### The core insight

A prompt is not a question — it's a **specification**. You are not asking the model what it thinks; you're specifying what you need produced, with enough detail that a competent person reading only that specification could produce something close to what you want. If you wouldn't hand Prompt A to a freelance writer and expect a usable result, you shouldn't expect one from an LLM either — and for the same reason: critical information is simply missing, not implied.

---

## Part 2: The Four Pillars of a Great Prompt

Every effective prompt, regardless of task, tends to cover four distinct dimensions. Missing any one of them is usually where a "not quite right" output comes from.

### Pillar 1: Clarity

Clarity means the *core task* is unambiguous. Not "write about X" but "write a [specific thing] that does [specific job]." Vague verbs ("discuss," "talk about," "cover") are a warning sign — they describe an activity, not a deliverable. Specific verbs ("summarize," "compare," "draft," "classify," "translate") describe an actual output.

**Weak:** "Talk about the meeting."
**Clear:** "Summarize the key decisions and action items from this meeting transcript in 5 bullet points."

### Pillar 2: Context

Context means giving the model the background information it needs to make good decisions — information that isn't part of the instruction itself, but shapes what a good answer looks like. This connects directly to Session 1.2's context window concept: context is *literally* what you're choosing to put on the model's "desk."

**Without context:** "Write a follow-up email." (Follow-up to what? About what? To whom?)
**With context:** "Write a follow-up email to a client who attended our product demo last week but hasn't responded since. We offered a 10% discount during the call that's still on the table."

### Pillar 3: Constraints

Constraints define the boundaries of the output — length, format, tone, what to include, and importantly, what to *exclude*. Constraints are where most "technically correct but unusable" outputs get fixed. A model given no length constraint might write 50 words or 500; a model given no format constraint might return prose when you needed a table.

**Examples of constraints:** "Keep it under 150 words." "Respond only in valid JSON." "Don't mention pricing." "Write in second person." "Use no more than 2 sentences per paragraph."

### Pillar 4: Format Specification

Format specification is related to constraints but deserves its own focus, because it's so often the difference between an answer you can *use* and one you have to *rework*. If you need structured output (a list, a table, JSON, a specific template), say so explicitly and show the shape if it's not obvious. Don't assume the model will guess the exact structure your downstream code or workflow needs.

**Vague:** "Give me the pros and cons."
**Specified:** "Give me the pros and cons as two separate bulleted lists, with a maximum of 4 points each, under the headers 'Pros' and 'Cons'."

---

## Part 3: A Worked Rewrite, Pillar by Pillar

Let's take a genuinely bad prompt and rebuild it methodically, naming which pillar each addition addresses.

**Starting prompt:** "Help with customer email."

This fails on every pillar simultaneously — there's no specific task (clarity), no background (context), no boundaries (constraints), and no shape (format). Let's fix it one pillar at a time.

**+ Clarity:** "Draft a reply to a customer email." (Better — now we know the deliverable is a reply, not advice or analysis.)

**+ Context:** "Draft a reply to a customer who emailed asking for a refund on a product that arrived damaged. They've been a customer for 3 years and this is their first complaint." (Now the model knows the situation, the customer's history, and can calibrate tone accordingly — a first-time complainer with 3 years of loyalty deserves a different response than a chronic complainer.)

**+ Constraints:** "...Approve the refund, apologize for the inconvenience, and offer a 15% discount on their next order as a goodwill gesture. Keep the tone warm and personal, not corporate. Maximum 120 words." (Now the model knows exactly what outcome to deliver, not just the situation.)

**+ Format:** "...Format as a complete email including a subject line." (Now the output is immediately usable — not a paragraph you have to manually turn into an email.)

**Final prompt:** "Draft a reply to a customer who emailed asking for a refund on a product that arrived damaged. They've been a customer for 3 years and this is their first complaint. Approve the refund, apologize for the inconvenience, and offer a 15% discount on their next order as a goodwill gesture. Keep the tone warm and personal, not corporate. Maximum 120 words. Format as a complete email including a subject line."

Notice this isn't a *longer* prompt for the sake of length — every addition did real work. This is the difference between padding and precision.

---

## Part 4: When More Detail Stops Helping

A reasonable question at this point: doesn't there come a point where you're just over-engineering a prompt for a simple task? Yes — and recognizing that point is itself part of the skill.

**Signal that you've added enough:** could a competent person, reading only your prompt, produce something close to what you actually need, without having to guess at anything important? If yes, you're done — further additions are diminishing returns at best, and at worst can clutter the prompt in ways that actually hurt focus (recall Session 1.2's "lost in the middle" effect with very long contexts).

**Signal that you need more:** the model's output technically answers the prompt but isn't usable, and when you look back at your prompt, you can identify a specific piece of information you knew but never actually told the model. That gap — something *you* knew that *the model* had no way to know — is almost always the fix.

---

## Points to Remember

- **A prompt is a specification, not a question.** Missing information doesn't get intelligently inferred — it gets filled in with whatever's statistically generic, which is usually not what you wanted.
- **Four pillars: clarity (unambiguous core task), context (background the model needs), constraints (boundaries on length/tone/content), and format (the actual shape of the output).** Most disappointing outputs trace back to a missing pillar, not a "dumb" model.
- **Specific verbs over vague verbs.** "Summarize," "compare," "classify" describe a deliverable; "discuss," "cover," "talk about" describe an activity.
- **The test for "is this prompt good enough":** could a competent person, given only this prompt, produce something close to what you need without guessing at anything important?
- **More detail isn't always better.** Once a prompt covers what's genuinely needed, additional padding can clutter focus rather than improve output.

---

## Quick Check: Fill in the Blanks

1. A prompt should be treated as a __________, not a question — you're specifying what you need produced.
2. The four pillars of a great prompt are clarity, __________, constraints, and __________.
3. Vague verbs like "discuss" describe an __________, while specific verbs like "summarize" describe a __________.
4. Context in a prompt is literally what you're choosing to put on the model's __________, connecting back to Session __________.
5. The test for whether a prompt has enough detail: could a __________ person, given only the prompt, produce something close to what you need without __________ at anything important?

**Answers:** 1. specification — 2. context, format — 3. activity, deliverable — 4. desk (or context window), 1.2 — 5. competent, guessing

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-02/session-2.1-quiz.md`](../../assessments/quizzes/week-02/session-2.1-quiz.md) · Answer key: [`assessments/answer-keys/week-02/session-2.1-quiz-answers.md`](../../assessments/answer-keys/week-02/session-2.1-quiz-answers.md)

Interview-style questions for this topic:

1. *"Here's a vague prompt: 'Write something about our product.' What's wrong with it, and how would you fix it?"*
2. *"What's the difference between giving a model context and giving it constraints? Why do you need both?"*
3. *"How do you know when a prompt has enough detail versus when it needs more?"*
4. *"Walk me through rewriting a bad prompt live, explaining each change as you make it."*

---

## Core path — guided activity

**Prompt Rewrite Exercise.** You'll take 5 deliberately weak prompts and rewrite each one, explicitly identifying which of the four pillars was missing and what you added to fix it. Full instructions: [`codebase/exercises/week-02/session-2.1/`](../../codebase/exercises/week-02/session-2.1/).

## Pro path — extended challenge

You'll be given a prompt that LOOKS thorough (it's long, detailed, and well-formatted) but actually fails for a real business task because it's missing one critical, easy-to-overlook piece of context. You'll diagnose exactly what's missing, fix it, and explain why length and apparent thoroughness didn't guarantee correctness — directly reinforcing this chapter's Part 4.

## What's next

Session 2.2 — **Prompting Techniques I** — builds on this foundation with specific, named techniques: zero-shot, few-shot, and role prompting.
