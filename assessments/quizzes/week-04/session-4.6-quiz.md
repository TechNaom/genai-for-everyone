# Session 4.6 Quiz: Week 4 Lab

**This is a lab-focused quiz. Scenario-based questions test your understanding of the capstone.**

---

## Question 1: Research Planning

You're building a research agent on "The future of remote work post-2024". Describe a good research plan. What searches would you conduct? Why?

**Short answer:** (3-5 sentences)

---

## Question 2: Tool Calling in Research

Your research agent needs to search the web. Walk through how the agent would decide to call a search tool and what happens next.

**Short answer:** (3-4 sentences)

---

## Question 3: Handling Search Results

Your agent searches for "remote work productivity statistics" and gets 20 results. The agent needs to extract useful information. Should the agent:

A) Use all 20 results equally  
B) Read all 20 and summarize the most relevant ones  
C) Pick the first result and ignore the rest  
D) Ask a human which result to use  

**Answer:** B

**Why:** The agent should intelligently filter based on relevance and credibility, not use all equally or pick arbitrarily.

---

## Question 4: Multi-Turn Conversation

Your agent's workflow is:
1. Plan research
2. Execute searches
3. Analyze findings
4. Draft report

Why is it important to maintain message history across all 4 phases?

**Short answer:** (2-3 sentences)

**Expected answer:** So the agent remembers the original plan, search results, and analysis when writing the report. Without message history, it would lose context and hallucinate.

---

## Question 5: Fact-Checking

Your research report claims: "According to recent studies, 72% of remote workers report higher productivity."

In your fact-checking phase, you can't verify this statistic. What do you do?

A) Delete the claim  
B) Keep the claim and hope no one notices  
C) Flag the claim as [⚠️ UNVERIFIED] and note the concern  
D) Assume it's true because AI agents are usually right  

**Answer:** C

**Why:** Transparency about unverified claims builds trust. Flagging uncertainty is better than deleting content or ignoring problems.

---

## Question 6: Workflow Evaluation

You built a research agent. It produced a 800-word report in 12 seconds. Evaluate it:

**Scenario:**
- Report covers 3 aspects of remote work
- 5 searches were conducted
- 3 citations included
- 1 unverified claim (flagged)

Is this good? What would you improve?

**Short answer:** (4-5 sentences)

**Rubric (2 pts):**
| Points | Criteria |
|--------|----------|
| 2 pts | Identifies what's good (speed, scope, citations, transparency) AND what could improve (more depth, more citations, longer research) |
| 1 pt | Notes strengths or weaknesses but not both |
| 0 pts | No substantive answer |

---

## Question 7: Production Considerations

You want to deploy your research agent as a service:
- Users submit topics
- Agent researches and returns report
- Expected: 100 requests/day

**Consider:**
1. How would you handle cost? (Each LLM call costs money)
2. How would you ensure quality? (Fact-checking takes time)
3. How would you handle failures? (What if search API is down?)

**Short answer:** (5-7 sentences)

**Rubric (3 pts):**
| Points | Criteria |
|--------|----------|
| 3 pts | Addresses all 3 concerns with practical solutions (caching, rate limiting, fallbacks) |
| 2 pts | Addresses 2 concerns thoughtfully |
| 1 pt | Addresses 1 concern |
| 0 pts | No meaningful answer |

---

## Question 8: Agent vs. Human

When would a human researcher outperform your agent? When would the agent be better?

**Short answer:** (4-6 sentences)

**Expected thinking:**
- **Humans better at:** Creative insights, understanding nuance, catching subtle biases, fact-checking accuracy, questioning assumptions
- **Agents better at:** Speed, consistency, breadth of sources, handling volume, tireless searching

---

*Session 4.6 Quiz | GenAI for Everyone | Week 4 Lab*
