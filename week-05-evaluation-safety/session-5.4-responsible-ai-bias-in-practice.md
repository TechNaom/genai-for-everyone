# Session 5.4: Responsible AI & Bias in Practice

**Week 5: Evaluation, Safety & Responsible AI**  
**Live session format:** 60–90 minutes  
**Outcome:** Audit model outputs for bias (bias audit on sample set)

---

## Why this chapter exists

Your model works well. Technically sound. Passes safety tests. But then:

- A hiring chatbot recommends men 40% more often than women
- A loan approval system denies loans to minorities at higher rates
- A customer support bot responds better to some accents than others
- An image captioner misses people with disabilities

These aren't bugs. They're **bias**: systematic unfairness baked into the model.

This chapter teaches you to recognize bias, measure it, and reduce it.

---

## Part 1: Types of Bias

### Bias 1: Representation Bias
Some groups are under-represented in training data.

**Example:** If training data has 10% women in technical roles, model learns "engineers are mostly male."

**Impact:**
- Career advice biased against women
- Hiring systems favor male candidates
- Women feel excluded

**Mitigation:**
- Audit training data composition
- Oversample underrepresented groups
- Use balanced datasets

### Bias 2: Performance Bias
Model performs differently across groups.

**Example:** Speech-to-text has 35% error rate for Latinx accents, 5% for standard US English.

**Impact:**
- Deaf/hard-of-hearing with certain accents can't use system
- Accessibility barriers
- Exclusion by tech

**Mitigation:**
- Benchmark performance per group
- Collect data from diverse speakers
- Improve model fairness

### Bias 3: Allocation Bias
System denies resources/opportunities unfairly.

**Example:** Loan approval denies 30% of applications from Black applicants vs. 10% from white applicants.

**Impact:**
- Financial discrimination
- Perpetuates inequality
- Illegal in many jurisdictions

**Mitigation:**
- Monitor approval rates by group
- Audit historical data for bias
- Adjust thresholds for fairness

### Bias 4: Associational Bias
Model learns harmful associations.

**Example:** "Doctor" → male, "nurse" → female. "CEO" → white.

**Impact:**
- Reinforces stereotypes
- Users internalize biased beliefs
- Perpetuates societal inequality

**Mitigation:**
- Audit word associations
- Debias embeddings
- Use gender-neutral language

---

## Part 2: Measuring Bias

### Metric 1: Demographic Parity
Do groups get equal treatment?

```
Approval rate for group A = 80%
Approval rate for group B = 50%

Difference = 30% (bias exists)
Target: <5% difference
```

### Metric 2: Equal Opportunity
Do groups have equal chance of positive outcome?

```
True positive rate for group A = 90%
True positive rate for group B = 70%

Difference = 20% (bias exists)
```

### Metric 3: Calibration
Are predictions equally accurate across groups?

```
When model predicts 80% likelihood:
- Group A: 80% actually approve → Calibrated
- Group B: 60% actually approve → Biased
```

### Metric 4: Representation
Do groups appear fairly in outputs?

```
Occupations in job recommendations:
- Female candidates: 40% tech, 60% non-tech
- Male candidates: 60% tech, 40% non-tech

Difference suggests bias
```

---

## Part 3: Audit Framework

### Step 1: Define groups
```
Protected attributes:
- Gender (male, female, non-binary)
- Race/ethnicity (self-identified)
- Age (18-30, 31-50, 51+)
- Disability status (yes/no)
- Geographic region
```

### Step 2: Collect sample data
```
Sample 1000 model outputs across:
- 5 groups × 5 metrics = 25 conditions
- 40 samples per condition
- Diverse scenarios (not cherry-picked)
```

### Step 3: Annotate ground truth
```
For each output, human annotators label:
- Is it accurate? (Yes/No)
- Is it helpful? (Yes/No/Partial)
- Is it fair? (Yes/No)
- Does it respect dignity? (Yes/No)
```

### Step 4: Calculate metrics per group
```
For group A:
- Accuracy: 92%
- Helpfulness: 85%
- Fairness: 88%

For group B:
- Accuracy: 75%
- Helpfulness: 60%
- Fairness: 50%

Gaps suggest bias
```

### Step 5: Document findings
```
BIAS AUDIT REPORT
==================

Finding 1: Accuracy disparity
- Group A: 92% accurate
- Group B: 75% accurate
- Gap: 17%
- Severity: HIGH

Finding 2: Representation
- Group A appears 60% of outputs
- Group B appears 40% of outputs
- Gap: 20%
- Severity: MEDIUM
```

---

## Part 4: Mitigations

### Mitigation 1: Data Balancing
```python
# Oversample underrepresented groups
from sklearn.utils import resample

df_majority = data[data['group'] == 'A']
df_minority = data[data['group'] == 'B']

# Oversample minority
df_minority_upsampled = resample(df_minority, 
                                 n_samples=len(df_majority),
                                 random_state=1)

df_balanced = pd.concat([df_majority, df_minority_upsampled])
```

### Mitigation 2: Fairness Constraints
```python
# During training, add fairness objective
fairness_loss = abs(accuracy_group_A - accuracy_group_B)
total_loss = model_loss + lambda * fairness_loss
```

### Mitigation 3: Post-Hoc Adjustment
```python
# After model training, adjust thresholds
# Use different thresholds per group

if group == 'A':
    threshold = 0.5
elif group == 'B':
    threshold = 0.3  # Lower threshold for underserved group

prediction = 1 if score > threshold else 0
```

### Mitigation 4: Transparency & Documentation
```
Model Card (document model behavior):
- Overall accuracy: 85%
- Accuracy per group: A=92%, B=75%
- Known limitations: Lower accuracy for group B
- Recommended use: Not recommended for high-stakes decisions without human review
```

---

## Part 5: Real Incidents

### Incident 1: Amazon Hiring Bot
**What happened:** Amazon's ML hiring tool showed bias against women.
**Why:** Training data from 10 years of male-dominated tech hiring.
**Impact:** Women less likely to be recommended.
**Lesson:** Bias in training data → bias in model.

### Incident 2: COMPAS Recidivism
**What happened:** Criminal risk assessment biased against Black defendants.
**Why:** Historical bias in criminal justice system.
**Impact:** Higher false positive rates for Black people.
**Lesson:** Historical bias → perpetuated bias.

### Incident 3: Google Images
**What happened:** Image search for "CEO" showed mostly white men.
**Why:** Web images reflect societal bias + search ranking bias.
**Impact:** Reinforced stereotype that CEOs are white men.
**Lesson:** Representation matters; defaults matter.

### Incident 4: Healthcare AI
**What happened:** Model for patient health risk used race as proxy for socioeconomic status.
**Why:** Race correlated with healthcare access (due to inequality).
**Impact:** Black patients assessed as lower-risk and denied care.
**Lesson:** Proxies for sensitive attributes can cause harm.

---

## Part 6: Fairness Framework

**No single definition of fairness.** Choose based on context:

| Fairness Type | Definition | Example |
|---------------|-----------|---------|
| Demographic Parity | Equal treatment across groups | Same % approval for all groups |
| Equalized Odds | Equal true positive & false positive rates | Same hiring accuracy for all genders |
| Calibration | Predictions equally accurate across groups | Model 80% confident = 80% likely for all groups |
| Individual Fairness | Similar individuals treated similarly | Two similar job applicants get similar scores |

**Trade-offs:**
- Can't optimize for all simultaneously
- Choose based on stakeholder values
- Be transparent about choice

---

## Part 7: Accessibility

Fairness isn't just about protected groups. It's about **everyone**.

### Accessibility dimensions:
- **Vision:** Blind users, low vision, color blindness
- **Hearing:** Deaf users, hard of hearing
- **Motor:** Users who can't use keyboard/mouse
- **Cognitive:** Dyslexia, ADHD, autism
- **Language:** Non-native speakers, different dialects

### Audit checklist:
```
✓ Does system work with screen readers?
✓ Are captions/transcripts provided?
✓ Can users interact without mouse?
✓ Is text large enough (18pt+)?
✓ Are color contrasts sufficient (4.5:1)?
✓ Is language clear and simple?
✓ Are there multiple ways to complete tasks?
```

---

## Points to Remember

1. **Bias is systematic, not intentional.** It comes from data and design choices.
2. **You can't ignore bias.** It causes real harm.
3. **Measure fairness explicitly.** What you measure, you improve.
4. **Different fairness definitions exist.** Choose based on context.
5. **Representation matters.** What groups appear in outputs?
6. **Accessibility benefits everyone.** Clear captions help everyone.
7. **No perfect fairness.** Trade-offs are unavoidable. Be transparent.

---

## Quick Check: Fill in the Blanks

1. **Representation bias** happens when \_\_\_\_\_\_\_\_\_\_\_\__ groups are under-represented in training data.
   - Answer: *some*

2. **Performance bias** means model \_\_\_\_\_\_\_\_\_\_\_\__ differently across groups.
   - Answer: *performs* or *works*

3. **Allocation bias** denies \_\_\_\_\_\_\_\_\_\_\_\__ unfairly to some groups.
   - Answer: *resources* or *opportunities*

4. **Demographic parity** means groups get \_\_\_\_\_\_\_\_\_\_\_\__ treatment.
   - Answer: *equal*

5. You can't optimize for all fairness definitions simultaneously; you must \_\_\_\_\_\_\_\_\_\_\_\__.
   - Answer: *choose* or *trade-off*

---

## Quiz and Interview Questions

**Full quiz:** [assessments/quizzes/week-05/session-5.4-quiz.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/quizzes/week-05/session-5.4-quiz.md)  
**Answer key:** [assessments/answer-keys/week-05/session-5.4-quiz-answers.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/answer-keys/week-05/session-5.4-quiz-answers.md)  
**Interview questions:** [assessments/interview-questions/week-05-interview-qs.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/interview-questions/week-05-interview-qs.md)

---

## Core path and Pro path exercises

### Core path
**Bias audit on model outputs:**
1. Given: 50 model outputs (hiring, lending, job recommendations)
2. Audit for bias across 3 groups
3. Calculate metrics: accuracy, fairness, representation
4. Document findings
5. Suggest mitigations

Scaffolded. Focus on conducting audit.

### Pro path
**Design bias audit framework:**
1. Define audit scope (which groups, which metrics)
2. Collect sample data (1000 outputs)
3. Annotate ground truth (manual review)
4. Calculate metrics
5. Create model card (document findings)

More challenging: requires designing comprehensive audit.

---

## What's next

**Session 5.5** covers **Guardrails & Mitigations** — implementing defenses from 5.3 and guardrails.

For now, commit to measuring fairness. You can't fix bias if you don't measure it.

---

*Session 5.4 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
