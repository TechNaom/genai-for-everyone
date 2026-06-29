# Session 4.3 Quiz: Multi-Step Task Agents

**Week 4 | Session 4.3**

Answer the following 6 questions. Mix of multiple-choice and short-answer. Answers are in `assessments/answer-keys/week-04/session-4.3-quiz-answers.md`.

---

## Question 1: Explicit vs. Implicit Planning

**Which statement best describes the difference between explicit and implicit planning in agents?**

(a) Explicit planning is faster; implicit planning is more thorough.  
(b) Explicit planning means the agent writes out steps first; implicit planning means the LLM figures it out as it goes.  
(c) Explicit planning requires more tool calls; implicit planning requires fewer.  
(d) There is no real difference; they produce the same result.

---

## Question 2: Stopping Conditions

**Your multi-step agent is supposed to research a topic and stop when it's done. You've tested it on 5 tasks and it stops correctly. However, a colleague says: "What if the agent just gets lazy and stops early without gathering enough info?"**

**What's the most practical way to mitigate this?**

(a) Increase the max iterations limit to 50.  
(b) Rewrite the system prompt to emphasize thoroughness and remind the agent it must verify all aspects.  
(c) Add a tool called `stop_and_summarize` that forces the agent to make a final judgment call.  
(d) Both (b) and (c) are good approaches.

---

## Question 3: Working Memory and Forgetting

**You build a multi-step agent and test it on a 5-step research task. After 3 steps, you notice the agent's final summary doesn't include findings from steps 1 and 2. Why might this happen?**

(a) The agent is intentionally filtering out less relevant findings.  
(b) The context window is filling up and the LLM has forgotten earlier results.  
(c) The agent's prompt tells it to only focus on the last two searches.  
(d) Tool results are not being included in the agent's working memory.

---

## Question 4: Detecting Agent Loops (Debugging)

**Your agent is supposed to research "machine learning frameworks" and it's been looping for 20 iterations calling `search_web` over and over with slightly different query variations like:**
- "ML frameworks"
- "machine learning frameworks"
- "deep learning frameworks"
- "ML libraries"

**What's the most likely cause, and how would you fix it?**

Short answer (2-3 sentences):

---

## Question 5: Scenario — Multi-step Task Design

**You're building an agent to "Find the three most cost-effective cloud providers and explain why." The agent makes 3 searches (AWS pricing, Google Cloud pricing, Azure pricing) and stops.**

**Is this sufficient? Why or why not? What else might the agent need to do?**

Short answer (3-4 sentences):

---

## Question 6: Iterative Refinement

**After testing your multi-step agent, you discover:**
- The plan is clear and correct
- The agent executes the right searches
- But the final summary doesn't mention one of the key findings

**What's the most likely reason, and name two ways to debug this:**

Short answer (2-3 sentences for reason, then 2 debugging approaches):

---

## Submission

Submit your answers as a markdown file or text file. For short-answer questions, be specific and reference concepts from the chapter where relevant.

**Time estimate:** 20–30 minutes  
**Passing score:** 5 out of 6 correct
