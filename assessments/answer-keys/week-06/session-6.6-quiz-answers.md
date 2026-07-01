# Session 6.6 Quiz Answers and Grading Guide

---

## Question 1: What "Deployable" Actually Means

**Answer:** (1) One-command startup, (2) configuration read from the environment rather than hard-coded, (3) logging of every request, (4) graceful degradation via a fallback strategy when a provider fails, (5) a passing regression check before going live.

**Full credit (2 pts):** Lists all 5 (or close paraphrases) tied to the correct sessions.
**Partial credit (1 pt):** Lists 3-4.
**No credit:** Lists fewer than 3, or lists unrelated properties.

---

## Question 2: Hosted Demo Without a Cloud Bill

**Answer:** B) A local service demoed live, or a free-tier host, both satisfy the lab

**Grading:**
- **Full credit (1 pt):** Answer is B
- **No credit:** Any other answer

**Explanation:** The lab's bar is a working, well-documented service — not a specific hosting bill. A locally-run service demoed live over a call satisfies the exact same learning objective as a free-tier cloud deployment.

---

## Question 3: Startup-Time vs. CI-Time Gates

**Answer:** A CI-only check only fires when a change goes through the normal PR pipeline. It can't catch a service that's started with bad configuration outside that pipeline — a manual deploy that skips CI, an environment variable set wrong at the infrastructure level, or a stale/wrong prompt version loaded at runtime. A startup-time check catches these because it runs every time the process boots, regardless of how it got there.

**Full credit (1 pt):** Names at least one concrete scenario CI would miss (manual deploy, bad env var, stale config) and explains why the startup check catches it (runs on every boot, not just on PR).
**Partial credit (0.5 pts):** Vague "it's an extra safety layer" without a concrete scenario.
**No credit:** Says there's no difference between the two.

---

## Question 4: The 5-Minute Test

**Answer:** They should be able to install dependencies, set the required environment variables (per `DEPLOY.md`), start the service with one command, and verify it's working (e.g., via the `/health` endpoint or a sample request) — all without needing to ask the original author anything.

**Full credit (1 pt):** Mentions install + config + start + verify, achievable without asking the author.
**Partial credit (0.5 pts):** Mentions "get it running" without the verification step.
**No credit:** No meaningful answer.

---

## Question 5: Combining the Pieces

**Answer example:** Not strictly a Week 6 pipeline failure — the regression gate can only catch what's represented in the golden dataset, and by definition a genuinely new failure mode wasn't in it yet. This is exactly why Session 6.4's monitoring and feedback loop exist: to catch failures the golden dataset didn't anticipate, and feed them back in as new golden dataset examples so the regression gate catches this specific failure mode next time.

**Full credit (2 pts):** As described in the rubric above.
**Partial credit (1 pt):** Says yes/no without explaining the golden-dataset coverage limitation.
**No credit:** No substantive answer.

---

## Grading Summary

| Question | Type | Points |
|----------|------|--------|
| 1 | Short | 2 |
| 2 | MC | 1 |
| 3 | Short | 1 |
| 4 | Short | 1 |
| 5 | Scenario | 2 |
| **Total** | | **7** |

---

## Common Misconceptions

1. **"Deployable means it's on a specific cloud host"** — No, it's a set of properties (config, logging, fallback, gating) independent of the host.
2. **"A CI regression gate alone is sufficient"** — No, a startup-time check catches config drift a CI check can't see.
3. **"A passing regression gate means the system is fully safe"** — No, it only covers what's in the golden dataset; monitoring exists precisely because gates have blind spots.

---

*Session 6.6 Answer Key | GenAI for Everyone | Week 6 Lab*
