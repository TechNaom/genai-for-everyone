# Session 1.6: Week 1 Lab — Mini Build Day

**Week:** 1 — Foundations of GenAI & LLMs
**Format:** Live build session + self-paced extension + quiz
**Reading time:** ~15 minutes (this session is mostly building, not reading)

---

## Why this chapter exists

Five sessions in, you've built a genuinely solid mental model: the predictive/generative split, tokens and embeddings and context windows, the landscape of providers, the mechanics of a real API call, and the honest limitations of hallucination and bias. Today, none of that is new information — today is about *proving to yourself* that it all actually connects, by building one complete, polished tool that touches almost every idea from this week.

This matters more than it might seem. There's a real difference between "I understood that when I read it" and "I can build with it under my own steam." Today is where you find out which one is actually true — and where any gaps quietly surface so you can close them before Week 2 builds on top of this foundation.

---

## Part 1: The Build — "Explain It To Me Simply"

### What you're building

A command-line tool that takes any topic and an audience level, and produces an explanation calibrated to that audience — a 10-year-old gets a different explanation than a working professional, who gets a different explanation than a domain expert wanting a quick refresher.

This sounds simple. It's deliberately simple — today isn't about complexity, it's about correctly assembling pieces you already understand into something that actually works end to end.

### Why this particular tool, and not something else

This project was chosen specifically because building it well requires touching almost everything from this week:

- **Session 1.1's distinction** matters because you're building a generative tool — every output is freshly composed for the specific topic and audience, not selected from a fixed list.
- **Session 1.2's mechanics** matter because audience-appropriate explanations are fundamentally a *context* problem — you're shaping what the model considers when generating, which is the same idea as a context window holding relevant information.
- **Session 1.3's landscape thinking** matters because you'll make a real, defensible choice about which model tier fits this task (hint: this is a good task to think hard about whether you need a frontier-tier model, or whether a smaller, faster tier does just as well).
- **Session 1.4's mechanics** are the literal foundation — system/user roles, constructing a request, parsing a response.
- **Session 1.5's honesty** matters because you'll add a small but meaningful safeguard: flagging when a topic is the kind of thing where hallucination risk is especially high (very specific dates, statistics, niche technical claims) versus more conceptual topics where the risk profile is different.

### The build, step by step

**Step 1 — Design the audience levels.** Decide on at least three distinct audience levels (a reasonable default: "complete beginner / curious kid," "working professional, no specialized background," "domain expert wanting a refresher"). For each, write one sentence describing what should change — not just vocabulary, but depth, analogy use, and assumed background knowledge.

**Step 2 — Design the system prompt.** This is where Session 1.4's roles become concrete. Your system prompt needs to instruct the model on *how* to adapt — not just "explain simply" (too vague) but something that specifies tone, length, and what kind of analogies are appropriate for each level.

**Step 3 — Build the input handling.** Your tool should accept a topic and an audience level (command-line arguments are simplest), validate the audience level against your defined options, and give a clear error message if something's missing or invalid — basic, professional input handling.

**Step 4 — Make the API call.** Apply Session 1.4 directly: construct the request with the right roles, send it, parse the response, handle the case where the API call itself fails (network issue, invalid key) gracefully rather than crashing with a raw error trace.

**Step 5 — Add the honesty flag.** Before displaying the explanation, do a simple check: does the topic or the generated explanation contain very specific numbers, dates, or claims that would be worth independently verifying? If so, append a short, non-alarmist note suggesting the user double-check specific factual claims — directly applying Session 1.5's lesson about hallucination risk on specific factual details.

**Step 6 — Test across all three levels with the same topic.** This is the real test of whether your system prompt actually works — if "explain quantum entanglement" produces meaningfully different, appropriately-calibrated output across all three audience levels, your tool is working. If all three outputs sound suspiciously similar, your system prompt needs more specific instructions per level.

---

## Part 2: A Worked Example of "Done Well" vs. "Done Technically"

It's possible to build something that runs without errors and still misses the point of the exercise. Here's the difference, concretely.

**Done technically (passes, but misses the point):** The tool accepts a topic and a level, sends a generic prompt like "explain {topic} for a {level}," and prints whatever comes back. It runs. It doesn't crash. But the outputs across levels often sound nearly identical, just slightly shorter or longer — because the system prompt never actually specified *what should differ* beyond length.

**Done well (the actual goal):** The system prompt for each level specifies concrete behavioral instructions — for the "curious kid" level, explicitly requiring a relatable everyday analogy and forbidding jargon entirely; for the "domain expert" level, explicitly allowing field-specific terminology and skipping basic setup the expert would find condescending. The difference between these two versions isn't more code — it's a more thoughtful system prompt, which is exactly the kind of judgment Week 2 (Prompt Engineering) will formalize into a repeatable skill.

---

## Part 3: Reflection — What Clicked, What's Still Fuzzy

Before moving into Week 2, take five honest minutes (this is genuinely worth doing, not just a suggested platitude) to answer these for yourself:

- Could you explain, without looking back at any chapter, why an LLM might confidently give a wrong answer to a very specific factual question? If this still feels shaky, revisit Session 1.5 before Monday.
- Could you sketch, from memory, what happens between typing a message and seeing a response, including the role of conversation history? If not, Session 1.4 is worth a second pass.
- Did building today's tool surprise you anywhere — a place where you thought you understood something until you actually had to implement it? That surprise is valuable information about where your understanding is genuinely solid versus where it's still surface-level.

This isn't busywork. The single best predictor of struggling in Week 2 (and beyond) is carrying forward an unexamined gap from Week 1, because everything after this point assumes this foundation is solid.

---

## Points to Remember

- **Today's build deliberately touches every major idea from Week 1** — the predictive/generative distinction, context and tokens, model choice, request/response mechanics, and honest handling of hallucination risk.
- **"Runs without errors" and "actually demonstrates understanding" are different bars.** A tool that produces nearly identical output across audience levels has a system prompt problem, not a code problem — and recognizing that distinction is itself a Week 1 skill.
- **The quality of an adaptive tool like this lives almost entirely in the system prompt's specificity** — vague instructions produce vague differentiation; concrete behavioral instructions (banned jargon, required analogy types, assumed background) produce real differentiation.
- **Honest self-assessment now is cheaper than discovering a gap later.** Week 2 builds directly on this week's foundation; an unexamined gap here compounds.

---

## Quick Check: Fill in the Blanks

1. Building an audience-adaptive explanation tool is fundamentally a __________ problem — shaping what the model considers when generating its response.
2. A system prompt that just says "explain simply" is too __________ — effective differentiation needs concrete behavioral instructions like banned jargon or required analogy types.
3. The honesty flag added in Step 5 applies the lesson from Session __________ about hallucination risk on specific factual claims.
4. A tool that runs without errors but produces nearly identical output across audience levels has a __________ problem, not necessarily a code problem.
5. The single best predictor of struggling in later weeks is carrying forward an __________ gap from earlier material.

**Answers:** 1. context — 2. vague — 3. 1.5 — 4. system prompt (or prompt-design) — 5. unexamined

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-01/session-1.6-quiz.md`](../../assessments/quizzes/week-01/session-1.6-quiz.md) · Answer key: [`assessments/answer-keys/week-01/session-1.6-quiz-answers.md`](../../assessments/answer-keys/week-01/session-1.6-quiz-answers.md)

Interview-style questions for this topic:

1. *"You're asked to build a tool that explains technical concepts differently for different audiences. What design decisions matter most, and why?"*
2. *"What's the difference between a chatbot that 'runs without errors' and one that's actually well-built? Give a concrete example."*
3. *"How would you decide which model tier to use for an explanation-generation tool — does it need frontier capability?"*
4. *"What's one honest safeguard you'd add to a tool like this, knowing what you know about hallucination?"*

The full Week 1 written exam, covering all six sessions, is in [`assessments/written-exams/week-01-exam.md`](../../assessments/written-exams/week-01-exam.md).

---

## Core path — guided activity

Build the full "Explain It To Me Simply" tool following Parts 1–2 of this chapter, with at least three audience levels and the honesty flag from Step 5. Full starter structure: [`codebase/exercises/week-01/session-1.6/`](../../codebase/exercises/week-01/session-1.6/).

## Pro path — extended challenge

Extend the tool with a comparison mode: given one topic, generate all three audience-level explanations in a single run and display them side by side, then write a short paragraph critiquing your own system prompts — where did the differentiation work well, and where did two levels still sound too similar? This pushes you to evaluate your own prompt design critically, a habit that becomes formal practice in Week 5.

## What's next

**Week 2: Prompt Engineering & Application Design** begins Monday. Everything from this week — especially the system-prompt judgment you just exercised in today's build — becomes the explicit, structured subject of the next six sessions.
