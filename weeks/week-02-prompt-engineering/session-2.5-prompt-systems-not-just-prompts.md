# Session 2.5: Prompt Systems, Not Just Prompts

**Week:** 2 — Prompt Engineering & Application Design
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes

---

## Why this chapter exists

Every prompt you've built so far in this program has lived in one place at a time — a script, an exercise, a single use case. That's exactly right for learning the techniques. But the moment you're building something real — a product with several AI-powered features, a team with more than one person touching prompts, a feature that needs to evolve over months — a collection of one-off prompts scattered across files stops being a minor inconvenience and starts being a genuine liability.

This chapter is about making that transition deliberately: from individual prompts to a **prompt system** — reusable templates, named variables, and some structure around how prompts are stored, versioned, and tested. This is also a direct preview of Week 6's CI/CD-for-prompts content; the habits you build today are the foundation that later, more formal tooling builds on.

---

## Part 1: A Prompt vs. A Prompt System

### The distinction that matters

A single good prompt solves one specific case, written for one specific moment. A **prompt system** is something different in kind, not just in scale: it involves **reusable templates with variables** (the same structure, filled in differently each time), **some notion of versioning** (so you can tell what changed and roll back if a change makes things worse), **consistent testing across a representative range of inputs** (not just the one example you happened to try first), and often **chaining multiple prompts together** into a multi-step pipeline.

### Why this distinction has real consequences

Imagine two engineers building the same feature — a customer support reply generator. Engineer A writes a great prompt, hardcodes it directly into the function that calls the API, and ships it. Engineer B writes the same quality prompt, but stores it as a template with named variables (`{customer_name}`, `{issue_description}`, `{tone}`), in a separate file from the application logic, with a version number and a few test cases attached.

Six months later, when the company wants to add a new tone option, or a product manager wants to see exactly what prompt is currently live, or a bug report comes in and someone needs to determine whether a recent prompt change caused it — Engineer A's approach means digging through application code to find and understand a hardcoded string, with no history of what it used to say. Engineer B's approach means looking at one well-organized file with a clear change history. Same starting prompt quality; wildly different maintainability six months out.

---

## Part 2: Prompt Templates and Variables

### The basic idea

A prompt template is a prompt with placeholders for the parts that change between uses, written once and reused with different values substituted in. You've actually already been doing a simplified version of this in earlier exercises — using Python's `.format()` or f-strings to substitute values into a prompt string. A prompt system formalizes this practice deliberately, rather than leaving it as an incidental implementation detail.

### A concrete example

**Not a template (hardcoded, one-off):**
```python
prompt = "Write a polite follow-up email to Sarah Chen about her unpaid invoice from March 15th, mentioning a 5% late fee."
```

**A template:**
```python
FOLLOW_UP_TEMPLATE = """Write a polite follow-up email to {customer_name} about
their unpaid invoice from {invoice_date}, mentioning a {late_fee_pct}% late fee."""

prompt = FOLLOW_UP_TEMPLATE.format(
    customer_name="Sarah Chen",
    invoice_date="March 15th",
    late_fee_pct=5
)
```

The template version separates the *reusable structure* from the *specific data*, meaning the exact same well-tested prompt structure gets used for every customer, every invoice — rather than someone re-writing a slightly different version of this prompt by hand each time, with all the inconsistency and untested-edge-case risk that implies.

### Why this matters for quality, not just convenience

A template that's been tested against a representative range of inputs (different customer name formats, different fee percentages, different date formats) is far more reliable than re-deriving a similar prompt from scratch each time you need it. This connects directly to Session 2.4's lesson about testing structured-output prompts against a range of inputs, not just convenient examples — a template gives you one well-tested artifact to maintain, instead of many slightly-different, individually-untested variants scattered throughout a codebase.

---

## Part 3: Organizing a Prompt Library

### Separating prompts from application code

A meaningful practice, even for a solo developer: don't bury prompt strings directly inside the application logic that calls the API. Keep them in a dedicated location — a separate module, a folder of template files — so anyone (including future you) can find and review every prompt the application uses without having to read through unrelated business logic.

### Naming and documentation conventions

Each template benefits from a clear name describing its purpose, and a short comment or docstring describing exactly what variables it expects and what each one means. This sounds like a small thing, but it's the difference between a six-month-old prompt library being genuinely usable versus being an archaeology project every time someone needs to touch it.

### A lightweight example structure

```python
# prompts/customer_communications.py

FOLLOW_UP_TEMPLATE = """..."""  # expects: customer_name, invoice_date, late_fee_pct

REFUND_APOLOGY_TEMPLATE = """..."""  # expects: customer_name, product_name, refund_amount

# prompts/data_extraction.py

RESUME_PARSER_TEMPLATE = """..."""  # expects: resume_text
```

This is genuinely simple — there's no special framework required to get real value from this practice. The discipline of *separating, naming, and documenting* templates is what creates the value, not any particular tool.

### A note on testing

Even a lightweight test — a small set of representative example inputs with expected characteristics in the output (not necessarily an exact string match, since LLM output naturally varies, but checks like "does it include the customer's name," "is it under the specified length," "does it avoid mentioning competitors") — catches a meaningful fraction of regressions before they reach production. This is a preview of what Week 5 formalizes into a complete evaluation discipline; for now, the habit of having *any* repeatable check beyond "I tried it once and it looked fine" is the valuable starting point.

---

## Part 4: Chaining Prompts Together

### What chaining means

Sometimes a task is genuinely better solved as a sequence of separate prompts, each handling one well-defined sub-task, with the output of one feeding into the input of the next — rather than one enormous prompt trying to do everything at once.

### A worked example

Consider building a tool that processes an incoming customer email: it needs to (1) classify the email's category, (2) extract any specific order numbers or dates mentioned, and (3) draft an appropriate reply. You could attempt all three in one giant prompt, or you could chain three focused prompts:

**Step 1:** Classify the email (using few-shot, from Session 2.2) → category.
**Step 2:** Extract structured data (using Session 2.4's techniques) → order numbers, dates, as JSON.
**Step 3:** Draft a reply, with the category and extracted data from steps 1–2 included as context → final reply text.

Each step is simpler, more testable in isolation, and easier to debug than one combined mega-prompt — if the final reply is wrong, you can check each step's output independently to find exactly where things went wrong, rather than trying to diagnose a failure buried inside one large, opaque request.

### The honest trade-off

Chaining adds latency (multiple API calls instead of one) and complexity (more code to manage the handoffs between steps). It's the right choice when a task genuinely has distinct sub-problems that benefit from focused, separately-testable prompts — not a default to apply to every task regardless of whether it actually has that structure. A simple task that doesn't need decomposition shouldn't be artificially split into a chain just because chaining is available as a technique.

---

## Points to Remember

- **A prompt system differs from a single prompt in kind, not just scale**: reusable templates with variables, versioning, consistent testing, and often chaining multiple prompts together.
- **Templates separate reusable structure from specific data**, meaning one well-tested prompt structure serves every use case rather than many untested, slightly-different one-off variants.
- **Separate prompts from application code**, with clear naming and documentation of expected variables — this is what makes a prompt library maintainable six months later, not any particular framework.
- **Even lightweight testing** (checking for specific characteristics in output, not exact string matches) catches a meaningful fraction of regressions before production, previewing Week 5's evaluation discipline.
- **Chaining prompts is for tasks with genuinely distinct sub-problems** — it adds latency and complexity, so it's a deliberate choice, not a default.

---

## Quick Check: Fill in the Blanks

1. A prompt system involves reusable templates with __________, some notion of __________, and consistent testing across a range of inputs.
2. A prompt template separates the reusable __________ from the specific __________ that changes each time.
3. Prompts should be kept __________ from application code, with clear naming and documentation of expected variables.
4. Chaining prompts means breaking a task into a __________ of separate prompts, each handling one well-defined __________.
5. The honest trade-off of chaining is added __________ and __________, so it's appropriate for tasks with genuinely distinct sub-problems, not a default.

**Answers:** 1. variables, versioning — 2. structure, data — 3. separate — 4. sequence, sub-task — 5. latency, complexity

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-02/session-2.5-quiz.md`](../../assessments/quizzes/week-02/session-2.5-quiz.md) · Answer key: [`assessments/answer-keys/week-02/session-2.5-quiz-answers.md`](../../assessments/answer-keys/week-02/session-2.5-quiz-answers.md)

Interview-style questions for this topic:

1. *"What's the difference between 'a good prompt' and 'a good prompt system,' and why does that distinction matter for a real product?"*
2. *"How would you organize a library of prompt templates for a team building several different AI features?"*
3. *"When would you chain multiple prompts together instead of using one larger prompt?"*
4. *"What's a lightweight way to test a prompt template without requiring an exact-match output check?"*

---

## Core path — guided activity

**Reusable Prompt Template Library.** You'll build a small library of 5+ prompt templates for a consistent theme (e.g., customer communications), each with named variables, a docstring describing expected inputs, and at least one lightweight test check. Full instructions: [`codebase/exercises/week-02/session-2.5/`](../../codebase/exercises/week-02/session-2.5/).

## Pro path — extended challenge

You'll build a simple 3-step prompt chain (classify → extract → draft reply, following Part 4's worked example) where each step's output feeds into the next, with the ability to inspect and log the intermediate output of each step independently — directly demonstrating the debuggability advantage chaining provides over one large combined prompt.

## What's next

Session 2.6 — **Week 2 Lab: Mini Build Day** — integrates everything from this week into a single build: a customer-support reply generator with tone control.
