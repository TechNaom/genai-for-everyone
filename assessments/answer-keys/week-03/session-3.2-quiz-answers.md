# Session 3.2 Quiz — Answer Key

---

**1. Answer: B**

An embedding is a numeric vector representation of text where semantic similarity is reflected in vector closeness — texts with similar meaning produce similar-looking vectors, and texts with different meaning produce vectors that look very different. It's not a compression format, not just a unique-word list (that's closer to a vocabulary or bag-of-words concept), and not a summary — it's a geometric encoding of meaning.

---

**2. Answer: B**

Embeddings work in meaning-space rather than word-space. Because the comparison is based on learned semantic similarity rather than literal vocabulary overlap, "getting reimbursed for travel" and "expense submission procedures" can land as nearby vectors despite almost no shared words, since they're about closely related real-world concepts. There's no human-maintained synonym list doing this — it's a property that emerges from how the embedding model represents meaning.

---

**3. Answer: C**

Cosine similarity specifically measures the angle between two vectors — how aligned their *direction* is — while deliberately ignoring their magnitude (length). Two vectors pointing in nearly the same direction get a score near 1, regardless of whether one is "longer" than the other. It says nothing directly about literal word overlap (A), isn't the same as straight-line distance between endpoints (B, that would be Euclidean distance, a different metric), and dimension count isn't what it measures (D) — though both vectors do need the same number of dimensions to compute it at all.

---

**4. Sample answer:**

A cosine similarity around 0.95 suggests the two pieces of text are very closely related in meaning — likely paraphrases of each other, or two ways of expressing nearly the same idea, even if the wording differs. A cosine similarity around 0.05 suggests the two pieces of text are essentially unrelated in meaning — their embedding vectors point in very different directions in meaning-space, the way a sentence about pets and a sentence about financial markets would.

---

**5. Answer: B**

The globe-to-map analogy is about the unavoidable distortion that comes from projecting something with more "true" structure (a sphere; a high-dimensional embedding space) down into fewer dimensions (a flat map; a 2D plot) for the sake of visualization — Greenland looking oversized on a flat map despite being smaller in reality is the same kind of artifact you should expect in a 2D embedding plot. It says nothing about embeddings being literally 2D internally (A), doesn't imply maps and embeddings share a formula (C), and has nothing to do with the historical origin of embedding models (D).

---

**6. Sample answer:**

With only 20 short sentences, there simply wasn't enough raw text for word-count statistics alone to reveal which words relate to which topics — sentences within the same topic (e.g. about pets) were deliberately written using different specific words ("puppy," "cat," "dog," "parrot"), so they shared almost no literal vocabulary with each other, and pure word-count vectors showed almost no more similarity within a topic than across topics. A real production embedding model doesn't run into this problem because it's trained on a vastly larger amount of text — billions of words across huge, diverse documents — which gives it enough exposure to learn, automatically and without any hand-built topic lists, that words like "puppy," "dog," and "canine" tend to appear in similar contexts and represent related concepts. Scale of training data, not a different kind of math, is what lets real embeddings cluster by meaning without anyone hand-seeding topic categories.
