# Session 4.4 Quiz: Multi-Agent Patterns

**Answer all 6 questions. Mix of multiple choice and short answer.**

---

## Question 1: Orchestrator-Worker Pattern

In an **orchestrator-worker** multi-agent system, what is the primary role of the orchestrator agent?

A) Execute all the technical tasks by itself  
B) Coordinate task distribution and synthesize results  
C) Review and critique the workers' output  
D) Debate different perspectives on the task

**Answer:** B

---

## Question 2: When to Use Debate Pattern

A debate pattern (where agents argue opposing views) is most useful when:

A) You need to make a decision quickly  
B) One agent can handle the task alone  
C) You want to explore multiple perspectives and surface trade-offs  
D) Cost is your primary concern  

**Answer:** C

---

## Question 3: Reviewer Pattern Trade-offs

In a reviewer pattern (writer + multiple critics), what is the main trade-off?

**Short answer:** Higher quality output (more reviewers catch errors), but slower and more expensive (multiple API calls). Trade latency and cost for quality.

---

## Question 4: Convergence Checking

In the pro path exercise, "convergence" means:

A) All agents agree on the final answer  
B) Feedback stops changing (reviewers are giving similar feedback)  
C) The writer has revised 3 times  
D) The cost of the system has converged to zero  

**Answer:** B

---

## Question 5: Communication Between Agents

Why is a **structured communication protocol** important in multi-agent systems?

**Short answer:** Agents need to understand each other's output format. Unstructured prose feedback can be ambiguous or hard to parse. Structured formats (e.g., JSON with specific fields) make feedback actionable and reduces confusion.

---

## Question 6: Scenario - Choose the Pattern

**Scenario:** You're building a system to generate marketing copy for a new product. The copy needs to be accurate (claims backed by data), engaging (compelling prose), and on-brand (matches company voice). You want high-quality output but your budget allows for multiple API calls.

Which multi-agent pattern would you choose and why?

**Expected answer:** Reviewer pattern (writer + three critics for accuracy, engagement, brand voice). Each reviewer specializes in their area, catches different types of errors. The writer revises based on all feedback. More expensive but produces high-quality copy where accuracy and tone both matter.

---

*Session 4.4 Quiz | GenAI for Everyone | Week 4*
