# Session 4.5 Project — Multi-Step Email Workflow (Pro Path)

## Goal

Build the Pro-path challenge: a sophisticated `EmailWorkflow` class that
runs the full hybrid pipeline — monitor → analyze → draft → track — across
a batch of emails, recording cost and timing at every step. This is less
scaffolded than the core-path exercise; you're studying a mostly-complete
implementation and extending it, not filling in blanks.

## Free/open vs. paid API

`simple_monitor()` is pure keyword logic with no API dependency.
`agent_analyze()` and `agent_draft_response()` both make real calls to the
Anthropic API. To run it end to end:

```bash
export ANTHROPIC_API_KEY=your-key-here
pip install anthropic --break-system-packages
python starter.py
```

No key yet? You can still trace `simple_monitor()`'s filtering logic
against `MOCK_EMAILS` and reason about which emails would pass through to
the (costed) agent steps, without making any API calls.

## Instructions

1. Open `starter.py`. The `EmailWorkflow` class is mostly implemented.
2. Run it as-is: `python starter.py`.
3. Study how:
   - `simple_monitor()` filters with a free rule before any API cost is spent.
   - `agent_analyze()` extracts structured JSON (category, action items,
     sentiment, priority score).
   - `agent_draft_response()` generates a draft only for urgent/important
     emails.
   - `self.costs` and `processing_time` are tracked per operation and
     rolled up in `summary()`.
4. Take on the challenges (modify the code):
   - Add a `"confidence"` field (0.0–1.0) to the agent's analysis response.
   - Implement conflict resolution: if `simple_monitor()` flags an email
     as urgent-pattern-matching but the agent categorizes it as
     `"normal"`, decide which one wins and justify it in a comment.
   - Add a `send_draft_for_approval()` method that simulates emailing a
     human the draft, called whenever confidence is below `0.8`.
   - Track which emails the simple rule and the agent would have agreed
     on, to measure how much traffic the rule alone could safely handle.

## What "done" looks like

- The workflow runs end to end and prints a summary with total emails,
  skipped count, analyzed count, drafts created, total time, and
  estimated cost.
- Your confidence field appears in every `agent_analyze()` response and
  is actually used somewhere (by the conflict-resolution or
  human-approval challenge).
- `send_draft_for_approval()` fires exactly when confidence is below your
  chosen threshold, not on every draft.

## Extensions

- **Cost optimization:** tighten `simple_monitor()`'s pattern list to
  catch more obvious cases without calling the agent, and measure how
  much your estimated cost drops.
- **A/B testing:** run both `simple_monitor()` and a full agent
  categorization on the same batch, and log every case where they
  disagree.
- **Scheduling:** wrap `process_batch()` in a `schedule.every(5).minutes.do(...)`
  call so the workflow runs unattended, matching Pattern 2 from the lesson.

## Further reading

- Session 4.1–4.4: agents and tool-use foundations this workflow builds on.
- Session 5.2: evaluation methods for measuring workflow accuracy.
- Session 6.2: cost & latency engineering for optimizing workflows like
  this one at scale.

## Stuck?

A fully worked reference is in `solution.py` — run it with
`python solution.py`.

---

*Session 4.5 | GenAI for Everyone | Week 4: Tool Use, Agents & Automation*
