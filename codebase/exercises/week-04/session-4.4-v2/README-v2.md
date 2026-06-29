# Session 4.4 Exercises: Multi-Agent Patterns

## Overview

Build a multi-agent system where agents collaborate. Choose your own path:

- **Core Path:** Simple writer + critic loop (scaffolded, 2 agents, 1 revision)
- **Pro Path:** Multi-reviewer with convergence checking (3 reviewers, adaptive revisions)

Both paths use **mocked agents** (no real API calls needed) for testing. Once you get the structure working, swap in real API calls.

---

## Core Path: Writer + Critic (Scaffolded)

**File:** `core_path_starter.py`

### What you'll build
A two-agent system:
1. **Writer Agent** — Creates an essay
2. **Critic Agent** — Reviews and gives feedback
3. **Writer Agent (again)** — Revises based on feedback

### How to work through it
1. Open `core_path_starter.py`
2. Find **TODO 1**: Write the prompt for the writer agent (both initial and revision cases)
3. Find **TODO 2**: Write the prompt for the critic agent
4. Find **TODO 3**: Implement the loop (already partially done, fill in the blanks)
5. Test with: `python3 core_path_starter.py`

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
- How agents specialize (writer writes, critic critiques)
- How to structure feedback for revision
- Simple multi-agent loop pattern

---

## Pro Path: Multi-Reviewer with Convergence (Challenge)

**File:** `pro_path_starter.py`

### What you'll build
A sophisticated multi-reviewer system:
1. **Writer Agent** — Creates/revises essay
2. **Fact-Checker Agent** — Reviews accuracy
3. **Style-Checker Agent** — Reviews clarity
4. **Impact-Checker Agent** — Reviews engagement

With **convergence checking**: Loop stops when feedback stops changing (agents agree).

### How to work through it
1. Open `pro_path_starter.py`
2. Reviewers are already implemented (fact, style, impact)
3. Run it as-is: `python3 pro_path_starter.py`
4. Study how:
   - Multiple independent reviewers give feedback
   - Feedback is aggregated and passed to writer
   - Convergence score measures feedback similarity
5. **Challenges** (modify the code):
   - Change `convergence_threshold` to 0.5 or 0.8 — do more/fewer revisions happen?
   - Add a 4th reviewer (e.g., audience-relevance checker)
   - Replace similarity_score with an LLM-based similarity check

### Expected output
```
Topic: The ethics of AI in hiring

=== Revision Round 1 ===
Fact-checking...
  → AI hiring systems have documented bias issues [sources needed]...

Checking style...
  → Strong opening, but paragraph 3 is dense...

Checking impact...
  → Good ethical framing, but missing a call-to-action...

Convergence score: 0.42
Writer revising...

=== Revision Round 2 ===
[More feedback, higher convergence...]

Convergence score: 0.68
Feedback converged (> 0.65). Stopping.

RESULTS SUMMARY
Topic: The ethics of AI in hiring
Total revisions: 2
Stopped because: convergence
```

### Key learning
- How to coordinate multiple specialized reviewers
- Feedback aggregation patterns
- Convergence detection (when to stop iterating)
- Trade-offs: more reviewers = higher quality but more API calls

---

## No Real API Keys Needed

Both exercises use **mocked agents** in development mode. To switch to real API calls:

```python
# Already configured to use real API
response = client.messages.create(
    model=MODEL_ID,
    max_tokens=1024,
    messages=messages
)
```

Just make sure `ANTHROPIC_API_KEY` is set in your environment:
```bash
export ANTHROPIC_API_KEY="sk-..."
python3 core_path_starter.py
```

---

## Debugging Tips

### "Agent produced nonsense"
- Add print statements to see the intermediate steps
- Check the prompt — is it clear about what the agent should do?

### "Loop runs forever"
- Add a `max_iterations` limit (already done in pro path)
- Check stopping condition logic

### "Agents are disagreeing"
- That's okay! Multi-agent systems often surface disagreements
- Use a voting/synthesis mechanism to resolve

### "Too slow / too expensive"
- Reduce `max_tokens` if possible
- Reduce number of agents
- Cache prompts to avoid re-processing

---

## Extensions

### 1. Orchestrator Pattern
Instead of writer + critic, try:
- **Orchestrator Agent** assigns tasks ("researcher, find data")
- **Researcher Agent** runs searches
- **Writer Agent** synthesizes into report

### 2. Debate Pattern
Implement competing viewpoints:
- **Pro Agent** argues for a position
- **Con Agent** argues against it
- **Moderator Agent** synthesizes findings

### 3. Persistence
Save drafts and feedback to JSON:
```python
import json
with open("result.json", "w") as f:
    json.dump(result, f, indent=2)
```

### 4. Feedback Scoring
Let the writer rank which feedback was most helpful:
```python
ranking = writer_agent(topic, prompt="Rank this feedback by importance: ...")
```

---

## Further Reading

- **Session 4.3:** Multi-Step Task Agents (single agent, multiple steps)
- **Session 4.5:** Automation Workflows (when to use agents vs. automation)
- **Session 5.2:** Evaluation Methods (how to measure multi-agent output quality)

---

*Session 4.4 | GenAI for Everyone | Week 4: Tool Use, Agents & Automation*
