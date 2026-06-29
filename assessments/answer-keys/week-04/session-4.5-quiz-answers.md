# Session 4.5 Quiz Answers and Grading Guide

---

## Question 1: Simple Automation vs. Agents

**Answer:** B) When the task is predictable and doesn't require reasoning

**Grading:**
- **Full credit (1 pt):** Answer is B
- **No credit:** Any other answer

**Explanation:** Simple automation excels at predictable, repetitive tasks (cron jobs, scheduled alerts). Agents are better for variable, reasoning-heavy tasks. Cost is secondary to the nature of the task.

---

## Question 2: Hybrid Workflow Logic

**Answer:** B) Only if the simple rule is unsure

**Grading:**
- **Full credit (1 pt):** Answer is B
- **No credit:** Any other answer

**Explanation:** Hybrid workflows use rules first (cheap/fast) and only call agents when rules can't decide. This optimizes cost while maintaining quality.

---

## Question 3: Cost Comparison

**Answer:** Hybrid approach. 10x cheaper than agent-only, nearly as accurate.

**Grading:**
- **Full credit (1 pt):** Correctly identifies hybrid, explains it's cheaper and almost as accurate
- **Partial credit (0.5 pts):** Chooses hybrid but reasoning is weak
- **No credit:** Chooses agent-only (too expensive) or rules-only (too inaccurate)

**Acceptable reasoning:**
- "Hybrid is sweet spot: cost vs. accuracy"
- "Rules handle 95% of cases, agent handles edge cases"
- "Agent-only is wasteful; rules-only misses cases"

---

## Question 4: Workflow Debugging

**Answer:** Test each step independently. Isolate which step is slow (rule check, agent call, or action execution), then optimize or parallelize.

**Grading:**
- **Full credit (1 pt):** Tests steps independently AND identifies optimization strategy
- **Partial credit (0.5 pts):** Tests steps but no optimization plan, OR has optimization but vague testing
- **No credit:** "Just make it faster" with no debugging plan

**Acceptable answers:**
- "Benchmark each step separately"
- "Log timing for each phase"
- "Parallelize if possible"
- "Replace slow step with faster alternative"

---

## Question 5: Scheduled vs. Real-Time Agents

**Answer:** Scheduled agent (once/week). Feedback analysis is batched, not reactive.

**Grading rubric (2 pts):**
| Points | Criteria |
|--------|----------|
| 2 pts | Correctly chooses **scheduled agent**, explains why (batched, weekly cadence, cost-effective) |
| 1.5 pts | Chooses scheduled agent with weak reasoning |
| 1 pt | Chooses real-time agent but acknowledges cost (defensible but not ideal) |
| 0.5 pts | Chooses an option but reasoning is unclear |
| 0 pts | No answer or wrong choice without reasoning |

**Good reasoning:**
- "Weekly batching doesn't need real-time; scheduled agent is cheaper"
- "One agent per week = $0.01; real-time per feedback would be $10+/week"
- "Feedback can wait for weekly synthesis"

**Acceptable alternatives:**
- Hybrid: real-time rule to flag critical feedback, scheduled agent for summary (defensible)

---

## Question 6: Human-in-Loop Design

**Answer:** Human review catches errors, builds trust, enables learning, ensures high-stakes decisions are approved before acting.

**Grading rubric (2 pts):**
| Points | Criteria |
|--------|----------|
| 2 pts | Clearly explains **advantage** (safety, trust, audit trail, error catch) AND acknowledges **trade-off** (slower, but worth it) |
| 1.5 pts | Lists advantages but doesn't address trade-off |
| 1 pt | Mentions human-in-loop is safer, but no detail |
| 0.5 pts | Vague answer about "being careful" |
| 0 pts | Doesn't address the question |

**Good answers:**
- "Safety: humans catch agent mistakes before customers see them"
- "Accountability: audit trail of who approved what"
- "Learning: humans review agent outputs, improve prompts"
- "Trust: customers trust systems with human oversight"

---

## Grading Summary

| Question | Type | Points |
|----------|------|--------|
| 1 | MC | 1 |
| 2 | MC | 1 |
| 3 | Short | 1 |
| 4 | Short | 1 |
| 5 | Scenario | 2 |
| 6 | Scenario | 2 |
| **Total** | | **8** |

---

## Common Misconceptions to Watch For

1. **"Agents are always better"** — No. Simple automation is faster, cheaper, and good enough for predictable tasks.
2. **"Hybrid is complex"** — It's not. Just: rule → agent if unsure → done.
3. **"Cost doesn't matter"** — It does. $0.50 per query at 1M queries/year = $500k.
4. **"Humans slow things down"** — Yes, but they prevent costly mistakes. Trade-off worth making.
5. **"Scheduled = always slower"** — Not if you batch. Weekly agent beats real-time for non-urgent tasks.

---

*Session 4.5 Answer Key | GenAI for Everyone | Week 4*
