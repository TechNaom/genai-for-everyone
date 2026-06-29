# Session 4.4 Quiz Answers and Grading Guide

---

## Question 1: Orchestrator-Worker Pattern

**Answer:** B) Coordinate task distribution and synthesize results

**Grading:**
- **Full credit (1 pt):** Answer is B
- **Partial credit (0.5 pts):** Answer is B but explanation is vague
- **No credit:** Any other answer

**Why:** The orchestrator's job is to break down tasks, assign them to workers, and integrate results. Workers execute; orchestrators manage flow.

---

## Question 2: When to Use Debate Pattern

**Answer:** C) You want to explore multiple perspectives and surface trade-offs

**Grading:**
- **Full credit (1 pt):** Answer is C
- **No credit:** Any other answer

**Why:** Debate is for exploring disagreement and nuance, not for speed (A is wrong) or simple tasks (B is wrong). Cost is secondary to value (D is wrong).

---

## Question 3: Reviewer Pattern Trade-offs

**Answer:** Higher quality output (more reviewers catch errors), but slower and more expensive (multiple API calls). Trade latency and cost for quality.

**Grading:**
- **Full credit (1 pt):** Student identifies both:
  - Benefit: quality improvement
  - Cost: latency/expense
- **Partial credit (0.5 pts):** Mentions one side but not both
- **No credit:** Misses the trade-off or is wrong

**Acceptable variations:**
- "Multiple reviewers find more bugs, but each call costs money and takes time"
- "Better output but slower and pricier"
- "Quality vs. cost/speed trade-off"

---

## Question 4: Convergence Checking

**Answer:** B) Feedback stops changing (reviewers are giving similar feedback)

**Grading:**
- **Full credit (1 pt):** Answer is B
- **No credit:** Any other answer

**Why:** Convergence means the feedback pattern has stabilized; further revisions likely won't improve much. It's a stopping condition for loops.

---

## Question 5: Communication Between Agents

**Answer:** Agents need to understand each other's output format. Unstructured prose feedback can be ambiguous or hard to parse. Structured formats (e.g., JSON with specific fields) make feedback actionable and reduces confusion.

**Grading:**
- **Full credit (1 pt):** Student explains why structure matters (clarity, parsability, actionability)
- **Partial credit (0.5 pts):** Mentions structure is important but weak explanation
- **No credit:** Misses the point or says structure doesn't matter

**Acceptable variations:**
- "Agents need consistent formats to understand each other"
- "Prevents misunderstandings, makes feedback actionable"
- "Structured > prose for machine readability and clarity"

---

## Question 6: Scenario - Choose Pattern and Justify

**Model answer:**
Reviewer pattern (writer + three critics: accuracy/fact-checker, engagement/style-checker, brand-voice/brand-checker). Each reviewer specializes in their domain and catches different errors. The writer revises based on aggregate feedback. This is expensive but produces high-quality copy where accuracy, engagement, and brand consistency all matter.

**Grading rubric (2 pts total):**

| Points | Criteria |
|--------|----------|
| 2 pts | Correctly identifies **reviewer pattern**, explains why it fits (quality > cost), and identifies appropriate reviewers |
| 1.5 pts | Identifies reviewer pattern and explains trade-off, but reviewers are generic or not well-justified |
| 1 pt | Identifies a pattern (any of the three), explains why, but it's not the strongest choice |
| 0.5 pts | Identifies a pattern but reasoning is weak or incomplete |
| 0 pts | Wrong pattern or no justification |

**Acceptable alternatives:**
- Orchestrator + writer + fact-checker agents (less ideal but defensible)
- Debate between brand voice and engagement (less ideal; both matter equally)

---

## Grading Summary

| Question | Type | Points |
|----------|------|--------|
| 1 | MC | 1 |
| 2 | MC | 1 |
| 3 | Short | 1 |
| 4 | MC | 1 |
| 5 | Short | 1 |
| 6 | Scenario | 2 |
| **Total** | | **7** |

---

## Common Misconceptions to Watch For

1. **"Orchestrator = the smartest agent"** — No, it's just the coordinator. Workers do specialized work.
2. **"More agents = always better"** — No, more agents = more cost/latency. Only add if value justifies it.
3. **"Debate pattern is for disagreements"** — Not exactly. It's for exploring perspectives, even when there's no "right" answer.
4. **"Convergence means all agents agree"** — No, it means feedback patterns stop changing; agents can still disagree.

---

*Session 4.4 Answer Key | GenAI for Everyone | Week 4*
