# Answer Key — Session 6.5 Quiz

**1.** A prompt is a specification for behavior — a single word change can measurably shift accuracy, tone, cost, and latency at once, the same way a small code change can introduce a regression. "Small" in text size doesn't mean "small" in behavioral impact.

**2.** Against a stored baseline score — the last known-good version's score on the same golden dataset — not against a fixed absolute number in isolation. This lets the gate detect a meaningful *drop* even if the absolute score is still reasonably high.

**3.** False. Non-determinism means you can't check for exact output equality, but you can still score behavior against a rubric or golden dataset (as in Session 5.1/5.2) and compare that score to a baseline — this is exactly what a regression gate does, and it works fine with non-deterministic outputs.

**4.** CI should fail and block the merge, because the drop (14 points) exceeds the 5-point threshold. The prompt change should not ship until the regression is investigated and fixed (or the change is judged worth the trade-off and the threshold/baseline is deliberately updated with that reasoning documented).

**5.** Standalone files make prompt changes visible in diffs, give them their own version history, and prevent teammates from unknowingly running different, untracked copies of "the same" prompt duplicated across multiple files.

**6.** Yes — the golden dataset should be versioned alongside the prompts it evaluates, because the dataset itself evolves (new production failures get added per Session 6.4's feedback loop), and you need to know which dataset version produced which score to make baseline comparisons meaningful over time.

**7.** The fastest safe first response is rolling back to the last known-good prompt version, because it immediately stops users from experiencing the regression while you investigate. Investigating root cause first is riskier because it leaves the broken behavior live in production for longer than necessary — rollback buys time to investigate safely.
