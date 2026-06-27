# Session 3.4 — Building a RAG Pipeline

## Retrieval → Augmentation → Generation, End to End, with Citation Grounding

---

### The last mile

You've now built every individual piece of a RAG system without ever actually using one to answer a question. Session 3.1 gave you the reason RAG exists at all. Session 3.2 gave you the math underneath "find the relevant text." Session 3.3 gave you a working local vector store that could take a real question about a real PDF and hand back the most relevant passages — and then, deliberately, stopped right there.

That stopping point was the right place to pause, but it's an uncomfortable one to leave a system in for long. Imagine asking a brilliant research assistant a question, watching them correctly pull the three most relevant pages out of a filing cabinet, lay them neatly on your desk — and then just stand there. They did real, useful work. But you still don't have an answer. Today, your research assistant finally speaks.

This session connects retrieval to generation for the first time, and in doing so, makes the "augmented" in Retrieval-Augmented Generation a concrete, visible step rather than an abstract phrase from Session 3.1. You'll also add something neither 3.1 through 3.3 needed to worry about: **citation grounding** — making sure the model's final answer can be traced back to the specific retrieved passages that actually support it, rather than trusting that it used them faithfully.

---

### The third step, finally made real

Recall the three-step move from Session 3.1: retrieve, augment, generate. You've already built retrieve (Sessions 3.2–3.3 gave you the embeddings and vector store that make it work). Today's session is almost entirely about the other two:

**Augment** means taking the chunks your vector store handed back and inserting them into the prompt, alongside the user's actual question, in a structured way the model can clearly tell apart from the question itself. This sounds almost too simple to need much thought — and the basic mechanics genuinely are simple — but *how* you structure that insertion has a real effect on answer quality, which is worth treating with the same care you gave prompt design back in Week 2.

**Generate** means asking the model to actually answer the question, but with an instruction that fundamentally changes what kind of answer you're asking for. You're not asking "what do you know about X?" anymore. You're asking "given specifically this retrieved text, answer this specific question, using only what's in front of you." That's a different task than open-ended generation, and the prompt needs to say so explicitly — otherwise you risk the model quietly falling back on its own training-data memory instead of the text you worked hard to retrieve, which defeats the entire purpose of building a retrieval pipeline in the first place.

---

### A RAG prompt template, dissected

Here is roughly what a grounded RAG prompt looks like in practice, and every piece of it is doing a specific job:

```
You are answering a question using ONLY the information in the provided
context below. If the context does not contain enough information to
answer the question, say so explicitly rather than guessing or using
outside knowledge.

CONTEXT:
[1] {retrieved chunk 1 text}
[2] {retrieved chunk 2 text}
[3] {retrieved chunk 3 text}

QUESTION: {user's question}

Answer the question, and cite which numbered context chunk(s) support
each part of your answer.
```

Look at what each part is actually doing, because none of it is filler:

- **"ONLY the information in the provided context"** is the single most load-bearing instruction in the entire template. Without it, you've built an elaborate, carefully-tuned retrieval system whose output the model is free to simply ignore in favor of its own memorized (and possibly outdated, possibly hallucinated) knowledge. This instruction is what actually makes the system *retrieval-augmented* rather than just retrieval-adjacent.
- **"If the context does not contain enough information... say so explicitly"** directly addresses Session 3.1's central warning about confident-sounding fabrication. A retrieval system will sometimes retrieve chunks that are topically related but don't actually answer the question — you saw this happen yourself in Session 3.3's honest results. Without this instruction, a model handed near-miss context will often still produce a fluent, confident answer anyway, quietly papering over a retrieval gap instead of surfacing it.
- **Numbered chunks** turn an undifferentiated wall of retrieved text into addressable units. This single formatting choice is what makes citation possible at all in the next step — you cannot ask a model to cite "which part of the context" supported an answer if the context has no internal structure to point to.
- **"cite which numbered context chunk(s) support each part of your answer"** is the citation grounding instruction, and it's the piece that turns "the model says it used the context" into something you can actually verify.

---

### Why citation grounding matters more than it might seem

It's worth pausing on why citation grounding deserves to be treated as a first-class part of the pipeline rather than a nice-to-have polish step you could add later.

Without it, a RAG system's output looks exactly the same whether the model faithfully grounded its answer in the retrieved chunks or quietly ignored them and answered from memory instead. Both produce a fluent paragraph of text. There's no visible difference between "the system worked as designed" and "the system silently bypassed its own safeguards" — which is precisely the kind of failure that's invisible until it causes real damage, echoing exactly the fluent-failure problem from Session 3.1.

Citation grounding turns an invisible failure mode into a checkable one. If a model's answer cites chunk [2], you can go look at chunk [2] and verify, directly, whether it actually supports what the model claimed. If the model's answer makes a specific claim with no citation attached, that's an immediate, visible signal that something may have gone wrong — either the model used outside knowledge, or it failed to ground a claim it should have grounded. This doesn't make a RAG system bulletproof (a model can still cite a chunk that doesn't actually support its claim, which is a deeper problem you'll learn to systematically catch in Session 3.5), but it converts the central trust problem from Session 3.1 — "I can't tell if this is grounded or fabricated" — into something with at least a visible paper trail.

---

### Where the seams show: connecting 3.3's output to 3.4's input

There's a small but genuinely important engineering detail worth naming explicitly, because it's the kind of thing that's easy to get subtly wrong on a first attempt: the format your retrieval step hands off needs to match what your generation step expects to receive.

Session 3.3's `VectorStore.search()` returned a list of `(chunk_text, similarity_score)` tuples. That similarity score was essential for *building* the retrieval system and for the kind of diagnostic work you did comparing chunk sizes — but it has no place inside the final prompt you send to the model. A user's question doesn't need to know that chunk 2 scored 0.74; the model needs the chunk's actual text, clearly numbered, and nothing else cluttering the context. Part of today's exercise is this exact translation step: taking retrieval's internal representation (text plus a similarity score, useful for you and your code) and reshaping it into generation's input format (clean, numbered context, useful for the model). This kind of small "adapter" step between pipeline stages is extremely common in real production RAG systems, and it's worth getting comfortable with rather than treating as an annoying afterthought.

This is also a good moment to notice something about pipeline design more generally: each stage of a RAG system — chunking, embedding, storing, retrieving, augmenting, generating — has its own internal data shape that's optimized for what that stage needs to do its job well, and almost none of those internal shapes are identical to each other. A chunk during embedding is just a string. The same chunk during retrieval is a string paired with a similarity score. The same chunk again during generation is a numbered, labeled unit of context. None of this is incidental complexity to be embarrassed about — it's the normal shape of a multi-stage pipeline, and learning to recognize "this is an adapter step between two stages" as a distinct, ordinary kind of code you'll write often is a genuinely useful pattern to take with you past this course.

---

### A second design choice: where citations actually point

There's a subtlety in citation grounding worth calling out explicitly, because it's easy to design a system that looks like it has working citations while actually being far less useful than it appears. A citation is only as good as what it points back to. If your numbered context chunks are large, a citation that says "see chunk [2]" still leaves the user (or your downstream system) hunting through several hundred words to find the specific sentence that actually supports the claim. This is a direct echo of Session 3.3's chunking trade-off, reappearing in a new form: the same chunk size decision that affects retrieval quality also affects how *precise* a citation can possibly be, since a citation can never be more specific than the chunk it points to. There's no single fix to put in place today — just a connection worth holding onto, since you'll see exactly this tension again when re-ranking and finer-grained retrieval come up in Session 3.5.

---

### Defensive thinking, carried forward from Week 2

If Session 2.4's lesson about defensive parsing and Session 2.6's lesson about designing for graceful failure feel like they're showing up again here, that's not a coincidence — it's the same engineering discipline, applied to a new kind of pipeline. A few things worth building defensively into your RAG generation step today:

- **What happens if retrieval returns nothing useful?** If the top-k chunks all have very low similarity scores, the honest answer is often "I don't have enough information to answer this" — and your system should be willing to say that, rather than forcing a confident-sounding answer out of weak context, exactly as the prompt template's second instruction specifies.
- **What happens if the model ignores the citation instruction?** Models don't always perfectly follow every formatting instruction every time. A production system should have a plan for what to do if a citation is missing or malformed, rather than assuming the instruction will always be followed flawlessly. (You won't build a full validation layer for this today — that's adjacent to the parsing work from Session 2.4 — but it's worth noticing the gap and thinking about how you'd close it.)
- **What happens if the question is genuinely unanswerable from the document set?** This is different from "retrieval found weak matches" — this is "the document set fundamentally doesn't contain this information at all." Both should lead to the same honest "I don't have enough information" response, for the same underlying reason Session 3.1 first introduced: a system that knows the boundary of what it can answer is more trustworthy than one that always sounds confident.

---

### What today's exercise will produce

By the end of today, you'll have a single function that takes a raw user question, runs it through retrieval (reusing Session 3.3's vector store), augments a prompt with the retrieved chunks in proper numbered format, sends that prompt to an LLM, and returns a generated answer with citations attached — pointing back at the exact chunks that supported it. This is, for the first time in this course, a complete, working RAG application, end to end, over a real document.

It will not be a perfect one. You already know from Session 3.3's honest results that retrieval itself sometimes returns near-misses rather than clean hits, and nothing about adding a generation step on top fixes that underlying problem — it can only generate an honest "I don't have enough information" response *if* you've built the defensive instructions to allow for that outcome, or it will generate a fluent answer from a flawed retrieval, which looks identical to a correct one from the outside. That gap — between a RAG system that runs without errors and a RAG system that's actually trustworthy — is exactly where Session 3.5 picks up. Today, you build the complete machine. Next session, you learn to find out where it's lying to you.
