# Week 3 Written Exam

_Deeper, scenario-based exam covering all of Week 3's sessions (3.1–3.6): why LLMs need external knowledge, embeddings and semantic similarity, vector databases and retrieval, building a RAG pipeline, RAG failure modes and fixes, and applied integration._

**Format:** 7 short-answer questions + 3 scenario-analysis questions + 1 synthesis question
**Suggested time:** 60–75 minutes
**Open book:** Yes — this tests understanding and application, not memorization

---

## Section A — Short Answer

**A1.** What does it mean for an LLM to have a "knowledge cutoff," and why does this cause hallucination specifically — as opposed to the model just saying "I don't know"? Give one example of a question type where this failure mode is especially dangerous in a business context.

**A2.** RAG is not always the right tool. Describe one scenario where RAG would clearly help (per the "RAG or not?" framework from Session 3.1), and one scenario where adding RAG would be unnecessary overhead or even actively unhelpful. Be specific about *why* in each case.

**A3.** What does cosine similarity actually measure between two embedding vectors, and why is it generally preferred over raw Euclidean distance for comparing text embeddings? (Hint: think about what happens to vectors of different lengths/magnitudes representing similar content.)

**A4.** A teammate builds a toy embedding scheme using raw word-count vectors and is surprised when sentences about completely different topics show roughly the same similarity to each other as sentences about the same topic. Explain *why* a naive word-count (bag-of-words) approach can fail to produce clean topic clustering, and name one concrete fix.

**A5.** Define "chunking" in the context of building a vector store, and explain why chunk size is a trade-off rather than something you can simply maximize or minimize. What goes wrong if chunks are too large? What goes wrong if they're too small?

**A6.** In a RAG pipeline, what is "citation grounding," and what specific failure does it protect against that retrieval alone does not? 

**A7.** Name two distinct RAG failure modes covered in Session 3.5 (e.g., chunking errors, retrieval misses, context stuffing, lack of re-ranking) and, for each, describe an observable symptom you'd see in the system's output that would tip you off to that specific failure mode (as opposed to a different one).

---

## Section B — Scenario Analysis

**B1. The PDF that loses its structure**
You're building a vector store over a company policy PDF using a Python PDF-extraction library. The PDF has clear visual section breaks (headers, blank lines between sections) when viewed normally, but after extraction, your chunking logic — which splits on blank lines — produces only 2 giant chunks instead of the 15 distinct policy sections you expected.

Diagnose what's likely happening here, propose a more reliable chunking strategy, and explain why your proposed strategy is more robust to this specific failure than blank-line-based chunking.

**B2. The chunk size that "should" work but doesn't**
You're testing a RAG pipeline over an employee handbook and specifically need it to correctly answer "How many sick days do I get in my first year?" You test three chunk sizes (200, 500, and 1000 tokens) expecting that a "Goldilocks" middle size will work best. After actually running retrieval at all three sizes, you find the question is **not cleanly answered at any of the three chunk sizes** — the relevant numbers exist in the document, but they're split across a policy paragraph and a separate table that never end up in the same chunk together regardless of size.

What does this result tell you about the limits of chunk-size tuning alone? Propose at least one fix that doesn't just mean "try a fourth chunk size," and explain what category of RAG failure mode (per Session 3.5) this really is.

**B3. The retrieval miss that wasn't quite what it looked like**
A RAG system fails to answer "Can I work remotely on Fridays?" — instead it answers based on an unrelated section. On inspection, the top-1 retrieved chunk is irrelevant, but you discover that the **rank-2** chunk does contain the word "remote," just in a different context (e.g., a section about remote *office locations*, not remote *work policy*).

Explain why this is a more nuanced failure than a simple "retrieval missed everything relevant" case, what it suggests about the limitations of pure keyword/lexical overlap versus true semantic relevance, and what concrete change (e.g., re-ranking, better embeddings, hybrid search, query rewriting) you'd try first and why.

---

## Section C — Synthesis

**C1.** You've been asked to explain, to a non-technical executive who is skeptical of "AI hallucination risk," why your team's RAG-based company-policy Q&A bot (the Week 3 Lab build) is *more* trustworthy than just asking a general-purpose LLM the same question directly — but you also need to be honest that RAG does not eliminate hallucination risk entirely.

Write a 150–250 word explanation, in plain language (no jargon like "embeddings" or "cosine similarity" without explaining it), that:
- Explains in one or two sentences *why* a bare LLM might confidently give a wrong policy answer
- Explains *how* RAG changes what the model has access to when answering
- Honestly names at least one way the RAG bot could still give a wrong or incomplete answer (grounded in a real failure mode from this week, e.g., chunking or retrieval misses)
- Recommends one practical safeguard (e.g., citation display, human review for high-stakes questions) given that residual risk

---

## Answer Key

### Section A

**A1.** A knowledge cutoff means the model's training data ends at some point in time, so it has no information about anything after that — and critically, the model has no built-in mechanism to *know what it doesn't know*. It generates the statistically most plausible continuation of text whether or not that continuation is true, which is why it hallucinates confidently rather than flagging uncertainty: there's no internal "knowledge cutoff alarm." This is especially dangerous for **fast-changing factual questions** — e.g., "What is our current refund policy?" or "Who is our current VP of Sales?" — where the model may confidently state outdated or fabricated information as if it were current fact.

**A2.** RAG clearly helps when the answer depends on **information not in the model's training data and that changes or is proprietary** — e.g., answering questions against a specific company's internal policy documents. RAG is unnecessary overhead when the task is **general knowledge or reasoning that doesn't depend on private/current facts** — e.g., "explain how photosynthesis works" — where retrieval adds latency, cost, and pipeline complexity without improving an answer the model already produces well from its training knowledge alone.

**A3.** Cosine similarity measures the **angle** between two vectors (via the cosine of that angle), capturing how similarly *directed* they are regardless of their magnitude. This matters for text embeddings because vector magnitude can vary with factors like document/sentence length or word-frequency scaling that have nothing to do with semantic meaning — two sentences expressing the same idea at different lengths could have very different magnitudes but should still point in a similar direction in embedding space. Euclidean distance is sensitive to magnitude differences and can therefore judge two semantically similar but differently-scaled vectors as "far apart" even when their direction (meaning) is nearly identical.

**A4.** Raw word-count (bag-of-words) vectors fail to cluster by topic because they only capture *which exact words appear and how often*, with no notion of meaning, synonymy, or context — two sentences about the same topic using different vocabulary will look dissimilar, while two sentences from different topics that happen to share common/generic words (e.g., "the," "is," "very") can look artificially similar, especially in short texts where a few shared filler words dominate the vector. One concrete fix: a **hybrid seed-word + bag-of-words approach** (i.e., weighting or selecting topic-indicative seed words rather than treating all words equally) — or more generally, moving to a representation (like a real embedding model) that captures semantic meaning rather than literal token overlap.

**A5.** Chunking is splitting a document into smaller pieces before embedding/indexing them for retrieval. It's a trade-off because **large chunks** preserve more surrounding context per chunk but dilute relevance — a chunk covering multiple topics has a "blended" embedding that may not closely match a narrow query, and retrieving it pulls in a lot of irrelevant text alongside the useful bit (context stuffing risk). **Small chunks** are more precisely matchable to specific queries, but risk **splitting a single fact or answer across chunk boundaries**, so the complete answer is never retrievable in one piece — or losing context needed to interpret the chunk correctly on its own.

**A6.** Citation grounding means the system explicitly ties each generated claim back to the specific retrieved source passage(s) it came from (e.g., showing "according to Section 4.2..." or inline citations), rather than just using retrieved text as silent background context. It protects against a failure that retrieval alone does not: the model **still generating ungrounded or fabricated claims even when correct source material was successfully retrieved** — i.e., retrieval finding the right passage doesn't guarantee the generation step actually used it faithfully; citation grounding makes that link visible/checkable and discourages the model from drifting from the retrieved text.

**A7.** Example pairs (any two, with correct symptom mapping):
- **Chunking errors** → symptom: the system seems to "almost" know the answer or gives a partial/incomplete answer, because the needed fact is split across chunk boundaries and no single retrieved chunk contains the complete information.
- **Retrieval misses** → symptom: the answer is confidently wrong or based on clearly unrelated content, because the chunk that actually contains the answer was never retrieved in the top-k at all.
- **Context stuffing** → symptom: the answer is vague, diluted, or buries the correct point among irrelevant details, because too many (or too broad) chunks were stuffed into the context window, and the model fails to prioritize the relevant part.
- **Lack of re-ranking** → symptom: a relevant chunk *was* retrieved but ranked low (e.g., rank 4 of 5) and got cut off or deprioritized, while a more lexically-similar but less relevant chunk ranked higher and dominated the answer.

### Section B

**B1.** The likely cause is that the PDF-extraction library doesn't preserve blank lines between visual sections — many PDF text extractors flatten whitespace/layout information, so what looks like a clear paragraph break in the rendered PDF becomes no blank line (or an inconsistent one) in the extracted raw text. Blank-line-based chunking then has nothing reliable to split on, so it collapses multiple real sections into one giant chunk. A more robust strategy: **chunk on section headers** (e.g., detecting heading patterns like numbered sections, ALL-CAPS titles, or markdown-style headers if present) rather than relying on whitespace, since header text tends to survive extraction even when blank-line formatting doesn't. This is more robust because it keys off content that's actually present and detectable in the extracted text, rather than a layout artifact (whitespace) that the extraction process may not preserve.

**B2.** This result shows that chunk size alone cannot fix a structural problem — when the answer genuinely depends on combining information from two different parts of a document (a paragraph and a separate table) that were never written to be adjacent, no chunk size will reliably place them in the same chunk together, because chunking operates on document position/length, not on logical relationship between facts. A fix that isn't "try a fourth size": **retrieve multiple chunks and let the generation step synthesize across them** (i.e., increase top-k and rely on the LLM to combine retrieved pieces), or **restructure/pre-process the source document** so related facts (the policy statement and the table row) are co-located before chunking, or use a **chunking strategy aware of document structure** (e.g., keeping a table together with its preceding explanatory paragraph as one unit). This is fundamentally a **retrieval/chunking-strategy limitation**, not a tunable-parameter problem — it's the chunking-error failure mode, but specifically the "single answer spans multiple disjoint source locations" variant.

**B3.** This is more nuanced than a total retrieval miss because the system didn't fail to find *anything* related to the query term — it found a chunk containing the literal word "remote," just in an unrelated sense (remote office *locations* vs. remote *work* policy), and that chunk simply wasn't ranked highly enough (or was ranked below an even-less-relevant chunk) to be used. This exposes the limitation of relying on **lexical/keyword overlap** as a proxy for relevance: surface word matching can't distinguish between different *senses* of the same word, whereas true semantic relevance requires understanding that "remote" in "remote office in Austin" and "remote" in "work remotely on Fridays" are different concepts despite identical text. The first thing to try: **improving the embedding/similarity step or adding re-ranking** — a stronger embedding model (or a re-ranker that scores semantic relevance more precisely than the initial retrieval pass) is more likely to correctly distinguish "remote work policy" from "remote office location" than tweaking chunk size or top-k alone, since the problem is a relevance-discrimination issue, not a missing-content issue.

**C1.** Sample model answer (grade for content, not exact wording):

> A general AI assistant answers questions by predicting the most likely-sounding response based on everything it learned during training — it has no actual copy of our company's policy documents, so if you ask it a specific policy question, it can generate a confident, fluent-sounding answer that is simply made up. Our policy Q&A bot works differently: before answering, it first searches our actual policy documents for the most relevant sections, and only then writes an answer using that retrieved text as its source — similar to how a well-prepared employee would look up the handbook before answering rather than guessing from memory. This makes wrong answers much less likely, but not impossible: if a question's answer is split across two different sections of the handbook that don't get retrieved together, or if the search step pulls up a similar-sounding but wrong section, the bot can still give an incomplete or incorrect answer. Because of this, for any high-stakes policy question — anything involving pay, leave, or legal compliance — we display the source section alongside the answer and require a human to confirm it before it's treated as final, rather than trusting the bot's answer alone.

### Section A: 7 × ~3 pts = 21 pts | Section B: 3 × 8 pts = 24 pts | Section C: 1 × 15 pts = 15 pts

---

## Grading Guidance

- **Section A (21 pts):** Full credit requires the correct mechanism/definition *and* a relevant example or "why" — not just a definition. Half credit for a correct but unexplained answer.
- **Section B (24 pts):** Grade holistically against the answer key's reasoning. These scenarios are deliberately drawn from real verified findings (toy embedding clustering failure, chunk-size testing results, and a real retrieval-miss diagnosis) — award strong credit for answers that correctly identify the *category* of failure (chunking vs. retrieval vs. semantic-discrimination) even if the proposed fix differs from the model answer, as long as the reasoning for the fix is sound.
- **Section C (15 pts):** Grade on four components: (1) correctly explains why a bare LLM can hallucinate on policy questions [4 pts], (2) correctly explains what RAG changes [4 pts], (3) honestly names a real residual risk grounded in an actual Week 3 failure mode rather than a generic disclaimer [4 pts], (4) proposes a concrete, practical safeguard [3 pts]. Deduct for jargon used without explanation, per the question's explicit instruction.
- **Total: 60 pts.** Suggested cutoffs: 54+ = excellent, 42–53 = solid, 30–41 = needs review (check which session cluster — embeddings/3.2, chunking/3.3, or failure modes/3.5 — the missed questions trace to), <30 = recommend revisiting Week 3 sessions before Week 4.
