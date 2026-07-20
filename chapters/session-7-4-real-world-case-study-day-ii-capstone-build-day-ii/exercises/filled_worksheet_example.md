# Case Study Analysis Worksheet: Contract Review Assistant

_This is a filled-in reference example — one reasonable way to answer the worksheet, not the only correct answer. Compare your own worksheet against this after making a genuine attempt, not before._

## Why no auto-approval path exists
Legal review carries asymmetric risk: a missed or mishandled clause can cause real financial and legal harm, while extra human review time is a bounded, recoverable cost. Requiring sign-off on every flagged clause means the AI's job is narrowed to surfacing candidates for review, not making unsupervised legal judgments — keeping a licensed human accountable for every decision that actually matters.

## What actually caused the near-miss
Not a bug in the traditional sense — the model's severity scoring relied on lexical similarity to the standard clause, and a legally significant word substitution happened to look like a minor wording difference on the surface. The design gap was treating "looks similar" as a reliable proxy for "means something similar," which broke down exactly for the kind of subtle, high-stakes edit an adversarial or careless drafter might introduce.

## The fix, and its trade-off
The firm now forces indemnification/liability clauses to always be scored at least "medium" severity, regardless of the model's own confidence. The trade-off is more careful reads on clauses that often turn out to be fine — a small, predictable, recurring cost accepted in exchange for closing off the specific failure mode that nearly caused real harm.

## Apply one lesson to your own capstone
For my invoice Q&A capstone (Session 7.1), the lesson is: I shouldn't let my confidence-gating (if I add one) trust similarity scores uniformly for every field — dollar amounts and payment terms are exactly the kind of field where a "looks close enough" match could hide a materially wrong number, so those fields should always get flagged for the user to double-check, regardless of how confident the retrieval match looks.
