# Answer Key — Session 7.5 Quiz

**1.** The problem and user (not just the tech), the approach and *why* that approach over alternatives, one specific hard trade-off/decision made, and the actual success criteria (how you know it works).

**2.** Because it lists a tech stack without demonstrating judgment — it tells the interviewer what tools were used but nothing about why those were the right choices, what problem was actually being solved, or how you know the result was good. Describing the problem and a specific reasoned decision (chunking strategy chosen for a reason) demonstrates the judgment interviewers are actually screening for.

**3.** False. It's primarily testing whether you ask the right questions first (who's the user, is this actually a RAG problem, what's the eval plan, what's the cost/scale story) before describing any architecture — not whether you know specific API syntax.

**4.** Questions clarifying the actual user and problem (who's using this, what's the current pain point), whether retrieval/RAG is actually needed for this problem (Session 3.1's "RAG or not?"), and what the eval plan would be (how would you know if this design works) — architecture comes after these, not before.

**5.** Read the specific symptom and example failures carefully to identify the pattern (is it a formatting issue, missing context, wrong retrieval, ambiguous instructions?) rather than guessing at a fix immediately. Diagnosing the actual failure mode first is what separates a real debugging answer from a lucky guess.

**6.** "That was good" gives no information the person can act on to improve. Better feedback is specific and actionable, e.g., "You jumped straight into describing your architecture before mentioning who the user was — a real interviewer would want that context first."

**7.** Pattern recognition in failures — the ability to look at a broken prompt, pipeline, or eval result and identify the underlying cause (from Sessions 2.1-2.3 and 3.5's debugging instincts) rather than making random changes and hoping something works.
