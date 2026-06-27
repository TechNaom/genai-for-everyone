# Session 3.4 Quiz — Answer Key

---

**1. Answer: B**

Without an explicit instruction to use only the provided context, a model is free to quietly fall back on its own training-data memory instead of the retrieved text — which means all the careful work building chunking, embedding, and retrieval has no guaranteed effect on the final answer at all. This instruction is specifically what makes a system *retrieval-augmented* rather than just retrieval-adjacent. It has nothing to do with prompt length, API requirements, or blocking citations — in fact it's paired with a citation instruction, not opposed to one.

---

**2. Answer: C**

Numbering retrieved chunks turns an undifferentiated wall of text into addressable units, which is the prerequisite for citation: a model can only "cite chunk [2]" if chunk 2 is a distinguishable, numbered thing in the first place. Without numbering, there's no way to ask the model to point to a specific part of the context, because there's no structure to point to. This isn't about appearance, model reading ability, or processing speed.

---

**3. Answer: False**

A citation marker shows that the model *attempted* to ground that part of its answer in a specific chunk — it does not guarantee the chunk actually supports the claim. A model can cite a chunk that's topically related but doesn't actually contain the specific fact being claimed, which is a real and deeper failure mode (covered further in Session 3.5). Citation grounding makes this checkable by a human or a system that verifies citations against real chunk text — it doesn't make verification automatic or guaranteed correct on its own.

---

**4. Sample answer:**

Without citations, a RAG system's output looks identical whether the model faithfully used the retrieved context or quietly ignored it and answered from memory instead — both produce a fluent paragraph with no visible difference. That's the invisible failure mode: there's no way to tell, from the outside, whether the system worked as designed or silently bypassed its own safeguards. A citation lets you check something concrete: go look at the specific chunk the model cited, and verify directly whether it actually supports the claim attached to it. This converts an invisible "I can't tell if this is grounded" problem into a visible, checkable one — even though, as the quiz's earlier question notes, the check itself still has to actually be done; a citation existing doesn't automatically mean it's correct.

---

**5. Answer: C**

The similarity score is genuinely useful — for building and diagnosing the retrieval system itself — but it has no role in the model's actual task of answering the question. Including it in the final prompt only adds numeric clutter that has nothing to do with the content the model is supposed to focus on and ground its answer in. This is a deliberate translation step between the retrieval stage's internal data shape and the generation stage's expected input, not a security, technical-limitation, or legal requirement.

---

**6. Sample answer:**

Citations only verify that the model attempted to point to a specific chunk — they don't verify that the retrieval step actually found the right chunk in the first place, or that the cited chunk genuinely supports the specific claim attached to it. Session 3.3 showed directly that retrieval itself can return weak or even wrong-topic matches (the PTO-vs-sick-leave confusion, the generic intro paragraph winning by surface vocabulary) even with reasonable settings. A model can cite one of these flawed retrieved chunks in full good faith, producing an answer that has a citation attached but is still wrong or unsupported, because the upstream retrieval — not the generation or citation step — was the actual point of failure. Citations make grounding checkable; they don't make retrieval correct, and treating "it has citations" as proof of "it never hallucinates" skips the actual verification work citations are meant to enable.
