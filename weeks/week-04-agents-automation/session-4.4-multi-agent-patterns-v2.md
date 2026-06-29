# Session 4.4: Multi-Agent Patterns

**Week 4: Tool Use, Agents & Automation**  
**Live session format:** 60–90 minutes  
**Outcome:** Build a two-agent system where one agent writes and another critiques, understanding orchestrator-worker, debate, and reviewer patterns

---

## Why this chapter exists

In Session 4.3, you built a *single* agent that planned, executed tools, and summarized. That agent did all the thinking — planning, searching, deciding when to stop. Powerful, but limited.

Real intelligence emerges from *collaboration*. When you have a hard problem, you don't solve it alone; you get a colleague to challenge your reasoning, you assign specialized tasks to different people, you have one person drive while another navigates and watches for hazards.

**Multi-agent systems** apply this principle to AI. Instead of one big agent doing everything, you run *multiple* agents that specialize, collaborate, and critique each other. One agent drafts a blog post, another reviews it for accuracy. One agent proposes a plan, another argues against it to surface flaws. One agent gathers data, another synthesizes it.

This chapter teaches you three powerful patterns:
1. **Orchestrator-Worker** — One agent manages, others execute specialized tasks
2. **Debate** — Multiple agents argue different positions to find truth through disagreement
3. **Reviewer** — One agent creates, others verify and critique

By the end, you'll understand not just *how* to build multi-agent systems, but *when* to use each pattern and what trade-offs each involves.

---

## Part 1: Why go from one agent to many?

A single multi-step agent (Session 4.3) has limits:

**Problem 1: Context window limits**  
When an agent runs for many iterations, the token count grows. By iteration 10, earlier observations are buried in context. The agent forgets what it learned in step 2.

**Problem 2: Specialization**  
Some tasks need different reasoning styles. Writing needs creativity and flow. Fact-checking needs rigor and skepticism. One agent trying both trades off quality in each.

**Problem 3: No verification**  
A single agent can confidently output nonsense. If a second agent reviews it independently, errors surface.

**Solution: Multiple agents, each with a role.**

Instead of:
```
[Single Agent: Plan → Search → Search → Search → Summarize]
```

You run:
```
[Agent A: Researcher] → [Agent B: Writer] → [Agent C: Critic] → [Agent D: Fact-Checker]
```

Each agent has fewer iterations, cleaner context, and specialized reasoning. Each can do one thing exceptionally well.

---

## Part 2: Three multi-agent patterns

### Pattern 1: Orchestrator-Worker

**Idea:** One "boss" agent coordinates. Other agents execute specialized tasks.

**When to use:**
- Task is naturally decomposable (e.g., "research market, research competitors, analyze risks")
- Tasks are independent or loosely coupled
- You want one entity managing flow

**Example:**
```
User: "Prepare a competitive analysis for Q3"

Orchestrator Agent:
  "I'll break this into 3 tasks:
   1. Task A (Research): Analyze Market Trends → Worker 1
   2. Task B (Execution): Research Competitors → Worker 2
   3. Task C (Integration): Synthesize findings → Worker 3"

Worker 1: Calls search tools, returns market data
Worker 2: Calls search tools, returns competitor data
Worker 3: Integrates both, writes summary

Orchestrator: "Great! Here's the final report..."
```

**Pros:**
- Clear separation of concerns
- Easy to parallelize (workers can run in parallel)
- Simple to understand and debug

**Cons:**
- Requires explicit task decomposition (must tell orchestrator how to split work)
- Single point of failure (if orchestrator fails, whole system fails)

---

### Pattern 2: Debate

**Idea:** Multiple agents argue opposing positions. Truth emerges from disagreement.

**When to use:**
- Problem has no obvious right answer
- You want to explore multiple perspectives
- Truth emerges from healthy disagreement (e.g., "is this marketing claim true?")

**Example:**
```
Query: "Is remote work more productive than office work?"

Agent 1 (Pro-Remote):
  "Studies show: fewer distractions, no commute, flexible hours.
   Remote workers are 13% more productive (Stanford 2020)."

Agent 2 (Pro-Office):
  "Counter-evidence: collaboration, mentorship, serendipitous meetings.
   Office workers have 40% higher engagement (Microsoft survey)."

Agent 3 (Synthesizer):
  "Context matters: remote is better for focused, individual work;
   office is better for brainstorming and mentorship."
```

**Pros:**
- Explores trade-offs naturally
- Harder to get stuck in one perspective
- Models how humans actually reason

**Cons:**
- Can get into circular arguments
- Requires stopping condition (when to declare "done debating?")
- Computationally more expensive

---

### Pattern 3: Reviewer

**Idea:** One or more agents create, others verify independently.

**When to use:**
- Output quality is critical (writing, code, legal docs)
- You want independent verification
- Errors are costly

**Example:**
```
Task: "Write blog post about LLM safety"

Writer Agent:
  "Here's a draft about alignment, RLHF, and robustness..."

Fact-Checker Agent:
  "Fact-check: RLHF acronym is correct, date of GPT-4 release is correct...
   But this claim about alignment is unsupported by the cited paper."

Style Reviewer Agent:
  "The tone is too academic. Simplify technical jargon in paragraphs 2-4."

Synthesizer:
  "Updated draft incorporating feedback..."
```

**Pros:**
- Catches errors the original agent missed
- Quality scales with number of reviewers
- Each reviewer can specialize (one checks facts, one checks style, etc.)

**Cons:**
- Expensive (multiple agents = multiple API calls)
- Slower than single agent
- Can generate conflicting feedback

---

## Part 3: The code — Writer + Critic pattern

Let's build a **Reviewer pattern**: one agent writes, another critiques, writer revises.

### Setup

```python
from anthropic import Anthropic

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

def writer_agent(topic: str, previous_feedback: str = None) -> str:
    """
    Agent 1: Writer. Writes a short essay on a topic.
    If given feedback, revises based on it.
    """
    if previous_feedback:
        prompt = f"""You are an expert writer. 
Topic: {topic}

Here is previous feedback on your draft:
{previous_feedback}

Please revise your essay addressing this feedback. Keep it to 3-4 paragraphs."""
    else:
        prompt = f"""You are an expert writer.
Write a clear, engaging essay on: {topic}
Keep it to 3-4 paragraphs. Use accessible language."""
    
    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        messages=messages
    )
    
    return "".join([block.text for block in response.content if hasattr(block, "text")])

def critic_agent(essay: str) -> str:
    """
    Agent 2: Critic. Reviews the essay for clarity, accuracy, and impact.
    Returns feedback, not a revised essay.
    """
    prompt = f"""You are a harsh but fair critic. Your job is to improve writing.

Read this essay:
{essay}

Provide 2-3 specific, actionable pieces of feedback. Be constructive but direct.
Focus on: clarity, accuracy, impact, and engagement."""
    
    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=512,
        messages=messages
    )
    
    return "".join([block.text for block in response.content if hasattr(block, "text")])

def multi_agent_writing_loop(topic: str, num_iterations: int = 2) -> dict:
    """
    Two-agent loop: Writer → Critic → Revision → Critic → Done
    """
    print(f"Topic: {topic}\n")
    
    result = {
        "topic": topic,
        "drafts": [],
        "feedback_rounds": [],
        "final_essay": None
    }
    
    # Initial draft
    print("=== Iteration 1: Initial Draft ===")
    draft = writer_agent(topic)
    result["drafts"].append(draft)
    print(f"Draft:\n{draft}\n")
    
    # Feedback + revision loop
    for iteration in range(num_iterations):
        print(f"=== Iteration {iteration + 2}: Feedback & Revision ===")
        
        # Critic reviews
        feedback = critic_agent(draft)
        result["feedback_rounds"].append(feedback)
        print(f"Feedback:\n{feedback}\n")
        
        # Writer revises
        draft = writer_agent(topic, previous_feedback=feedback)
        result["drafts"].append(draft)
        print(f"Revised Draft:\n{draft}\n")
    
    result["final_essay"] = draft
    return result

# Run the multi-agent system
if __name__ == "__main__":
    topic = "The future of AI in education"
    result = multi_agent_writing_loop(topic, num_iterations=2)
    
    print("=== FINAL RESULT ===")
    print(result["final_essay"])
```

**What's happening:**

1. **Writer creates** an initial essay
2. **Critic reviews** and gives feedback
3. **Writer revises** based on feedback
4. **Repeat** (typically 1-2 times)

The beauty: each agent is simpler than the multi-step agent in Session 4.3. Writer doesn't have to critique itself. Critic doesn't have to write. They specialize.

---

## Part 4: Real-world patterns in production

### Orchestrator-Worker in the wild

**Example: Hiring pipeline**
```
Orchestrator:
  → Recruiter Agent: Screen résumés
  → Interview Agent: Conduct technical interview
  → Reference Agent: Check references
  → Decision Agent: Synthesize → Hiring decision
```

### Debate in the wild

**Example: Risk assessment**
```
Bull Agent: "Stock price will rise because..."
Bear Agent: "No, it will fall because..."
Moderator: "Given both arguments, the risk is..."
```

### Reviewer in the wild

**Example: Code review**
```
CodeWriter Agent: Writes Python code
SecurityReviewer: "This has an SQL injection vulnerability"
StyleReviewer: "This variable name is unclear"
PerformanceReviewer: "This loop is O(n²), can be O(n)"
→ CodeWriter: Revises
```

---

## Part 5: Trade-offs and when NOT to use multi-agent

**When single-agent is better:**
- Task is simple (one step, one answer)
- Cost matters (more agents = more API calls)
- Latency matters (agents run sequentially)
- Consistency is critical (multiple agents might disagree)

**When multi-agent is worth it:**
- Output quality is critical
- Task naturally decomposes
- Different specialized reasoning helps
- You have budget and time for multiple calls

---

## Part 6: Building resilient multi-agent systems

Three things to get right:

### 1. Communication protocol
Agents need to understand each other's output format.

```python
# Good: Structured output
feedback = {
    "clarity_issues": ["Paragraph 2 is confusing"],
    "factual_errors": ["Date of GPT-4 release is wrong"],
    "impact_improvements": ["Add a concrete example"]
}

# Bad: Unstructured
"This is okay but could be better in some ways"
```

### 2. Stopping conditions
When does the multi-agent loop end?

```python
# Example: Stop after feedback converges (no new issues)
previous_feedback = "..."
current_feedback = "..."

if are_similar(previous_feedback, current_feedback):
    print("Feedback converged, stopping.")
else:
    continue_loop()
```

### 3. Conflict resolution
When agents disagree, who wins?

```python
# Option A: First agent wins
use_agent_a_output()

# Option B: Majority vote (if 3+ agents)
if vote_majority(agents):
    use_majority_output()

# Option C: Human decides
ask_human_to_choose()
```

---

## Points to Remember

1. **Multi-agent systems trade latency for quality.** More agents = more API calls = slower, but better output.
2. **Orchestrator-worker** suits decomposable tasks. **Debate** suits exploring perspectives. **Reviewer** suits verification.
3. **Agents must communicate clearly** — use structured formats, not prose.
4. **Define stopping conditions** before building (when does the loop end?).
5. **Cost and latency matter in production.** Don't add agents unless they add real value.
6. **Test with mocked agents first** before using real API calls.

---

## Quick Check: Fill in the Blanks

1. In an **orchestrator-worker** pattern, the \_\_\_\_\_\_\_\_\_\_\_\_\_\_ agent coordinates, while \_\_\_\_\_\_\_\_\_\_\_\_\_\_ agents execute tasks.
   - Answer: *orchestrator* and *worker*

2. A **debate** pattern is useful when you want to explore \_\_\_\_\_\_\_\_\_\_\_\_\_\_ and find truth through \_\_\_\_\_\_\_\_\_\_\_\_\_\_.
   - Answer: *multiple perspectives* and *disagreement*

3. In a **reviewer** pattern, the writer creates, and \_\_\_\_\_\_\_\_\_\_\_\_\_\_ verify independently.
   - Answer: *reviewer agents* or *critics*

4. Multi-agent systems are slower than single agents because \_\_\_\_\_\_\_\_\_\_\_\_\_\_.
   - Answer: *more agents = more API calls running sequentially*

5. Before building a multi-agent system, you must define \_\_\_\_\_\_\_\_\_\_\_\_\_\_ so the loop knows when to stop.
   - Answer: *stopping conditions*

---

## Quiz and Interview Questions

**Full quiz:** [assessments/quizzes/week-04/session-4.4-quiz.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/quizzes/week-04/session-4.4-quiz-v2.md)  
**Answer key:** [assessments/answer-keys/week-04/session-4.4-quiz-answers.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/answer-keys/week-04/session-4.4-quiz-answers-v2.md)  
**Interview questions:** [assessments/interview-questions/week-04-interview-qs.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/interview-questions/week-04-interview-qs.md)

---

## Core path and Pro path exercises

### Core path
Build a **writer + critic** two-agent system:
1. Writer creates an essay on a topic
2. Critic reviews and gives feedback
3. Writer revises once based on feedback
4. Return final essay

Starter code scaffolds the loop. Mocked agents (no real API calls) for testing.

### Pro path
Build a **multi-reviewer** system:
1. Writer creates an essay
2. Three independent reviewers (fact-checker, style-checker, impact-checker) review
3. Writer synthesizes feedback from all three
4. Implements a "convergence" check — when do we stop revising?
5. Return final essay + review history

More complex feedback aggregation, handling conflicting feedback.

---

## What's next

**Session 4.5** covers **Automation Workflows** — when to use agents vs. simple automation, and how to combine them for real-world tasks like "every Tuesday at 9am, check email, extract action items, send report."

For now, focus on getting agents to talk to each other effectively. The magic isn't in individual agents—it's in collaboration.

---

*Session 4.4 | GenAI for Everyone | Week 4: Tool Use, Agents & Automation*
