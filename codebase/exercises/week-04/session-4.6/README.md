# Session 4.6 Exercises: Week 4 Lab — Research Agent

## Overview

This is the **capstone lab for Week 4**. Build a research agent that investigates a topic and drafts a comprehensive report. This ties together everything from Sessions 4.1–4.5.

- **Core Path:** Research agent (plan → search → analyze → draft)
- **Pro Path:** Research + fact-checking (adds verification layer)

Both use **mocked search data**. Swap in real APIs (SerpAPI, Firecrawl) in production.

---

## Core Path: Research Agent (Scaffolded)

**File:** `core_path_starter.py`

### What you'll build
A **four-phase research agent**:
1. **Phase 1: Plan** — Agent creates a research plan
2. **Phase 2: Research** — Agent executes searches (mocked)
3. **Phase 3: Analyze** — Agent evaluates findings
4. **Phase 4: Draft** — Agent writes a comprehensive report

### How to work through it

1. Open `core_path_starter.py`
2. Find **TODO 1**: Write the planning prompt
   - Ask agent to plan 4-5 searches
   - Define credibility criteria
   - Outline report structure
3. Find **TODO 2**: Extract searches and execute them
   - Parse the plan to identify searches
   - Call `mock_search()` for each
   - Store results
4. Find **TODO 3**: Write the analysis prompt
   - Ask agent to identify themes, conflicts, gaps
   - Rank sources by credibility
5. Find **TODO 4**: Write the drafting prompt
   - Ask for executive summary, main body, implications
   - Request citations of sources
   - Target 1000+ words
6. Test with: `python3 core_path_starter.py`

### Expected output

```
============================================================
RESEARCH AGENT: AI regulation trends 2024-2025
============================================================

PHASE 1: PLANNING
------
PLAN:
I will search for:
1. US AI regulation approach
2. EU AI Act details
3. China's AI policy
4. Global trends 2024
...

PHASE 2: RESEARCHING
------
Searching: AI regulation trends 2024-2025 united states
  Found: The US approach to AI is sector-based...
...

PHASE 3: ANALYZING
------
ANALYSIS:
Key themes:
- Global move toward regulation
- EU leading with strictest rules
- US taking sectoral approach
...

PHASE 4: DRAFTING REPORT
------

============================================================
FINAL REPORT
============================================================
[Full 1500+ word report with sections and citations]
```

### Key learning

- Multi-turn LLM conversations (building on prior turns)
- Structured workflow (plan → execute → analyze → draft)
- Using agent reasoning to guide research
- Grounding report in actual findings

---

## Pro Path: Research + Fact-Checking (Challenge)

**File:** `pro_path_starter.py`

### What you'll build
**Four-step workflow with fact-checking**:
1. Research phase (gather information)
2. Draft phase (write initial report)
3. Fact-check phase (verify key claims)
4. Revision phase (incorporate feedback)

### How it works

The agent writes a draft, then:
1. Extract key factual claims
2. Fact-check them against known sources
3. Flag unverified claims in the report
4. Revise with uncertainty notes

### Run it

```bash
python3 pro_path_starter.py
```

### Expected output

```
============================================================
RESEARCH AGENT WITH FACT-CHECKING: AI regulation trends 2024-2025
============================================================

STEP 1: RESEARCH
------
✓ AI regulation trends 2024-2025 united states: The US approach...
✓ AI regulation trends 2024-2025 european union: The EU AI Act...
...

STEP 2: DRAFT REPORT
------
✓ Draft report generated
✓ Length: 1523 words

STEP 3: FACT-CHECKING
------
Found claims to verify:
1. NIST AI Risk Management Framework 2024
2. EU AI Act passed in 2024
3. FTC issued warnings about AI
...

✓ NIST AI Risk Management Framework 2024: VERIFIED - Released Sept 2023
✓ EU AI Act 2024: PARTIALLY VERIFIED - Passed 2024, enforcement varies
⚠ Congress debating AI legislation: VERIFIED - Multiple bills proposed

STEP 4: REVISE BASED ON FACT-CHECKS
------
✓ Report revised based on fact-checks

============================================================
FINAL REPORT (WITH FACT-CHECK ANNOTATIONS)
============================================================
[Report with [⚠️ UNVERIFIED] tags and Verification Notes section]

Fact-Check Summary: 7/9 claims verified
```

### Key learning

- Multi-agent collaboration (researcher + fact-checker)
- Structured extraction (parsing claims from prose)
- Uncertainty tracking (marking unverified claims)
- Quality gates (revision based on feedback)

---

## Mocked vs. Real APIs

### Core Path & Pro Path (Current)
Both use mocked search data:
```python
MOCK_SEARCH_DB = {
    "ai regulation united states": "...",
    "ai regulation european union": "...",
}
```

### To use real APIs

**Option 1: SerpAPI (Google search)**
```python
import serpapi

def real_search(query):
    client = serpapi.Client(api_key="YOUR_API_KEY")
    results = client.search({"q": query})
    return results
```

**Option 2: Firecrawl (Web scraping)**
```python
from firecrawl import Firecrawl

def get_page_content(url):
    app = Firecrawl(api_key="YOUR_API_KEY")
    result = app.scrape_url(url)
    return result['markdown']
```

Replace `mock_search()` calls with real functions.

---

## Debugging Tips

### "Agent isn't following the plan"
- Make plan prompt more specific
- Add examples of good plans
- Check if agent understood the format

### "Report is too short/long"
- Specify target word count in prompt
- Break into sections with size targets
- Check if agent is hallucinating or summarizing

### "Fact-checks are wrong"
- Improve the fact-check database
- Add more context to claims
- Consider using semantic similarity instead of keyword matching

### "Citations missing"
- Explicitly ask agent to cite sources
- Require format: "According to [source], ..."
- Count citations in output

---

## Extensions

### 1. Multi-Source Synthesis
Add a step where agent compares findings from different searches:
```python
# After research phase:
comparison = agent.call_llm(f"Compare findings from US vs EU searches. What's different?")
```

### 2. Citation Tracking
Track which search result each claim came from:
```python
findings = [
    {"query": "...", "result": "...", "claims": ["claim1", "claim2"]},
]
```

### 3. Debate Agent
Add a second agent that argues against the first draft:
```python
devil_agent = ResearchAgent()
critique = devil_agent.critique_report(draft)
final = original_agent.revise_based_on_critique(critique)
```

### 4. Real-Time Monitoring
Track the agent's performance:
- Time per phase
- Number of searches
- Citation accuracy
- User satisfaction rating

---

## Production Considerations

### Speed
- Research phase: 2-5 searches = 5-10 seconds
- Analysis: 2-3 seconds
- Drafting: 5-10 seconds
- **Total: 15-25 seconds for a full report**

### Cost
- Each search: ~$0.002 (mocked, free)
- Each LLM call: ~$0.01
- Full workflow: ~$0.04-0.10 per report
- 1000 reports/day: $40-100

### Quality
- Fact-check accuracy: ~80-90%
- Citation accuracy: ~70-80%
- Report usefulness: Depends on research quality

### Next steps for production
1. Integrate real search APIs
2. Add caching (don't re-search same topic)
3. Implement proper citation tracking
4. Add human review step
5. Monitor fact-check accuracy

---

## Further Reading

- **Sessions 4.1–4.5:** Building blocks (agents, tools, multi-agent, automation)
- **Week 5:** Evaluation (measure report quality)
- **Week 6:** Deployment (scale to production)

---

*Session 4.6 | GenAI for Everyone | Week 4: Tool Use, Agents & Automation*
