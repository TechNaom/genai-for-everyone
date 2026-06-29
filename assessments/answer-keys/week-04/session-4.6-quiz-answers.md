# Session 4.6 Quiz Answers and Grading Guide

---

## Question 1: Research Planning

**Answer:** A good plan for "The future of remote work post-2024" might include:

**Full credit (1 pt):**
- Identifies 3+ specific searches (e.g., "remote work trends 2024", "productivity studies remote workers", "return-to-office 2024", "hybrid work policies")
- Explains why each search matters (different angles: trends, research, policies)
- Mentions credibility criteria (academic sources, company reports, government data)

**Partial credit (0.5 pts):**
- Lists searches but weak reasoning

**No credit:**
- Vague ("search for remote work stuff")

**Good answers sound like:**
- "I'd search for: (1) recent productivity studies (academic sources), (2) corporate return-to-office policies (company announcements), (3) employee preferences surveys (trusted pollsters), (4) industry forecasts (analyst reports). This gives breadth: research, policy, preferences, predictions."

---

## Question 2: Tool Calling in Research

**Answer:** The agent decides it needs information, outputs a tool_use block requesting a search, the system calls the search tool, the tool returns results, and those results are added back to the conversation so the agent can read and respond to them.

**Full credit (1 pt):**
- Explains the cycle: decide → output request → system calls → result → agent reads

**Partial credit (0.5 pts):**
- Gets most of the cycle but skips a step

**No credit:**
- "The agent calls the search function" (misses the structured output concept)

---

## Question 3: Handling Search Results

**Answer:** B) Read all 20 and summarize the most relevant ones

**Grading:**
- **Full credit (1 pt):** Answer is B
- **No credit:** Any other answer

**Explanation:** An intelligent agent filters based on relevance, not volume. Using all 20 equally wastes effort, picking one risks missing better sources, and asking a human defeats the point of an agent.

---

## Question 4: Multi-Turn Conversation

**Answer:** Message history allows the agent to maintain context from the plan, remember search results, reference its earlier analysis, and write a report grounded in all prior work. Without it, each phase starts fresh and the agent loses crucial information.

**Full credit (1 pt):**
- Explains that history preserves context across phases
- Notes that losing history = losing coherence/hallucination risk

**Partial credit (0.5 pts):**
- "It's important for context" but vague

**No credit:**
- "Just saves messages"

---

## Question 5: Fact-Checking

**Answer:** C) Flag the claim as [⚠️ UNVERIFIED] and note the concern

**Grading:**
- **Full credit (1 pt):** Answer is C
- **No credit:** Any other answer

**Explanation:**
- A (delete): Loses information; maybe the claim is true
- B (ignore): Dishonest and risky
- C (flag): Transparent; tells reader to be cautious
- D (assume true): Dangerous; agents hallucinate

Flagging unverified claims builds trust and accountability.

---

## Question 6: Workflow Evaluation

**Answer example (2 pts):**

"Good aspects: The agent was fast (12s), covered multiple angles (3 aspects), included citations (3), and was transparent about limitations (flagged 1 unverified claim). This shows responsible AI.

To improve: The report is short (800 words). Most research reports should be 1200-1500 words minimum for depth. More searches (7-10 instead of 5) would add breadth. More citations (8-10) would strengthen credibility."

**Full credit (2 pts):**
- Identifies strengths (speed, scope, citations, transparency)
- Suggests improvements (longer report, more research, more citations)

**Partial credit (1 pt):**
- Identifies either strengths OR improvements but not both

**No credit:**
- Vague or no substantive answer

---

## Question 7: Production Considerations

**Answer example (3 pts):**

"**Cost:** Cache search results—if two users request the same topic, reuse results from the first. This cuts API calls by ~50%. Each LLM call costs ~$0.01, so 100 requests/day at 4 calls each = $4/day. Acceptable.

**Quality:** Fact-checking takes time (adds 5-10s per report). For production, run async: return draft immediately, send fact-checks later. Or require human review for high-stakes topics, auto-approve for low-stakes.

**Failures:** If search API is down, fallback to cached results or return a note: 'Search unavailable, using recent data.' Implement circuit breaker pattern. Test all failure modes before launch."

**Full credit (3 pts):**
- All 3 concerns addressed with practical solutions
- Mentions caching, async processing, fallbacks, monitoring

**Partial credit (2 pts):**
- Addresses 2 concerns well

**Partial credit (1 pt):**
- Addresses 1 concern thoughtfully

**No credit:**
- Vague or no plan

---

## Question 8: Agent vs. Human

**Answer example:**

"**Humans better at:** Catching subtle biases in sources, understanding nuance (what's implied vs. stated), questioning assumptions, fact-checking accuracy, and creative synthesis (connecting dots agents miss).

**Agents better at:** Speed (report in 15s vs. hours), consistency (same quality every time), breadth (juggling 10 sources without forgetting), and tirelessness (work 24/7 without fatigue).

**The hybrid:** Agent does bulk research, human does quality review and fact-checking. Best of both."

**Full credit (1 pt):**
- Clearly identifies agent strengths (speed, consistency, breadth)
- Clearly identifies human strengths (insight, nuance, accuracy)
- Shows understanding of complementary skills

**Partial credit (0.5 pts):**
- Lists strengths/weaknesses but reasoning is weak

**No credit:**
- "Agents are better" or "Humans are better" (misses the point)

---

## Grading Summary

| Question | Type | Points |
|----------|------|--------|
| 1 | Short | 1 |
| 2 | Short | 1 |
| 3 | MC | 1 |
| 4 | Short | 1 |
| 5 | MC | 1 |
| 6 | Scenario | 2 |
| 7 | Scenario | 3 |
| 8 | Short | 1 |
| **Total** | | **11** |

---

## Common Misconceptions

1. **"More searches = better report"** — No. Better to have 5 good searches than 20 unfocused ones.
2. **"Agents never hallucinate facts"** — Wrong. Always fact-check and flag uncertainties.
3. **"Reports must be long"** — Wrong. Focused 800-word report > rambling 3000-word one.
4. **"Humans are obsolete"** — Wrong. Humans catch nuances and biases agents miss.
5. **"Caching is cheating"** — Wrong. It's smart engineering—reuse when appropriate.

---

*Session 4.6 Answer Key | GenAI for Everyone | Week 4 Lab*
