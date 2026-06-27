# Session 3.3 Quiz — Vector Databases & Retrieval

*6 questions. Mixed multiple-choice and short-answer.*

---

**1.** Why is embedding an entire 40-page document as a single vector generally a poor strategy for retrieval?

A) It takes too long to compute one embedding
B) That single vector becomes an average/blur of everything in the document, making it a poor match for specific questions about narrow parts of it
C) Vector stores cannot hold large vectors
D) Documents longer than a few pages cannot be embedded at all

---

**2.** What problem does chunk *overlap* (e.g. 20% overlap between consecutive chunks) specifically help prevent?

A) Two chunks ending up with identical embeddings
B) An idea or sentence that spans a chunk boundary getting orphaned — split so that neither chunk fully contains it
C) The vector store running out of storage space
D) Cosine similarity scores exceeding 1.0

---

**3.** A brute-force (exhaustive) vector search compares a query against every stored vector directly. Why do production vector stores typically use ANN (Approximate Nearest Neighbor) indexing instead?

A) ANN indexing is required by law for storing personal data
B) Brute-force search becomes too slow at scale (e.g. millions of vectors), and ANN trades a small amount of accuracy for a large gain in speed
C) Cosine similarity only works with ANN indexing
D) ANN indexing produces more accurate similarity scores than brute-force search

---

**4. Short answer.** Explain, in your own words, the trade-off involved in choosing top-k retrieval's value of *k*. What goes wrong if k is set too low? What goes wrong if it's set too high?

---

**5.** In this session's exercise, a generic introductory paragraph that briefly mentioned every topic in a handbook ("leave, remote work, expenses, and benefits") sometimes scored deceptively well against unrelated queries. What does this illustrate?

A) Word-count-based similarity can be fooled by a chunk that's superficially relevant to everything but substantively useful for nothing
B) The PDF was corrupted and needs to be regenerated
C) This only happens with real embedding models, not toy ones
D) Introductory paragraphs should always be deleted before chunking

---

**6. Short answer.** A teammate suggests: "Let's just always use a chunk size of 500 words and k=10 for every document we ever build a RAG system over — that way we never have to think about it again." Using what you learned this session, explain why this isn't a safe default to apply universally.
