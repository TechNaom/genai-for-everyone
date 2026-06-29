# Session 4.3 Quiz: Answer Key & Grading Guidance

**Week 4 | Session 4.3**

---

## Question 1: Explicit vs. Implicit Planning

**Answer: (b)**

**Grading guidance:**
- **(b) is correct.** Explicit planning = agent writes a plan first before executing. Implicit = LLM reasons step-by-step without a formal plan upfront. Session 4.3 Part 2 covers this distinction.
- **(a)** is wrong. Speed and thoroughness depend on other factors, not just explicit vs. implicit.
- **(c)** is wrong. Tool call count isn't inherently tied to planning type.
- **(d)** is wrong. They produce different outputs and different agent behavior patterns.

**Key concept:** Understand the two planning approaches and when to use each. Explicit is better for 5+ step tasks; implicit is simpler but can loop.

---

## Question 2: Stopping Conditions

**Answer: (d) — Both (b) and (c) are good approaches.**

**Grading guidance:**
- **(d) is best.** Both rewriting the prompt (b) and adding an explicit stop tool (c) are legitimate mitigations. The best production systems use both: prompt reinforcement + a formal stopping signal.
- **(a)** Increasing iterations doesn't prevent early stopping — it just allows more iterations.
- **(b)** alone is better than nothing, but doesn't force a decision.
- **(c)** alone is good but requires prompt training for the agent to use it.

**Key concept:** Early stopping is a real risk. Mitigate by emphasizing thoroughness and/or requiring explicit stop signals. Session 4.3 Part 4 discusses stopping conditions.

---

## Question 3: Working Memory and Forgetting

**Answer: (b) — The context window is filling up.**

**Grading guidance:**
- **(b) is correct.** Long tool results consume tokens. After several iterations, the LLM may have less context left and forgets earlier findings. Session 4.3 Part 5 discusses this as "Gotcha 4."
- **(a)** Agents don't intentionally filter. They use what's in context.
- **(c)** If the prompt said this, it would be poor prompt design, but isn't the typical cause.
- **(d)** Is plausible but less likely than (b). If tool results are structured correctly, (b) is more common.

**Key concept:** Context is limited. On long tasks, implement a working memory summary to prevent forgetting. Truncate large results.

---

## Question 4: Detecting Agent Loops (Debugging)

**Expected answer:**

*Likely cause:* The agent thinks it's learning something new from each slight variation of the query, but it's actually getting similar results. This is the "looping" problem (Session 4.3 Part 5, Gotcha 1).

*How to fix:* 
- Add a stopping rule: "If you've searched for the same topic with similar queries twice, stop and summarize what you've found."
- OR: Pass a summary of prior results back to the agent each iteration (working memory).
- OR: Add diversity detection — tell the agent to only search if the query is substantially different from prior searches.

**Grading guidance:**
- Full credit (1 point): Identifies the loop problem and suggests at least one practical fix.
- Partial credit (0.5 points): Identifies the problem but fix is vague or impractical.
- No credit: Misdiagnoses or suggests impractical solutions (e.g., "use a different model").

---

## Question 5: Scenario — Multi-step Task Design

**Expected answer:**

No, 3 searches are not sufficient. The agent got pricing from each provider, but didn't:
- Compare the pricing models (per GB, per request, egress costs differ)
- Consider other factors (reliability, support, compliance)
- Define "cost-effective" for the learner's use case (small startup vs. enterprise)

The agent should add:
- Comparison searches (e.g., "AWS vs. Google Cloud cost comparison")
- Use-case searches (e.g., "cloud storage for startups vs. enterprises")
- A final synthesis step before stopping.

**Grading guidance:**
- Full credit (1 point): Recognizes that 3 searches alone are insufficient and explains why. Suggests additional steps.
- Partial credit (0.5 points): Identifies a gap but doesn't fully explain or suggest fixes.
- No credit: Says 3 searches are sufficient or doesn't address the multi-step reasoning.

**Key concept:** Multi-step agents need to verify sufficiency, not just execute a fixed number of steps.

---

## Question 6: Iterative Refinement

**Expected answer:**

*Likely reason:* The finding might be in the tool results but got lost during message construction, or the LLM didn't recognize it as important and didn't include it in the summary.

*Two debugging approaches:*
1. **Inspect the messages:** Print all messages sent to the LLM before the final summary. Check if the missing finding is present in the context.
2. **Trace the finding:** Search for the missing fact in the working memory / tool results. If it's there, it's a prompt/summarization issue. If it's not, it's a search/extraction issue.

**Alternative fixes:**
- Add a reflection step: After each tool call, ask the agent to explicitly note "Key finding: ..."
- Restructure the final prompt to require mentioning all findings.

**Grading guidance:**
- Full credit (1 point): Identifies the likely reason and provides 2 specific debugging approaches (not generic suggestions).
- Partial credit (0.5 points): Identifies reason but debugging approaches are vague.
- No credit: Misdiagnoses or suggests unhelpful solutions.

**Key concept:** Session 4.3 Part 5 covers debugging patterns. Systematic inspection of messages and working memory is key.

---

## Summary

| Question | Topic | Difficulty |
|----------|-------|------------|
| 1 | Explicit vs. implicit planning | Easy |
| 2 | Stopping conditions | Medium |
| 3 | Context & forgetting | Medium |
| 4 | Loop detection & fixes | Hard |
| 5 | Multi-step reasoning | Hard |
| 6 | Debugging | Hard |

**Passing threshold:** 5/6 or 4/6 with full credit on at least 2 hard questions.

**If learner struggles:**
- Q1-Q2 struggles: Re-read Session 4.3 Part 2 & 4.
- Q3-Q4 struggles: Re-read Session 4.3 Part 5 (gotchas and debugging).
- Q5-Q6 struggles: Practice building agents on more complex tasks. Test on real APIs.
