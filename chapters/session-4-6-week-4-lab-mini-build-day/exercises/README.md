# Session 4.6 Exercises — Week 4 Lab: Research Agent

## Overview

This is the **capstone lab for Week 4**. Build a research agent that
investigates a topic and drafts a comprehensive report. This ties together
everything from Sessions 4.1–4.5: tool use, planning, multi-step execution,
structured output, and pragmatic decision-making about when agents make sense.

- **Core Path:** Research agent (plan → search → analyze → draft)
- **Pro Path:** Research + fact-checking (adds a verification layer)

Both use **mocked search data**. Swap in real APIs (SerpAPI, Firecrawl) in
production — the workflow logic doesn't change, only the function behind
`mock_search()` does.

---

## Core Path: Research Agent

**Files:** `core_path_starter.py` (work from this) / `core_path_solution.py` (reference)

### What you'll build

A **four-phase research agent**:
1. **Phase 1: Plan** — agent creates a research plan
2. **Phase 2: Research** — agent executes searches (mocked)
3. **Phase 3: Analyze** — agent evaluates findings
4. **Phase 4: Draft** — agent writes a comprehensive report

### How to work through it

1. Open `core_path_starter.py` and read through `ResearchAgent` end to end
   before changing anything — notice that every phase routes through the same
   `call_llm()` method, which is what keeps one running conversation across
   all four phases.
2. **TODO 1** (`phase_1_plan`): write the planning prompt — ask for 4-5
   specific searches, credibility criteria, and a report structure.
3. **TODO 2** (`phase_2_research`): extract searches from the plan and call
   `mock_search()` for each, storing the results.
4. **TODO 3** (`phase_3_analyze`): write the analysis prompt — ask the agent
   to identify themes, contradictions, gaps, and source credibility.
5. **TODO 4** (`phase_4_draft_report`): write the drafting prompt — ask for
   an executive summary, sectioned body, key findings, implications, and
   citations, targeting 1000+ words.
6. Run it: `python3 core_path_starter.py`

### Expected output shape

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

- Multi-turn LLM conversations (each phase builds on the last)
- Structured workflow (plan → execute → analyze → draft)
- Using agent reasoning to guide research, not just generate text
- Grounding the report in actual findings, not invented content

---

## Pro Path: Research + Fact-Checking (Challenge)

**Files:** `pro_path_starter.py` (work from this) / `pro_path_solution.py` (reference)

This one is **less scaffolded** — you design more of the architecture
yourself.

### What you'll build

A **four-step workflow with fact-checking**:
1. Research phase (gather information)
2. Draft phase (write initial report)
3. Fact-check phase (verify key claims)
4. Revision phase (incorporate feedback, flag what couldn't be verified)

### How it works

The agent writes a draft, then:
1. Extracts key factual claims from that draft
2. Fact-checks them against a known-answers database
3. Flags unverified claims in the final report
4. Revises the report with uncertainty notes attached

### Run it

```bash
python3 pro_path_starter.py
```

### Expected output shape

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
[Report with [⚠️ UNVERIFIED] tags and a Verification Notes section]

Fact-Check Summary: 7/9 claims verified
```

### Key learning

- Multi-agent-style collaboration (researcher role + fact-checker role)
- Structured extraction (parsing claims out of prose)
- Uncertainty tracking (marking unverified claims instead of hiding them)
- Quality gates (revision driven by feedback, not just a single pass)

---

## Running these exercises

You'll need Python 3 and the `anthropic` package installed
(`pip install anthropic`), plus a valid `ANTHROPIC_API_KEY` in your
environment — unlike earlier sessions' offline stubs, this capstone calls a
real model directly, since the point is to see genuine multi-turn agent
behavior across four real phases. `MOCK_SEARCH_DB` still keeps the "search"
step free and deterministic; only the reasoning calls hit the API.

## Checking your work

There's no automated grader. For the Core Path, confirm: the plan names
specific searches (not vague ones), Phase 2 actually searches based on the
plan, the analysis meaningfully synthesizes the findings rather than
repeating them verbatim, and the final report is well-structured, cites the
searches, and clears roughly 1000 words. For the Pro Path, confirm the
fact-check phase actually catches the claims seeded in `FACT_CHECK_DB`, and
that the final report visibly flags anything it couldn't verify rather than
quietly presenting every claim as equally certain.

Compare your implementation against the `*_solution.py` files once you've
made a genuine attempt.

## A bug worth finding

Before you assume `mock_search()` is beyond scrutiny because "it's just
mock data," look closely at how it decides which entry in `MOCK_SEARCH_DB`
to return for a given query — see the "Debug the Code" task on the
exercises page for a hint. It's a good example of a defensive-parsing-style
bug (Week 2) showing up again in an entirely different context: code that
runs without error and still returns the wrong thing every time.

---

## Further Reading

- **Sessions 4.1–4.5:** Building blocks (agents, tools, multi-agent, automation)
- **Week 5:** Evaluation (measuring report quality, not just producing it)
- **Week 6:** Deployment (scaling this to production)

---

*Session 4.6 | GenAI for Everyone | Week 4: Tool Use, Agents & Automation*
