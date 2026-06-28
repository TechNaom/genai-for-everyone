# Session 4.1 Quiz — Answer Key

*Answer key for [session-4.1-quiz.md](../../quizzes/week-04/session-4.1-quiz.md).*

---

**1. C** — An agent is defined by the model deciding what to do next based on what just happened, repeatedly, toward a goal, without a human choosing each step. (A) is too broad — it would include plain chatbots. (B) describes a workflow. (D) describes a stateful chatbot, which is still single-turn-reactive per turn and has no action/observation loop.

**2. B** — Every step and the branching condition ("if sentiment is negative...") were decided by a programmer in advance. The LLM is doing the summarizing and classifying, but it isn't deciding *what sequence of actions to take* — that's fixed. This is the textbook example of a workflow that uses LLMs without being an agent.

**3. Plan, Act, Observe** (in that order, repeating). Some students may name ReAct's "Thought, Action, Observation" — accept this as equivalent phrasing.

**4. Sample answer:** The rigid workflow always tried to read a `chance_of_rain_pct` field from the weather tool's result, assuming that field would always be present. When the city wasn't in the database, the tool returned an `{"error": ...}` dictionary instead, which has no `chance_of_rain_pct` key — so the line that tried to read it raised a `KeyError` and crashed. The reactive agent, by contrast, checked whether the result contained an `"error"` key *before* deciding what to do next. When it found one, it changed its plan: instead of trying to report a rain percentage, it told the user honestly that no data was available. The key difference is that the agent's next step was chosen based on what it actually observed, while the workflow's next step was fixed regardless of what came back.

**5. B** — A genuinely agentic system can react to cases the designer didn't specifically plan for, because the decision-making lives in the model's run-time reasoning rather than in pre-written branches. If swapping in a flowchart wouldn't change behavior even on unanticipated cases, the system was really just following a fixed script — i.e., a workflow.

**6. Sample answers (any one is sufficient):** Full agentic systems are less predictable and harder to test exhaustively, since you can't enumerate every path the model might take. They can also be slower and more expensive (more model calls per task), and they introduce new failure modes — like infinite loops, calling the wrong tool, or taking an action you didn't intend — that a fixed workflow simply can't exhibit because every path through it was specified in advance. For most business problems, a workflow that calls an LLM at a few points is more reliable and cheaper to operate than a fully autonomous agent, and should be preferred unless the task genuinely requires the model to handle situations that can't be enumerated ahead of time.
