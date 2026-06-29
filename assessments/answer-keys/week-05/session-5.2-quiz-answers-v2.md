# Session 5.2 Quiz Answers (v2)

---

## Q1: Semantic Similarity's Blind Spot
**Answer:** B) The summary still captures most of the clause's overall
meaning; similarity has no concept of which specific detail is most important
- Semantic similarity measures closeness in meaning space overall — it
  was never told a class-action waiver matters more than other phrasing
  differences.

---

## Q2: LLM-as-Judge Generosity
**Expected answer:** Without explicit guidance, an LLM asked "is this
accurate?" evaluates whether the stated content is TRUE, not whether
anything important was left OUT. A summary that's 100% true about the
part it covers will score well on a vague accuracy question, even if
it silently dropped the most consequential detail.

**Full credit:** Identifies that the judge is answering "is what's
here true" rather than "is everything that matters here."

---

## Q3: The Partial-Failure Cap
**Answer:** B) It counters the LLM-judge's tendency to rate partial
truths generously, by defining in advance what counts as a capped failure
- This is the targeted fix from Part 2 — without it, omission and
  LLM-judge generosity compound each other.

---

## Q4: Routing Logic
**Expected answer:** The dangerous failures in this task hide in the
middle band, not at the bottom — a summary that's mostly faithful but
missing one detail scores moderately high (0.70-0.85), not low. A
naive "flag only low scores" rule assumes failures always score low,
which isn't true for omission-type errors specifically.

**Full credit:** Explains that omission failures cluster in the middle
band, which a naive low-score threshold doesn't cover.

---

## Q5: Picking a "Winner" Variant
**Expected answer:** No — not without checking what's driving the
score difference first. If Variant C's lower average reflects tone
penalties rather than missing or inaccurate information, picking B
"because the number is higher" would mean choosing based on a stylistic
preference disguised as a quality difference. The team should manually
verify what each score is actually measuring before ranking variants by it.

**Full credit (1 pt):** Says no, AND explains that the score difference
needs to be understood before trusting it.
**Partial credit (0.5 pts):** Says no without explaining why.

---

## Q6: Scenario — Design a Routing Rule

**Example response:**

```
Flag for nurse review if:
  - The note type is flagged high-risk (new medication, dosage change,
    any controlled substance) — always review regardless of score
  - The LLM-judge score is in an uncertain middle range (not clearly
    excellent, not clearly bad)
  - Semantic similarity to the reference summary falls in a middle band
    (e.g., 0.70-0.85) — this is where a summary that nails the diagnosis
    but drops a specific instruction (timing, dosage, food interaction)
    is most likely to hide
```

**Full credit (1 pt):** Mirrors the chapter's 3-part structure
(high-risk category override, uncertain LLM score, middle-band
similarity) adapted sensibly to the medical context.
**Partial credit (0.5 pts):** Only proposes a low-score threshold,
missing the middle-band insight.

---

*Session 5.2 Answer Key (v2) | GenAI for Everyone | Week 5*
