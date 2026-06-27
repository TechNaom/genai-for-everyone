# Session 3.5 Quiz — Answer Key

---

**1. Answer: B**

This is the textbook signature of a chunking error caused by insufficient (or zero) overlap: a single idea or instruction spans a chunk boundary, and the hard cut leaves neither resulting chunk with the complete fact. The fix is increasing overlap (or adjusting chunk size/boundaries) so an idea near a cut point is fully captured in at least one chunk. It's not context stuffing (which is about retrieving too much weak content), a retrieval miss (the relevant text WAS found, just split badly), or a citation issue (no generation or citation step is even involved here).

---

**2. Answer: C**

This is specifically a retrieval miss: the correct chunk exists in the document but never makes it into the top-k results, here because of a vocabulary mismatch between how the user phrased the question ("telecommute") and how the source document phrases the same concept ("remote," "hybrid"). It's not a chunking error (the chunk boundaries aren't the problem here), context stuffing (no excess of weak chunks is described), or a re-ranking failure (re-ranking hasn't been applied yet in this scenario — it's one possible fix, not the failure itself).

---

**3. Answer: B**

Raising k retrieves more chunks unconditionally — it doesn't filter for whether those additional chunks are actually relevant. If similarity scores drop sharply after the first few results (as you saw directly in this session's exercise), a higher k mostly adds low-relevance or near-zero-relevance chunks into the context, diluting the genuinely useful ones rather than adding more useful signal. This has nothing to do with embedding model speed, a hard k limit, or cosine similarity becoming "invalid" at any particular k — cosine similarity works the same way regardless of how many results you ask for.

---

**4. Sample answer:**

Re-ranking works in two passes: a wide initial retrieval (e.g., top-20 by cosine similarity) followed by a more careful, more expensive comparison that re-scores just those 20 candidates and keeps only the best few. This helps with retrieval misses because casting a wider net initially gives a near-miss — a chunk that scored just outside a narrower top-3 or top-5 cutoff — a chance to be reconsidered by the second, more careful pass, rather than being permanently discarded by the first pass alone. It helps with context stuffing because, even though the initial pool is wide, only the re-ranked best few make it into the final prompt — you get the safety net of a wider initial search without committing to handing all 20 candidates to the model.

---

**5. Answer: B**

A wrong answer from a generation step looks identical whether the model genuinely failed to follow instructions or whether it was simply given the wrong, incomplete, or excessive context to work with in the first place — this is the exact "fluency tells you nothing about correctness" lesson from Session 3.4, applied to debugging. Checking what was actually retrieved is the necessary first step to distinguish a pipeline (retrieval/chunking) problem from an actual generation problem, rather than jumping to a conclusion about the model based on the final answer's tone or grammar.

---

**6. Sample answer:**

A chunking error, a retrieval miss, and context stuffing all have a discoverable, specific cause inside the pipeline and a correspondingly specific fix — the kind of "pipeline problem" this session is about. But not every wrong answer comes from one of these; some wrong answers happen even when chunking, retrieval, and context assembly all technically worked correctly, which is closer to a "trust problem" requiring the kind of systematic evaluation Week 5 covers, rather than a single component fix. If you only note "the answer was wrong" without diagnosing which failure mode (or whether it's a pipeline problem at all), you risk applying the wrong fix entirely — for example, adjusting chunk size when the real issue was vocabulary mismatch in retrieval, or assuming a deeper evaluation/trust problem when a simple overlap adjustment would have solved it. Correct diagnosis is what connects the symptom to the right layer of the system to actually fix.
