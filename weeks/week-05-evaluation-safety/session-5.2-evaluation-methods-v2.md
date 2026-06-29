# Session 5.2: Evaluation Methods

**Week 5: Evaluation, Safety & Responsible AI**
**Live session format:** 60–90 minutes
**Outcome:** Build an eval harness that scores 3 prompt variants using multiple methods

---

## Why this chapter exists

A legal tech startup builds a tool that reads contract clauses and produces a one-sentence plain-English summary — meant for a non-lawyer to quickly understand what a clause actually commits them to. A summary like *"You're giving up your right to sue in court and agreeing to arbitration instead"* for an arbitration clause.

The team needs to evaluate three different prompt variants before picking one to ship. But how do you score "is this summary faithful to the clause" at scale? You can't read all 3 variants' output on 500 clauses yourself — that's 1,500 summaries. You also can't just trust an automated score blindly, because a summary can use completely different words and still be faithful, or use very similar words and still misrepresent the clause's actual legal effect.

This is exactly the problem Session 5.1's golden dataset and rubric don't fully solve on their own: a rubric is accurate but doesn't scale to 1,500 summaries by hand, and a single automated metric can be fooled. This chapter covers four evaluation methods, what each one is actually good at, and how to combine them so you're not relying on any single one's blind spots.

---

## Part 1: Rubric Grading (Manual)

**What it is:** A human scores each output against explicit criteria — the same approach from Session 5.1, just formalized as one tool among several here.

**Pros:**
- ✅ Catches subtle legal misrepresentation a keyword match would miss
- ✅ Can judge things a machine can't easily check, like "does this summary downplay how serious the clause actually is"
- ✅ Transparent — you can explain exactly why a summary scored low

**Cons:**
- ❌ Slow — a lawyer reviewing summaries for legal accuracy might take 2-3 minutes each
- ❌ Doesn't scale — 1,500 summaries at 2 minutes each is 50 hours
- ❌ A tired reviewer on summary #380 grades differently than on summary #12

**When to use:**
- The final, smaller-scale check before shipping (golden dataset size, not the full test set)
- Anywhere subjective legal/ethical judgment is the actual bottleneck

**Example rubric for a clause summary:**

```python
def grade_summary(clause_text, summary, expected_meaning):
    """Manual rubric grading — same shape as Session 5.1's rubric"""

    # Legal Accuracy (0-2): does the summary correctly state what the
    # clause actually does, legally?
    accuracy = 2  # human judgment call

    # Completeness (0-2): does it omit a legally significant detail?
    # e.g., an arbitration clause that also waives class actions —
    # summarizing only "arbitration" and skipping "no class action"
    # is incomplete even if the arbitration part is correct
    completeness = 2

    # Plain Language (0-1): would a non-lawyer actually understand it?
    plain_language = 1

    # Severity Match (0-2): does the summary's TONE match how serious
    # the clause actually is? A summary of a binding arbitration clause
    # written in a breezy, low-stakes tone is a failure even if the
    # facts are technically correct
    severity_match = 2

    return accuracy + completeness + plain_language + severity_match  # /7
```

---

## Part 2: LLM-as-Judge (Automated)

**What it is:** Use an LLM to score the summaries automatically, instead of a human reading all 1,500.

**Pros:**
- ✅ Fast — scores 1,500 summaries in minutes, not 50 hours
- ✅ Consistent in the sense that it doesn't get "tired" the way a human reviewer does
- ✅ Can still make a judgment call on something a rule-based metric can't, like tone

**Cons:**
- ❌ Tends to be generous — an LLM judge often rates things "pretty good" even when they're subtly wrong
- ❌ Can be fooled by confident-sounding language, the same way humans skimming quickly can be
- ❌ Costs money per call, though far less than 50 hours of legal review

**When to use:**
- Large test sets where manual review of everything is infeasible
- As a first-pass filter, with human review reserved for what it flags

**Example LLM-as-judge for the contract summarizer:**

```python
from anthropic import Anthropic

client = Anthropic()

def llm_score_summary(clause_text, summary):
    """Use an LLM to judge faithfulness of a contract clause summary"""

    prompt = f"""You are reviewing a plain-English summary of a legal
contract clause for accuracy.

Clause text:
{clause_text}

Summary given to the user:
{summary}

Score 0-10 on whether the summary is legally accurate AND captures
the full practical effect of the clause (not just part of it).
A summary that is technically true but misses a legally significant
detail (e.g., mentions arbitration but omits a class-action waiver)
should score no higher than 5.

Score (just the number):"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )

    return int(response.content[0].text.strip())
```

**A concrete failure mode for this exact use case:** an LLM judge asked simply "is this summary accurate?" will often score a summary that mentions arbitration but completely omits a buried class-action waiver as an 8 or 9 — because the part it DID say is accurate. The fix above is narrow on purpose: it explicitly tells the judge that an incomplete-but-true summary should be capped at 5. Without that instruction, LLM-as-judge's generosity bias and the specific failure mode of this task (partial truths) compound each other.

---

## Part 3: Automatic Metrics

**What they are:** Computational metrics that compare the generated summary to a reference summary, without any LLM call.

### Semantic Similarity
Embeds both summaries and compares meaning, forgiving different wording.

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(summary_a, summary_b):
    emb_a = model.encode(summary_a)
    emb_b = model.encode(summary_b)
    return util.pytorch_cos_sim(emb_a, emb_b).item()  # 0-1
```

**Where this metric actively misleads, for THIS task specifically:**

```
Reference summary: "You agree to arbitration and waive your right
                     to join a class action lawsuit."

Candidate A: "You agree to settle disputes through arbitration
              instead of going to court, and you give up the
              ability to join a class action."
  → Semantic similarity: 0.91 (genuinely faithful, different wording)

Candidate B: "You agree to arbitration for any disputes that arise."
  → Semantic similarity: 0.79 (still reasonably high!)
  → But this candidate OMITS the class-action waiver entirely —
    arguably the more legally significant part of the clause.
```

A 0.79 looks "pretty good" on a 0-1 scale. But Candidate B is missing the single most consequential detail in the clause. Semantic similarity measures how close in *meaning space* two pieces of text are — it has no concept of "which omitted detail matters more," because it was never told there's a hierarchy of importance within the clause. This is the central limitation to understand: semantic similarity catches paraphrasing well and catches *selective omission* poorly, because an incomplete-but-related summary is still semantically close to a complete one.

**When to use:** As a fast, free sanity check across a large set, paired with a method that can catch omission — never as the only signal for a task where missing details are dangerous.

---

## Part 4: Human-in-the-Loop

**What it is:** Combine automation (covers everything) with humans (covers what automation gets wrong) — LLM-as-judge scores all 1,500, a lawyer reviews only the cases that need it.

**The routing decision matters more than the math.** For this task, route to human review when:
- LLM-as-judge score is in the uncertain middle (4-7), not just low scores
- Semantic similarity is moderate-high (0.7-0.85) — exactly the band where Candidate B above lives, since a clean 0.95+ is probably genuinely faithful and a clean <0.5 is probably genuinely bad, but the middle band is where omission hides
- The clause type is flagged as high-risk (arbitration, class-action waivers, indemnification) regardless of any score, because the cost of missing a real failure here is much higher than for a low-stakes clause like a notice-period definition

```python
def needs_human_review(llm_score, semantic_sim, clause_type):
    HIGH_RISK_CLAUSES = {"arbitration", "class_action_waiver", "indemnification"}

    if clause_type in HIGH_RISK_CLAUSES:
        return True  # always human-reviewed, regardless of score
    if 4 <= llm_score <= 7:
        return True  # uncertain LLM judgment
    if 0.70 <= semantic_sim <= 0.85:
        return True  # the omission-prone middle band
    return False
```

Notice this routing logic is built around the *specific failure mode* identified in Part 3 — the omission-prone middle band of semantic similarity — not a generic "flag anything uncertain" rule. A human-in-the-loop system is only as good as the routing logic deciding what reaches the human; if you don't know your method's specific blind spot, you can't route around it.

---

## Part 5: Building an Evaluation Harness

An eval harness runs all of this — rubric (on a small subset), LLM-as-judge (on everything), semantic similarity (on everything), and the routing logic — and reports a verdict per prompt variant.

```python
class ContractSummaryEvalHarness:
    def __init__(self, golden_dataset, reference_summaries):
        self.dataset = golden_dataset  # clause texts + clause types
        self.references = reference_summaries  # human-verified summaries
        self.results = {}

    def eval_variant(self, summarize_fn, variant_name):
        scores = {"llm_judge": [], "semantic": [], "needs_review": []}

        for clause in self.dataset:
            summary = summarize_fn(clause["text"])
            reference = self.references[clause["id"]]

            llm_score = llm_score_summary(clause["text"], summary)
            sem_sim = semantic_similarity(summary, reference)
            flagged = needs_human_review(llm_score, sem_sim, clause["type"])

            scores["llm_judge"].append(llm_score)
            scores["semantic"].append(sem_sim)
            scores["needs_review"].append(flagged)

        self.results[variant_name] = {
            "avg_llm_judge": sum(scores["llm_judge"]) / len(scores["llm_judge"]),
            "avg_semantic": sum(scores["semantic"]) / len(scores["semantic"]),
            "pct_flagged_for_review": (sum(scores["needs_review"]) /
                                        len(scores["needs_review"])) * 100,
        }
        return self.results[variant_name]

    def compare(self, variant_names):
        print("\nVariant Comparison:")
        for name in variant_names:
            r = self.results[name]
            print(f"\n{name}:")
            print(f"  LLM-judge avg:        {r['avg_llm_judge']:.1f}/10")
            print(f"  Semantic similarity:  {r['avg_semantic']:.2f}")
            print(f"  % needing human review: {r['pct_flagged_for_review']:.1f}%")
```

The third metric — **% flagged for human review** — is arguably the most useful one for a decision-maker, even though it's not a "quality score" at all. A prompt variant with a slightly lower LLM-judge average but a much lower flag rate may be the better choice in practice, because it means less human review time at scale.

---

## Part 6: Combining Methods — A Worked Comparison

Suppose the team tests 3 prompt variants on the same 50-clause golden dataset:

```
Variant A ("concise"): instructed to keep summaries under 15 words
  LLM-judge avg: 6.8/10
  Semantic similarity avg: 0.81
  % flagged for review: 38%
  → Short summaries frequently omit secondary details (the class-action
    waiver problem from Part 3) to hit the word count

Variant B ("thorough"): instructed to mention every material term
  LLM-judge avg: 8.9/10
  Semantic similarity avg: 0.93
  % flagged for review: 9%
  → Longer, but catches the details that matter

Variant C ("plain language emphasis"): instructed to prioritize a
  non-lawyer being able to understand it, with no length constraint
  LLM-judge avg: 8.1/10
  Semantic similarity avg: 0.88
  % flagged for review: 14%
  → Slightly less complete than B in rare cases, but the rubric scores
    from a manual review of its flagged 14% show it's still catching
    the high-risk clause types correctly — it just phrases things more
    casually, which the LLM-judge mildly penalizes despite no real
    accuracy loss
```

Reading these three numbers together tells a story none of them tells alone: Variant A's lower semantic similarity and high flag rate point to the same root cause (omission for brevity). Variant B's high scores across the board make it look like the clear winner — but the team still needs the manual rubric on its flagged 9% to confirm those flags are genuinely low-risk and not high-risk clauses slipping through quietly. Variant C looks worse than B by the numbers, but a 10-minute manual rubric check on its flagged cases reveals the LLM-judge's score is penalizing tone, not accuracy — information no single automated number would have surfaced.

---

## Part 7: Common Pitfalls

### ❌ Pitfall 1: Trusting semantic similarity alone for a task where omission is dangerous
As shown in Part 3, a 0.79 similarity score can hide a missing class-action waiver. Always pair it with a method that checks completeness.

### ❌ Pitfall 2: Letting LLM-as-judge's generosity bias go unchecked
An ungrounded "is this accurate?" prompt will rate an incomplete-but-true summary too highly. The fix is a judge prompt that explicitly defines what counts as a partial failure (Part 2).

### ❌ Pitfall 3: Routing to human review based only on "low score"
The omission problem hides in the *middle* band of semantic similarity, not the bottom. A naive "review anything under 0.5" rule misses exactly the failures this task cares most about.

### ❌ Pitfall 4: Picking the variant with the single highest average score
Variant C's lower LLM-judge score, once manually checked, turned out to reflect tone, not accuracy. Without checking the actual flagged cases, the team would have under-rated a perfectly good variant.

### ❌ Pitfall 5: Never validating the automated methods against human judgment at all
If you never compare LLM-judge or semantic similarity scores to actual human review on at least a sample, you have no way of knowing which of these pitfalls is actively happening in your own system.

---

## Points to Remember

1. **No single method is reliable in isolation** for this kind of faithfulness check — each one has a known blind spot (rubric: slow; LLM-judge: generous; semantic similarity: blind to omission).
2. **Know your task's specific failure mode**, then design your routing/grading logic around THAT — not a generic "flag low scores" rule.
3. **The most useful output of an eval harness might not be a quality score at all** — "% needing human review" can be the decision-relevant number.
4. **A worse-looking automated score doesn't always mean a worse system.** Check what's actually driving the number before ranking variants by it.
5. **Validate your automated methods against human judgment periodically**, or you'll never know which blind spot is currently biting you.

---

## Quick Check: Fill in the Blanks

1. Semantic similarity can be fooled by a summary that is faithful in tone but \_\_\_\_\_\_\_\_\_\_\_\_ a legally significant detail.
   - Answer: *omits* or *misses*

2. LLM-as-judge tends to be too \_\_\_\_\_\_\_\_\_\_\_\_, rating incomplete-but-true content higher than it deserves, unless the judge prompt explicitly defines partial failure.
   - Answer: *generous*

3. The omission problem in this chapter hides in the \_\_\_\_\_\_\_\_\_\_\_\_ band of semantic similarity scores, not the lowest scores.
   - Answer: *middle*

4. "% of outputs flagged for human review" is a decision-relevant number even though it is not itself a \_\_\_\_\_\_\_\_\_\_\_\_ score.
   - Answer: *quality*

5. Before trusting an automated method's verdict on which variant is best, you should check what's actually \_\_\_\_\_\_\_\_\_\_\_\_ the score, not just compare the numbers.
   - Answer: *driving*

---

## Quiz and Interview Questions

**Full quiz:** [assessments/quizzes/week-05/session-5.2-quiz-v2.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/quizzes/week-05/session-5.2-quiz-v2.md)
**Answer key:** [assessments/answer-keys/week-05/session-5.2-quiz-answers-v2.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/answer-keys/week-05/session-5.2-quiz-answers-v2.md)
**Interview questions:** [assessments/interview-questions/week-05-interview-qs.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/interview-questions/week-05-interview-qs.md)

---

## Core path and Pro path exercises

### Core path
Build an evaluation harness for a contract clause summarizer that:
1. Implements LLM-as-judge scoring with an explicit "partial-failure cap" instruction
2. Implements semantic similarity scoring
3. Tests 3 mock prompt variants against a small golden dataset
4. Reports which variant has the highest "real" quality once you manually spot-check flagged cases

### Pro path
Build the full routing system from Part 4:
1. Implement `needs_human_review()` with the middle-band logic, not a naive low-score threshold
2. Run it against a dataset designed to include the "Candidate B" failure (high similarity, missing detail)
3. Measure: does your routing logic actually catch the omission cases that a naive threshold would miss?
4. Report false negative rate specifically for omission-type failures

---

## What's next

**Session 5.3** covers **Safety Fundamentals** — using an internal company wiki search assistant as the running example, where the attack surface shifts from customer-facing prompts to cross-department data leakage.

---

*Session 5.2 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
