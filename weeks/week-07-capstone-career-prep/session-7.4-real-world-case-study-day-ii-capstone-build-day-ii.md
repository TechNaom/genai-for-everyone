# Session 7.4: Real-World Case Study Day II + Capstone Build Day II

**Week:** 7 (Capstone Career Prep)
**Format:** Live session + self-paced exercise + quiz

## Learning objective

Analyze a second, higher-stakes industry case study (legal document review), then continue your capstone build from Checkpoint 2/3 toward a complete, evaluated v2 — incorporating a peer review of your v1.

## Concept (shared by everyone)

This session has two halves, deliberately paired: a case study in a domain where GenAI mistakes carry serious consequences, followed by continued build time where you apply the same scrutiny to your own project.

## Case Study: Contract Review Assistant at a Mid-Size Law Firm

*(A composite, realistic scenario — not a specific real firm.)*

**The problem:** Associates spend hours per contract manually checking for non-standard clauses (unusual indemnification terms, missing termination clauses, non-market payment terms) before partner review. The firm wants an AI assistant that flags likely-problematic clauses for an associate to verify — explicitly *not* an AI that makes legal judgments unsupervised.

**The system:** A RAG-based pipeline retrieves the firm's internal "standard clause" library, compares each contract clause against it, and flags deviations with a suggested severity (low/medium/high) and a one-line explanation of what's unusual. Every flagged clause requires a licensed associate's sign-off before the contract moves forward — there is no auto-approval path, by design, given the stakes.

**What went right:** Associates report the tool catches nearly all the "boilerplate deviation" cases they used to find by tedious manual comparison, cutting review time roughly in half, while every actual legal judgment still runs through a human.

**What went wrong:** In one incident, the tool flagged a clause as "low severity, minor wording difference" when it was actually a **significant departure** in indemnification liability — the flagging model under-weighted a legally significant word substitution because it looked lexically similar to the standard clause (a near-miss in phrasing, not in meaning). The associate, trusting the "low severity" label, gave it a quick glance instead of the careful read a "high severity" flag would have gotten, and nearly missed it — caught only because a partner happened to review that specific contract personally.

**The fix:** The firm added a rule: severity scoring for indemnification and liability clauses specifically is *never* fully automated — those clause types are always flagged at minimum "medium" severity regardless of the model's lexical-similarity score, forcing a closer associate read every time, because the cost of a missed high-stakes clause vastly outweighs the cost of a few extra careful reads on clauses that turn out to be fine.

## Core path — guided activity

Complete the second Case Study Analysis Worksheet, then return to your capstone: move from Checkpoint 2 toward Checkpoint 3 (a real eval pass), incorporating one specific lesson from either case study (this one, or Session 7.2's) into your own project's design. Full instructions: [`codebase/exercises/week-07/session-7.4/`](../../codebase/exercises/week-07/session-7.4/).

## Pro path — extended challenge

Exchange your capstone v1 with a peer (or self-review using the provided peer-review checklist) and produce a written review identifying: one thing that's working well, one specific risk you'd want addressed before this went further, and whether the stated success criteria from the Session 7.1 proposal are actually being measured yet.

## Real-world scenario

A stakeholder asks "why does this need a human in the loop if the AI is usually right?" The contract-review case study is the answer: "usually right" isn't the bar for a domain where a rare miss is catastrophic — the value of the human-in-the-loop design is precisely in the cases the model gets subtly, confidently wrong, not the many cases it gets right.

## Key takeaways

- In high-stakes domains, severity/confidence scoring should sometimes be deliberately overridden for specific high-risk categories, rather than trusted uniformly — "usually accurate" isn't the same as "safe to automate everywhere."
- A near-miss in phrasing (lexical similarity) is not the same as a near-miss in meaning — a model comparing text similarity can under-weight a legally or factually critical distinction that looks small on the surface.
- Peer review of your own capstone applies the same "read someone else's system critically" skill from Session 7.2 to a project with real stakes: yours.
- Continuing to build without checking your success criteria against reality (are you actually measuring what your proposal promised?) risks a demo day that looks impressive but can't answer "does it work?"

## Quiz

See [`assessments/quizzes/week-07/session-7.4-quiz.md`](../../assessments/quizzes/week-07/session-7.4-quiz.md)

## Slide deck

See `assets/slides/week-07/session-7.4.pptx`
