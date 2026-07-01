# Quiz — Session 6.6: Week 6 Lab

**This is a lab-focused quiz. Scenario-based questions test your understanding of the Week 6 capstone.**

---

## Question 1: What "Deployable" Actually Means

List the five properties (from Sessions 6.1-6.5) that make a service "deployable," independent of which specific cloud host it runs on.

**Short answer:** (list format is fine)

---

## Question 2: Hosted Demo Without a Cloud Bill

A learner says "I can't do this lab, I don't have a cloud hosting account." What would you tell them?

A) They're right, this lab requires a paid cloud account
B) A local service demoed live, or a free-tier host, both satisfy the lab — the artifact that matters is the README + working service, not the specific host
C) They should skip the lab entirely
D) Only Docker deployments count as "real" deployment

**Answer:** B

**Why:** The lab is about producing a deployable, well-documented artifact — that property doesn't depend on whether it's demoed locally or on a specific paid host.

---

## Question 3: Startup-Time vs. CI-Time Gates

Your Pro path adds a regression check that runs when the service starts, not just in CI. What failure mode does a startup-time check catch that a CI-only check would miss?

**Short answer:** (3-4 sentences)

**Expected answer:** A CI check only runs when code/prompts change through the normal PR pipeline. A startup-time check catches cases where the service is started with a misconfigured environment (wrong prompt version loaded, wrong golden dataset, stale config) that CI never saw — e.g., a manual deploy that skips the pipeline, or an environment variable set incorrectly at the infrastructure level.

---

## Question 4: The 5-Minute Test

You hand your project to a teammate with just the repo and a `DEPLOY.md`. What should they be able to do within 5 minutes, according to this session's definition of "deployable"?

**Short answer:** (2-3 sentences)

---

## Question 5: Combining the Pieces

Your service passes its regression gate, but then a red-team-style failure appears in production (from Week 5's concepts) that the golden dataset never covered. Is this a failure of the Week 6 deployment pipeline? Explain.

**Short answer:** (3-5 sentences)

**Rubric (2 pts):**
| Points | Criteria |
|--------|----------|
| 2 pts | Recognizes this isn't strictly a Week 6 pipeline failure — a regression gate only catches what's in the golden dataset; it connects this to the Week 6.4 monitoring/feedback loop as the mechanism that should catch and feed this new failure back into the dataset |
| 1 pt | Says "yes it's a failure" or "no it's not" without explaining the golden-dataset coverage limitation |
| 0 pts | No substantive answer |

---

*Session 6.6 Quiz | GenAI for Everyone | Week 6 Lab*
