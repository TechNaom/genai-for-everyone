# Session 1.4: Your First GenAI Application

**Week:** 1 — Foundations of GenAI & LLMs
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes

---

## Why this chapter exists

Everything so far has been building a mental model. Today, you build something that actually runs. By the end of this chapter, you will have written and run a real Python program that sends a message to an LLM API and gets a genuine response back — not a demo, not a simulation, an actual working chatbot.

This is also where a handful of conceptual gaps tend to surface for the first time — things that were invisible while we were just *talking* about LLMs, but become unavoidable the moment you have to write actual code that calls one. The biggest one, which surprises almost everyone the first time: **the model has no memory of your previous messages unless you explicitly send them again, every single time.** That single fact reshapes how you'll think about every chatbot, every API call, and every multi-turn conversation for the rest of this program.

---

## Part 1: The Three Roles — System, User, Assistant

Every message you send to a modern LLM API isn't just "text in, text out." It's structured as a sequence of labeled turns, each tagged with a **role**. Understanding these three roles is the single most important piece of mechanical knowledge in this chapter.

### The system role: setting the stage

The **system** role (sometimes called a "system prompt") is instructions from *you, the developer* — set once, defining how the model should behave for the entire conversation. It's not something the end user sees or writes; it's the stage-setting you do behind the scenes.

Think of it like the instructions you'd give a new employee on their first day: "You're a customer support agent for a software company. Be friendly but concise. If you don't know an answer, say so rather than guessing. Never discuss pricing for competitors' products." None of that came from the customer the employee will talk to — it's the operating context the employee carries into every conversation.

**Example system prompt:**
> "You are a helpful coding assistant specializing in Python. Keep explanations concise. Always include a working code example. If a question is ambiguous, ask a clarifying question before answering."

### The user role: what the human actually says

The **user** role is the live, real input from the actual person using your application — the question they typed, the message they sent. This is the part that changes every single turn of a real conversation.

**Example user message:**
> "How do I read a CSV file in Python?"

### The assistant role: what the model said back

The **assistant** role represents the model's own previous responses. This matters more than it might seem at first, because of something we're about to cover in Part 2: when you're building a multi-turn conversation, you don't just send the system prompt and the latest user message — you send the *entire history*, including everything the assistant said in earlier turns, every single time.

### Putting the three roles together

A real API request, simplified, looks conceptually like this:

```
system:    "You are a helpful coding assistant specializing in Python..."
user:      "How do I read a CSV file in Python?"
assistant: "You can use the built-in csv module, or pandas for more powerful..."
user:      "Show me the pandas version."
```

That whole block — all four entries — gets sent together, every time, even though only the last line is "new." This is the part that catches almost everyone off guard the first time they build something real.

---

## Part 2: The Single Most Important Mechanical Fact — Statelessness

Here it is, stated as plainly as possible: **the model does not remember your previous messages on its own.** Each API call is independent. If you want the model to "remember" what was said three messages ago, *you* — the developer — have to include that entire earlier conversation in every new request you send.

### Why this surprises people

When you use a chat app like Claude.ai or ChatGPT, it *feels* like you're having a continuous conversation with persistent memory. That feeling is an illusion carefully maintained by the application layer, not a property of the model itself. Behind the scenes, every single time you send a new message in that chat window, the application is silently re-sending the *entire conversation history* — every previous user message and every previous assistant response — bundled together with your new message, as one fresh request. The model receiving that request has no idea it's "the same conversation" in any deeper sense; it's simply being handed a long block of text (formatted with those role labels) and asked to predict what should come next, exactly as we covered in Session 1.1 and 1.2.

### Why this matters practically, right now

When you build your own chatbot today, *you* are responsible for doing what the chat app normally does invisibly: maintaining a running list of the conversation so far, and sending that entire list with every new request. If you forget to do this — if you only ever send the latest message — your chatbot will have no memory of anything said previously, and it will feel broken and disjointed, even though the model itself is working exactly as designed.

### The analogy: a brilliant consultant with no memory between meetings

Imagine hiring a brilliant consultant who is genuinely excellent at their job — but who has zero memory between meetings. Every single time you meet with them, you have to hand them a full written transcript of every previous meeting before they can pick up where you left off. If you forget to hand over that transcript, they'll greet you like a stranger and have no idea what you discussed last time, even if it was five minutes ago. That's not a flaw in the consultant's intelligence — it's just how their memory works, and it's entirely on you to compensate for it by bringing the transcript every time. This is *exactly* how working with an LLM API works, and once this analogy clicks, building a coherent multi-turn chatbot stops being mysterious.

---

## Part 3: The Request-Response Cycle, End to End

Let's walk through exactly what happens when your code "talks" to an LLM, since this demystifies what's otherwise a black box.

1. **Your code constructs a request** — a structured list of role-tagged messages (system, then alternating user/assistant turns, ending with the newest user message) — and sends it to the provider's API over the internet, usually as JSON.

2. **The provider's servers receive that request**, run the actual model (the tokenize → embed → predict loop from Session 1.2) using everything in that request as context, and generate a response.

3. **The response comes back to your code**, also as structured JSON — not just raw text, but a data structure containing the generated text plus metadata (which model was used, how many tokens were consumed, why the response stopped, and more).

4. **Your code extracts the actual text** from that structured response and does something with it — prints it to the screen, displays it in a web page, speaks it aloud, whatever your application needs.

5. **If the conversation continues, your code appends both the user's new message AND the assistant's response to its own running history**, so the *next* request includes everything that came before — closing the loop described in Part 2.

This cycle, repeated, is the entirety of how every chatbot you've ever used actually works under the hood. There's no hidden magic beyond what you'll build yourself in today's exercise.

---

## Part 4: A Realistic Mistake, Worked Through

Here's a mistake almost every beginner makes once, and recognizing it now will save you real debugging time later.

**The setup:** You build a simple chatbot. The first exchange works great. The user asks a follow-up question that depends on the previous answer — something like "can you make that shorter?" — and the model responds as if it has no idea what "that" refers to, sometimes asking "shorter version of what?"

**What went wrong:** Almost certainly, the code is only sending the user's latest message on each request, not the full conversation history. The model isn't being forgetful or confused in some deep sense — it genuinely never received the earlier exchange at all. From its perspective, "make that shorter" arrived as a completely standalone, contextless message, because that's literally all it was given.

**The fix:** Maintain a list (in code, often literally a Python list of dictionaries) representing the conversation so far. Every time you get a new user message, append it to that list. Every time you get a response back, append *that* too. Send the entire growing list with every new request. This is precisely what you'll implement in today's exercise.

---

## Points to Remember

- **Every request to an LLM API is structured with roles**: system (developer instructions, set once), user (the live human input), and assistant (the model's own previous responses).
- **The model has no memory between API calls on its own.** Any sense of "continuous conversation" is something your application code creates, by re-sending the entire conversation history with every new request.
- **The illusion of persistent memory in chat apps like Claude.ai or ChatGPT is maintained by the application layer**, not the model itself — every new message you send silently includes everything said before it.
- **The request-response cycle is: construct a role-tagged request → send it → receive structured JSON back → extract the text → append both the new user message and the new assistant response to your running history for next time.**
- **The most common beginner bug** is forgetting to maintain and resend conversation history, which makes a chatbot seem "forgetful" even though the model is behaving exactly as designed.

---

## Quick Check: Fill in the Blanks

1. The __________ role holds developer instructions set once for the whole conversation, while the __________ role holds the live human input.
2. The model does not remember previous messages on its own — this property is called __________.
3. The illusion of persistent memory in chat apps is created by the __________ layer re-sending the full conversation __________ with every new message.
4. A response from an LLM API comes back as structured __________, not just raw text — it includes metadata like which model was used and why the response stopped.
5. The most common beginner chatbot bug is forgetting to maintain and resend the conversation __________, which makes the model seem forgetful even though it's working as designed.

**Answers:** 1. system, user — 2. statelessness (or being stateless) — 3. application, history — 4. JSON (or data/a data structure) — 5. history

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-01/session-1.4-quiz.md`](../../assessments/quizzes/week-01/session-1.4-quiz.md) · Answer key: [`assessments/answer-keys/week-01/session-1.4-quiz-answers.md`](../../assessments/answer-keys/week-01/session-1.4-quiz-answers.md)

Interview-style questions for this topic:

1. *"Walk me through what happens, end to end, when your code sends a message to an LLM API and gets a response back."*
2. *"What's the difference between the system prompt, the user prompt, and the assistant's previous responses in a chat application?"*
3. *"A junior developer is confused why their chatbot 'forgets' context after just one exchange. What's the likely bug, and how would you explain it to them?"*
4. *"Why does a chat app like Claude.ai or ChatGPT feel like it has persistent memory, when the underlying model is stateless?"*
5. *"What's actually inside the response your code receives from an LLM API call, beyond just the generated text?"*

---

## Core path — guided activity

**Working CLI Chatbot.** You'll build a command-line chatbot in Python that correctly maintains conversation history across multiple turns — so a follow-up question like "make that shorter" actually works. Full instructions and starter code: [`codebase/exercises/week-01/session-1.4/`](../../codebase/exercises/week-01/session-1.4/).

## Pro path — extended challenge

You're given a broken chatbot script with the exact "forgetful" bug described in Part 4. You'll diagnose the bug from the code alone (not just from watching it run), fix it, then add a feature: a `/reset` command that clears conversation history without exiting the program — testing whether you understand exactly *what* the history list represents and *when* it's safe to clear it.

## What's next

Session 1.5 — **Limitations, Hallucination & Bias** — goes deeper into why even a correctly-built application like today's can still confidently produce wrong information, and what that means for how you should design around it.
