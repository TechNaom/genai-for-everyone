# Week 5 Written Exam

_Deeper, scenario-based exam covering all of Week 5's sessions (5.1–5.6): the eval mindset, evaluation methods, safety fundamentals, responsible AI and bias, guardrails and mitigations, and the eval + safety report capstone._

**Format:** 7 short-answer questions + 3 scenario-analysis questions + 1 synthesis question
**Suggested time:** 60–75 minutes
**Open book:** Yes — this tests understanding and application, not memorization

---

## Section A — Short Answer

**A1.** Explain why "I tried it a few times and it worked" does not constitute evaluation, and name the specific artifact that replaces this kind of anecdotal check.

**A2.** What is the core difference between rubric-grading and LLM-as-judge as evaluation methods, and name one weakness specific to LLM-as-judge that rubric-grading doesn't share.

**A3.** Define prompt injection in your own words, and explain why an injection embedded in a *retrieved document* is a different threat than one typed directly by a user.

**A4.** Why can a bias check never be performed using a single output in isolation? What's the minimum structure a real bias check requires?

**A5.** Name two distinct categories of guardrail (e.g., input filtering, output filtering, system-prompt hardening, human review gates) and, for each, describe one specific way it could still fail to catch a real attack.

**A6.** In the eval + safety report format from Session 5.6, why does a "residual risk" section matter even after you've added a guardrail that measurably improved the system?

**A7.** A golden dataset scored 95% at launch. Explain a concrete way the system could get worse in production over the following months without a single line of code changing.

---

## Section B — Scenario Analysis

**B1. The Deceptively Reasonable Score**
Your semantic-similarity eval gives a summarizer's output a 0.78 similarity score against the reference summary — comfortably in the "probably fine" range you'd expect. On manual review, you discover the summary omitted a legally significant detail (a liability cap) while still using enough similar wording and structure to score reasonably high. What does this reveal about relying on similarity scores alone, and what specific mechanism (from Session 5.2) should exist alongside it to catch this exact failure?

**B2. The Guardrail That Didn't Quite Work**
You add an output filter that blocks any response containing the phrase "system prompt," specifically to prevent instruction leakage. A red-team attempt gets the model to describe its own instructions using different wording, avoiding the filtered phrase entirely. Is this guardrail a failure? What should your eval + safety report say about it, and what's the general lesson about keyword-based output filters?

**B3. The Bias Gap Nobody Noticed for Months**
A hiring-assistant tool has been in production for six months with a 92% golden-dataset pass rate. A new audit reveals that resumes with a specific university's name attached are systematically scored higher, even when work experience is held constant, and this was never caught because the golden dataset happened to not include any comparative demographic/framing tests. Explain why a high golden-dataset pass rate did not protect against this gap, and what specifically should have been in place to catch it earlier.

---

## Section C — Synthesis

**C1.** Your team's eval + safety report on a customer-facing RAG chatbot shows: 88% golden-dataset pass rate, 1 of 5 red-team attempts partially succeeded (MEDIUM severity, since patched), and no bias gaps found in the two comparisons run so far. A product manager asks: "Great, can we ship this today?" Write a 150–250 word response, in plain language, that:
- Gives a clear answer (yes, no, or conditional) grounded in the specific numbers given
- Explains what "no bias gaps found in two comparisons" does and doesn't tell you (per the bias-testing lesson from 5.4)
- Names at least one thing you'd want in place (monitoring, additional red-teaming, more bias comparisons) before considering this fully "safe to ship and forget"

---

## Answer Key

### Section A

**A1.** "I tried it a few times and it worked" is anecdotal, cherry-picked, and untracked — it has no systematic coverage of edge cases, no objective scoring, and no written record to compare against later. The artifact that replaces it is a golden dataset: a defined set of examples (happy path, edge case, boundary, adversarial) with expected outputs, scored against an explicit rubric, producing a repeatable, comparable result.

**A2.** Rubric-grading applies a fixed, human-defined set of criteria and scoring levels consistently to every output — it's deterministic and auditable but requires someone to grade each example (or automate grading against the rubric). LLM-as-judge uses a model to score outputs against a description of what "good" looks like — it scales far better than human grading but introduces its own weakness: the judge model can share the same blind spots and biases as the model being evaluated, or be fooled by fluent-but-wrong output the same way a naive human skim-reader might be.

**A3.** Prompt injection is text — hidden in user input or elsewhere — crafted to make a model ignore its original instructions and follow the attacker's instead. An injection embedded in a retrieved document is different from a user-typed one because the system doesn't need the attacker to have direct access to the chat interface at all — any document the retrieval step might pull in becomes a viable attack surface, and retrieved content is often treated as trusted context inserted into the prompt without the scrutiny applied to direct user input.

**A4.** A bias check requires a comparison — the same underlying question or task, varied only in a demographic/framing detail, with outputs compared against each other — because bias is fundamentally about *unequal treatment*, which can't be observed from a single output in isolation. The minimum structure is at least two matched variants differing in exactly one relevant dimension, with their outputs compared for unjustified differences in quality, tone, or completeness.

**A5.** Any two, each with a failure example: **Input filtering** (blocking known attack patterns in user input) can fail against novel phrasings or attacks embedded in non-user-input sources like retrieved documents. **Output filtering** (blocking responses containing certain keywords/phrases) can fail against semantically equivalent responses that avoid the exact filtered keywords. **System-prompt hardening** (explicit instructions resisting override) can fail against sufficiently creative reframings/roleplay attacks that don't trigger the specific override language it was hardened against. **Human review gates** can fail if reviewers develop automation bias (trusting the tool's output without genuinely scrutinizing it), especially for low-severity-labeled items.

**A6.** A residual risk section matters because a guardrail reducing risk is not the same as eliminating it — most guardrails (especially keyword/pattern-based ones) can still be bypassed by a sufficiently motivated or creative attacker. Documenting the residual risk honestly, even after a real improvement, is what keeps the report from becoming a false "all clear" and gives the next person (or the next audit) the information needed to keep closing the gap.

**A7.** The system can degrade without code changes via drift: the actual questions users ask shift over time (new product launches, changed policies) in ways the original golden dataset didn't anticipate; the underlying provider silently updates a model behind a version alias; or, for RAG systems, the underlying documents change or go stale while the retrieval logic and golden dataset stay the same, so what used to be correct grounding becomes outdated grounding.

---

### Section B

**B1.** This reveals that similarity/overlap scores can reward outputs that are structurally and lexically close to the reference while still missing a critical piece of meaning — high similarity is not the same as high correctness, especially for high-stakes specific details. The mechanism that should exist alongside it, per Session 5.2, is an LLM-as-judge (or rubric) score with an explicit penalty/cap rule: if a known-critical detail is omitted, the score should be capped low regardless of how high the surface similarity is, rather than letting a good "gist" match mask a specific factual omission.

**B2.** Not a total failure, but not a complete fix either — this is exactly the expected limitation of keyword-based output filters: they catch the literal phrasing they were built to catch, and can be bypassed by any equivalent rephrasing. The eval + safety report should document this specific bypass explicitly as an open, unresolved risk (not omit it because "we already added a guardrail"), and the general lesson is that keyword filters are one layer of defense, not a complete solution — they reduce but don't eliminate the underlying risk, and should be paired with monitoring/red-teaming that specifically tries rephrased attacks over time.

**B3.** A high golden-dataset pass rate only tells you the system performs well on the specific examples in that dataset — it says nothing about scenarios the dataset never included, which is exactly what happened here: no comparative demographic/framing test existed, so there was no mechanism that could have surfaced this gap regardless of how high the pass rate climbed. What should have been in place: dedicated bias-comparison tests (per Session 5.4) as a required, separate category in the golden dataset/eval process — not something a general accuracy eval incidentally catches — run and reviewed on an ongoing basis, not just once at launch.

---

### Section C

**C1.** Sample model answer (grade for content, not exact wording):

> Based on these numbers, I'd say this is conditionally ready to ship, not an unconditional yes. The 88% pass rate and the single patched MEDIUM-severity finding are reasonable for a customer-facing tool, provided we're comfortable with the roughly 12% failure rate on the golden dataset and confident the patch actually closed that specific red-team gap rather than just hiding the symptom. The bigger caveat is the bias testing: "no gaps found in two comparisons" only tells us those two specific comparisons didn't reveal a difference — it doesn't mean the system is bias-free, since we've only tested two framings out of many possible ones. Before I'd call this fully safe to ship and move on, I'd want ongoing monitoring in place (logging real user interactions and a feedback mechanism) so we catch anything the golden dataset and our two bias tests didn't anticipate, plus a plan to expand bias testing to more scenarios over the following weeks rather than treating two clean comparisons as sufficient coverage.

**Full credit (15 pts):** Gives a grounded conditional/qualified answer tied to the actual numbers [6 pts], correctly explains the limited scope of "two comparisons, no gaps found" [5 pts], names a concrete next step (monitoring, more bias tests, continued red-teaming) [4 pts].
**Partial credit:** Gives an unqualified yes/no without grounding in the specific numbers, or treats "no bias gaps found" as if it proves the system is unbiased.

---

## Grading Guidance

- **Section A (21 pts, 3 pts each):** Full credit requires the correct mechanism/definition and the "why it matters" connection.
- **Section B (24 pts, 8 pts each):** Grade holistically — strong credit for correctly identifying the underlying failure category (similarity-vs-correctness gap, keyword-filter brittleness, or bias-testing coverage gap) even with a differently worded fix, as long as the reasoning holds.
- **Section C (15 pts):** See rubric above.
- **Total: 60 pts.** Suggested cutoffs: 54+ = excellent, 42–53 = solid, 30–41 = needs review (trace missed questions back to evaluation methods/5.2, safety fundamentals/5.3, or responsible AI/5.4), <30 = recommend revisiting Week 5 sessions before Week 6.
