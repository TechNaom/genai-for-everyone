# Session 3.5 Quiz — RAG Failure Modes & Fixes

*6 questions. Mixed multiple-choice and short-answer.*

---

**1.** A RAG system retrieves a chunk that ends mid-sentence with "...employees who relocate must" and the next chunk begins with "notify their manager within 14 days." Neither chunk alone contains the complete instruction. What failure mode is this?

A) Context stuffing
B) A chunking error — the idea was orphaned across a chunk boundary
C) A retrieval miss
D) A citation grounding failure

---

**2.** A user asks "Can I telecommute?" and the document's actual remote-work policy uses only the words "remote" and "hybrid" — never "telecommute." The correct chunk doesn't appear anywhere in the top-k results. What's the most precise name for this failure mode?

A) Chunking error
B) Context stuffing
C) Retrieval miss
D) Re-ranking failure

---

**3.** Why can simply increasing k (e.g., from k=3 to k=20) make a context-stuffing problem worse rather than better, even though it might also help catch a near-miss?

A) Higher k always slows down the embedding model
B) A higher k retrieves more chunks regardless of whether they're actually relevant, so if relevance drops off sharply after the first few results, the model ends up with mostly noise diluting the few useful chunks
C) Vector stores have a hard limit of k=5
D) Cosine similarity scores become invalid above k=10

---

**4. Short answer.** Explain how re-ranking can help address both a retrieval miss and context stuffing at the same time, using the two-pass structure (wide initial retrieval, then a more careful second pass) described in the session.

---

**5.** A teammate sees a wrong answer from a RAG system and concludes: "The model just isn't very good at following instructions." What should you check FIRST, before accepting that conclusion?

A) Whether the model's output is grammatically correct
B) What chunks were actually retrieved and handed to the model — since a wrong answer built on missing or poor context looks identical, from the outside, to a model failing to follow instructions
C) Whether the user asked the question politely
D) The exact wording of the system prompt's greeting

---

**6. Short answer.** Two different RAG failure modes can produce the exact same visible symptom: a wrong final answer. Using this session's distinction between a "pipeline problem" and a "trust problem" (the kind Week 5 covers), explain why correctly diagnosing WHICH failure mode occurred matters, rather than just noting that the answer was wrong.
