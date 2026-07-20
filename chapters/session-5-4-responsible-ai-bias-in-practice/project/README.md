# Session 5.4 Project: Comprehensive Bias Audit Framework (Pro Path)

## Overview

Build a full, end-to-end bias audit framework:

1. **Audit configuration** (define scope: which groups, which metrics)
2. **Data collection** (collect a balanced sample)
3. **Annotation** (ground truth labels)
4. **Metrics calculation** (compute fairness metrics per group)
5. **Model card** (document findings)
6. **Parity checking** (identify violations against a threshold)

`starter.py` is already a complete, working implementation of all six steps
&mdash; there's nothing missing to fill in. This is less scaffolded than the
Core Path exercise in the sense that you're expected to *understand and then
extend* a real framework, not complete blanks in one.

## Run it

```bash
python starter.py
```

## Expected output

```
======================================================================
COMPREHENSIVE BIAS AUDIT REPORT
======================================================================

MODEL CARD:
{
  "model_name": "Hiring Recommendation System",
  "overall_metrics": {
    "accuracy": 0.845
  },
  "group_performance": {
    "accuracy": {"male": 0.92, "female": 0.75, ...},
    ...
  },
  "parity_violations": {
    "accuracy": true,
    "representation": false
  },
  "limitations": [
    "Significant disparity in accuracy across groups"
  ],
  "recommended_use": "Not recommended for high-stakes decisions..."
}
```

## Worth noticing before you extend it

The `fairness_score` metric in `starter.py` is simulated using
`hash(group) % 10` &mdash; a placeholder. Python's string hashing is
randomized per process by default, so this number will actually differ every
time you run the script. That's fine for seeing the framework's *shape*, but
it's not a real fairness measurement, which is exactly what Challenge 1 below
asks you to fix.

## Challenges

1. **Replace the simulated fairness score.** Swap `hash(group) % 10` for a
   deterministic calculation &mdash; e.g. derive it from the group's actual
   annotated-match rate, so re-running the script on the same data always
   produces the same number. `solution.py` shows one worked version of this.
2. **Add a 4th group.** Add a new group (e.g. `"asian"`) to both
   `AuditConfig.groups` and the sample data, and confirm the framework handles
   it with zero other code changes.
3. **Export just the model card.** Add an `export_model_card()` method that
   writes only the model card dict to its own JSON file, separate from the
   full text report &mdash; useful when a model card needs to be shared with a
   non-technical stakeholder on its own.

## Key learning

- The full end-to-end audit workflow, not just isolated metric calculations.
- Model cards as a documentation practice, not just an internal artifact.
- Trade-off analysis in fairness &mdash; how a parity violation on one metric
  changes the model card's recommended-use language.
- Communicating audit risks to stakeholders in a structured, repeatable format.

---

*Session 5.4 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
