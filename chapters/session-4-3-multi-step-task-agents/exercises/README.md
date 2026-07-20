# Session 4.3 Exercise: Multi-Step Research Agent

## Overview

Build a **research agent** that takes a topic and:
1. Plans a 3-step research strategy
2. Executes searches (simulated, so this runs for free)
3. Stops when it has enough information
4. Returns a structured summary

This exercise teaches the core multi-step agent loop with explicit planning and
working memory — the same pattern the lesson builds in Parts 3 and 6.

## Learning objectives

- Understand the agent loop: plan → execute → observe → decide to continue or stop
- Implement an explicit planning phase
- Build a tool-calling loop with a correct stopping condition
- Debug agent behavior by inspecting the working memory

## Setup

1. Download `starter.py` below.
2. Install the SDK:
   ```bash
   pip install anthropic
   ```
3. Set your API key:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```

The search tool itself is simulated (a small lookup table), so the only real
API cost is the planning call plus a few iterations — this is intentionally
cheap to run on a free-tier key.

## Files in this exercise

- `starter.py` — skeleton with TODOs (core path)
- `solution.py` — reference implementation

## The task

Open `starter.py`. Complete the three TODO sections:

1. **TODO 1 — the planning prompt.** Write a prompt that asks the LLM to plan
   3 research steps for the task, and explicitly tells it *not* to execute yet.
2. **TODO 2 — the execution prompt.** Write a short follow-up message telling
   the agent to now execute its plan using the available tool.
3. **TODO 3 — the execution loop.** Extract `tool_use` blocks and text blocks
   from each response, implement the stopping condition (no tool calls means
   the agent is done), and make sure tool results get appended back into
   `messages` so the next iteration can see them.

## Testing your code

Run your agent on the provided test topic:
```bash
python3 starter.py
```

Expected behavior:
- Agent prints a plan before making any tool calls.
- Agent makes 2–4 tool calls (searches).
- Agent stops on its own and returns a summary — it should not hit
  `max_iterations_reached` on this task.

## Troubleshooting

**Agent doesn't stop:**
- Check: does your stopping condition correctly detect when the LLM's response
  contains no `tool_use` blocks?
- Add: `print(tool_calls)` to see what the LLM is actually returning.

**Agent ignores tool results:**
- The tool results aren't being passed back to the LLM. Double-check the
  message structure in the loop — every tool call needs a matching
  `tool_result` with the same `tool_use_id`.

**Plan is ignored during execution:**
- This is common. Make sure your execution prompt explicitly says something
  like "Follow your plan. Execute each step in order."

## Checking your work

There's no automated grader. Compare your structure against `solution.py`
(run it with `python3 solution.py`) once you've made a genuine attempt — check
that your plan phase never calls a tool, that your stopping condition matches
"no tool_use blocks," and that `working_memory["findings"]` has one entry per
search actually performed.

## Submission checklist

Before moving to the project (Fact-Checking Agent), make sure you have:
- [ ] Agent completes a 3-step research task
- [ ] Agent stops on its own (doesn't loop forever)
- [ ] Output includes: plan, tool calls made, final summary
- [ ] Code runs without errors

---

**Next:** The project pushes this same loop further — a fact-checking agent
that has to weigh conflicting evidence and score a claim's veracity.
