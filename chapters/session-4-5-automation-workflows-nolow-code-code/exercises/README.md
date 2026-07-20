# Session 4.5 Exercises — Hybrid Email Categorizer (Core Path)

## Goal

Build the core-path version of this session's central pattern: a free,
instant **simple rule** catches the obvious cases, and an **LLM agent**
only gets called when the rule is genuinely unsure. `starter.py` already
contains a fully worked implementation (each concern is bounded by
`TODO N START` / `TODO N END` comments) — the tasks below have you trace
it and then extend it, rather than fill in blanks from scratch.

## Free/open vs. paid API

`simple_categorize()` and `take_action()` are pure logic with no API
dependency. `agent_categorize()` makes a real call to the Anthropic API
and is only reached for emails the simple rule can't resolve. To run the
full workflow end to end:

```bash
export ANTHROPIC_API_KEY=your-key-here
pip install anthropic --break-system-packages
python starter.py
```

No key yet? You can still do real, verifiable work: trace
`simple_categorize()` by hand against `MOCK_EMAILS`, confirm which ones
it resolves on its own, and modify its keyword/VIP lists — all without
touching the network.

## Instructions

1. Open `starter.py`.
2. Work through TODO 1–4 in order:
   - **TODO 1** (`simple_categorize`) — trace which mock emails the rule
     catches, then add a keyword and a VIP address of your own.
   - **TODO 2** (`agent_categorize`) — read the categorization prompt,
     then extend it to also return a one-sentence `reason`.
   - **TODO 3** (`take_action`) — add a fourth `"spam"` category with its
     own action, and update the agent prompt to offer it as an option.
   - **TODO 4** (`workflow`) — add a fourth mock email designed to force
     the rule → agent hand-off, and confirm the printed output shows
     `simple_result: None` with `agent_result` populated for it.
3. Run `python starter.py` and check the printed trace against your
   expectations for each email.

## What "done" looks like

- You can explain, for each of the original three mock emails, whether
  the simple rule or the agent produced the final category.
- Your new `"spam"` category has both a way to be produced (rule or
  agent) and a `take_action` branch that handles it.
- Your added fourth email demonstrably falls through to the agent (its
  `simple_result` is `None`).

## Debugging tip

If `agent_categorize()`'s fallback (`if result not in [...]: result =
"normal"`) is catching more responses than expected, print the raw
`response.content[0].text` before it's stripped/lowered — a trailing
period or extra explanation text from the model will silently trigger
the fallback instead of raising an error, which is exactly the fragile
validation bug called out in the exercise page's debug task.

## Stuck?

A fully worked reference is in `solution.py` — run it with
`python solution.py`. Once you're comfortable with this hybrid
rule-then-agent pattern, head to the project for the Pro-path challenge:
a multi-step workflow that adds analysis, drafting, and cost tracking on
top of it.

---

*Session 4.5 | GenAI for Everyone | Week 4: Tool Use, Agents & Automation*
