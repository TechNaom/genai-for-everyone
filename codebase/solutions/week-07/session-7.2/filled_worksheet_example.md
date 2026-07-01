# Case Study Analysis Worksheet: Support Ticket Triage

## Predictive vs. generative components
The 6-category ticket classifier is predictive AI — it selects from a fixed, known set of routing categories, never inventing a new one. The RAG-based suggested-response drafter for technical tickets is generative — it composes new response text grounded in retrieved documentation, which is a fundamentally different job than classification.

## Where each Week 1-6 concept shows up
RAG grounding (Week 3): the suggested-response drafter retrieves internal docs before generating. Confidence-based gating (Week 4/5 evaluation mindset): high-confidence classifications auto-route, low-confidence ones go to a human. Drift (Week 6.4): new product lines introduced ticket types the classifier had never seen, and confidence scores stayed high even as accuracy silently dropped. Guardrails (Week 5.5): the fix added mandatory human review for high-risk topics regardless of confidence — a guardrail applied inconsistently before the incident.

## Root-cause analysis: the data-loss incident
The immediate trigger was a stale internal doc being retrieved and used to draft incorrect setup instructions, but the real root cause is two compounding gaps: no process existed for retiring outdated documents from the retrieval index, so an obsolete doc remained fully retrievable and indistinguishable from current ones; and there was no mandatory human-review requirement specifically for topics with data-loss risk, so the agent's default trust in the tool wasn't overridden by an extra check on this particular high-stakes category. Either gap alone might not have caused real harm, but together they let a stale, wrong answer flow through to a customer unchecked.

## What would you have caught earlier?
Before launch, I'd have flagged the lack of any document-freshness signal in the retrieval index as the highest-risk gap — a RAG system with no way to distinguish current from superseded documents will eventually surface stale information with full confidence, and that risk grows every time the underlying docs change without the index being explicitly refreshed.
