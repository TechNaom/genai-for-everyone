# Session 5.2 (v2) Exercises: Evaluation Methods for a Contract Summarizer

## Overview

- **Core Path:** Build an eval harness combining LLM-as-judge (with a
  partial-failure cap) and semantic similarity, and see the "deceptive
  middle band" problem appear in real numbers
- **Pro Path:** Prove that proper routing logic catches omission
  failures a naive threshold misses

---

## Core Path: Eval Harness

**File:** `core_path_starter.py`

### What you'll do
1. `llm_judge_score()` (TODO 1) — score with an explicit partial-failure cap
2. `needs_human_review()` (TODO 2) — implement the chapter's routing rules
3. `eval_variant()` (TODO 3) — run the full harness across 3 prompt variants

### Run it
```bash
python3 core_path_starter.py
```

### What to look for
Variant A's two omission cases (`arb_1`, `indem_1`) land at **0.75
semantic similarity** — squarely in the chapter's "deceptive middle
band" (0.70-0.85). On its own, that number looks "pretty good." The
LLM-judge's partial-failure cap is what actually catches it, dragging
the score down to 5/10 once it knows a detail was omitted.

### Key learning
A method that looks reasonable in isolation (0.75/1.0 similarity) can
still be hiding exactly the failure you care about most. This is why
the chapter pairs semantic similarity with a method specifically
designed to catch omission.

---

## Pro Path: Routing Strategy Comparison

**File:** `pro_path_starter.py`

### What you'll do
Implement `proper_routing_review()` (TODO 1) and a comparison harness
(TODO 2) that measures false negative rate **specifically among real
omission cases** — not just overall accuracy.

### Run it
```bash
python3 pro_path_starter.py
```

### Expected result
The naive "flag if similarity < 0.5" rule misses **60%** of real
omission cases, because most of them score in the deceptive 0.70-0.85
band, not low enough to trip a naive threshold. The proper routing
logic (high-risk type OR mid-band score OR uncertain LLM score)
catches all but one — at the cost of a higher overall flag rate.

### Key learning
A lower false negative rate on the failures that matter most is worth
a higher review workload. The trade-off is the point, not a flaw.

---

*Session 5.2 (v2) | GenAI for Everyone | Week 5*
