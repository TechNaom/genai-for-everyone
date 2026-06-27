# Session 3.3 Quiz — Answer Key

---

**1. Answer: B**

A single embedding for an entire long document has to represent everything in that document at once — the executive summary, page 23's specific detail, and an unrelated appendix all blend into one averaged vector. A specific question about one narrow part of the document then has to match against this single blurred representation of "the whole document, vaguely," which doesn't give the precise matching that retrieval needs. This isn't about computation time, storage limits, or any hard length cutoff on what can be embedded.

---

**2. Answer: B**

Overlap exists specifically to prevent an idea or sentence near a chunk boundary from being orphaned — split so that the end of one chunk and the beginning of the next each contain only half of something that should be read together. By sharing some words between consecutive chunks, an idea spanning that boundary is still fully present in at least one of the two chunks. It has nothing to do with identical embeddings, storage space, or similarity score ranges.

---

**3. Answer: B**

Brute-force search scales linearly with the number of stored vectors — checking a million vectors means computing a million similarity scores per query, which becomes too slow for interactive use at real-world scale. ANN indexing organizes vectors so a search can skip over most of the database without checking it directly, trading a small chance of missing the single mathematically-best match for a large gain in speed. This is a performance/scale trade-off, not a legal requirement, not a requirement for cosine similarity to function at all, and it doesn't make individual similarity scores more accurate — if anything, it's an approximation of the exact brute-force result.

---

**4. Sample answer:**

Setting k too low (e.g. k=1) risks missing the actual answer if it's split across two adjacent chunks, or if the single highest-cosine-similarity chunk isn't actually the most useful one for fully answering the question — there's no fallback if that one chunk happens to be a near-miss. Setting k too high (e.g. k=50) reintroduces the problem RAG was meant to solve in the first place: the model gets handed a large pile of mostly-irrelevant text, diluting the genuinely useful passages, which increases cost and latency and can measurably hurt answer quality if the model gets distracted by a lot of similar-sounding but unhelpful surrounding context. The right k is a balance, typically tuned per use case rather than fixed.

---

**5. Answer: A**

A chunk that briefly name-drops every topic in a document shares at least a little vocabulary with almost any query, so word-count-based (and, to a lesser but still real extent, real embedding-based) similarity can score it deceptively well even though it doesn't substantively answer any specific question. This is a genuine, common retrieval failure mode worth watching for in real systems — it has nothing to do with PDF corruption, being unique to toy embeddings (similar dynamics can affect real embeddings too, just less severely), or implying that intro paragraphs should always be deleted (that's one possible mitigation, not a universal rule).

---

**6. Sample answer:**

Chunk size and k are both genuine trade-offs that depend on the specific documents and the kind of questions being asked — there's no single setting proven safe for every case. A chunk size of 500 words might be far too large for documents where closely related but distinct topics (like PTO vs. sick leave in this session's exercise) sit near each other and share vocabulary, since a large chunk dilutes the specific signal needed to tell them apart; the same size might be perfectly fine, or even too small, for a different kind of document. Similarly, k=10 might dilute results badly for a document where most chunks are short and specific, while being entirely reasonable for a different retrieval setup. Treating these as fixed defaults skips the actual engineering work — testing chunk size and k against real, representative questions for the specific documents in question — which is exactly the kind of tuning this session, and Session 3.5's systematic diagnosis, are meant to teach.
