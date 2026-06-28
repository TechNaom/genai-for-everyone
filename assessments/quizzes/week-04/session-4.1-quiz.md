# Session 4.1 Quiz — What "AI Agents" Actually Means

*6 questions. Mixed multiple-choice and short-answer.*

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
