# Session 4.3 Exercise: Multi-Step Task Agent

## Overview

Build a **research agent** that takes a topic and:
1. Plans a 3-step research strategy
2. Executes searches (simulated or real)
3. Stops when it has enough information
4. Returns a summary

This exercise teaches the core multi-step agent loop with explicit planning and working memory.

## Learning objectives

- Understand the agent loop: plan → execute → observe → decide to continue or stop
- Implement explicit planning phase
- Build a tool-calling loop with stopping conditions
- Debug agent behavior by inspecting the working memory

## Path options

### Core path (guided)
Use the provided starter skeleton. TODOs guide you through:
1. Creating the plan-phase prompt
2. Building the execution loop
3. Implementing the stopping condition
4. Returning structured results

Estimated time: 45–60 minutes  
API required: Yes (Anthropic, free tier works)

### Pro path (less scaffolded)
- Implement a **fact-checking agent** that verifies claims and scores confidence
- Handle conflicting evidence
- Add a "confidence score" field to track certainty
- Implement a safeguard: stop if confidence exceeds a threshold

Estimated time: 90–120 minutes  
Deliverable: Working agent + example output showing conflicting sources handled correctly

## Setup

1. **Clone or download the starter code** from the exercise folder.
2. **Set your API key:**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```
3. **Install dependencies:**
   ```bash
   pip install anthropic
   ```

## Files in this exercise

- `research_agent_starter.py` — Skeleton with TODOs (core path)
- `fact_checker_starter.py` — Skeleton with TODOs (pro path)
- `README.md` — This file
- Solution files in `codebase/solutions/week-04/session-4.3/`

## Testing your code

### Core path
Run your agent on a few test topics:
```bash
python3 research_agent_starter.py
```

Expected behavior:
- Agent outputs a plan
- Agent makes 2–4 tool calls (searches)
- Agent stops and returns a summary

### Pro path
Run your fact-checker:
```bash
python3 fact_checker_starter.py
```

Test with claims like:
- "GPT-4 was released in March 2023" (verifiable)
- "Claude can access the internet in real-time" (false)
- "Python is the most popular programming language" (debatable)

## Troubleshooting

**Agent doesn't stop:**
- Check: Does your stopping condition correctly detect when the LLM stops calling tools?
- Add: `print(tool_calls)` to see what the LLM is returning.

**Agent ignores tool results:**
- The tool results aren't being passed back to the LLM. Double-check the message structure in the loop.

**Plan is ignored during execution:**
- This is common. Add a system prompt that reminds the agent: "Follow your plan. Execute each step in order."

**Context window fills up:**
- Long responses from tool results eat tokens. Truncate results to key info: `result = result[:500]`.

## Submission checklist

Before moving to 4.4, make sure you have:
- [ ] Core path: Agent completes a 3-step research task
- [ ] Agent stops (doesn't loop forever)
- [ ] Output includes: plan, tool calls made, final summary
- [ ] Code runs without errors
- [ ] Pro path (optional): Fact-checker handles conflicting evidence

---

**Next:** Session 4.4 (Multi-Agent Patterns) introduces agents that work together or critique each other.
