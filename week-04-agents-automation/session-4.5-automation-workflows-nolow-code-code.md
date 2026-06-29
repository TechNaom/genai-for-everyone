# Session 4.5: Automation Workflows (No/Low-Code + Code)

**Week 4: Tool Use, Agents & Automation**  
**Live session format:** 60–90 minutes  
**Outcome:** Build an end-to-end automation workflow combining no-code triggers, LLM agents, and code-based actions

---

## Why this chapter exists

You've built agents. You've understood multi-agent patterns. But when you step back, not every problem needs an intelligent agent. Sometimes a simple trigger ("every Monday at 9am, do X") is better than an LLM that costs $0.50 per run.

This chapter teaches you to think like a systems engineer, not just an AI engineer. When should you use:
- **Simple automation** (fast, cheap, predictable)
- **LLM agents** (flexible, can reason, but slower and more expensive)
- **Hybrid** (combination of both)

The real world is messy. You'll use Zapier for "send reminder emails." You'll use an agent for "research and summarize competitor announcements." You'll chain both together for "monitor email inbox, flag interesting ones, draft responses, and ask human for approval."

This chapter teaches you to choose the right tool for each part of your workflow.

---

## Part 1: The Three Types of Automation

### Type 1: Simple Automation (Scheduled Tasks)

**What it is:** Trigger → Action. No reasoning.

**Examples:**
- Every day at 6am, send a summary email
- Every Friday at 5pm, generate a weekly report
- Every hour, check server health and alert if down

**Technology:** Cron jobs, Zapier, Make.com, IFTTT

**Cost model:** Usually free or $10-50/month (flat rate)

**Speed:** Instant—no API calls, just execute

```python
# Pseudo-code: Daily email recap
schedule.every().day.at("06:00").do(send_recap_email)

def send_recap_email():
    messages = fetch_important_emails(since="yesterday")
    summary = format_email_summary(messages)
    send_email(recipient="you@company.com", body=summary)
```

**When to use:**
- Task is predictable (same thing every time)
- No reasoning needed
- High frequency (cost matters)
- No user input required

---

### Type 2: LLM-Based Agents

**What it is:** User input → Agent thinks → Agent acts → Response

**Examples:**
- Research a topic and summarize
- Draft a marketing email based on product features
- Analyze a customer complaint and suggest resolution

**Technology:** Python + LLM SDK (OpenAI, Anthropic, etc.)

**Cost model:** Per-request ($0.01–$1 per request, depending on task)

**Speed:** Slow—multiple LLM calls, tool invocations

```python
# Pseudo-code: Research agent
user_query = "What are competitors doing with AI?"

agent = ResearchAgent(tools=[search_web, summarize])
result = agent.run(user_query)  # Takes 10-30 seconds, costs $0.10-0.50
```

**When to use:**
- Task requires reasoning or creativity
- Input is variable
- Quality > cost
- User can wait (seconds, not milliseconds)

---

### Type 3: Hybrid (Automation + Agent)

**What it is:** Scheduled trigger → Agent runs → Actions

**Examples:**
- Every Monday, agent researches market trends, sends email
- Every hour, agent analyzes logs for anomalies, alerts on findings
- Every week, agent reviews customer feedback, drafts response strategy

**Technology:** Scheduler + LLM + Action tools

**Cost model:** Per-run (Scheduler free, Agent costs $0.10 per run)

**Speed:** Slow, but scheduled so users don't wait

```python
# Pseudo-code: Weekly trends agent
schedule.every().monday.at("09:00").do(run_trends_agent)

def run_trends_agent():
    agent = TrendsAgent(tools=[search_web, send_email])
    result = agent.analyze_trends()  # Runs once a week, costs $0.20
    agent.send_email_report(result)
```

**When to use:**
- Reasoning needed, but on a schedule
- Task runs infrequently (cost is acceptable)
- Humans want the results, not real-time interaction

---

## Part 2: Decision Framework

**How to choose:**

```
Is the task predictable and repetitive?
├─ YES → Use simple automation
└─ NO → Does it require reasoning?
    ├─ NO → Use simple automation with parameters
    └─ YES → Can it be scheduled?
        ├─ YES → Use hybrid (scheduled agent)
        └─ NO → Use agent (real-time)
```

---

## Part 3: Real-World Example — Email Triage Workflow

Let's build a **hybrid workflow**: Monitor inbox, flag important emails, draft responses for critical ones.

### Architecture:

```
[Email arrives] 
    ↓
[Scheduler: Every 5 minutes, check inbox]
    ↓
[Simple rule: Filter unread emails]
    ↓
[Agent: Categorize importance, extract action items]
    ↓
[Simple automation: Flag in Gmail if urgent]
    ↓
[Agent: Draft response for urgent emails]
    ↓
[Simple automation: Send draft to human for review]
```

### Step 1: Scheduled check (Simple automation)

```python
import schedule
from gmail_api import get_unread_emails, mark_important

def check_inbox():
    """Run every 5 minutes"""
    emails = get_unread_emails()
    for email in emails:
        if categorize_simple(email) == "urgent":
            mark_important(email)

def categorize_simple(email):
    """Simple rule-based categorization"""
    if "URGENT" in email.subject.upper():
        return "urgent"
    if email.from_address in VIP_CLIENTS:
        return "urgent"
    if "error" in email.body.lower() and "server" in email.body.lower():
        return "urgent"
    return "normal"

schedule.every(5).minutes.do(check_inbox)
```

**Cost:** Free (no API calls)  
**Speed:** <1 second

### Step 2: Agent categorizes and extracts (LLM Agent)

```python
from anthropic import Anthropic

client = Anthropic()
MODEL = "claude-3-5-sonnet-20241022"

def agent_categorize_email(email_content):
    """Use agent to intelligently categorize"""
    prompt = f"""Analyze this email and categorize it.

Email:
Subject: {email_content['subject']}
From: {email_content['from']}
Body: {email_content['body']}

Respond with JSON:
{{
  "category": "urgent" | "important" | "normal",
  "reason": "why?",
  "action_items": ["item1", "item2"],
  "sentiment": "positive" | "neutral" | "negative"
}}"""
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    
    import json
    return json.loads(response.content[0].text)

# Test
result = agent_categorize_email(email)
print(result["category"])  # "urgent" → flag it
```

**Cost:** $0.01 per email  
**Speed:** 1-2 seconds

### Step 3: Draft response (Agent with tool)

```python
def agent_draft_response(email_content, category):
    """If urgent, draft a response"""
    if category != "urgent":
        return None
    
    prompt = f"""Draft a professional response to this urgent email.

Original Email:
From: {email_content['from']}
Subject: {email_content['subject']}
Body: {email_content['body']}

Guidelines:
- Keep it brief (3-4 sentences)
- Be professional
- Address the main concern
- Offer next steps

Draft response:"""
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.content[0].text

# Test
draft = agent_draft_response(email, "urgent")
print(draft)  # "Hi, Thanks for reaching out..."
```

**Cost:** $0.01 per draft  
**Speed:** 1-2 seconds

### Step 4: Send to human for approval (Simple automation)

```python
def send_for_review(email_id, draft):
    """Simple action: email human the draft"""
    review_email = f"""
New urgent email (ID: {email_id})

Suggested response:
{draft}

Approve? Reply-all to accept."""
    
    send_email(
        to="you@company.com",
        subject="Review: Urgent email response",
        body=review_email
    )

# Trigger
if draft:
    send_for_review(email["id"], draft)
```

**Cost:** Free  
**Speed:** <1 second

---

## Part 4: Building Hybrid Workflows

### Pattern 1: Scheduled Agent

```python
import schedule

def daily_market_analysis():
    agent = MarketAgent(tools=[search_web, send_email])
    trends = agent.analyze_trends()
    agent.send_report(trends)

schedule.every().monday.at("09:00").do(daily_market_analysis)
```

### Pattern 2: Triggered Agent

```python
def on_new_customer_email(email):
    agent = SupportAgent(tools=[search_knowledge_base, draft_reply])
    response = agent.handle(email)
    send_draft_for_review(response)

# Trigger: Gmail webhook on new email
webhook.on("new_email", on_new_customer_email)
```

### Pattern 3: Human-in-Loop

```python
def workflow():
    # Step 1: Automation
    data = fetch_data()
    
    # Step 2: Agent
    agent = AnalysisAgent()
    analysis = agent.analyze(data)
    
    # Step 3: Human review
    if analysis["confidence"] < 0.8:
        ask_human_for_review(analysis)
    else:
        execute_action(analysis)
```

---

## Part 5: No-Code/Low-Code Tools

For teams without software engineers, tools like **Zapier**, **Make.com**, **n8n**, **IFTTT** enable automation without code.

### Example: Zapier workflow

```
Trigger: New email in Gmail
   ↓
Action 1: Extract email data (no code)
   ↓
Action 2: Call LLM API to categorize (low code: simple HTTP call)
   ↓
Action 3: If important, send Slack notification
   ↓
Action 4: Add to spreadsheet
```

**Pros:**
- No coding required
- Visual workflow builder
- Pre-built integrations (Gmail, Slack, Salesforce, etc.)

**Cons:**
- Limited to pre-built actions
- Harder to implement complex logic
- Vendor lock-in

**When to use:** Non-technical teams, simple workflows, rapid prototyping

---

## Part 6: Cost Analysis

### Scenario: Email triage for 100 emails/day

**Simple automation only:**
- Scheduler: $0 (Cron job)
- Categorization rules: $0
- **Daily cost: $0**
- Accuracy: ~70% (misses complex cases)

**Agent only:**
- Categorization: 100 emails × $0.01 = $1.00
- Draft responses: 20 urgent × $0.02 = $0.40
- **Daily cost: $1.40**
- Accuracy: ~95%

**Hybrid (simple + agent):**
- Simple rule filter: $0 (99% accuracy on obvious cases)
- Agent on edge cases: 5 emails × $0.02 = $0.10
- Draft responses: 5 urgent × $0.02 = $0.10
- **Daily cost: $0.20**
- Accuracy: ~90%

**Winner:** Hybrid (10x cheaper than agent-only, 20% better than rules-only)

---

## Part 7: Debugging Hybrid Workflows

When something goes wrong:

1. **Identify the failure point:**
   - Did the scheduler trigger? (Check logs)
   - Did simple automation work? (Test the rule)
   - Did agent produce output? (Check for API errors)
   - Did the action execute? (Verify result)

2. **Test in isolation:**
   - Test scheduler independently
   - Test agent with mock data
   - Test action without agent

3. **Add observability:**
   - Log each step
   - Track costs (agent calls)
   - Monitor latency

---

## Points to Remember

1. **Not every problem needs an agent.** Simple automation is faster and cheaper.
2. **Choose based on predictability:** Predictable → rules. Variable → agent.
3. **Hybrid is often best:** Use rules for 90% of cases, agent for edge cases.
4. **Cost matters:** Simple automation = free. Agent = $0.01-1 per run.
5. **Speed matters:** Scheduled workflows let you use slower agents.
6. **Human-in-loop increases trust:** Especially for high-stakes decisions.
7. **Test each component separately:** Don't debug the whole workflow at once.

---

## Quick Check: Fill in the Blanks

1. **Simple automation** is best for tasks that are \_\_\_\_\_\_\_\_\_\_\_\_ and \_\_\_\_\_\_\_\_\_\_\_\_.
   - Answer: *predictable* and *repetitive*

2. An **LLM agent** costs more but provides better \_\_\_\_\_\_\_\_\_\_\_\_ for variable tasks.
   - Answer: *accuracy* or *reasoning*

3. A **hybrid workflow** combines \_\_\_\_\_\_\_\_\_\_\_\_ (cheap, fast) with \_\_\_\_\_\_\_\_\_\_\_\_ (smart, flexible).
   - Answer: *rules* and *agents*

4. If a scheduled agent runs once per day, the cost for 365 runs is acceptable even if each run costs \_\_\_\_\_\_\_\_\_\_\_\_.
   - Answer: *several dollars* or *$0.50+*

5. When building workflows, \_\_\_\_\_\_\_\_\_\_\_\_ each component separately before testing the whole thing.
   - Answer: *test*

---

## Quiz and Interview Questions

**Full quiz:** [assessments/quizzes/week-04/session-4.5-quiz.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/quizzes/week-04/session-4.5-quiz.md)  
**Answer key:** [assessments/answer-keys/week-04/session-4.5-quiz-answers.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/answer-keys/week-04/session-4.5-quiz-answers.md)  
**Interview questions:** [assessments/interview-questions/week-04-interview-qs.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/interview-questions/week-04-interview-qs.md)

---

## Core path and Pro path exercises

### Core path
Build an **email categorization workflow**:
1. Simple rule checks if email is urgent (keywords, sender)
2. If rule is unsure, call LLM agent to categorize
3. Based on category, take action (flag, send to Slack, etc.)

Starter code scaffolds the workflow. Mocked email data and LLM.

### Pro path
Build a **multi-step automation workflow**:
1. Monitor inbox (simple rule)
2. Agent categorizes + extracts action items
3. Agent drafts response for urgent emails
4. Send draft to human for approval (no-code Zapier integration)
5. Track completion

More complex, involves multiple tools, human-in-loop, and integration.

---

## What's next

**Session 4.6** is the **Week 4 Lab — Mini Build Day**. You'll integrate everything: build an agent that researches a topic and drafts a full report, combining multi-step reasoning, tool use, and structured output.

For now, think about where agents fit. Not everywhere—but in the right places, they're transformative.

---

*Session 4.5 | GenAI for Everyone | Week 4: Tool Use, Agents & Automation*
