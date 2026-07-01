# Week 7 Written Exam

_Deeper, scenario-based exam covering all of Week 7's sessions (7.1–7.6): capstone kickoff, real-world case studies, capstone build days, mock technical interviews, and demo day/program wrap._

**Format:** 7 short-answer questions + 3 scenario-analysis questions + 1 synthesis question
**Suggested time:** 60–75 minutes
**Open book:** Yes — this tests understanding and application, not memorization

---

## Section A — Short Answer

**A1.** What are the four questions a capstone proposal must answer concretely, and why does "an AI assistant that helps with everything" fail all four?

**A2.** Why should a strong capstone visibly use 2-3 techniques from this program rather than being "just a chatbot"?

**A3.** Explain the MVP-first build-day discipline in your own words, and describe the specific risk it's designed to prevent.

**A4.** In the support-ticket-triage case study, what caused the classifier's confidence scores to become unreliable months after launch, even though the model itself never changed?

**A5.** Why did the contract-review case study's fix force certain clause types to always be at least "medium" severity, regardless of the model's own confidence score?

**A6.** What are the four elements of a strong "walk me through your project" interview answer, and why does listing technologies used fail to demonstrate the same thing?

**A7.** Why is a portfolio README's primary audience someone who will never talk to you, and what does that imply about how much context it needs to include?

---

## Section B — Scenario Analysis

**B1. The Ambitious Proposal That Won't Finish**
A learner proposes a capstone: "a multi-agent system that autonomously monitors five different data sources, cross-references claims, and publishes a fact-checked daily newsletter." They have 2-3 build sessions left. Diagnose the scoping problem here using the four-question framework from Session 7.1, and propose a concretely scoped-down version that could realistically reach a working, evaluated v1 in the time remaining.

**B2. The Confidence That Wasn't Checked**
A learner's capstone build log shows Checkpoint 1 (thin end-to-end pipeline) completed at 60% of their build time, not the ~25% the lesson recommends. What should have happened at that point, according to the build-day discipline, and what's the risk of continuing on the original plan without adjusting?

**B3. The Interview Answer That Missed the Point**
In a mock interview, a candidate describes their capstone as: "I used LangChain, ChromaDB, and Claude to build a RAG chatbot over some PDFs." Using the case studies and interview-prep material from this week, explain specifically what's missing from this answer, and rewrite it (2-3 sentences) to include what's missing, using a plausible detail you invent for the example.

---

## Section C — Synthesis

**C1.** You're at Capstone Demo Day, about to present. Write out your actual 5-beat demo script (per Session 7.6) for a hypothetical capstone of your choosing (invent a plausible one in 1 sentence first, then write the 5 beats). Beats should include: the problem in one sentence, a description of a live example, one specific thing that went wrong during building and how it was fixed, your actual success criteria and whether they were met, and what you'd build next.

---

## Answer Key

### Section A

**A1.** The four questions: (1) what specific problem, for what specific user; (2) what does it actually do, end to end; (3) what techniques from the program does it use, and why; (4) how will you know if it worked. "An AI assistant that helps with everything" fails all four: it names no specific user or problem (1), gives no concrete input→output description (2), implies no particular technique choice tied to a real need (3), and offers no way to define or check success (4) — it's a wish, not a scope.

**A2.** Because the capstone is meant to demonstrate the depth built across the program's six prior weeks — a project that's "just a chatbot" wastes that depth and looks identical to something buildable in an afternoon with no RAG, evaluation, or safety training behind it. Visibly using 2-3 techniques (e.g., RAG + evaluation, or agents + guardrails) for a real reason shows distinct, defensible skills rather than a single surface-level feature.

**A3.** MVP-first means building the thinnest possible end-to-end version of the project first — however crude — before improving any individual piece, so that a complete (if rough) pipeline exists early rather than several unfinished, individually-polished pieces. The specific risk it prevents is running out of build time with nothing that runs end to end at all, which is a much worse outcome than a working-but-simple v1.

**A4.** The company added new product lines, introducing ticket types that didn't fit any of the classifier's original categories. Rather than being recognized as new/unknown, these were force-fit into the closest existing (wrong) category, often with high confidence — the real-world distribution of tickets drifted while the classifier's fixed categories and calibration stayed the same.

**A5.** Because the cost of a rare miss on a high-stakes clause type (indemnification, liability) is far greater than the cost of a few extra careful human reads on clauses that turn out to be fine — the firm chose to accept a small, predictable, recurring cost (more review time) in exchange for closing off the specific failure mode where a legally significant issue could slip through with a falsely low severity label.

**A6.** The four elements: the problem and user (not just the tech stack), the approach and *why* that approach was chosen over alternatives, one specific hard trade-off made during building, and the actual success criteria and whether they were met. Listing technologies used fails to demonstrate the same thing because it describes tools, not judgment — it gives no evidence of why those choices were right for this specific problem or how the result was actually verified.

**A7.** Because the actual audience for a portfolio README — a recruiter or hiring manager browsing GitHub — has no prior context about the program, the presenter, or the project's backstory, and will typically spend under two minutes deciding whether the project is worth a closer look. This means the README needs to be fully self-contained: explaining what the project does, for whom, how it was evaluated, and how to run it, without assuming any shared context with the reader.

---

### Section B

**B1.** This proposal fails the scoping test on multiple fronts: the user/problem is vague ("monitor five data sources" for whom, solving what specific pain point?), it implies significant multi-agent orchestration and real-time monitoring infrastructure that's unlikely to be buildable and evaluable in 2-3 sessions, and there's no stated success criterion. A scoped-down version: pick a single data source and a single specific claim-checking task (e.g., "given a news article, cross-reference its top 3 factual claims against two reference sources and flag unsupported ones"), using RAG + evaluation as the 2 techniques, with a golden dataset of 8-10 articles and a defined pass rate as the success criterion — buildable end-to-end in the remaining time, and honestly scoped as a narrower proof-of-concept rather than the full autonomous newsletter system.

**B2.** At 60% elapsed with only Checkpoint 1 complete, the build-day discipline calls for immediate scope simplification — cutting a feature, hard-coding something that was meant to be dynamic, or shrinking the dataset — rather than continuing on the original plan and hoping to catch up. The risk of continuing unchanged is running out of time before reaching Checkpoint 3 (an actual eval pass), ending the build day with an impressive-looking but unevaluated system — exactly the "demo without evidence it works" problem the eval mindset (Week 5) warns against.

**B3.** What's missing: any mention of the actual problem or user this solved, any explanation of *why* those specific tools/techniques were chosen over alternatives, any hard trade-off or decision made during building, and any stated success criteria or evaluation result — it's a list of technologies with no judgment demonstrated. Rewrite example: "Freelancers I know kept losing track of overdue invoices across multiple clients, so I built a RAG pipeline over their uploaded invoice PDFs to answer questions like 'which invoices are overdue' — I chose RAG specifically because I needed every answer grounded in the real documents rather than risking a hallucinated dollar amount. The hardest call was requiring user confirmation on any answer involving a specific number, which added friction but felt necessary given the stakes, and I validated it against a 10-question golden dataset, hitting 90% accuracy with zero hallucinated amounts across my red-team tests."

---

### Section C

**C1.** Sample model answer (grade for content, not exact wording):

> Capstone: a Q&A bot that helps solo freelancers track overdue invoices and payment terms across multiple clients, grounded in their own uploaded invoice documents.
>
> **Beat 1 (Problem):** "Freelancers juggling several clients often lose track of which invoices are overdue and what payment terms each client agreed to."
> **Beat 2 (Live example):** "Watch: I ask 'which invoices are overdue?' and it answers with the specific invoice numbers and dates, citing the actual uploaded documents — not a guess."
> **Beat 3 (What went wrong):** "Early on, it occasionally hallucinated a dollar amount when the retrieved invoice was ambiguous — so I added a rule requiring user confirmation on any answer involving a specific number, even though that added a small amount of friction."
> **Beat 4 (Success criteria):** "I measured this against a 10-question golden dataset requiring 80%+ accuracy and zero hallucinated dollar amounts — it hit 90% accuracy with zero hallucinations across 5 red-team attempts."
> **Beat 5 (What's next):** "With more time, I'd add support for multi-currency invoices and a lightweight reminder-scheduling feature."

**Full credit (15 pts):** All 5 beats present and correctly shaped [3 pts each], with beat 3 describing a real, specific problem+fix (not generic) and beat 4 stating actual numbers rather than vague impressions.
**Partial credit:** Missing one beat, or beats 3/4 are vague/generic rather than specific.

---

## Grading Guidance

- **Section A (21 pts, 3 pts each):** Full credit requires the correct mechanism/definition and its connection to the "why."
- **Section B (24 pts, 8 pts each):** Grade holistically — strong credit for correctly diagnosing the underlying issue (scoping discipline, build-day checkpoint discipline, or interview-answer substance) even with different specific wording, provided the reasoning holds.
- **Section C (15 pts):** See rubric above.
- **Total: 60 pts.** Suggested cutoffs: 54+ = excellent, 42–53 = solid, 30–41 = needs review (trace missed questions back to capstone kickoff/7.1, case studies/7.2 & 7.4, or mock interviews/7.5), <30 = recommend revisiting Week 7 sessions before demo day.
