# Session 5.2 Exercises: Evaluation Methods

## Overview

Learn 4 ways to evaluate GenAI systems and build an evaluation harness.

- **Core Path:** Eval harness comparing 3 prompt variants (rubric + semantic)
- **Pro Path:** Multi-method harness (rubric, LLM-as-judge, semantic, human-in-loop)

---

## Core Path: Evaluation Harness

**File:** `core_path_starter.py`

### What you'll build

An eval harness that:
1. Takes 3 prompt variants (v1, v2, v3)
2. Tests on golden dataset (5 examples)
3. Scores using 2 methods:
   - **Rubric grading** (manual, 0-7)
   - **Semantic similarity** (automatic, 0-1)
4. Compares results

### How to work through it

1. Find **TODO 1**: Implement `grade_rubric()`
   - Score on Relevance (0-2), Accuracy (0-2), Helpfulness (0-2), Conciseness (0-1)
2. Find **TODO 2**: Implement `eval_prompt_variant()`
   - Run prompt on each example
   - Score with rubric and semantic
   - Calculate averages
3. Find **TODO 3**: Implement `compare()`
   - Print results table
   - Identify best variant
4. Run: `python3 core_path_starter.py`

### Expected output

```
Evaluating 3 prompt variants...

======================================================================
EVALUATION HARNESS RESULTS
======================================================================

Variant              Rubric (0-7)         Semantic (0-1)       Average   
----------------------------------------------------------------------
Variant V1 (Basic)   4.00                 0.65                 0.510    
Variant V2 (Helpful) 5.50                 0.80                 0.653    
Variant V3 (Verbose) 6.00                 0.75                 0.688    
======================================================================

✅ Best variant: Variant V3 (Verbose)
```

### Key learning

- Multiple evaluation methods give better picture
- Trade-offs are explicit (speed vs. helpfulness)
- Harness is reusable (test new variants easily)

---

## Pro Path: Multi-Method Harness

**File:** `pro_path_starter.py`

### What you'll build

A harness comparing 4 methods on same dataset:
1. **Manual rubric** (accurate but slow)
2. **LLM-as-judge** (fast but can hallucinate)
3. **Semantic similarity** (automatic, captures meaning)
4. **Human-in-the-loop** (combine LLM + human for uncertain cases)

### Run it

```bash
python3 pro_path_starter.py
```

### Expected output

```
Evaluating with 4 methods...

======================================================================
MULTI-METHOD EVALUATION COMPARISON
======================================================================

RUBRIC               Average: 0.650
LLM_JUDGE            Average: 0.680
SEMANTIC             Average: 0.670
HUMAN_IN_LOOP        Average: 0.700

----------------------------------------------------------------------
Analysis:
----------------------------------------------------------------------

Rubric vs LLM-as-judge difference: 0.030
  → Methods mostly agree. Good sign.

Human-in-loop improvement over LLM: +0.020
  → Human review helps catch edge cases.

Semantic similarity consistency: 0.895
  → Semantic aligns well with human judgment.

======================================================================
Recommendation for YOUR use case:
----------------------------------------------------------------------

✅ Use Human-in-the-loop: balances speed and accuracy
```

### Key learning

- Different methods measure different things
- Comparing methods reveals which is most reliable
- Choose based on your constraints (speed, cost, accuracy)

---

## Understanding Each Method

### Rubric Grading
**How:** You score manually on explicit criteria  
**Pros:** Most accurate, captures nuance  
**Cons:** Slow, biased, doesn't scale  
**Cost:** ~1-2 min per response  
**Use:** Small golden dataset, subjective eval

### LLM-as-Judge
**How:** Use LLM to score automatically  
**Pros:** Fast, scalable, handles open-ended responses  
**Cons:** Can be too generous, hallucinate reasoning  
**Cost:** $0.001-0.01 per response  
**Use:** Large datasets, rapid evaluation

### Semantic Similarity
**How:** Compare embeddings  
**Pros:** Fast, captures meaning, forgiving of paraphrasing  
**Cons:** Requires embedding model, not all metrics  
**Cost:** Cheap (local model)  
**Use:** Sanity check, paraphrasing-heavy tasks

### Human-in-the-Loop
**How:** LLM on all, human review flagged cases  
**Pros:** Balance speed + accuracy, only humans where needed  
**Cons:** Still requires human time  
**Cost:** ~20% human review time  
**Use:** Medium datasets, subjective metrics

---

## Strategy by Dataset Size

**< 50 examples:**
- Use manual rubric
- Maybe supplement with semantic

**50-500 examples:**
- LLM-as-judge on all
- Human review 20% (uncertain cases)
- Use human-in-the-loop

**500-5000 examples:**
- Semantic similarity on all (cheap)
- LLM-as-judge on sample (validate)
- Extrapolate results

**5000+ examples:**
- Semantic similarity on all
- LLM-as-judge on random sample
- No human review (impractical)

---

## Pitfalls to Avoid

### ❌ Over-relying on one metric
"Semantic similarity is 0.9, so we're good."  
**Fix:** Use multiple methods. Check agreement.

### ❌ LLM-as-judge without validation
"I scored with Claude API, shipping now!"  
**Fix:** Validate LLM scores against human review on subset.

### ❌ Metric misalignment
"BLEU score improved" but users say quality dropped.  
**Fix:** Metrics must match actual goals.

### ❌ Not analyzing disagreement
Methods disagree. Why? What does each capture?  
**Fix:** Investigate disagreement. It's informative.

---

## Production Checklist

Before shipping:
- ✅ Define your primary metric (speed? accuracy? safety?)
- ✅ Use 2+ evaluation methods
- ✅ Have humans validate on subset
- ✅ Document metric trade-offs
- ✅ Know failure modes

---

*Session 5.2 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
