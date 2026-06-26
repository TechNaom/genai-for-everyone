# Session 2.4: Structured Outputs

**Week:** 2 — Prompt Engineering & Application Design
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes

---

## Why this chapter exists

Every technique so far has produced output meant for a human to read. Today's chapter is about output meant for *code* to read — JSON, structured fields, data your application will parse and act on programmatically. This is a genuinely different problem, with a genuinely different failure mode: a human reading slightly-off prose barely notices; a parser handed slightly-off JSON crashes outright.

This matters enormously in real GenAI applications, because the moment you're building anything beyond a simple chatbot — a form-filler, a data extractor, an agent calling tools (which you'll formalize in Week 4) — you need the model's output in a precise, predictable shape your code can rely on. Getting this wrong is one of the most common sources of real production bugs in GenAI applications, and it's almost always avoidable with the practices in this chapter.

---

## Part 1: Why Reliable JSON Is Harder Than It Sounds

### The naive assumption

It's tempting to assume that asking a model "return this as JSON" is enough. Sometimes it is. But models can — and regularly do — add explanatory text before or after the JSON ("Sure, here's the JSON you requested:"), use inconsistent field names across calls, produce syntactically malformed JSON (a trailing comma, an unescaped quote inside a string), or simply misunderstand which fields you actually wanted.

### Why this happens, mechanically

Recall Session 1.1: the model is predicting the most statistically plausible next token. "Sure, here's the JSON you requested:" followed by an explanation is an *extremely* common pattern in the kind of text models train on — people explaining what they're about to show you. Without explicit instruction otherwise, that conversational politeness pattern can leak into output specifically meant to be machine-parsed, which is exactly the kind of mismatch that breaks a parser expecting JSON and nothing else.

### The real-world cost of getting this wrong

If your code does something like `json.loads(model_response)` and the model prepended "Here's the JSON:" before the actual JSON object, that call throws an exception. In a live application, that's not a cosmetic issue — it's a crash, or at minimum a swallowed error that silently breaks a feature. This is precisely the gap between "looks like it works in a quick test" and "works reliably in production," and it's one of the most common, most avoidable gaps in real GenAI applications.

---

## Part 2: Techniques That Actually Improve Reliability

### Technique 1: Explicit schema definition in the prompt

Don't just say "return JSON" — show the exact shape you want, field by field, ideally with the expected type for each field.

**Weak:** "Extract the name and email from this text as JSON."

**Strong:** 
```
Extract the name and email from this text and return ONLY a JSON object
in exactly this format, with no other text before or after:
{
  "name": "string",
  "email": "string"
}
```

The second version removes ambiguity about field names (is it "name" or "full_name"? "email" or "email_address"?) and explicitly forbids the conversational wrapper text that causes parsing failures.

### Technique 2: Explicit "no preamble" instructions

Directly instructing the model to return *only* the JSON, with no introductory or closing text, meaningfully reduces (though doesn't perfectly eliminate) the conversational-wrapper problem described in Part 1. Phrases like "Respond with ONLY the JSON object, no other text" or "Do not include any explanation" are doing real, specific work — they're not just politeness.

### Technique 3: Using a provider's structured-output / JSON mode, when available

Many model providers offer a dedicated feature — sometimes called "JSON mode" or "structured outputs" — that constrains the model's output generation at a mechanical level to guarantee syntactically valid JSON, sometimes even validating against a schema you provide. When available, this is meaningfully more reliable than prompt instructions alone, because it's enforced by the generation process itself rather than relying on the model choosing to follow an instruction. Check your specific provider's documentation, since exact implementation and naming varies.

### Technique 4: Defensive parsing in your code — the most important technique

Here's the technique that matters most, and the one most often skipped: **never assume the model's output is valid just because you asked nicely.** Always parse defensively:

```python
import json

def parse_model_json(raw_text: str):
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        # Attempt a fallback: maybe there's wrapper text around the JSON.
        # Try to find the first { and last } and extract just that span.
        start = raw_text.find('{')
        end = raw_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw_text[start:end + 1])
            except json.JSONDecodeError:
                pass
        return None  # signal failure clearly rather than crashing
```

This isn't elaborate — it's a simple, honest acknowledgment that even a well-engineered prompt can occasionally fail, and your code's job is to handle that failure gracefully (log it, retry, fall back to a default) rather than crash the entire application. This connects directly to Session 1.5: even with every mitigation in this chapter applied, you are still working with a system that doesn't guarantee its own output, and good engineering plans for that reality rather than hoping around it.

---

## Part 3: A Worked Example — Resume Parser

Let's combine these techniques into something realistic: a prompt that extracts structured data from a resume's text.

```
Extract the following information from this resume text and return ONLY
a JSON object in exactly this format, with no other text before or after:

{
  "name": "string",
  "email": "string or null if not found",
  "years_experience": "number, your best estimate based on listed roles",
  "skills": ["array", "of", "strings"]
}

If a field cannot be determined from the text, use null for strings/numbers
or an empty array for skills. Do not guess at information not present.

Resume text:
{resume_text}
```

Notice several deliberate choices here: the schema is explicit with types; there's explicit handling instruction for missing data (null, not a guess — connecting to Session 1.5's hallucination concerns: an absent field is far better than a confidently invented one); and the "no other text" instruction guards against the conversational-wrapper problem. Combined with defensive parsing in the surrounding code, this is a realistic, production-reasonable approach — not a toy example.

---

## Part 4: When Structured Output Still Goes Wrong

Even with every technique applied, a few realistic failure modes remain worth knowing about:

**Type mismatches.** You asked for `years_experience` as a number; the model returns the string `"5 years"` instead of the integer `5`. Defensive parsing should validate types, not just successfully parse JSON syntax — successfully parsed JSON can still have the wrong shape.

**Hallucinated fields filled in anyway**, despite explicit "use null" instructions — this is a real, documented failure mode, not a hypothetical. This is exactly why a human review step matters for any genuinely high-stakes extraction task, and why you shouldn't treat "I told it not to guess" as a guarantee.

**Schema drift across many calls.** A prompt that reliably returns a consistent shape in your testing might occasionally drift on a particularly unusual input it wasn't tested against. This is part of why Week 5's evaluation practices exist — testing against a representative range of real inputs, not just a few convenient examples.

---

## Points to Remember

- **Models can wrap JSON in conversational text, use inconsistent field names, or produce malformed syntax** — none of this is a hypothetical edge case; it's common enough to plan for by default.
- **Four techniques that help: explicit schema definition with types, explicit "no preamble" instructions, a provider's structured-output mode when available, and defensive parsing in your own code.**
- **Defensive parsing is the most important technique**, because it's the one that doesn't depend on the model behaving — it's your code's responsibility to handle failure gracefully rather than crash.
- **For missing data, instruct null/empty rather than guessing** — an absent field is far safer than a confidently hallucinated one, directly connecting to Session 1.5.
- **Successfully parsed JSON can still have the wrong shape or types** — validate structure and types, not just JSON syntax validity.

---

## Quick Check: Fill in the Blanks

1. Models can wrap JSON output in __________ text, which breaks code expecting pure JSON to parse.
2. Explicit __________ definition with field types reduces ambiguity about what shape the model should return.
3. The most important technique for reliability is __________ parsing in your own code, since it doesn't depend on the model behaving.
4. For missing data, you should instruct the model to return __________ rather than guessing, connecting to Session __________'s lesson on hallucination.
5. Successfully parsed JSON can still have the wrong __________ or __________, so validation should go beyond syntax checking.

**Answers:** 1. conversational (or wrapper) — 2. schema — 3. defensive — 4. null (or empty), 1.5 — 5. shape, types

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-02/session-2.4-quiz.md`](../../assessments/quizzes/week-02/session-2.4-quiz.md) · Answer key: [`assessments/answer-keys/week-02/session-2.4-quiz-answers.md`](../../assessments/answer-keys/week-02/session-2.4-quiz-answers.md)

Interview-style questions for this topic:

1. *"Why is getting reliable JSON output from an LLM harder than it sounds, and how do you make it more reliable?"*
2. *"You're building a resume parser that returns structured JSON. What happens if the LLM returns a field with the wrong data type, and how do you guard against that breaking your application?"*
3. *"What's the difference between a prompt that successfully produces parseable JSON and one that's actually production-reliable?"*
4. *"Why would you instruct a model to return null for missing fields instead of letting it guess?"*

---

## Core path — guided activity

**Resume Parser Prompt.** You'll build the structured-extraction prompt from Part 3, test it against several different resume-style inputs (including a deliberately messy one missing some fields), and implement defensive parsing around it. Full instructions: [`codebase/exercises/week-02/session-2.4/`](../../codebase/exercises/week-02/session-2.4/).

## Pro path — extended challenge

You'll be given a resume parser prompt that mostly works, but reliably fails on a specific kind of input (e.g., resumes with non-standard date formats, or candidates with no listed email). You'll diagnose the failure pattern by testing systematically, fix the prompt, and add a corresponding validation check in the parsing code so a future regression would be caught automatically rather than silently passing through.

## What's next

Session 2.5 — **Prompt Systems, Not Just Prompts** — moves from individual prompts to reusable prompt templates, variables, and small prompt libraries you can maintain across a real project.
