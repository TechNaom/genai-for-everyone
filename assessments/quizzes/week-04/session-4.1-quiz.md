# Session 4.1 Quiz — What "AI Agents" Actually Means

*6 questions. Mixed multiple-choice and short-answer. Answer key included below — no peeking until you've tried each one.*

---

**1. (Multiple choice)** Which of the following is the most accurate one-sentence definition of an agent, as used in this course?

A. Any system that uses a large language model
B. A system where a human writes a fixed sequence of steps, one of which calls an LLM
C. A system where a language model decides what to do next, based on what just happened, repeatedly, toward a goal
D. A chatbot that remembers previous messages in the conversation

---

**2. (Multiple choice)** A company builds a system that always runs these three steps in this exact order: (1) summarize an incoming email with an LLM, (2) classify the summary's sentiment with a second LLM call, (3) if sentiment is negative, forward to a human — otherwise auto-reply. Which best describes this system?

A. An agent, because it uses two LLM calls
B. A workflow, because the sequence and the branching condition were both fixed in advance by a programmer
C. A chatbot, because it replies to emails
D. Not a real system, because it has a branch

---

**3. (Short answer)** Name the three repeating phases of the agent loop described in this chapter, in order.

---

**4. (Short answer)** In the umbrella/weather trace from the chapter, the rigid workflow crashed when run on a city not in the weather database. Explain *in your own words* why it crashed, and explain specifically what the reactive agent version did differently in that same situation.

---

**5. (Multiple choice)** According to the test proposed in the chapter ("if you replaced the model's decision points with a human-designed flowchart, would the system behave differently on an unanticipated case?"), which answer indicates a system is **genuinely agentic**?

A. "No" — it would behave the same either way
B. "Yes" — it would behave differently, because the model is reacting to something the flowchart's designer didn't plan for
C. It doesn't matter, since all LLM-based systems are agents by definition
D. The test only applies to multi-agent systems

---

**6. (Short answer)** The chapter argues that most production systems should be "mostly workflow, with a small, carefully-scoped agentic piece." Give one practical reason why a team might *not* want to make an entire system fully agentic, even if it's technically possible.

---
---

## Answer Key

**1. C** — An agent is defined by the model deciding what to do next based on what just happened, repeatedly, toward a goal, without a human choosing each step. (A) is too broad — it would include plain chatbots. (B) describes a workflow. (D) describes a stateful chatbot, which is still single-turn-reactive per turn and has no action/observation loop.

**2. B** — Every step and the branching condition ("if sentiment is negative...") were decided by a programmer in advance. The LLM is doing the summarizing and classifying, but it isn't deciding *what sequence of actions to take* — that's fixed. This is the textbook example of a workflow that uses LLMs without being an agent.

**3. Plan, Act, Observe** (in that order, repeating). Some students may name ReAct's "Thought, Action, Observation" — accept this as equivalent phrasing.

**4. Sample answer:** The rigid workflow always tried to read a `chance_of_rain_pct` field from the weather tool's result, assuming that field would always be present. When the city wasn't in the database, the tool returned an `{"error": ...}` dictionary instead, which has no `chance_of_rain_pct` key — so the line that tried to read it raised a `KeyError` and crashed. The reactive agent, by contrast, checked whether the result contained an `"error"` key *before* deciding what to do next. When it found one, it changed its plan: instead of trying to report a rain percentage, it told the user honestly that no data was available. The key difference is that the agent's next step was chosen based on what it actually observed, while the workflow's next step was fixed regardless of what came back.

**5. B** — A genuinely agentic system can react to cases the designer didn't specifically plan for, because the decision-making lives in the model's run-time reasoning rather than in pre-written branches. If swapping in a flowchart wouldn't change behavior even on unanticipated cases, the system was really just following a fixed script — i.e., a workflow.

**6. Sample answers (any one is sufficient):** Full agentic systems are less predictable and harder to test exhaustively, since you can't enumerate every path the model might take. They can also be slower and more expensive (more model calls per task), and they introduce new failure modes — like infinite loops, calling the wrong tool, or taking an action you didn't intend — that a fixed workflow simply can't exhibit because every path through it was specified in advance. For most business problems, a workflow that calls an LLM at a few points is more reliable and cheaper to operate than a fully autonomous agent, and should be preferred unless the task genuinely requires the model to handle situations that can't be enumerated ahead of time.
