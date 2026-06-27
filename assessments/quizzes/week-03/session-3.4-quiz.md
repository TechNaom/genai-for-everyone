# Session 3.4 Quiz — Building a RAG Pipeline

*6 questions. Mixed multiple-choice and short-answer.*

---

**1.** In a grounded RAG prompt, why is an instruction like "answer using ONLY the information in the provided context" considered the single most load-bearing line in the template?

A) It makes the prompt shorter
B) Without it, the model is free to ignore the retrieved context entirely and answer from its own (possibly outdated or fabricated) memory, defeating the purpose of retrieval
C) It is required by the Anthropic API to function
D) It prevents the model from using citations

---

**2.** Why does a RAG prompt typically present retrieved chunks as numbered units (`[1]`, `[2]`, `[3]`) rather than as one undifferentiated block of text?

A) Numbering makes the prompt look more professional
B) The model cannot read unnumbered text
C) Numbering is what makes citation possible at all — you can't ask a model to cite "which part of the context" supported an answer if the context has no addressable units to point to
D) Numbered chunks process faster than unnumbered ones

---

**3.** True or False: if a model's RAG-generated answer includes a citation like `[2]`, that guarantees the claim attached to it is actually supported by chunk 2's real content.

---

**4. Short answer.** Explain why citation grounding is described as turning an "invisible failure mode into a checkable one." What's the failure mode, and what specifically does the citation let you check?

---

**5.** Session 3.3's `VectorStore.search()` returns `(chunk_text, similarity_score)` tuples. Why does the similarity score need to be stripped out before the chunk text is inserted into the final generation prompt?

A) Similarity scores are classified information
B) The model would crash if it saw a decimal number
C) The score was useful internally for retrieval and diagnostics, but the model doesn't need it, and including it just adds irrelevant clutter to the context the model is meant to focus on
D) Cosine similarity scores must be kept secret from end users for legal reasons

---

**6. Short answer.** A teammate says: "We added citations to our RAG system's answers, so now we know it's never hallucinating." Explain what's wrong with this conclusion, using the relationship between citation grounding and the kind of retrieval quality issues covered in Session 3.3.
