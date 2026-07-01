# Session 4.3: Multi-Step Task Agents

**Week 4: Tool Use, Agents & Automation**  
**Live session format:** 60–90 minutes  
**Outcome:** Build and debug an agent that plans and executes a real 3-step research task

---

## Why this chapter exists

You've learned what agents are (Session 4.1) and how to make them call functions (Session 4.2). But so far, every task you've given your agent has been trivial: "Get today's weather" or "Calculate 15 × 8." The agent makes one tool call, gets a result, and you're done.

Real work doesn't work that way. Your manager asks: *"Research our three biggest competitors' pricing strategies for Q3 and tell me how we compare."* Your partner asks: *"Find three good vegan restaurants near me that have outdoor seating and are open after 9pm."* A journalist needs: *"Investigate whether this politician's claim about unemployment rates is accurate — find current data, historical context, and any conflicting sources."*

These aren't one-tool-call problems. They're *multi-step tasks*, and they're where agents start to earn their keep. To solve them, an agent needs to:

1. **Break down the problem** — What steps does this actually require?
2. **Execute in sequence** — Search, observe, adapt, search again.
3. **Know when it's done** — When is there enough information to stop?

This is what separates a toy chatbot from something that can actually *do work*. And unlike simple agents, multi-step agents can break in interesting ways — they get stuck in loops, forget what they found, stop too early, or reason backward (trying to conclude before gathering data). This chapter teaches you how to build one *and* how to debug it when it inevitably goes sideways.

---

## Part 1: The anatomy of a multi-step task

Let's start with a concrete example: **research the cost of cloud storage across providers.**

A human would break this down roughly like:
1. **Plan:** "I'll search for pricing from AWS, Google Cloud, and Azure. Then I'll compare the data. Once I have all three, I'll summarize."
2. **Execute step 1:** Search for AWS S3 pricing → get a page with pricing tiers
3. **Observe:** I see the data, but it's complex. Do I have enough?
4. **Execute step 2:** Search for Google Cloud Storage pricing → get their pricing page
5. **Observe:** Okay, I have two. I notice AWS is cheaper for small amounts, Google is better for egress. I need Azure to complete the picture.
6. **Execute step 3:** Search for Azure Blob Storage pricing
7. **Observe:** Now I have all three. I can summarize.
8. **Stop:** Hand back the comparison.

Notice the flow: **plan → do something → observe → decide whether to continue → loop back or stop.**

An agent does the same thing. The difference is that the agent needs to *learn* when to plan, when to take action, and when to stop — because it doesn't start with a human-written step-by-step guide.

---

## Part 2: Planning in agents — implicit vs. explicit

There are two ways agents plan: **implicit** and **explicit.**

### Implicit planning (the agent just does it)

Implicit planning means the agent doesn't explicitly write out a plan. Instead, it reasons step-by-step and the language model's own reasoning handles the planning.

In Session 4.2, your agent did this implicitly. The prompt said something like:
> "You are a helpful assistant. When the user asks for information, use the available tools to find it. Reason step-by-step."

The model, just by being prompted to "reason step-by-step," naturally figures out what to do next. For simple tasks, this works well.

**Pros:** Simple, fewer prompt overhead, fewer API calls.  
**Cons:** Can get stuck in loops. Harder to control. Less predictable on very complex tasks.

### Explicit planning (write the plan first)

Explicit planning means you ask the agent to write out a plan *before* it starts executing. It looks like:

1. **User asks:** "Research competitor pricing for cloud storage."
2. **Agent thinks (via LLM call 1):** "Okay, I'll need to:
   - Search for AWS S3 pricing
   - Search for Google Cloud Storage pricing
   - Search for Azure Blob Storage pricing
   - Compare them and summarize"
3. **Agent executes (loop over steps):** For each step in the plan, call the tool and record the result.
4. **Agent reflects:** "I've done all three searches. I have the data I need. I can now summarize."

**Pros:** More structured. Easier to debug (you can see the plan). Better for tasks with 5+ steps.  
**Cons:** Extra API call upfront. If the plan is wrong, the agent is locked into it.

---

## Part 3: Building a multi-step task agent — the code

Let's code a multi-step agent that researches a topic and writes a summary. We'll use explicit planning.

```python
from anthropic import Anthropic

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

# Define tools — same as Session 4.2
tools = [
    {
        "name": "search_web",
        "description": "Search the web for information. Returns top results as plain text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_current_date",
        "description": "Get today's date.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

# Simulate tool calls (in real use, these'd call actual APIs)
def search_web(query: str) -> str:
    """Fake search — in real use, call a real search API."""
    results = {
        "aws s3 pricing": "AWS S3: $0.023/GB for standard storage, $0.0125/GB for infrequent access.",
        "google cloud storage pricing": "GCS: $0.020/GB for standard, $0.010/GB for nearline.",
        "azure blob storage pricing": "Azure: $0.0184/GB for hot tier, $0.01/GB for cool tier.",
        "python libraries for web scraping": "Beautiful Soup, Scrapy, Selenium, Playwright.",
        "when did openai release gpt-4": "OpenAI released GPT-4 on March 14, 2023."
    }
    query_lower = query.lower()
    for key, value in results.items():
        if key in query_lower:
            return value
    return f"No results found for '{query}'. Assume the model would return real data in production."

def get_current_date() -> str:
    from datetime import date
    return str(date.today())

def process_tool_call(tool_name: str, tool_input: dict) -> str:
    """Process a tool call and return the result."""
    if tool_name == "search_web":
        return search_web(tool_input["query"])
    elif tool_name == "get_current_date":
        return get_current_date()
    else:
        return f"Unknown tool: {tool_name}"

# The core multi-step agent loop
def run_multi_step_agent(user_task: str) -> str:
    """
    Run an agent that:
    1. Plans the steps (explicit planning)
    2. Executes each step
    3. Stops when done
    """
    messages = []
    
    # Step 1: Ask the LLM to make a plan
    plan_prompt = f"""You are a research agent. The user has asked:

"{user_task}"

First, write out a clear plan of the steps you will take to complete this task. 
Be specific: list the searches you'll do, what data you need, and how you'll summarize.
Do NOT execute yet — just plan."""

    messages.append({"role": "user", "content": plan_prompt})
    
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        tools=tools,
        messages=messages
    )
    
    # Extract the plan text
    plan_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            plan_text += block.text
    
    print(f"Agent's plan:\n{plan_text}\n")
    messages.append({"role": "assistant", "content": response.content})
    
    # Step 2: Tell the agent to execute the plan
    messages.append({"role": "user", "content": "Now execute the plan step by step. Use the available tools."})
    
    # Step 3: Agentic loop — execute tools until the agent says it's done
    max_iterations = 10
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f"--- Iteration {iteration} ---")
        
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=2048,
            tools=tools,
            messages=messages
        )
        
        # Check if the agent is done (no tool calls, just text)
        tool_calls = [block for block in response.content if hasattr(block, "type") and block.type == "tool_use"]
        text_blocks = [block for block in response.content if hasattr(block, "text")]
        
        if not tool_calls:
            # Agent is done — collect all text as the final answer
            print("Agent determined it's done.")
            final_response = " ".join([block.text for block in text_blocks])
            return final_response
        
        # Agent made tool calls — process them
        print(f"Agent made {len(tool_calls)} tool call(s).")
        messages.append({"role": "assistant", "content": response.content})
        
        # Process each tool call
        tool_results = []
        for tool_call in tool_calls:
            print(f"  Calling {tool_call.name}...")
            result = process_tool_call(tool_call.name, tool_call.input)
            print(f"    Result: {result[:80]}...")  # Show first 80 chars
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result
            })
        
        # Add tool results back to messages
        messages.append({"role": "user", "content": tool_results})
    
    return "Max iterations reached without completion."

# Run the agent
if __name__ == "__main__":
    task = "Research the cost of cloud storage across AWS, Google Cloud, and Azure. Compare and summarize."
    result = run_multi_step_agent(task)
    print(f"\n=== FINAL RESULT ===\n{result}")
```

This code shows the key pattern:
1. **Plan phase:** LLM writes out the steps.
2. **Execute phase:** Loop that calls tools, processes results, and checks for stopping conditions.
3. **Stopping condition:** When the LLM stops calling tools and returns text instead, it's done.

---

## Part 4: Stopping conditions and the stopping problem

Here's a tricky question: **How does the agent know when to stop?**

There are several approaches:

### 1. **Token-based stopping**
Stop when the model produces text that says something like "I'm done" or "Summary:". 
- **Pro:** Simple.
- **Con:** Unreliable. The model might say "I need one more search" and then output text.

### 2. **Tool-call absence**
Stop when the model doesn't call any tools in its response — just outputs text.
- **Pro:** Works well in practice. If the model calls tools, it needs more data. If it doesn't, it's summarizing.
- **Con:** Doesn't guarantee the task is complete (agent might just give up).

### 3. **Explicit stop tool**
Add a tool called `stop_and_summarize` that the agent must call when done.

```python
{
    "name": "stop_and_summarize",
    "description": "Call this when you have gathered enough information and are ready to provide your final answer.",
    "input_schema": {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": "Your final summary or answer."
            }
        },
        "required": ["summary"]
    }
}
```

- **Pro:** Explicit. Forces the agent to decide it's done.
- **Con:** Requires retraining/prompting the agent to use it.

### 4. **Iteration limit + human-in-the-loop**
Stop after N iterations. If the agent hasn't finished, let a human review and decide.
- **Pro:** Safe. Prevents infinite loops.
- **Con:** Expensive if called every time.

**In practice:** Use approach #2 (tool-call absence) as your default. It's simple and works. Add iteration limits (#4) as a safety net.

---

## Part 5: Real-world gotchas — debugging multi-step agents

Multi-step agents fail in predictable ways. Here's how to debug them:

### Gotcha 1: The agent goes in circles
**Symptom:** Agent calls the same tool over and over with slightly different queries.  
**Cause:** The agent thinks it's learning something new, but it's not.  
**Fix:** 
- Add an explicit stopping rule: "If you've called the same tool twice with similar queries, stop."
- Add memory: Pass a summary of prior results back to the agent so it knows what it's already found.

### Gotcha 2: The agent stops too early
**Symptom:** Agent returns a partial answer and stops.  
**Cause:** Prompt doesn't emphasize thoroughness. Agent is satisficing (good-enough) not optimizing (best).  
**Fix:** Rewrite the system prompt to say "You must verify all aspects of the task before stopping. Don't settle for partial answers."

### Gotcha 3: The agent calls tools in the wrong order
**Symptom:** Agent searches for conclusions before gathering data.  
**Cause:** Plan was vague or the agent deviated from it.  
**Fix:** Explicit planning (Part 2 above) helps. Alternatively, add dependencies: "You must do step A before step B."

### Gotcha 4: Tool results are ignored
**Symptom:** Agent calls tools and gets results, but the summary doesn't include them.  
**Cause:** Context window limit. The agent forgot earlier results.  
**Fix:** 
- Summarize results as you go: After each tool call, ask the agent to note what it learned.
- Use smaller models (fewer tokens used per iteration) to save context.
- Implement a "working memory" that the agent updates (e.g., a dict of key findings).

---

## Part 6: Building a more resilient agent — adding memory and safeguards

Here's a refactor that adds a **working memory** and **stopping safeguards**:

```python
def run_multi_step_agent_v2(user_task: str, max_iterations: int = 10) -> dict:
    """
    Improved multi-step agent with working memory and safeguards.
    """
    messages = []
    working_memory = {
        "task": user_task,
        "findings": [],  # List of (step, result) tuples
        "iterations": 0
    }
    
    # Plan phase
    plan_prompt = f"""You are a research agent. Task: {user_task}

Write a detailed plan. Include:
1. Specific searches or information you need
2. Order of execution
3. How you'll know when you're done
"""
    
    messages.append({"role": "user", "content": plan_prompt})
    response = client.messages.create(model=MODEL_ID, max_tokens=1024, tools=tools, messages=messages)
    
    plan_text = "".join([block.text for block in response.content if hasattr(block, "text")])
    print(f"Plan:\n{plan_text}\n")
    working_memory["plan"] = plan_text
    messages.append({"role": "assistant", "content": response.content})
    
    # Execution phase with memory updates
    messages.append({"role": "user", "content": "Execute the plan. For each step, call the tools and then state what you learned."})
    
    for iteration in range(max_iterations):
        working_memory["iterations"] = iteration + 1
        print(f"--- Iteration {iteration + 1} ---")
        
        # Add context about what we've found so far
        if working_memory["findings"]:
            context = "Findings so far:\n" + "\n".join([f"- {f[0]}: {f[1][:100]}" for f in working_memory["findings"][-3:]])
            # Optionally insert this into the latest message to reinforce memory
        
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=2048,
            tools=tools,
            messages=messages
        )
        
        tool_calls = [b for b in response.content if hasattr(b, "type") and b.type == "tool_use"]
        text_blocks = [b for b in response.content if hasattr(b, "text")]
        
        # Check stopping condition
        if not tool_calls:
            # Agent is done
            result_text = " ".join([b.text for b in text_blocks])
            working_memory["final_result"] = result_text
            working_memory["status"] = "completed"
            return working_memory
        
        messages.append({"role": "assistant", "content": response.content})
        
        # Process tools and record findings
        tool_results = []
        for tool_call in tool_calls:
            result = process_tool_call(tool_call.name, tool_call.input)
            working_memory["findings"].append((tool_call.name, result))
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result
            })
            print(f"  {tool_call.name}: {result[:80]}...")
        
        messages.append({"role": "user", "content": tool_results})
    
    working_memory["status"] = "max_iterations_reached"
    return working_memory
```

Key improvements:
- **Working memory:** Tracks findings and plan so the agent can refer back.
- **Clear stopping:** Returns a dict with status, so the caller knows whether it succeeded.
- **Iteration tracking:** Easier to debug when things go wrong.

---

## Points to Remember

1. **Multi-step agents require planning.** Either implicit (let the model figure it out) or explicit (ask for a plan first).
2. **Stopping is hard.** Use tool-call absence as your stopping signal, and add iteration limits as a safety net.
3. **Memory matters.** Keep a working memory of findings so the agent doesn't forget what it learned.
4. **Debug systematically.** When an agent fails, check: Is the plan wrong? Is the agent ignoring tool results? Is it looping?
5. **Test offline first.** Mock your tools before using real APIs. Catch planning bugs early.

---

## Quick Check: Fill in the Blanks

1. **Explicit planning** means the agent writes out steps before executing them. The alternative is **\_\_\_\_\_\_\_\_\_\_ planning**, where the model figures out what to do as it goes.
   - Answer: *implicit*

2. **The most reliable stopping condition** for a multi-step agent is when the model \_\_\_\_\_\_\_\_\_\_\_\_\_\_ new tool calls in its response, only outputting text.
   - Answer: *stops making* or *doesn't make*

3. When an agent calls the same tool repeatedly with similar queries, it's likely \_\_\_\_\_\_\_\_\_\_\_\_\_ (a) stuck in a loop, (b) gathering diverse data, (c) almost done.
   - Answer: *(a) stuck in a loop*

4. **Working memory** in an agent is a running record of \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_ so the model can refer back without forgetting.
   - Answer: *findings, results, or observations*

5. If an agent stops too early with only partial answers, the fix is usually to \_\_\_\_\_\_\_\_\_\_\_\_\_ the prompt to emphasize thoroughness.
   - Answer: *rewrite* or *update*

---

## Quiz and Interview Questions

**Full quiz:** [assessments/quizzes/week-04/session-4.3-quiz-v2.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/quizzes/week-04/session-4.3-quiz-v2.md)  
**Answer key:** [assessments/answer-keys/week-04/session-4.3-quiz-answers-v2.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/answer-keys/week-04/session-4.3-quiz-answers-v2.md)  
**Interview questions:** [assessments/interview-questions/week-04-interview-qs.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/interview-questions/week-04-interview-qs.md)

---

## Core path and Pro path exercises

### Core path
Build a **research agent** that takes a topic and:
1. Plans 3 searches to research that topic
2. Executes the searches
3. Stops and returns a summary

Starter code with TODOs guides you through the loop structure.

### Pro path
Build a **fact-checking agent** that:
1. Takes a claim as input
2. Plans searches to verify it
3. Finds supporting and contradicting evidence
4. Scores the claim's veracity (0–100%)
5. Outputs a brief report with citations

Includes handling conflicting results and deciding when enough evidence exists.

---

## What's next

**Session 4.4** dives into **Multi-Agent Patterns** — what happens when you run multiple agents that work together or critique each other. You'll learn orchestrator-worker patterns, debate setups, and reviewer-reviewer loops.

For now, focus on getting a single agent to plan, execute, and stop reliably. That's the foundation everything else builds on.

---

*Session 4.3 | GenAI for Everyone | Week 4: Tool Use, Agents & Automation*
