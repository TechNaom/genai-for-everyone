# Exercise — Session 4.4: Multi-Agent Patterns

## Writer + Critic Two-Agent Loop (Core Path)

**Goal:** Build a two-agent system: a writer agent creates an essay, a critic agent reviews it and gives feedback (not a rewrite), and the writer revises once based on that feedback.

### Instructions

1. Open `starter.py`
2. Find **TODO 1**: write the prompt for the writer agent, covering both the initial-draft case and the revision-with-feedback case
3. Find **TODO 2**: write the prompt for the critic agent — ask for 2-3 specific, actionable pieces of feedback (not a rewrite), focused on clarity, accuracy, impact, and engagement
4. Find **TODO 3**: the loop is mostly scaffolded already — fill in the remaining pieces so it runs writer → critic → writer-revises in sequence
5. Run it: `python starter.py`

### Expected output

```
Topic: The role of AI in climate change solutions

=== Step 1: Initial Draft ===
Draft:
AI is increasingly recognized as a critical tool in combating climate change...

=== Step 2: Feedback & Revision ===
Feedback:
- Strengthen the evidence for claims in paragraph 2
- Add specific examples of AI applications

Revised Draft:
AI is increasingly recognized as a critical tool in combating climate change...

FINAL RESULT
Topic: The role of AI in climate change solutions
Revisions: 1
[Final essay here]
```

### Key learning

- How agents specialize (writer writes, critic critiques — neither does the other's job)
- How to structure feedback so a second pass can act on it
- The simplest possible multi-agent loop: two agents, one handoff, one revision

## Setup — this exercise makes real API calls

Unlike some earlier weeks' offline exercises, this one calls a live model —
that's the point: seeing the writer actually change its output in response to
real critic feedback. You'll need:

```bash
pip install anthropic
export ANTHROPIC_API_KEY="sk-..."
python starter.py
```

If you don't have an API key yet, read through `solution.py` to see the
finished prompts and loop structure — the reasoning behind *why* each prompt
is written the way it is (feedback-only for the critic, not a rewrite;
explicit paragraph limits for the writer) is the actual exercise content, even
without running it live.

## Debugging Tips

- **"Agent produced nonsense":** add print statements to see the intermediate steps; check that your prompt is clear about exactly what the agent should do.
- **"Critic just rewrote the essay instead of giving feedback":** tighten the critic's prompt — explicitly say "provide feedback, do not rewrite the essay."
- **"Feedback isn't actionable":** ask for a specific, bounded number of points (2-3) rather than open-ended commentary.

## Solution

See `solution.py` in this folder for a complete, working writer + critic loop with both prompts filled in.
