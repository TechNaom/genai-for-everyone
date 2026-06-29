# Session 4.6: Week 4 Lab — Mini Build Day

**Week 4: Tool Use, Agents & Automation**  
**Live session format:** 90 minutes (lab/build time)  
**Outcome:** Build an end-to-end research agent that investigates a topic and drafts a comprehensive report

---

## Why this chapter exists

For five sessions, you've learned the building blocks:
- **4.1:** What agents actually are
- **4.2:** How agents call tools
- **4.3:** Multi-step task agents (planning → execution → synthesis)
- **4.4:** Multi-agent patterns (orchestrator, debate, reviewer)
- **4.5:** When to use agents vs. automation

This is where it comes together. You'll build a **real research agent** that:
1. Takes a topic as input
2. Plans what to research
3. Executes searches and gathers information
4. Critically evaluates sources
5. Drafts a structured report with citations
6. Allows human review before finalizing

This is a **capstone for Week 4**. It pulls together everything you've learned: tool use, planning, multi-step execution, structured output, and pragmatic decision-making about when agents make sense.

---

## Part 1: System Design

### The Agent's Job

```
User Input: "Research the current state of AI regulation across countries"
    ↓
[Agent: Planner]
  → "I need to research: US, EU, UK, China, India regulations"
    ↓
[Agent: Researcher]
  → Search each country's regulations
  → Gather recent news and policy changes
  → Identify key stakeholders
    ↓
[Agent: Analyst]
  → Evaluate which sources are reliable
  → Identify trends and patterns
  → Note conflicting information
    ↓
[Agent: Writer]
  → Draft a structured report with sections:
    - Executive summary
    - Country-by-country breakdown
    - Emerging trends
    - Implications for AI companies
    - Citations
    ↓
Output: Full research report
```

### Architecture

**Single agent with multiple "modes":**
- Mode 1: Plan what to research
- Mode 2: Execute searches
- Mode 3: Analyze findings
- Mode 4: Write report

**Or multi-agent (if you want to extend):**
- Researcher agent (searches)
- Analyst agent (evaluates)
- Writer agent (drafts)

We'll start with single agent, multi-turn.

---

## Part 2: Tools Required

The agent needs access to:

```python
tools = [
    {
        "name": "search_web",
        "description": "Search the web for current information"
    },
    {
        "name": "get_page_content",
        "description": "Get full content from a specific URL"
    },
    {
        "name": "evaluate_source",
        "description": "Evaluate credibility of a source (news org, gov site, academic)"
    }
]
```

For the lab, we'll **mock these tools** with realistic data. In production, integrate real APIs (SerpAPI, Firecrawl, etc.).

---

## Part 3: The Workflow

### Phase 1: Planning (Agent talks to itself)

```
LLM Prompt: "You're a research expert. Topic: {user_topic}
Write a detailed plan for researching this. What searches will you do?
What sources matter? How will you structure the report?"

Agent Output: "I'll research:
1. Government policy documents from each country
2. Recent news (last 6 months)
3. Expert analysis from policy organizations
4. Company perspectives
..."
```

### Phase 2: Execution (Agent searches)

```
For each planned search:
  1. Agent outputs: "I'll search for: {query}"
  2. System calls: search_tool(query)
  3. System returns: Results
  4. Agent reads and notes: "Found X results. Key info: ..."
  5. Loop until agent says "I have enough information"
```

### Phase 3: Analysis (Agent evaluates)

```
LLM Prompt: "Review what you found. What's reliable? What contradicts?
What are the key trends?"

Agent Output: "Based on searches:
- Most countries moving toward regulation
- Difference between EU (strict) and US (light)
- China/India still developing frameworks
..."
```

### Phase 4: Drafting (Agent writes)

```
LLM Prompt: "Write a comprehensive report on {topic} based on your research.
Structure:
- Executive summary
- [Section for each country]
- Key trends
- Implications
- Citations (reference sources you found)"

Agent Output: [Full report with structure]
```

---

## Part 4: Implementation Outline

```python
from anthropic import Anthropic

class ResearchAgent:
    def __init__(self, topic):
        self.topic = topic
        self.client = Anthropic()
        self.model = "claude-3-5-sonnet-20241022"
        self.messages = []
        self.findings = []
    
    def plan(self):
        """Phase 1: Create research plan"""
        prompt = f"""You're a research expert. Topic: {self.topic}
        
Write a detailed research plan. What searches will you do?
What sources matter? How will you structure the report?"""
        
        response = self.call_llm(prompt)
        self.findings.append(("plan", response))
        return response
    
    def research(self):
        """Phase 2: Execute searches (mocked)"""
        # In real version: agent makes search decisions
        # Here: mock some searches
        searches = self.extract_search_queries_from_plan()
        
        for query in searches:
            # Mock search (replace with real API)
            results = mock_search(query)
            self.findings.append(("search", query, results))
        
        return self.findings
    
    def analyze(self):
        """Phase 3: Analyze findings"""
        findings_text = format_findings_for_analysis(self.findings)
        
        prompt = f"""Based on your research on {self.topic}:

{findings_text}

What are the key insights? What contradicts? What are the trends?"""
        
        analysis = self.call_llm(prompt)
        self.findings.append(("analysis", analysis))
        return analysis
    
    def draft_report(self):
        """Phase 4: Write report"""
        findings_text = format_findings_for_report(self.findings)
        
        prompt = f"""Write a comprehensive report on {self.topic}.

Base it on this research:
{findings_text}

Structure:
- Executive Summary (2 paragraphs)
- Main Body (section per key finding)
- Key Trends
- Implications
- Citations (reference sources)

Write professional report:"""
        
        report = self.call_llm(prompt)
        return report
    
    def call_llm(self, prompt):
        """Call LLM and track messages"""
        self.messages.append({"role": "user", "content": prompt})
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=self.messages
        )
        
        result = response.content[0].text
        self.messages.append({"role": "assistant", "content": result})
        
        return result
    
    def run(self):
        """Execute full workflow"""
        print("Phase 1: Planning...")
        self.plan()
        
        print("Phase 2: Researching...")
        self.research()
        
        print("Phase 3: Analyzing...")
        self.analyze()
        
        print("Phase 4: Drafting report...")
        report = self.draft_report()
        
        return report

# Usage
if __name__ == "__main__":
    agent = ResearchAgent("AI regulation trends 2024-2025")
    report = agent.run()
    
    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60)
    print(report)
```

---

## Part 5: What Makes This Real

### Differences from toy examples

1. **Realistic scope:** Research takes multiple searches, not 1-2
2. **Structured output:** Report has sections, not just rambling
3. **Citation tracking:** Agent must reference sources, not hallucinate
4. **Human review:** Draft goes to human before publishing
5. **Error handling:** What if search returns nothing? Handle gracefully

### Extensions for production

1. **Fact-checking:** Second agent verifies claims in draft
2. **Re-ranking:** Semantic search on top of keyword search
3. **Caching:** Don't re-search same query in same session
4. **Persistence:** Save plan, findings, report to database
5. **Versioning:** Track changes to report as research evolves

---

## Part 6: Evaluation Criteria

When you build this, ask yourself:

1. **Does the plan make sense?** Does agent understand the topic and what research is needed?
2. **Are searches relevant?** Do searches actually answer the plan?
3. **Is analysis grounded?** Does agent cite findings, or hallucinate?
4. **Is report structured?** Does it have clear sections and flow?
5. **Are citations accurate?** Does agent reference actual sources it found?
6. **Is length reasonable?** 1500-3000 words for a good report?

---

## Points to Remember

1. **Plans matter:** A good plan = good research. Bad plan = wasted effort.
2. **Search is iterative:** Agent might search, learn something, search again.
3. **Citations ground claims:** "According to X" is better than unsourced claims.
4. **Humans still matter:** Even good agents benefit from human review.
5. **Mocking is okay:** Don't wait for real APIs. Mock data → test structure first.
6. **Structure != length:** A 1000-word focused report > 5000-word rambling one.

---

## Quiz and Interview Questions

**Full quiz:** [assessments/quizzes/week-04/session-4.6-quiz.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/quizzes/week-04/session-4.6-quiz.md)  
**Answer key:** [assessments/answer-keys/week-04/session-4.6-quiz-answers.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/answer-keys/week-04/session-4.6-quiz-answers.md)  
**Interview questions:** [assessments/interview-questions/week-04-interview-qs.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/interview-questions/week-04-interview-qs.md)

---

## Core path and Pro path exercises

### Core path
Build a **research agent** that:
1. Takes a topic
2. Plans 3-5 searches
3. Executes searches (mocked data)
4. Analyzes findings
5. Drafts a 1000+ word report with citations

Starter code scaffolds the workflow. Mocked search tools.

### Pro path
Build a **fact-checking layer**:
1. Agent researches (as above)
2. Second agent fact-checks the draft
3. Issues are incorporated into final report
4. Report includes uncertainty notes ("This source contradicts X")

More complex, but closer to real production systems.

---

## What's Next

**Week 5:** Evaluation, Safety & Responsible AI  
You've built agents. Now learn how to measure their quality, find errors, and ensure they're safe.

---

*Session 4.6 | GenAI for Everyone | Week 4: Tool Use, Agents & Automation*
