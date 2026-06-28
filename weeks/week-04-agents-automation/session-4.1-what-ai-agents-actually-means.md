# Session 4.1 — What "AI Agents" Actually Means

## Part 1: The word everyone uses and almost nobody defines

If you've spent any time near a tech conference or a product launch lately, you've heard the word "agent" used to describe roughly everything. A chatbot with a system prompt? Agent. A script that calls an API on a schedule? Agent. A model that can use a calculator? Agent. Marketing has worn this word down until it barely means anything.

That's a problem if you're trying to build real things, because "I'll just build an agent" is not a spec. Before we write a single line of code this week, we're going to nail down a definition precise enough to build from — one that tells you, given any system in front of you, whether it's an agent, a workflow, or just a chatbot with extra steps.

Here's the definition we'll use for the rest of the course:

> **An agent is a system where a language model decides what to do next, based on what just happened, in order to make progress toward a goal — repeatedly, without a human choosing each step.**

Every word in that sentence is doing work. Let's take it apart.

**"Decides what to do next"** — this is the part that separates an agent from a workflow. In a workflow, the steps are fixed by the programmer ahead of time: do A, then B, then C, always, in that order. In an agent, the model looks at the current situation and *picks* the next action from a set of possibilities. The control flow lives inside the model's reasoning, not inside your `if` statements.

**"Based on what just happened"** — the model isn't just executing a pre-written plan blindly. It's reading the result of its last action before deciding on the next one. If a tool call fails, returns something unexpected, or reveals new information, the agent's next move can change because of it.

**"Toward a goal"** — there's a target state the system is trying to reach, not just a single response to generate. "Answer this question" is a single-turn task. "Research this topic and produce a report I'm satisfied with" is a goal that might take many turns, several tool calls, and some trial and error.

**"Repeatedly, without a human choosing each step"** — this is what makes it autonomous rather than just interactive. A human can still review the final output, or even approve risky steps, but the *sequence of intermediate decisions* is the model's, not a person typing each command one at a time.

If a system has all four properties, it's an agent. If it's missing any one of them, it's something else — and that something else often has a name we should use instead, because precision saves you from over-engineering.

## Part 2: The three things people conflate

Let's separate the three categories that get blurred together: **chatbot**, **workflow**, and **agent**.

**A chatbot** is single-turn (per turn) and reactive. You send a message, it generates a response, the turn ends. Even with memory of the conversation so far, it's still doing one thing per turn: producing text. There's no loop where it takes an action, observes a result, and decides what to do based on that result, all before getting back to you.

**A workflow** (sometimes called an automation or a pipeline) is a fixed sequence of steps that may use an LLM at one or more points, but the *sequence itself* is hard-coded by a person. "Summarize the input with an LLM call, translate the summary with another LLM call, then email the result" is a workflow. It can be sophisticated — branching, retries, parallel steps — but the branches are still decisions a programmer made in advance ("if the sentiment score is negative, escalate"), not decisions the model makes about what tool to reach for next based on something novel it just observed.

**An agent** is what you get when you hand the model the decision of *what to do next*, not just *what to say*. Concretely: the model has access to a set of tools, it chooses which one to call and with what arguments, it gets back the result, and it loops — possibly calling more tools, possibly changing its plan — until it decides the goal is met.

A useful test: **if you removed the LLM and replaced its decision points with a flowchart a human designed, would the system behave differently on a case it wasn't specifically planned for?** If no, it's a workflow with an LLM bolted on. If yes — if it can genuinely react to something the designer didn't anticipate — it's closer to a real agent.

This has real consequences. Workflows are cheaper, faster, and easier to test exhaustively. Agents are more flexible and can handle situations you didn't foresee, but are less predictable and can fail in stranger ways. Most production systems that work well are *mostly* workflow, with a small, carefully-scoped agentic piece where flexibility earns its cost. Knowing which parts actually need to be agentic — and keeping the rest as plain workflow — is one of the most valuable judgment calls you'll develop this week.

## Part 3: The loop, concretely — plan, act, observe

The mechanism underneath almost every real agent is a simple loop with three repeating phases. Different frameworks name it differently (ReAct's "Thought, Action, Observation" is the most famous version), but the shape is always the same:

1. **Plan** — given the goal and everything that's happened so far, the model reasons about what to do next.
2. **Act** — the model picks a specific tool and arguments, and that tool actually executes. This is the only phase where something happens outside the model.
3. **Observe** — the result comes back to the model as new information, added to what it can see, so the *next* planning step is informed by it.

Then the loop repeats — until the model decides it has enough information to answer, or hits a stopping condition (a step limit, a "done" signal, or simply deciding the goal is satisfied).

This explains both the power and the risk of agents in one structure. The power: each iteration can genuinely change direction based on real information, which a fixed script can't do. The risk: nothing inherently stops the loop from going wrong — looping forever, calling the wrong tool repeatedly, or confidently misreading an observation. Every agent you build from here needs an answer to "how does this loop know when to stop, and what happens if it doesn't?" We'll build real stopping conditions in Session 4.3.

Let's make this fully concrete with an actual trace — not a hypothetical, but a real run we can inspect step by step.

### A real trace: two sub-questions, two tools, one loop

Take this task: *"What's the total cost of 3 umbrellas at $14.50 each, and will I need one tomorrow in Chicago?"* This is a good toy example because it has two genuinely separate sub-problems needing two different tools: arithmetic and weather. Here's what the loop actually produces, with each tool call genuinely executed:

```
[Step 0] TASK
What's the total cost of 3 umbrellas at $14.50 each, and will I
need one tomorrow in Chicago?

[Step 1] PLAN
This task has two independent sub-questions: (1) total cost of 3
umbrellas at $14.50, (2) tomorrow's weather in Chicago. I'll solve
both with tools, then combine into one answer.

[Step 2] ACT
{ "tool": "calculator", "input": "3 * 14.50" }

[Step 3] OBSERVE
{ "result": 43.5 }

[Step 4] ACT
{ "tool": "weather_lookup", "input": "Chicago" }

[Step 5] OBSERVE
{ "result": { "tomorrow": "rain", "chance_of_rain_pct": 80 } }

[Step 6] FINAL_ANSWER
3 umbrellas at $14.50 each = $43.50 total. Chicago's forecast for
tomorrow is rain with an 80% chance of rain, so yes, you will
likely need one.
```

Notice the shape: plan once, alternate act/observe for each tool needed, then synthesize. The final answer's two numbers — $43.50 and 80% — both trace directly to real tool outputs in Steps 3 and 5. Nothing was invented; it's a recombination of verified observations. That traceability is the entire point of building things this way instead of asking a model to "guess" the cost and weather from training data — every number in the answer has a receipt.

### Where this breaks: agent vs. workflow, under stress

Here's the part that actually shows *why* the agent/workflow distinction matters, instead of just asserting it. Take the same task structure, but run it for a city the weather tool has no data for. We'll run two versions side by side: a **rigid workflow** that always executes the same two steps in the same order, and a **reactive agent** that inspects what each tool actually returned before deciding what to do next.

For a city the tool *does* have data for, both versions behave identically:

```
CITY: Chicago  (in DB: True)

--- Rigid workflow ---
  ('calculator', '3 * 14.50', 43.5)
  ('weather_lookup', 'Chicago', {'tomorrow': 'rain', 'chance_of_rain_pct': 80})
  OUTCOME: 80% chance of rain

--- Reactive agent ---
  ('calculator', '3 * 14.50', 43.5)
  ('weather_lookup', 'Chicago', {'tomorrow': 'rain', 'chance_of_rain_pct': 80})
  OUTCOME: 80% chance of rain
```

No visible difference — which is exactly why so many demos look identical whether they're "really" agentic or just well-written workflows. The difference only shows up under stress. Now try a city with no entry in the lookup table:

```
CITY: Miami  (in DB: False)

--- Rigid workflow ---
  ('calculator', '3 * 14.50', 43.5)
  ('weather_lookup', 'Miami', {'error': 'No data for Miami'})
  OUTCOME: CRASHED: workflow assumed a field that wasn't there

--- Reactive agent ---
  ('calculator', '3 * 14.50', 43.5)
  ('weather_lookup', 'Miami', {'error': 'No data for Miami'})
  ('replan', 'no data branch', 'No weather data available for Miami
   from this tool. Recommending the user check a live weather
   source instead.')
  OUTCOME: No weather data available for Miami from this tool.
  Recommending the user check a live weather source instead.
```

The rigid workflow breaks because it was written to always read a `chance_of_rain_pct` field from the tool's response, and that field doesn't exist when the lookup fails — it has no branch for "what if the tool didn't return what I expected," because nobody wrote one for this specific case. The reactive version *inspects the observation* before deciding what to do next, notices the error, and re-plans: it gives the user an honest answer about what's missing instead of crashing on a bad assumption.

This is the real, concrete payoff of "the model decides what to do next based on what just happened." It's the difference between a system that degrades gracefully on cases nobody anticipated and one that breaks the moment reality doesn't match the script. You could patch the workflow with a manual `try/except` for this *specific* case — and a good engineer would. But that's the point: a workflow only handles the cases someone thought to write a branch for. An agent's branching comes from the model's reasoning at run time, which can (within limits) cover cases nobody explicitly anticipated.

## Part 4: Why this matters for what you build this week

Week 4 is about giving models the ability to act, not just talk. Over the next five sessions, you'll go from defining a single tool (4.2), to chaining tool calls toward a multi-step goal (4.3), to coordinating more than one model working together (4.4), to deciding when a full agent is overkill and a simpler automation will do (4.5), and finally to building something that puts it all together (4.6).

Every session this week, ask: *is this piece of the system genuinely agentic — does it need the model deciding what happens next — or would a plain workflow do the job more cheaply and predictably?* Most of the time in real products, most of the system should be workflow, with only the part that truly benefits from in-the-moment decision-making made agentic. Knowing the difference is what separates engineers who ship reliable systems from people who call everything an agent because it sounds impressive.

---

## Points to Remember

- An **agent** is a system where the model decides what to do next based on what just happened, repeatedly, toward a goal — without a human choosing each step.
- A **chatbot** is single-turn and reactive: one message in, one response out, no loop of action and observation within a turn.
- A **workflow** may use an LLM at one or more steps, but the *sequence* of steps is fixed in advance by a programmer, not decided by the model at run time.
- The core agent mechanism is the **plan → act → observe** loop: reason about the next step, take an action (usually a tool call), observe the real result, and repeat.
- The test for "is this really agentic": if you replaced the model's decision points with a human-designed flowchart, would it behave differently on a case the designer didn't anticipate? If yes, it's agentic. If no, it's a workflow.
- Agentic flexibility comes at a cost: less predictability, harder testing, and new failure modes (like infinite loops or wrong tool calls). Most production systems are mostly workflow, with a small, deliberately-scoped agentic core.
- Every agent loop needs an explicit answer to "how does it know when to stop?" — we'll build real stopping conditions in Session 4.3.

---

## Quick Check: Fill in the Blanks

1. A system where the model decides what to do next based on what just happened is called an __________.
2. In a __________, the sequence of steps is fixed in advance by a programmer, even if an LLM is used at some steps.
3. The three repeating phases of the agent loop are plan, __________, and observe.
4. A chatbot is __________-turn and reactive, with no loop of action and observation within a single turn.
5. In the umbrella/weather trace, the rigid workflow crashed on Miami because it assumed a field would always be present in the tool's __________.
6. The test for genuine agency asks whether replacing the model's decisions with a human-designed __________ would change the system's behavior on an unanticipated case.

**Answers:** 1. agent — 2. workflow — 3. act — 4. single — 5. result/response (observation) — 6. flowchart

---

## Quiz and Interview Questions

<<<<<<< HEAD
Full quiz (includes answer key): [session-4.1-quiz.md](../../assessments/quizzes/week-04/session-4.1-quiz.md)
=======
This chapter's full quiz lives in [session-4.1-quiz.md](../../assessments/quizzes/week-04/session-4.1-quiz.md), and the answer key is in [session-4.1-quiz-answers.md](../../assessments/answer-keys/week-04/session-4.1-quiz-answers.md).
>>>>>>> 5b2640c (Fix Session 4.1: split quiz/answer-key, real markdown links matching 1.1 convention)

Interview-style questions for this topic:

1. "How would you explain the difference between an agent and a workflow to a non-technical stakeholder who keeps calling everything an agent?"
2. "Describe a real or hypothetical system where making it 'fully agentic' would actually be a worse engineering decision than keeping it a workflow."
3. "What's the practical difference between a system failing because it crashed and a system failing because it confidently gave a wrong answer? Which is worse, and why?"
4. "Walk through what 'stopping condition' means for an agent loop, and describe one way an agent loop could fail to stop even when it should."

---

## Core path

In the Core path exercise, you'll run and inspect the plan-act-observe loop yourself on a two-tool task (the same umbrella/weather example from this chapter), then deliberately break it by feeding it a city the weather tool doesn't know about — and watch a rigid, hard-coded version crash while a version that checks its own observations recovers gracefully. You won't be writing the loop from scratch; you'll be reading, running, and annotating a working trace to build the right mental model before you write your own tool-calling agent next session. Full instructions: [codebase/exercises/week-04/session-4.1/](../../codebase/exercises/week-04/session-4.1/README.md).

## Pro path

In the Pro path, you're given the same two tools but a **harder task with a hidden trap**: a request where a tool result *contradicts* an assumption baked into the question (for example, "tomorrow's umbrella weather" for a city where the tool returns clear skies — a naive system might still recommend an umbrella because the question implied it). Your job is to design the re-planning branch that makes the agent contradict the user's framing when the evidence demands it, and write a short note on what a workflow version would have to hard-code in advance to handle the same case.

---

## What's next

You now have a precise, testable definition of what makes something an agent — not vibes, but four concrete properties you can check any system against. Next session (4.2), you'll build the piece that makes the "act" phase possible at all: defining tools with schemas the model can actually call correctly, and seeing what happens when a model is given a real calculator and a real (if toy) weather tool and asked to use them. The trace you read today is the *destination*; 4.2 is where you build the machinery that produces it.
