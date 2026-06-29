# Session 5.4 Exercises: Responsible AI & Bias in Practice

## Overview

Conduct bias audits on model outputs to identify and measure unfairness.

- **Core Path:** Bias audit on 50 outputs (scaffolded)
- **Pro Path:** Comprehensive audit framework (design + implement)

---

## Core Path: Bias Audit

**File:** `core_path_starter.py`

### What you'll do

1. Load sample model outputs (hiring recommendations)
2. Audit for bias across 3 groups (male, female, latino)
3. Calculate metrics:
   - Accuracy per group
   - Representation per group
   - Occupational distribution
4. Document findings
5. Suggest mitigations

### Run it

```bash
python3 core_path_starter.py
```

### Expected output

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
FINDING: Significant accuracy disparity ⚠️

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

### Key learning

- How to measure bias systematically
- Trade-offs between fairness metrics
- Real impact of algorithmic bias

---

## Pro Path: Comprehensive Audit

**File:** `pro_path_starter.py`

### What you'll build

A full bias audit framework with:
1. **Audit configuration** (define scope: which groups, metrics)
2. **Data collection** (collect balanced sample)
3. **Annotation** (get ground truth labels)
4. **Metrics calculation** (compute fairness metrics)
5. **Model card** (document findings)
6. **Parity checking** (identify violations)

### Run it

```bash
python3 pro_path_starter.py
```

### Expected output

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

### Key learning

- End-to-end audit workflow
- Model cards as documentation
- Trade-off analysis in fairness
- Communicating risks to stakeholders

---

## Bias Types Explained

### Representation Bias
Some groups under-represented in training data.
```
If training data: 80% male engineers, 20% female engineers
→ Model learns "engineers are mostly male"
```

### Performance Bias
Model performs differently across groups.
```
Model accuracy: 95% for group A, 70% for group B
→ Groups get unequal service quality
```

### Allocation Bias
System denies resources unfairly.
```
Loan approval: 20% denial for group A, 40% for group B
→ Group B faces discrimination
```

### Associational Bias
Model learns harmful associations.
```
"Doctor" → male, "Nurse" → female
→ Reinforces stereotypes
```

---

## Fairness Metrics

### Demographic Parity
Same outcome rate for all groups.
```
Approval rate A = Approval rate B
(Gap < 5% is good)
```

### Equalized Odds
Same true positive & false positive rates.
```
TPR_A = TPR_B (same % approved of eligible)
FPR_A = FPR_B (same % rejected of ineligible)
```

### Calibration
Predictions equally accurate across groups.
```
When model says "80% likely":
Group A: 80% actually positive
Group B: 80% actually positive
```

### Individual Fairness
Similar individuals treated similarly.
```
Two similar applicants get similar scores
(regardless of protected attributes)
```

---

## Mitigations

### 1. Data Balancing
Oversample underrepresented groups in training.

### 2. Fairness Constraints
Add fairness objective during training.

### 3. Threshold Adjustment
Use different decision thresholds per group.

### 4. Transparency
Document findings in model card.

### 5. Human Review
Have humans review high-stakes decisions.

---

## Real Incidents

### Amazon Hiring Bot
Biased against women due to training data (10 years of male-dominated hiring).

### COMPAS Recidivism
Criminal risk assessment: higher false positives for Black defendants.

### Google Images
"CEO" image search: mostly white men (reflects societal bias).

### Healthcare AI
Used race as proxy for socioeconomic status, denied care to minorities.

---

## Production Checklist

- ✅ Define protected attributes (race, gender, age, disability, etc.)
- ✅ Collect balanced sample (1000+ examples)
- ✅ Annotate ground truth (humans label)
- ✅ Calculate metrics per group
- ✅ Document in model card
- ✅ Identify mitigations
- ✅ Monitor in production
- ✅ Plan for continuous auditing

---

*Session 5.4 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
