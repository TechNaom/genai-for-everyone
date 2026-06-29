# Week 4 Interview Questions: Tool Use, Agents & Automation

**Topic:** Agents, Tool Calling, Multi-Agent Patterns, and Automation  
**Format:** Open-ended technical questions designed for real interviews  
**Difficulty:** Intermediate-Advanced (assumes understanding of Sessions 4.1–4.6)

---

## Question 1: Tool Calling Fundamentals

**The Question:**
"Explain how an LLM 'calls' a tool or function. Walk through what happens step-by-step when a user asks an agent to check the weather."

**What a strong answer includes:**
- ✅ The request-response cycle:
  1. User asks: "What's the weather in San Francisco?"
  2. LLM (with tools defined) decides: "I need to call weather_tool"
  3. LLM outputs structured tool_use block (name, arguments)
  4. System extracts tool_use block, calls the actual function
  5. Tool returns result (e.g., "72°F, sunny")
  6. Result added back to conversation as tool_result
  7. LLM generates final answer to user
- ✅ Key detail: LLM doesn't actually call the tool—it *outputs a request for* the tool to be called
- ✅ Schema matters: Defines what arguments the tool accepts (prevents hallucination)
- ✅ Stopping condition: Loop continues if LLM outputs tool_use, stops if only text

**Red flags in weak answers:**
- "The LLM makes the actual HTTP call" (incorrect—it just decides to call)
- Doesn't mention schema/structured output
- Confuses tool_use with function_calling in code
- No mention of the loop pattern

**Follow-up if they nail it:**
"What happens if the LLM decides to call a tool that doesn't exist in your schema?"

---

## Question 2: Multi-Step Agent Design

**The Question:**
"Design a multi-step agent that researches a topic and writes a report. How would you structure it, what could go wrong, and how would you debug it?"

**What a strong answer includes:**
- ✅ High-level structure:
  - Phase 1 (Plan): Agent writes a plan for what to search
  - Phase 2 (Execute): Loop—agent calls search tools, observes results
  - Phase 3 (Synthesize): Agent stops calling tools and writes final report
- ✅ Implementation details:
  - Working memory to track findings (agent doesn't forget mid-task)
  - Max iteration limit (e.g., 10) as safety net
  - Stopping condition: No tool_use in response = agent is done
- ✅ Failure modes:
  - Infinite loops: Agent calls same tool over and over
  - Early stop: Agent outputs partial report and quits
  - Forgotten context: Early search results lost due to token limit
  - Wrong order: Agent searches for conclusions before gathering data
- ✅ Debugging strategies:
  - Log each iteration (what tool was called, what result came back)
  - Print the plan—does it make sense?
  - Check if results are in working memory
  - Verify stopping condition logic

**Red flags in weak answers:**
- "Just call search tools until you have enough data" (no structure)
- Doesn't mention working memory or iteration limits
- No debugging plan
- Confuses planning with execution

**Follow-up if they nail it:**
"Your agent researches 5 topics but only cites the last 2 in the report. Why?"

---

## Question 3: When to Use Agents vs. Simple Automation

**The Question:**
"You're building a system to: (A) send a reminder email every Monday morning, (B) research a topic and answer questions about it dynamically, (C) extract structured data from PDFs. For each, would you use an agent or simple automation? Why?"

**What a strong answer includes:**
- ✅ Reasoning for each:
  - (A) Simple automation: No reasoning needed, just schedule an email. Agents = overkill + cost.
  - (B) Agent: Topic changes, requires reasoning, tool use (search). Agents excel here.
  - (C) Depends: If fixed template, automation. If variable structures, agents help.
- ✅ Decision framework:
  - Agent if: Task is complex, requires reasoning, variable inputs, tool use
  - Automation if: Task is simple, predictable, high frequency (cost matters)
- ✅ Cost consciousness: "Agents are expensive. Use for high-value tasks only."
- ✅ Hybrid thinking: Combine both—simple automation for scheduling, agent for content

**Red flags in weak answers:**
- "Always use agents" (misses cost/complexity trade-off)
- "Agents can't scale" (false—they're just slower)
- No mention of cost
- Treats all tasks the same

**Follow-up if they nail it:**
"You used agents for (A) and it costs $1k/month. How do you fix it?"

---

## Question 4: Multi-Agent Patterns in Production

**The Question:**
"You're building a system for legal document review. Describe how you'd structure it as a multi-agent system. What pattern would you use (orchestrator-worker, debate, reviewer)? Why?"

**What a strong answer includes:**
- ✅ Pattern selection: **Reviewer pattern** is strongest
  - Writer agent: Drafts a summary of the document
  - Fact-checker agent: Verifies claims against the document
  - Risk-assessor agent: Identifies legal risks
  - Compliance-checker agent: Checks against regulations
- ✅ Reasoning:
  - Legal = high-stakes, errors are costly
  - Multiple reviewers catch different types of errors
  - Each agent specializes (expert system)
  - Writer synthesizes feedback
- ✅ Implementation details:
  - Structured feedback format (JSON with error types)
  - Stopping condition: Convergence (feedback stabilizes)
  - Conflict resolution: If agents disagree, human reviews
- ✅ Trade-offs:
  - Expensive (4 agents = 4 API calls)
  - Slower (sequential reviews)
  - But: Quality >> cost for legal domain

**Red flags in weak answers:**
- "Just use one agent" (misses the value of review)
- Picks orchestrator without reasoning
- Doesn't consider legal-specific needs
- No stopping condition strategy

**Follow-up if they nail it:**
"You ran 3 review rounds and still missed an error. What went wrong?"

---

## Question 5: Agent Loop Debugging and Stopping Conditions

**The Question:**
"Your agent is running for 20 iterations and not stopping. It keeps calling the same search tool with slightly different queries. How would you debug this, and how would you fix it?"

**What a strong answer includes:**
- ✅ Debugging approach:
  - Print each iteration: What tool is being called? What's the result?
  - Check stopping condition logic: Is it correct?
  - Inspect prompt: Is the agent clear about when to stop?
  - Look for patterns: Is the agent searching for the same thing over and over?
- ✅ Root causes:
  - No stopping condition (agent keeps searching forever)
  - Prompt isn't clear about success criteria
  - Agent doesn't know it already has the answer
  - Tool results are always slightly different (agent thinks it's new info)
- ✅ Fixes:
  - Add explicit stopping rule: "If you've called the same tool with similar queries twice, stop."
  - Improve prompt: "Stop when you have found X pieces of evidence."
  - Add memory: Track what's been searched, remind agent
  - Add iteration limit: Max 10 iterations as safety net
- ✅ Test with mocked tools first before real APIs

**Red flags in weak answers:**
- "Just set a timeout" (ignores root cause)
- Doesn't investigate what the agent is doing
- No mention of prompt clarity
- Suggests changes without testing

**Follow-up if they nail it:**
"You added a loop limit (10 iterations), but now the agent stops too early. Why?"

---

## Question 6: Tool Schema Design

**The Question:**
"Design a tool schema for a 'search_web' function that an agent will use. What arguments would you include, and how would you prevent the LLM from using the tool incorrectly?"

**What a strong answer includes:**
- ✅ Schema design:
  ```json
  {
    "name": "search_web",
    "description": "Search the web for information. Returns top 5 results.",
    "input_schema": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "Search query (1-10 words recommended)"
        },
        "num_results": {
          "type": "integer",
          "description": "Number of results (1-20)",
          "default": 5
        }
      },
      "required": ["query"]
    }
  }
  ```
- ✅ Clarity in descriptions: "Search query (1-10 words recommended)" guides the model
- ✅ Constraints: Type, required fields, defaults prevent misuse
- ✅ Error handling: What if the LLM sends a 500-word query? (Reject or truncate?)
- ✅ Testing: Verify LLM doesn't hallucinate tools or use it with invalid args

**Red flags in weak answers:**
- Vague descriptions ("query: some text")
- No constraints (LLM might send anything)
- Doesn't consider edge cases
- No validation logic

**Follow-up if they nail it:**
"The LLM keeps sending generic queries ('information', 'facts'). How do you fix it?"

---

## Question 7: Orchestrator-Worker Pattern for Task Decomposition

**The Question:**
"A user asks your system: 'Analyze our Q3 sales performance, compare to competitors, and recommend next quarter strategy.' Design this as an orchestrator-worker system. What tasks do you decompose into?"

**What a strong answer includes:**
- ✅ Task decomposition:
  - Task 1 (Worker 1): Analyze Q3 sales data (internal DB)
  - Task 2 (Worker 2): Research competitor Q3 results (search + analysis)
  - Task 3 (Worker 3): Market trends & forecasts (search + synthesis)
  - Task 4 (Orchestrator): Synthesize all three, recommend strategy
- ✅ Orchestrator's role:
  - Assigns tasks to workers
  - Collects results from each
  - Integrates into final recommendation
  - Could run tasks in parallel (if they're independent)
- ✅ Communication:
  - Each task has clear input/output format
  - Orchestrator passes results between workers if needed
  - Structured feedback (JSON with sections)
- ✅ Error handling:
  - If Task 2 fails (no competitor data), handle gracefully
  - If Task 1 times out, fallback to estimates

**Red flags in weak answers:**
- "One big agent does everything" (misses the benefit of decomposition)
- Tasks are interdependent but treats them as parallel
- Doesn't define what each worker returns
- No error handling

**Follow-up if they nail it:**
"Worker 1 takes 10s, Worker 2 takes 30s. How do you speed it up?"

---

## Question 8: Tool Calling vs. Function Calling

**The Question:**
"What's the difference between 'tool calling' (in the context of agents) and 'function calling' (in the LLM API)? Are they the same thing?"

**What a strong answer includes:**
- ✅ Terminology alignment:
  - Tool calling (agent context): Agent decides which tool to use and calls it
  - Function calling (LLM API): LLM outputs structured request for a function
  - They're **essentially the same concept**, different names
- ✅ In practice:
  - You define functions in your schema
  - LLM "function calls" = outputs a function_use block
  - System interprets that block and calls the actual function
  - Result goes back to LLM as tool_result
- ✅ Subtle difference:
  - "Tool calling" = broader concept (tools can be APIs, functions, external services)
  - "Function calling" = specifically LLM API feature for calling functions
- ✅ Related concepts:
  - Tool use = same as function calling
  - Plugins = tool calling with external APIs (ChatGPT style)

**Red flags in weak answers:**
- "They're completely different" (incorrect)
- Confuses with actual code function calls
- Doesn't explain the cycle (decide → call → result → respond)

**Follow-up if they nail it:**
"When would you use function calling vs. RAG retrieval?"

---

## Question 9: Bonus - Agent Cost & Performance Trade-offs

**The Question:**
"Your agent-based research system costs $0.50 per query and takes 30 seconds (5 API calls). A user complains it's too slow. You could: (A) use a faster model, (B) use fewer search iterations, (C) parallelize agent calls, (D) cache results. What would you recommend and why?"

**What a strong answer includes:**
- ✅ Analysis of options:
  - (A) Faster model: Reduces latency, may hurt quality. Test first.
  - (B) Fewer iterations: Faster, but less thorough research (quality risk)
  - (C) Parallelize: If tasks are independent, huge speed gain with same cost
  - (D) Cache: If queries repeat, instant response for cached queries
- ✅ Recommendation depends on:
  - Is it always slow or only sometimes? (C = sometimes, D = always)
  - Can tasks run in parallel? (Orchestrator pattern enables this)
  - How much quality can you lose? (B = risky)
  - User tolerance: 30s acceptable? Maybe not.
- ✅ Measurement: A/B test changes, measure latency + quality

**Red flags in weak answers:**
- "Just use a faster model" (ignores quality)
- Doesn't consider that tasks might be parallelizable
- No mention of measurement
- Suggests changes without understanding the bottleneck

**Follow-up if they nail it:**
"You parallelize and latency drops to 8s, but quality also drops. Why?"

---

## Question 10: Bonus - Real-World: Email Triage Agent

**The Question:**
"Design an agent that processes incoming emails, categorizes them (urgent, important, low-priority), and automatically drafts responses. Walk through how you'd build it, what could go wrong, and how you'd test it."

**What a strong answer includes:**
- ✅ Architecture:
  - Phase 1: LLM reads email, categorizes + extracts action items
  - Phase 2: For urgent emails, LLM drafts response
  - Phase 3: LLM decides if response needs human review
  - Phase 4: Human reviews, approves, agent sends
- ✅ Tool definitions:
  - `read_email`: Get email from inbox
  - `categorize`: Classify importance
  - `draft_response`: Generate response text
  - `send_email`: Actually send (behind approval gate)
  - `flag_for_review`: Mark for human if uncertain
- ✅ Safety mechanisms:
  - **Human in loop**: Emails sent only after approval
  - Confidence threshold: If agent isn't confident, escalate
  - Audit trail: Log what agent did and why
  - Test on historical emails (no real sends)
- ✅ Failure modes:
  - Sends wrong response to critical client (mitigated by human review)
  - Over-categorizes as urgent (tunable threshold)
  - Hallucinates response content (mitigated by human review + prompt guardrails)

**Red flags in weak answers:**
- No human review loop (dangerous!)
- Doesn't consider what happens if agent makes mistakes
- No testing strategy
- Treats email as simple classification (ignores response generation complexity)

**Follow-up if they nail it:**
"The agent flags everything as urgent. How do you debug and retune?"

---

## Rapid-Fire Technical Q&A

Quick checks during interviews:

1. **"What's a 'tool_use' block in an LLM response?"**  
   → Answer: Structured output where LLM specifies which tool to call and with what arguments

2. **"How does an agent know when to stop iterating?"**  
   → Answer: When response contains no tool_use blocks (only text), or iteration limit reached

3. **"What's the difference between implicit and explicit planning in agents?"**  
   → Answer: Implicit = agent figures it out; Explicit = agent writes plan first, then executes

4. **"Why would you use convergence checking in a multi-agent loop?"**  
   → Answer: To stop when feedback stabilizes (agents stop finding new issues)

5. **"What does 'grounding' an agent mean?"**  
   → Answer: Ensuring the agent's outputs are based on real tool results, not hallucinations

6. **"If an agent loops infinitely, what's the safest fix?"**  
   → Answer: Add iteration limit (hard stop), then debug the root cause

7. **"How do you test agents without real API calls?"**  
   → Answer: Mock the tools with fake data, verify logic in isolation first

---

## Interview Strategy Tips

1. **Listen for architecture thinking:** Do they consider scalability, safety, cost from the start?
2. **Probe edge cases:** "What if the tool returns an error?" — Shows defensive thinking
3. **Real-world grounding:** Ask about actual systems they've built, not theory
4. **Measurement mindset:** Strong candidates ask "how would we measure success?"
5. **Trade-off awareness:** Quality vs. cost, speed vs. accuracy—good candidates balance these
6. **Debugging approach:** Watch for systematic debugging (logging, isolation, hypothesis testing)

---

*Week 4 Interview Questions | GenAI for Everyone | Agents & Tool Use*
