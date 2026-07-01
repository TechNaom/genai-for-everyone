# Session 7.2: Real-World Case Study Day I

**Week:** 7 (Capstone Career Prep)
**Format:** Live session + self-paced exercise + quiz

## Learning objective

Analyze a real-shaped GenAI deployment end to end — problem, architecture, failure modes, and outcome — using the same vocabulary this program has built (RAG, evaluation, guardrails, cost, monitoring) to critique a system you didn't build.

## Concept (shared by everyone)

Everything so far has been building and evaluating your own small systems. Interviews and real jobs also require the reverse skill: reading someone *else's* GenAI system — in a design doc, a postmortem, or a live Q&A — and asking sharp, specific questions about it. Case study days build that muscle.

## Case Study: Support Ticket Triage at a Mid-Size SaaS Company

*(A composite, realistic scenario built from common patterns across the industry — not a specific real company.)*

**The problem:** A SaaS company's support team receives ~2,000 tickets/day. Human triage (routing to billing, technical, or account teams) takes an average of 12 minutes per ticket and is the #1 complaint in customer satisfaction surveys: "it took forever to reach the right person."

**The system they built:**
1. Incoming ticket text → embedded and classified into one of 6 categories (predictive AI, Week 1's distinction — this part isn't generative at all)
2. For technical tickets specifically, a RAG layer retrieves relevant internal documentation and drafts a suggested first-response for the human agent to review and send (generative, grounded)
3. A confidence score gates the workflow: high-confidence classifications auto-route with no human check; low-confidence ones get flagged for a human to manually triage

**What went right:**
- Average triage time dropped from 12 minutes to 40 seconds for auto-routed tickets
- The suggested-response draft cut average technical ticket first-response time by 60%, because agents were editing rather than writing from scratch

**What went wrong, three months in:**
- The classifier's confidence scores were well-calibrated at launch, but silently drifted as the company added two new product lines — new ticket types didn't fit any of the 6 original categories, so they got force-fit into the closest wrong bucket with *high* confidence (a category the eval-at-launch process never saw, exactly Session 6.4's drift lesson)
- One documented incident: the RAG-drafted response layer, for a niche technical question, retrieved an outdated internal doc (superseded 2 months earlier) and confidently drafted a response with incorrect setup instructions; an agent, trusting the tool, sent it without fully reading it — a customer executed the wrong steps and lost data
- Root cause traced to two compounding gaps: no process for retiring outdated docs from the retrieval index (Session 3.5's chunking/retrieval hygiene), and no review-gate requirement specifically for responses touching data-loss-risk topics (Session 5.5's guardrails, applied unevenly)

**The fix:**
- Added a lightweight "is this doc still current" tag, checked at retrieval time, addressing the stale-document problem directly
- Required mandatory human review (no auto-send) for any response touching a defined list of high-risk topics, regardless of confidence score
- Added a "new/unrecognized ticket type" category that routes to a human by default instead of force-fitting into an existing bucket — trading a little automation coverage for a lot less silent misclassification

## Core path — guided activity

Complete the Case Study Analysis Worksheet for this scenario: identify which Week 1-6 concepts show up where (predictive vs. generative, RAG grounding, confidence-based gating, drift, guardrails), and write your own one-paragraph root-cause analysis of the data-loss incident. Full instructions: [`codebase/exercises/week-07/session-7.2/`](../../codebase/exercises/week-07/session-7.2/).

## Pro path — extended challenge

Propose a specific, concrete redesign of the confidence-gating logic that would have caught the drift problem earlier (new/unrecognized ticket types being force-fit with high confidence) — write it as a short design note, as if proposing this change to the team that owns this system.

## Real-world scenario

In an interview, you're shown a system diagram you've never seen before and asked "what would you worry about here?" The candidates who stand out don't just say "looks good" — they immediately probe: where's the eval happening, what's the fallback if this fails, how do you know if this drifts. That's precisely the skill this case study exercises.

## Key takeaways

- Reading and critiquing someone else's GenAI system is a distinct, practicable skill from building your own — case studies exercise it directly.
- Confidence scores can be well-calibrated at launch and silently wrong later as the input distribution shifts (drift) — a system needs an explicit path for "I don't recognize this" rather than force-fitting everything into existing categories.
- Stale retrieved documents and inconsistent guardrail coverage often compound to cause the worst incidents — postmortems are rarely one root cause, they're two or three small gaps intersecting.
- The fix for a classification system's blind spot is often a new "I'm not sure" category, not a smarter classifier.

## Quiz

See [`assessments/quizzes/week-07/session-7.2-quiz.md`](../../assessments/quizzes/week-07/session-7.2-quiz.md)

## Slide deck

See `assets/slides/week-07/session-7.2.pptx`
