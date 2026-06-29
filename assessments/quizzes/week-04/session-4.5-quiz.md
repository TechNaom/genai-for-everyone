# Session 4.5 Quiz: Automation Workflows

**Answer all 6 questions. Mix of multiple choice, short answer, and scenario.**

---

## Question 1: Simple Automation vs. Agents

When should you use **simple automation** (rules + scheduler) instead of an agent?

A) Always—it's cheaper  
B) When the task is predictable and doesn't require reasoning  
C) Never—agents are always better  
D) Only for one-off tasks  

**Answer:** B

---

## Question 2: Hybrid Workflow Logic

In a hybrid workflow (rules → agent → action), when should the agent be called?

A) Always, for every input  
B) Only if the simple rule is unsure  
C) Never, just use the rule  
D) Only at scheduled times  

**Answer:** B

---

## Question 3: Cost Comparison

You process 1,000 emails/day. Which approach is cheapest?

- Simple rules only: $0 (70% accuracy)
- Agent only: 1,000 × $0.01 = $10 (95% accuracy)
- Hybrid (rules + agent on edge cases): Rules filter 950, agent on 50 = 50 × $0.01 = $0.50 (92% accuracy)

Which do you choose and why?

**Short answer:** Hybrid. It's 10x cheaper than agent-only and nearly as accurate. Rules handle the obvious cases for free, agent handles edge cases where it matters.

---

## Question 4: Workflow Debugging

Your email workflow is slow (10 seconds per email). Walk through how you'd debug it.

**Short answer:** Test each step independently: (1) Is the simple rule <1ms? (2) Is the agent call ~1-2s? (3) Is action execution <1s? Once you isolate which step is slow, optimize it or parallelize if possible.

---

## Question 5: Scheduled vs. Real-Time Agents

**Scenario:** You're building a system to analyze customer feedback and send weekly insights. Would you use a scheduled agent (runs once/week) or a real-time agent (runs on each feedback)? Why?

**Expected answer:** Scheduled agent. Feedback analysis is batched weekly, so a scheduled agent is appropriate. A real-time agent would be overkill and expensive. Hybrid could work too: real-time rule to flag urgent issues, scheduled agent for weekly summary.

---

## Question 6: Human-in-Loop Design

Design a workflow where: (1) Simple rule filters emails, (2) Agent analyzes, (3) Agent drafts response, (4) Human approves before sending. What's the advantage of this over a fully automated system?

**Expected answer:** Human-in-loop ensures high-stakes decisions (emails going to customers) are reviewed before sending. Catches agent mistakes, builds trust, and allows humans to learn from agent drafts. Trade-off: slower (human review adds time) but higher quality and safety.

---

*Session 4.5 Quiz | GenAI for Everyone | Week 4*
