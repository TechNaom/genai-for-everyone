# Session 4.2 — Function/Tool Calling

## Part 1: Giving the model real hands

Session 4.1 left you with a precise definition of an agent — a system where the model decides what to do next, based on what just happened, repeatedly, without a human choosing each step — and a trace you ran by hand, with the model's decisions scripted rather than real. That honesty mattered: nothing in that trace was actually decided by a live model. The `calculator` and `weather_lookup` functions were real, executable code, but the *choice* of when to call them was written by a human in advance, standing in for what a model would plausibly decide.

Today, that stand-in disappears. You're going to give an actual LLM real tools, and watch it genuinely decide — on its own, from the conversation alone — when to reach for one. This is the moment the "act" step of the agent loop stops being something you simulate and becomes something you build for real.

Here's the mental model worth holding onto from the start: **tool calling does not let the model run code.** A language model is fundamentally a text generator. It cannot reach out and execute a Python function, query a database, or hit an API on its own — it has no hands, no permissions, no execution environment of any kind. What tool calling actually gives the model is something narrower and, once you see it clearly, much less mysterious: a structured way to say "I want you to run this specific function, with these specific arguments" — and then it's entirely on your code to actually run it and report back what happened.

This matters because it reframes the whole topic. You are not teaching a model a new superpower. You are building a very specific, very deliberate communication protocol between a model that can reason but can't act, and your code, which can act but can't reason about *when* to. Tool calling is the bridge between those two halves.

---

## Part 2: The three things every tool needs

When you hand a model a tool, you're not handing it code — you're handing it a *description* of code: a name, an explanation of what it does, and a precise specification of what inputs it needs. The model never sees your function's implementation at all. It only ever sees these three things, and it has to decide when and how to call the tool based on nothing else.

**A name.** Short, specific, and unambiguous — `get_weather`, not `helper2`. The model uses this name both to refer to the tool internally and, often, as a signal about what the tool is for. A vague name produces vague reasoning about when to use it.

**A description.** This is the single highest-leverage piece of a tool definition, and it's worth treating with the same care you gave prompt design back in Week 2 — because that's exactly what it is, a prompt, just one the model reads to make a single decision rather than to generate a long response. A good description says what the tool does, and just as importantly, *when* to use it: "Get the current weather for a city. Use this when the user asks about weather conditions, temperature, or whether they'll need an umbrella." A vague description — "weather tool" — leaves the model guessing both about the tool's behavior and about whether this question even calls for it.

**An input schema.** This is a precise, machine-readable specification of exactly what arguments the tool needs, and what shape they should take — typically expressed as JSON Schema, the same kind of structured-format thinking you practiced in Session 2.4. A schema for a weather tool might require a `city` string and optionally accept a `units` field constrained to `"celsius"` or `"fahrenheit"`. The schema isn't decoration — it's what lets the model produce a call that your code can actually parse and execute without guessing at what it meant.

Put plainly: name tells the model *what to call it*, description tells the model *when and why to call it*, and the schema tells the model *exactly how to call it*. Get any one of the three vague, and the model's tool-calling behavior gets correspondingly unreliable — not because the model is bad at the task, but because you've under-specified the contract, in exactly the way Session 2.1 warned you an under-specified prompt produces an under-specified answer.

---

## Part 3: What actually happens when a model "calls" a tool

Here's the full round trip, made concrete, because the mechanics matter more than they might seem to at first glance.

1. You send the model a message, along with a list of tool definitions (name, description, schema) it's allowed to use.
2. The model reads the conversation and decides: does answering this require a tool? If yes, which one, and with what arguments?
3. If it decides to use a tool, the response you get back isn't ordinary text — it's a structured signal containing the tool's name and the specific arguments the model wants to call it with, along with an identifier tying this specific call to whatever response you send back.
4. **Your code** — not the model — actually runs the real function, with those arguments.
5. You send the tool's actual output back to the model, tagged with that same identifier, as a new message in the conversation.
6. The model reads the result and continues — either calling another tool, or producing a final, natural-language answer that incorporates what the tool returned.

Step 4 is the one people skim past and shouldn't. The model never executes anything. If your weather tool would, in a real implementation, hit a live weather API, the model has no idea whether that API call succeeded, failed, or returned garbage until you tell it, explicitly, in step 5. This is exactly why the defensive instincts from Session 2.4 (validate before trusting) and Session 2.6 (plan for the failure case, not just the happy path) show up again here: a tool call that fails needs to report failure back to the model honestly, the same way `weather_lookup` in Session 4.1's exercise returned an `{"error": ...}` dict rather than silently returning nothing or crashing.

There's a structural detail worth calling out because it trips people up the first time they build this loop by hand: steps 3 through 5 have to happen in a specific order in the conversation history. The tool result message has to come immediately after the tool call message — you cannot insert anything else between an assistant's tool-use request and your reply with the result. The model is reading the conversation sequentially, the same way it reads everything else; if the result doesn't directly follow the request, the model has no reliable way to connect the two.

---

## Part 4: When does a model actually decide to call a tool?

This is the question today's chapter title promises and the one most worth sitting with, because the honest answer is less mystical than "the AI decides" makes it sound.

The model calls a tool when, based on the conversation and the tool descriptions you provided, generating a tool-call response is the most plausible continuation — the same next-token-prediction process from every other session this course has covered, just now with "call this tool" as one of the available kinds of output, alongside ordinary text. There's no separate decision-making module bolted on. It's the same model, reading the same kind of context, just with a wider menu of valid response shapes.

This has a genuinely useful practical consequence: if a model isn't calling your tool when you expect it to, or is calling it when it shouldn't, the fix almost always lives in the same place a bad-prompt fix lives — clarify the description, tighten the schema, or add an example to the conversation showing the kind of question that should trigger this tool. You're not debugging a black box. You're doing the same prompt-engineering work from Week 2, applied to a tool definition instead of a task instruction.

It's also worth being honest about a real limitation here, in the same spirit Session 3.1 insisted on for retrieval: giving a model a tool doesn't guarantee it will use the tool correctly, or at all, every single time. A model might decide a question doesn't need a tool when it actually does, might pass a slightly malformed argument, or might call a tool when a direct answer would've been better. This is precisely why today's exercise asks you to actually run the loop and inspect what happens — not just read about the theory — because seeing a real tool-call decision (and occasionally a real misfire) is the only way to build accurate intuition for when this mechanism is reliable and when it needs guardrails.

---

## Part 5: Connecting back to the agent loop

Look at where this sits inside Session 4.1's plan-act-observe framing, because today's session is best understood as filling in exactly one piece of that loop, not introducing a new one.

**Plan** is the model deciding what to do next — which, today, includes deciding whether that "next thing" is calling a tool. **Act** is the tool call itself: the structured request, your code executing it for real. **Observe** is the tool result flowing back into the conversation, ready to inform the model's next decision. Session 4.1 simulated all three steps by hand. Today, you're building "act" for real, for the first time — and as a direct consequence, "plan" and "observe" become real too, since they're now driven by an actual model's actual decisions rather than a scripted policy standing in for them.

This is also where Session 4.1's chatbot-vs-workflow-vs-agent distinction gets sharper rather than more abstract. A chatbot with no tools can only ever produce text. A rigid workflow might call a weather API and a calculator in a fixed order regardless of what's actually being asked. What you're building today — a model that looks at a real question, decides for itself whether the question needs a calculator, a weather lookup, both, or neither, and only then acts — is the first genuinely agent-shaped system this course has built where every part of that description is true at once, with a live model making the call.

---

## Points to Remember

- Tool calling does not let a model execute code. It lets the model request that *your* code execute something specific, with specific arguments — your application remains entirely responsible for actually running the operation.
- Every tool definition has three load-bearing parts: a name, a description (which doubles as a prompt the model uses to decide *when* to call the tool, not just what it does), and an input schema specifying exactly what arguments it needs.
- The full round trip is sequential and strict: the model requests a tool call, your code executes it, and the result must be sent back immediately following that request, tagged so the model can match it to the original call.
- A model decides to call a tool through the same next-token-prediction process behind everything else it generates — there's no separate "decision module." Unreliable tool-calling behavior is usually a sign the tool's description or schema needs the same clarity work as a prompt.
- A tool that fails should report the failure honestly back to the model (an error result), not crash silently or fail invisibly — the same defensive design principle from structured outputs and graceful failure design earlier in this course.
- Today's build is the first time this course has implemented the "act" step of the agent loop for real, with a live model making genuine decisions, rather than a scripted stand-in.

---

## Quick Check: Fill in the Blanks

1. A model calling a tool does not mean the model __________ the underlying code — your application is what actually runs it.
2. The three required parts of a tool definition are its name, its __________, and its input schema.
3. A tool's description functions as a kind of __________ that the model reads to decide when and why to call that specific tool.
4. After a model requests a tool call, your code must execute it and send back a __________, tagged so the model can match it to the original request.
5. If a model's tool-calling behavior is unreliable, the most likely fix is clarifying the tool's __________ or schema, the same way you'd improve an unclear prompt.
6. A tool that fails should return an honest __________ result rather than crashing or failing silently.

**Answers:** 1. executes — 2. description — 3. prompt — 4. tool result (tagged with the matching call identifier) — 5. description — 6. error

---

## Quiz and Interview Questions

Full quiz: `assessments/quizzes/week-04/session-4.2-quiz.md`

Interview-style questions for this topic:

1. "A junior engineer says, 'I gave the model a tool, so now it can run code.' What's wrong with that statement, and how would you correct it?"
2. "Walk me through what happens, step by step, between a model deciding to call a tool and that tool's result reaching the model again."
3. "Your tool-calling agent sometimes calls the wrong tool, or doesn't call a tool when it should. Where do you look first to fix this, and why?"
4. "Why does a failed tool call need to report failure back to the model explicitly, instead of just being skipped or left out of the conversation?"

---

## Core path — guided activity

**An LLM that calls a real weather/calculator tool.** You'll take the same `calculator` and `weather_lookup` functions from Session 4.1 — already real, already tested — and wire them up to an actual LLM via the Anthropic API's tool-use feature. You'll define both tools' schemas, send a real question to the model, execute whichever tool(s) it actually decides to call, and feed the results back to get a final, grounded answer. Full instructions: `codebase/exercises/week-04/session-4.2/`.

## Pro path — extended challenge

Design and add a *third* tool with a deliberately ambiguous boundary against one of the first two — something where a reasonable question could plausibly call either tool, or where a vague description would make the model's choice unpredictable. Run a handful of real questions through your three-tool setup and observe: does the model pick the tool you'd expect every time? For any case where it picks the "wrong" one (or hesitates), rewrite that tool's description to resolve the ambiguity, and verify with the same questions that the fix actually worked — don't just assume it did.

---

## What's next

Session 4.3 — Multi-Step Task Agents — where a single tool call stops being the whole story. You'll build an agent that has to plan across several sub-tasks, decide when it actually has enough information to stop, and handle a genuinely multi-step research task end to end.
