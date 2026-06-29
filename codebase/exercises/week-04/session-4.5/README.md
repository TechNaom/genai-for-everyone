# Session 4.5 Exercises: Automation Workflows

## Overview

Choose your path: Build an email categorization workflow using a hybrid approach (simple rules + LLM agents).

- **Core Path:** Rule-based categorizer + fallback to agent (scaffolded)
- **Pro Path:** Multi-step workflow with analysis, drafting, and cost tracking (challenge)

Both use **mocked email data** for testing. Swap in Gmail API in production.

---

## Core Path: Hybrid Email Categorizer (Scaffolded)

**File:** `core_path_starter.py`

### What you'll build
A three-step workflow:
1. **Simple rule** checks if email is urgent (keywords, sender)
2. **If unsure**, call LLM agent to categorize
3. **Take action** based on category (flag, Slack, skip)

### How to work through it
1. Open `core_path_starter.py`
2. Find **TODO 1**: Implement simple rules (check keywords, VIP senders)
3. Find **TODO 2**: Write agent prompt to categorize emails
4. Find **TODO 3**: Define actions for each category
5. Find **TODO 4**: Implement the workflow (simple → agent → action)
6. Test with: `python3 core_path_starter.py`

### Expected output
```
============================================================
EMAIL CATEGORIZATION WORKFLOW
============================================================

--- Email 1 ---
From: boss@company.com
Subject: URGENT: Q4 budget approval needed
Simple rule: urgent
Final category: urgent
Action: [FLAG IN GMAIL] + [SLACK] 🚨 Email from boss...

--- Email 2 ---
From: newsletter@medium.com
Subject: Weekly digest: AI trends
Simple rule: None
Agent categorization: normal
Final category: normal
Action: [SKIP] Email from newsletter...
```

### Key learning
- When to use rules vs. agents
- Cost optimization (rules are free!)
- Hybrid approach: best of both worlds

---

## Pro Path: Multi-Step Workflow with Analysis (Challenge)

**File:** `pro_path_starter.py`

### What you'll build
A sophisticated workflow class:
1. **Monitor** inbox (simple rule filters)
2. **Analyze** with agent (categorize, extract action items, score priority)
3. **Draft** responses for urgent emails
4. **Track** costs and performance metrics

### How to work through it
1. Open `pro_path_starter.py`
2. The `EmailWorkflow` class is mostly implemented
3. Run it as-is: `python3 pro_path_starter.py`
4. Study how:
   - `simple_monitor()` filters with rules
   - `agent_analyze()` extracts structured data
   - `agent_draft_response()` generates drafts
   - Costs are tracked per operation
5. **Challenges** (modify the code):
   - Add a "confidence" field to agent response (how sure is it?)
   - Implement conflict resolution (if simple rule says urgent but agent says normal, which wins?)
   - Add a "resend_draft_for_approval" function that emails the draft to a human
   - Track which rules are most accurate vs. agent

### Expected output
```
============================================================
MULTI-STEP EMAIL WORKFLOW
============================================================

Email 1: boss@company.com
  Subject: URGENT: Q4 budget approval needed
  Passed monitor: True
  Category: urgent
  Priority: 9/10
  Action items: ['Approve Q4 budget', 'Respond to boss']
  Draft: Dear boss, Thanks for the urgent request...
  Action: draft_created
  Time: 2.15s

Email 2: newsletter@medium.com
  Subject: Weekly digest: AI trends
  Passed monitor: False
  Action: skipped
  Time: 0.01s

============================================================
SUMMARY
============================================================
Total emails: 3
Skipped (simple rule): 1
Analyzed by agent: 2
Drafts created: 1
Total processing time: 2.50s
Avg time per email: 0.83s
Estimated cost: $0.02
```

### Key learning
- Multi-step workflows (monitor → analyze → act → track)
- Cost tracking and optimization
- Structured output from agents (JSON)
- When to use agents vs. rules
- Human-in-loop patterns

---

## No Real API Keys Needed

Both exercises use mocked email data. To use real Gmail API:

1. Set up Gmail API credentials
2. Replace `MOCK_EMAILS` with actual Gmail fetch
3. Replace action functions with real Gmail API calls

```python
# Example: Real Gmail API
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Fetch real emails
emails = gmail_service.users().messages().list(...).execute()
```

---

## Debugging Tips

### "Workflow is too slow"
- Test each step independently
- Rule filtering should be <1ms
- Agent call is ~1-2s
- Draft generation is ~1-2s

### "Agent categorization is wrong"
- Improve the prompt (be more specific)
- Add examples to the prompt
- Check if rule should catch this case instead

### "Costs are higher than expected"
- Count how many agent calls you're making
- Can you use rules instead?
- Batch process at off-peak hours?

### "Human approval step missing"
- Add a check: `if needs_approval: send_draft_for_review(email, draft)`
- In production, integrate with Gmail/Slack API

---

## Extensions

### 1. Cost Optimization Challenge
Track which emails get agent calls. Can you improve the simple rule to catch more cases without calling the agent?

```python
# Before: 50 emails processed, 30 agent calls = $0.30
# After: Improve simple rule to catch 40 cases
# Now: 50 emails processed, 10 agent calls = $0.10
```

### 2. Confidence Scoring
Have the agent output a confidence score (0-1). Only take action if confident > 0.8.

```python
analysis = agent_analyze(email)
if analysis["confidence"] < 0.8:
    flag_for_human_review(email)
```

### 3. A/B Testing
Compare simple rule accuracy vs. agent accuracy on 100 emails.

```python
for email in test_set:
    rule_result = simple_categorize(email)
    agent_result = agent_categorize(email)
    if rule_result != agent_result:
        log_mismatch(email, rule_result, agent_result)
```

### 4. Scheduling
Run the workflow on a schedule (e.g., every 5 minutes).

```python
import schedule

def check_inbox():
    emails = get_new_emails()
    workflow.process_batch(emails)

schedule.every(5).minutes.do(check_inbox)
```

---

## Further Reading

- **Session 4.1–4.4:** Agents and tool use foundations
- **Session 5.2:** Evaluation methods (measure workflow accuracy)
- **Session 6.2:** Cost & latency engineering (optimize workflows)

---

*Session 4.5 | GenAI for Everyone | Week 4: Tool Use, Agents & Automation*
