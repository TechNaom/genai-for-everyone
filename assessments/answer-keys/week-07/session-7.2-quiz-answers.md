# Answer Key — Session 7.2 Quiz

**1.** The ticket classifier (routing to one of 6 categories) is predictive AI — it selects from a fixed, known set of categories. The RAG-drafted response for technical tickets is generative — it produces newly composed text grounded in retrieved documentation, not a selection from a fixed list.

**2.** The company added two new product lines, introducing ticket types that didn't fit any of the original 6 categories. Rather than being recognized as new/unknown, they were force-fit into the closest existing (wrong) category, often with high confidence — this is input drift (Session 6.4): the real-world distribution of tickets shifted while the classifier's categories stayed fixed.

**3.** False. Confidence calibration reflects the data distribution the classifier was built for; as that distribution shifts (new ticket types, new product lines), the same confidence scores can become unreliable without any code or model change — exactly what happened in the case study.

**4.** (1) No process for retiring/flagging outdated documents in the retrieval index, so a superseded doc was still retrievable and treated as current. (2) No mandatory human-review requirement specifically for responses touching data-loss-risk topics, so the agent's normal trust in the tool wasn't overridden by an extra check for this particular high-risk case.

**5.** Retraining on the new product lines only fixes the two specific new categories seen so far — it doesn't solve the general problem that *any* future new/unrecognized ticket type would again get force-fit into an existing wrong bucket. A dedicated "I don't recognize this" category is a structural fix that generalizes to future unknowns, not just the current ones.

**6.** They traded some automation coverage (a few extra tickets now require human review that a confident model would have auto-handled) for a large reduction in the risk of a high-confidence wrong response reaching a customer on a high-stakes topic — accepting a small efficiency cost to close a specific safety gap.

**7.** Questions probing exactly where evaluation happens and against what dataset, what the fallback/review path is when the system is uncertain or wrong, how drift would be detected (and whether confidence scores are re-validated over time), and whether guardrails/review requirements are applied consistently across all risk levels or just some.
