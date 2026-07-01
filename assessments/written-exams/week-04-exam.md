# Week 4 Written Exam

_Deeper, scenario-based exam covering all of Week 4's sessions (4.1–4.6): what agents actually are, function/tool calling, multi-step task agents, multi-agent patterns, automation vs. agents, and the research-agent capstone._

**Format:** 7 short-answer questions + 3 scenario-analysis questions + 1 synthesis question
**Suggested time:** 60–75 minutes
**Open book:** Yes — this tests understanding and application, not memorization

---

## Section A — Short Answer

**A1.** Define the "agent loop" (plan → act → observe) in your own words, and explain what specifically distinguishes an agent from a single-turn chatbot response.

**A2.** When an LLM "calls a tool," it doesn't actually execute anything itself. Explain precisely what the model outputs, and what has to happen next for the tool to actually run.

**A3.** Why does a tool's schema (its defined arguments and their types/descriptions) matter for reducing hallucination, specifically?

**A4.** Name two distinct stopping conditions an agent loop could use to know it's done, and explain a failure mode that occurs when a stopping condition is missing or too loose.

**A5.** Describe the difference between the orchestrator-worker pattern and the reviewer pattern in multi-agent systems, and give one example task better suited to each.

**A6.** A teammate wants to use a multi-step agent for a task that's actually a fixed, predictable, high-frequency operation (e.g., "send this exact reminder email every Monday"). Explain why simple automation is the better choice here, and what specifically about agents makes them worse for this case (beyond just "cost").

**A7.** What does it mean for an agent's output to be "grounded," and why is a citation-tracking fact-checking step (as in the Week 4 lab) not just a nice-to-have for a research agent specifically?

---

## Section B — Scenario Analysis

**B1. The Agent That Won't Stop**
Your research agent is on iteration 18 of a loop, still calling the same search tool with slightly reworded queries, and shows no sign of stopping. Diagnose the likely root cause(s), and propose at least two concrete fixes — one that addresses the immediate symptom, and one that addresses why the agent didn't recognize it already had enough information.

**B2. The Tool the Model Invented**
Your agent's schema defines three tools: `search_web`, `get_page_content`, and `evaluate_source`. In production, the model outputs a tool-call request for a tool named `verify_facts`, which doesn't exist in your schema. Explain why this happened, what your system should do when it receives this request, and one change to your schema or prompt that would reduce the odds of it happening again.

**B3. The Multi-Agent System That Disagreed With Itself**
You built a reviewer-pattern system for legal document summaries: a writer agent drafts a summary, and a fact-checker agent flags claims it can't verify against the source document. On a real contract, the writer agent's summary and the fact-checker's flags directly contradict each other — the fact-checker claims a clause was omitted that the writer insists it included. Explain how you'd resolve this conflict in your system design, and why "just trust the fact-checker, it's the safety layer" isn't automatically the correct default in every disagreement like this.

---

## Section C — Synthesis

**C1.** You're asked by a non-technical stakeholder: "Why does this agent-based feature cost so much more per request than our old simple chatbot?" Write a 150–250 word explanation, in plain language, that:
- Explains what specifically an agent does that a single-turn chatbot response doesn't (multiple LLM calls, tool use, iteration)
- Names one concrete lever (from Session 4.5/4.6's thinking, e.g., when agents vs. automation are appropriate, or caching/routing from later weeks) that could reduce this cost without abandoning the agent approach entirely
- Is honest about the trade-off rather than either over-defending the cost or promising an unrealistic fix

---

## Answer Key

### Section A

**A1.** The agent loop is: the agent plans what to do next, takes an action (often calling a tool), and observes the result, then repeats — using each observation to inform the next plan/action — until a stopping condition is met. This differs from a single-turn chatbot response because a chatbot produces one response to one input and stops; an agent can take multiple actions across multiple iterations, incorporating real-world feedback (tool results) between them, before producing a final answer.

**A2.** The model outputs a structured "tool use" request — specifying which tool it wants called and with what arguments — as part of its response, rather than any executable code or a real API call. The system running the agent then has to parse that structured request, actually invoke the corresponding real function/API, capture the result, and feed that result back into the conversation as a "tool result" before the model can continue.

**A3.** A clear, well-typed schema (specific argument names, types, and descriptions) constrains what the model can plausibly generate as a tool call, reducing the chance it invents malformed arguments, hallucinates parameters that don't exist, or misuses the tool in a way that produces garbage input — the schema acts as a guardrail on the model's own output, similar to how structured-output prompting (Week 2) reduces hallucination in generated JSON.

**A4.** Any two of: (1) the model's response contains no further tool-use requests (only text) — signaling it believes it's done; (2) a hard iteration limit is reached as a safety net; (3) an explicit convergence check in multi-agent systems (e.g., reviewer feedback stabilizes). Missing or too-loose stopping conditions cause the agent to loop indefinitely or excessively — repeatedly calling tools, burning cost and time, often on marginally-reworded queries that don't add new information.

**A5.** Orchestrator-worker decomposes a task into independent (or partially independent) sub-tasks, assigns them to specialized worker agents, and synthesizes their results — well suited to tasks that naturally split into parallel, distinct pieces of work (e.g., researching multiple countries' regulations). The reviewer pattern has one agent produce output and a second agent critique/verify it against a standard (facts, safety, quality) before finalizing — well suited to tasks where the risk of an unchecked error is high and a second, differently-focused pass adds real value (e.g., legal document review, fact-checking a research report).

**A6.** Simple automation is better here because the task requires no reasoning, no variable input handling, and no tool-use decision-making — it's the same fixed action every time. Agents add unnecessary latency, cost (multiple LLM calls per run), and a new source of failure (the model could reason its way into skipping the email, rewording it unpredictably, or looping) for a task that a scheduled script handles perfectly reliably and far more cheaply. The core issue isn't just cost — it's that agents are built for situations requiring judgment under uncertainty, and this task has none.

**A7.** A grounded output is one that's demonstrably based on real, verifiable information the agent actually retrieved or was given — not on the model's unaided generation. A citation-tracking fact-checking step matters specifically for a research agent because the entire value of the output is its claimed factual accuracy; without grounding and verification, a fluently written research report with fabricated statistics or misattributed sources is actively worse than no report at all, since it's indistinguishable in tone from a well-researched one.

---

### Section B

**B1.** Likely root causes: no explicit stopping condition beyond "keep searching until satisfied" (vague success criteria), and/or the agent isn't tracking what it's already searched for, so slightly reworded queries look like new ground to cover. Fix 1 (immediate symptom): add a hard iteration limit as a safety net, and/or explicit logic detecting near-duplicate queries to block repeated searches. Fix 2 (root cause): improve the prompt/planning step with an explicit, checkable success criterion (e.g., "stop once you have found information addressing each of your 3 planned research questions") and maintain working memory of what's already been searched so the agent can recognize it already has sufficient coverage.

**B2.** This happens because the model is pattern-matching on the *concept* of "fact verification" from its training data and generating a plausible-sounding tool name that doesn't actually exist in the schema it was given — likely because the system prompt or task framing implied a verification step without the schema explicitly listing all available tools clearly enough. The system should reject the unknown tool-use request gracefully (return a clear error like "tool not available" rather than crashing), not attempt to guess what the model meant. A schema/prompt fix: explicitly list all available tools in the system prompt as a numbered set of options, and/or add a tool description that clarifies fact-checking happens through `evaluate_source`, not a separate function, closing the gap that led the model to invent one.

**B3.** Resolving this requires a human review step for direct contradictions rather than automatically defaulting to either agent's claim — a well-designed reviewer-pattern system should route genuine disagreements to a human, not silently pick a winner, because "trust the fact-checker by default" can itself introduce errors if the fact-checker's own verification process is flawed (e.g., missed the clause due to its own retrieval/reading limitation) just as easily as the writer's could be. The reason it's not automatically correct to always trust the safety layer is that the safety layer is still a model subject to the same kinds of misses and hallucinations as the primary agent — treating it as infallible just relocates the trust problem rather than solving it.

---

### Section C

**C1.** Sample model answer (grade for content, not exact wording):

> Our agent-based feature does more work per request than the old chatbot: instead of one model call producing one answer, the agent may plan its approach, call search or other tools multiple times, read and evaluate the results, and then compose a final answer — often 4-8 separate model calls where the old system made one. Each of those calls costs money and takes time, which is why the per-request cost is higher. One concrete way to reduce this without giving up the agent approach: route simpler requests to a cheaper, faster model and reserve the full multi-step agent process for genuinely complex ones, since not every request actually needs the full research workflow. This won't get us back to the old chatbot's cost — the extra reasoning is exactly what makes the feature more capable — but it does mean we're not overpaying on the requests that didn't need it.

**Full credit (15 pts):** Explains the multiple-calls-per-request mechanism clearly [6 pts], names a concrete, relevant cost lever [5 pts], and is honest about the trade-off rather than overselling a fix [4 pts].
**Partial credit:** Missing the honest trade-off framing, or naming a vague lever ("just optimize it") without specifics.

---

## Grading Guidance

- **Section A (21 pts, 3 pts each):** Full credit requires the correct mechanism *and* a "why it matters" connection, not just a definition.
- **Section B (24 pts, 8 pts each):** Grade holistically — award strong credit for correctly diagnosing the *category* of failure (stopping-condition design, schema/prompt clarity, or trust/verification design) even if the specific proposed fix differs from the model answer, provided the reasoning is sound.
- **Section C (15 pts):** See rubric above.
- **Total: 60 pts.** Suggested cutoffs: 54+ = excellent, 42–53 = solid, 30–41 = needs review (revisit which session cluster the missed questions trace to — tool calling/4.2, multi-step agents/4.3, or multi-agent patterns/4.4), <30 = recommend revisiting Week 4 sessions before Week 5.
