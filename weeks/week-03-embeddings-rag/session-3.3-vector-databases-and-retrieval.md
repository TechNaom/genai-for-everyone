# Session 3.3 — Vector Databases & Retrieval

## Chunking Strategies, Vector Stores, and Top-k Retrieval

---

### From a handful of sentences to a real library

Session 3.2 left you somewhere genuinely useful but also genuinely small: 20 sentences, turned into vectors, plotted in 2D, with four clusters you could see with your own eyes. That was the right scale for *learning* what an embedding is. It is nowhere near the right scale for what you're actually going to build.

Picture the real version of this problem. Your company has a 200-page employee handbook, forty product specification documents, three years of meeting notes, and a customer support knowledge base with two thousand articles. A user asks a single question. Somewhere across all of that text — not in one convenient sentence, but possibly buried in paragraph fourteen of a forty-page PDF — is the actual answer. You can't hand the entire corpus to an LLM; even with a generous context window, that's slow, expensive, and often genuinely worse, because the model has to find a needle in a haystack you handed it directly instead of you handing it the needle. You need a system that, given a question, can instantly identify the *small number* of passages actually worth reading — out of potentially millions of candidates — and hand only those to the model.

That system has three parts, and today you build all three: **chunking** (deciding how to slice your documents into searchable pieces in the first place), **vector stores** (where you put the resulting embeddings so they can be searched efficiently), and **top-k retrieval** (the actual mechanism for pulling back the best few matches to a live query). Each one sounds simple in a sentence. Each one has a genuine, non-obvious failure mode you need to understand before you build the full RAG pipeline next session.

---

### Chunking: the decision nobody tells you is hard until you've made it badly

Here's a question that sounds almost too basic to need an answer: when you embed a document, what exactly do you embed? The whole document at once? Each paragraph? Each sentence?

It turns out this single decision — called **chunking** — has an outsized effect on whether your retrieval system actually works, and it's one of the first places real RAG systems go wrong in practice.

Embed an entire 40-page document as a single vector, and you've created something almost useless for retrieval: that one vector is now an average — a blur — of everything in the whole document, from the executive summary to an appendix about printer settings. A user's specific question about page 23 produces a query vector that has to compete, in similarity terms, against this single enormous blurred representation of "the whole document, vaguely." Specific questions deserve specific matches, and a whole-document vector cannot give you that.

Go to the opposite extreme — embed every single sentence as its own chunk — and you run into a different problem: context collapse. A sentence like "This also applies to part-time employees" is perfectly clear in the paragraph it came from and nearly meaningless on its own once it's been sliced out and embedded in isolation. The embedding can only encode the meaning that's actually present in the text you feed it; if you strip away the surrounding context that gave a sentence its meaning, the vector has nothing to represent.

The practical answer sits in between, and it's less a fixed rule than a genuine design decision: **chunk by a roughly fixed size (commonly somewhere in the range of a few hundred words, sometimes specified in tokens), with enough overlap between consecutive chunks that an idea spanning a chunk boundary doesn't get orphaned on one side of a hard cut.** A common pattern is something like 200–500 words per chunk with a 10–20% overlap between consecutive chunks. There is no single universally correct number — the right chunk size depends on your documents (dense legal text behaves differently than a casual FAQ) and on your retrieval goals, and tuning it is a real, recurring task in production RAG work, not a one-time setting you pick and forget.

There's a second, equally important dimension to chunking that's easy to overlook if you only think about chunk *size*: chunk *boundaries*. Where you cut matters as much as how big the pieces are. Cutting a chunk in the middle of a sentence, or worse, in the middle of a table or a numbered list, produces a chunk that's syntactically broken even before you think about its meaning. Better chunking strategies try to respect natural document structure — paragraph breaks, section headers, list boundaries — splitting *near* your target size rather than at a rigid character count that might land anywhere.

---

### Vector stores: a library card catalog for meaning

Once you've chunked your documents and embedded each chunk, you have a large pile of vectors, each one paired with the text it came from. You need somewhere to put them — specifically, somewhere that can answer the question "which of these thousands (or millions) of vectors is closest to this new query vector?" *fast*.

This is what a **vector store** (sometimes called a vector database) is for. You could, in principle, store your vectors in a plain list and compute cosine similarity against every single one whenever a query comes in — and for the 20-sentence example from last session, that would work just fine. But this approach, called a brute-force or exhaustive search, scales linearly with the number of vectors: search a million vectors, and you're computing a million similarity scores for every single query. At real-world scale, that becomes too slow for an interactive application.

Vector stores solve this with specialized indexing structures (the most common family is called **Approximate Nearest Neighbor**, or ANN, search) that organize vectors so that a search can skip over most of the database without checking it directly — trading a small amount of accuracy (you might occasionally miss the single mathematically-best match) for an enormous gain in speed. This is a genuinely different kind of database from the relational databases (think rows, columns, and exact-match queries) you may already be familiar with: a vector store is built from the ground up around the question "what's nearby?" rather than "what matches exactly?"

You'll encounter named vector stores throughout your GenAI career — some are standalone databases built specifically for this purpose, others are extensions bolted onto existing database systems, and some are lightweight, in-process libraries meant for smaller-scale or local use (which is exactly the category today's exercise uses, since you're building a local store over a single PDF rather than standing up production infrastructure). The names and specific APIs will keep changing as the field matures; the underlying concept — efficient nearest-neighbor search over embeddings — is what's worth actually understanding, because it transfers regardless of which specific tool you end up using on the job.

---

### Top-k retrieval: choosing how much is enough

So you have your chunks embedded and stored, and a system that can find the nearest vectors to a query quickly. The last piece is deciding: when a question comes in, how many matching chunks do you actually retrieve and hand to the model?

This is **top-k retrieval** — you retrieve the *k* most similar chunks to the query (by cosine similarity, the metric from Session 3.2), where *k* is a number you choose. And, true to the pattern of basically every real engineering decision in this course so far, the right value of *k* is a genuine trade-off, not a fixed constant.

Set *k* too low — say, k=1 — and you risk missing the actual answer if it happens to be split across two adjacent chunks, or if the single best-matching chunk by cosine similarity isn't actually the most useful one for fully answering the question. Set *k* too high — say, k=50 — and you start reintroducing the exact problem RAG was supposed to solve in the first place: you're handing the model a large pile of mostly-irrelevant text, diluting the genuinely useful passages, increasing cost and latency, and in some cases measurably *hurting* answer quality, because models can struggle to stay focused on the right information when it's surrounded by a lot of similar-sounding noise. A typical real-world starting point is somewhere in the range of k=3 to k=10, but exactly like chunk size, the right number depends on your documents, your typical query style, and direct experimentation — which is precisely the kind of practical tuning Session 3.5 covers when you learn to diagnose and fix retrieval problems systematically.

There's a subtlety worth naming here, because it previews a real limitation you'll meet head-on in Session 3.5: top-k retrieval based purely on cosine similarity finds chunks that are *semantically close* to the query — but semantically close is not automatically the same thing as *most useful for answering the question*. A chunk can be topically related without containing the specific fact being asked about, and the genuinely best answer might be split across two chunks that individually look like only moderate matches. This is one of several reasons production RAG systems often add a second step — re-ranking the initial top-k candidates with a more careful (and more expensive) comparison — which you'll meet by name in Session 3.5.

---

### Putting the three pieces together, end to end

Step back and look at the full pipeline you're building today, because it's worth seeing as a single connected sequence rather than three separate ideas:

1. **Chunk** the source document into appropriately-sized, sensibly-bounded pieces.
2. **Embed** each chunk using the same kind of vector representation from Session 3.2.
3. **Store** every chunk's vector (along with the original chunk text) in a vector store built for fast nearest-neighbor search.
4. When a real question arrives, **embed the question** using the same embedding approach.
5. **Retrieve** the top-k most similar chunks from the store.
6. Hand those retrieved chunks to the model as context — which is exactly the "augment" step from Session 3.1's retrieve-augment-generate framework, now made fully concrete.

Notice that step 6 is where this session connects directly back to where Week 3 started. Session 3.1 told you, conceptually, that RAG means handing the model real, relevant text instead of trusting its memory. Today, for the first time, you have an actual mechanism — chunking plus a vector store plus top-k retrieval — for deciding *which* real, relevant text to hand it. Nothing about generation has happened yet; today's exercise stops right after step 5, with a working local vector store that can take a real question about a real PDF and hand back the most relevant passages. That's deliberate. Session 3.4 adds the final step — actually generating a grounded answer from what you retrieve — and brings the entire system to life as a complete, working RAG pipeline.

---

### What today's exercise will make visible

When you build your local vector store over a real PDF today, pay close attention to one thing in particular: try a few different chunk sizes on the *same* document and the *same* test questions, and watch the retrieved results change. A chunk size that's too small will sometimes retrieve fragments that are technically on-topic but missing the context to actually answer the question. A chunk size that's too large will sometimes retrieve a chunk that contains the right answer buried inside three paragraphs of surrounding material that has nothing to do with the question. There is no single "correct" setting waiting to be discovered — there's a genuine engineering trade-off, and today is your first chance to feel it directly rather than just read about it.

That hands-on feel for the trade-off is exactly what Session 3.5 will ask you to diagnose systematically once you've seen a working pipeline misbehave in Session 3.4. For now: build the engine, watch it retrieve real passages from a real document in response to real questions, and notice where it does well and where it struggles. You're not just learning a technique today — you're building the actual component that decides what an LLM gets to see before it answers, which is, in a real sense, the single most consequential design decision in any RAG system you'll ever build.

---

## Points to Remember

- **Chunking is a genuine design decision, not a default setting.** Whole-document embeddings blur everything into one vague vector; single-sentence chunks can lose the surrounding context that gave them meaning. The practical answer sits in between, tuned to your documents.
- **Chunk boundaries matter as much as chunk size.** Cutting mid-sentence or mid-list produces a chunk that's broken even before you consider its meaning — better chunkers respect natural structure like paragraphs and headers.
- **A vector store exists to answer "what's nearby?" fast**, using Approximate Nearest Neighbor indexing to avoid comparing a query against every single vector in the database.
- **Top-k retrieval is a trade-off, not a fixed constant.** Too low a k risks missing the answer; too high a k reintroduces noise and can measurably hurt answer quality by diluting the genuinely relevant passages.
- **Semantically close is not the same as most useful for answering the question.** A chunk can be topically related without containing the specific fact being asked about — this is exactly what motivates re-ranking, covered in Session 3.5.
- **Today's exercise stops deliberately after retrieval, before generation.** Chunking, embedding, storing, and retrieving form a complete sub-system on their own — Session 3.4 adds the final generation step on top.

---

## Quick Check: Fill in the Blanks

1. Embedding an entire document as a single vector produces a __________ representation that blurs together everything from the summary to the appendix.
2. Embedding individual sentences in isolation risks __________, where a sentence that was clear in context becomes nearly meaningless once sliced out on its own.
3. A vector store uses __________ indexing to avoid comparing a query against every single stored vector.
4. Setting top-k too __________ risks missing the answer if it's split across chunks; setting it too __________ reintroduces irrelevant noise.
5. A chunk being semantically close to a query is not the same as the chunk being __________ for actually answering the question — a gap that motivates re-ranking in Session 3.5.

**Answers:** 1. blurred / averaged — 2. context collapse — 3. Approximate Nearest Neighbor (ANN) — 4. low, high — 5. most useful

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-03/session-3.3-quiz.md`](../../assessments/quizzes/week-03/session-3.3-quiz.md) · Answer key: [`assessments/answer-keys/week-03/session-3.3-quiz-answers.md`](../../assessments/answer-keys/week-03/session-3.3-quiz-answers.md)

Interview-style questions for this topic:

1. *"Why can't you just embed an entire document as a single vector for retrieval purposes?"*
2. *"What's the difference between a vector store and a traditional relational database, conceptually?"*
3. *"Walk me through the trade-off in choosing top-k for a retrieval system. What happens at the extremes?"*
4. *"Give an example of a chunk that would be semantically close to a query but still not useful for answering it."*

---

## Core path — guided activity

**Build a Local Vector Store Over a PDF.** You'll chunk a real sample company handbook, embed each chunk using the word-count approach from Session 3.2, store the vectors, and retrieve the top-k most relevant chunks for real test questions — the full pipeline minus the final generation step. Full instructions: [`codebase/exercises/week-03/session-3.3/`](../../codebase/exercises/week-03/session-3.3/).

## Pro path — extended challenge

Run the same sick-leave question ("How many sick days do employees get and do they roll over?") against the handbook at two different chunk sizes and compare the actual retrieved results — don't predict the outcome in advance, run it and look. At one setting you'll likely see retrieval miss the sick-leave chunk entirely in favor of an unrelated PTO chunk that shares surface words like "days" and "employees"; at a smaller chunk size, the genuinely correct chunk should appear, though not always cleanly in the top slot. This is the real, occasionally messy trade-off chunking forces on you — worth seeing with your own generated numbers rather than taking on faith.

## What's next

Session 3.4 — **Building a RAG Pipeline** — retrieval, augmentation, and generation, brought together end to end, with citation grounding so every answer can be traced back to the real passage it came from.
