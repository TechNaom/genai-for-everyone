# Session 5.4 Exercises: Bias Audit (Core Path)

## Overview

Run a bias audit on 48 sample model outputs (hiring recommendations), across
three groups: male, female, latino.

`starter.py` is already a complete, working audit -- there are no blanks to
fill in. The point of this exercise is to **trace how it works**, run it, and
then **extend it** using the ideas below, rather than complete missing TODOs.

## Run it

```bash
python starter.py
```

## Expected output

```
======================================================================
BIAS AUDIT REPORT
======================================================================

1. ACCURACY DISPARITY
------
MALE            Accuracy: 92.0%
FEMALE          Accuracy: 75.0%
LATINO          Accuracy: 65.0%

Accuracy gap: 27.0% (target: <5%)
FINDING: Significant accuracy disparity

2. REPRESENTATION
------
MALE            Representation: 40.0%
FEMALE          Representation: 35.0%
LATINO          Representation: 25.0%

3. OCCUPATIONAL DISTRIBUTION
------

MALE:
  engineer: 60.0%
  management: 30.0%
  ...
```

## What each method does

- `calculate_accuracy()` -- treats any output with `score > 0.8` as "accurate,"
  then reports the percentage per group.
- `calculate_representation()` -- what percentage of all outputs belong to
  each group.
- `calculate_occupational_distribution()` -- what occupations get recommended
  per group, as percentages.
- `generate_report()` -- ties all three together, prints gaps against a
  target threshold (<5% for accuracy, <10% for representation), and prints a
  fixed list of mitigation suggestions.

## Extend it

Three ideas, roughly in order of difficulty:

1. **Add a 4th group.** Add sample outputs for another group (e.g. `"asian"`)
   to `SAMPLE_OUTPUTS`, and confirm the audit picks it up automatically (it
   should -- `self.groups` is derived from whatever groups appear in the data).
2. **Add a `severity()` helper.** Turn a bare gap percentage into a
   `"HIGH"`/`"MEDIUM"`/`"LOW"` label, matching the severity levels used in the
   lesson's Part 3 audit report format.
3. **Add a `save_report_json()` method.** Write the three metrics dicts (plus
   the gap and severity) to a JSON file, so the audit's numbers are
   machine-readable instead of only printed to the terminal.

`solution.py` shows one worked version of all three -- compare your approach
against it once you've made a genuine attempt, especially on the severity
thresholds you chose.

## Key learning

- How to measure bias systematically, not by impression.
- The trade-offs between different fairness metrics (accuracy, representation,
  occupational distribution all tell you something different).
- The real impact algorithmic bias has when a system reaches production.

---

*Session 5.4 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
