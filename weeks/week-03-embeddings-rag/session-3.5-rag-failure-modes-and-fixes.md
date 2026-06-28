# Session 3.5 — RAG Failure Modes & Fixes

## Chunking Errors, Retrieval Misses, Context Stuffing, and Re-Ranking

---

### You've already seen every failure mode in this lesson

Most sessions in this course introduce something genuinely new. This one doesn't, and that's deliberate. Every failure mode you're about to learn the name for, you've already watched happen with your own eyes, using your own code, on real output you generated yourself.

In Session 3.3, you ran the exact same question — about sick leave — through three different chunk sizes, and not one of them got it cleanly right. At chunk_size=100, retrieval confidently handed back a PTO chunk instead of the sick-leave chunk it was actually asked about. At chunk_size=250, a generic intro paragraph that name-drops every topic in the handbook started winning the top spot for questions it had no business answering. In Session 3.4, you built a generation step on top of that same retrieval system and learned, in the abstract, that a confident-sounding answer built on weak context is indistinguishable from one built on strong context — unless you actually go check.

Today is the session where all of that stops being "things that happened to occasionally go wrong" and becomes a vocabulary: a small number of named, recognizable failure patterns, each with a specific diagnosis and a specific fix. Naming a failure mode is not just an academic exercise — it's what turns "huh, that's weird" into "I know exactly what to check next," which is the actual difference between debugging by luck and debugging by skill.

---

### Failure mode 1: Chunking errors

You met this one directly. A **chunking error** is any case where the way you split a document actively works against retrieval — either by orphaning an idea across a chunk boundary (too-small chunks, no overlap), or by diluting a specific fact inside a chunk so broad it competes poorly against more "generically relevant-sounding" text (too-large chunks).

The diagnostic signal is specific: if you ask a system a question with a clear, factual answer that you know exists verbatim somewhere in the source documents, and the top retrieved chunk either doesn't contain that fact at all, or contains it buried in the middle of several paragraphs of unrelated material, you're looking at a chunking error. The fix isn't a single universal chunk size — you already learned that in Session 3.3 — but a documented process: test multiple chunk sizes against a representative set of real questions (not just one or two — a handful spanning the range of topics and phrasing your real users actually use), and watch specifically for cases like your sick-leave example, where two related-but-distinct topics share enough vocabulary that a clumsy chunk size blurs the boundary between them.

---

### Failure mode 2: Retrieval misses

A **retrieval miss** is a broader category than a chunking error, though chunking errors are one common cause of it. A retrieval miss is simply: the chunk that actually contains the answer exists somewhere in your document set, but it didn't make it into the top-k results handed to the model at all.

This can happen for reasons that have nothing to do with chunk size. Recall Session 3.2's central limitation of the toy word-count embeddings you built: a query asking about "canine companions" and a document discussing "dogs" would show low similarity under a word-count approach, even though they mean almost the same thing, because there's no shared vocabulary for the math to find. Real embedding models reduce this risk substantially (that's the entire reason they're trained on enormous amounts of text), but they don't eliminate it — any embedding-based retrieval system can miss a genuinely relevant chunk simply because the query and the answer happen to be phrased very differently from each other.

The diagnostic signal here is almost identical to a chunking error from the outside — "the system didn't find the right answer" — which is exactly why you need to actually inspect *which* chunks got retrieved, not just whether the final answer was right. If the correct chunk never appears anywhere in your top-k results, no matter how generously you set k, that's a retrieval miss, and the fix is different from a chunking fix: you might need a larger k, a better embedding model, or — as you'll see shortly — a re-ranking step that can recover a near-miss the first retrieval pass almost found.

---

### Failure mode 3: Context stuffing

**Context stuffing** is the failure mode hiding inside a temptation that feels completely reasonable the first time you encounter it: "retrieval is uncertain, so why not just set k very high and hand the model a lot of context — surely more information can only help?"

It can't, and you already met the theoretical version of this in Session 3.3's top-k discussion. Context stuffing is what happens when that theoretical risk becomes concrete: the model is handed ten, twenty, or fifty retrieved chunks, most of which are only weakly relevant or entirely irrelevant, and somewhere in that pile is the one chunk that actually matters. Models don't have unlimited, uniform attention across an enormous block of text — burying a single relevant fact inside a large amount of surrounding noise measurably increases the odds the model either misses it, blends it with irrelevant nearby text, or produces a vaguer, hedgier answer than the same fact would have gotten if it had been handed cleanly and alone.

The diagnostic signal: if you find yourself increasing k as a generic fix for "retrieval doesn't seem reliable enough," without first checking *why* the right answer isn't showing up at lower k, you're at serious risk of trading a retrieval-miss problem for a context-stuffing problem instead. The two failure modes can look superficially similar (both can produce a wrong or weak final answer) but call for opposite fixes — one wants more retrieved context, the other wants less, more precisely chosen.

---

### The fix that addresses both misses and stuffing: re-ranking

You were promised this term back in Session 3.3, and here it is. **Re-ranking** is a second retrieval pass: instead of trusting the first round of top-k cosine-similarity results as final, you retrieve a larger initial pool of candidates (say, the top 20 instead of the top 3), then run a more careful, more computationally expensive comparison between the query and each of those 20 candidates specifically, and keep only the best few after this second look.

Why does this help with both failure modes at once? For retrieval misses: casting a wider net initially (top 20 instead of top 3) gives a near-miss — a chunk that scored just outside your original top-3 cutoff but is actually the right answer — a real chance to be reconsidered, rather than being permanently discarded by the first pass's cutoff. For context stuffing: the re-ranking step itself acts as a quality filter, so you can retrieve a more generous initial pool without committing to handing all 20 candidates to the generation step — only the re-ranked, genuinely-best few make it into the final prompt.

The "more careful, more expensive comparison" in re-ranking is usually a different and more computationally intensive kind of model than the embedding similarity you used for the first pass — one that can directly evaluate "how well does this specific chunk answer this specific query" rather than just measuring vector closeness. This is exactly why re-ranking is typically applied as a second pass over a smaller candidate pool rather than as the primary search mechanism over your entire document set: it's too expensive to run against every chunk in a large corpus, but very practical to run against the 20 candidates your first-pass retrieval already narrowed things down to.

---

### A genuinely important distinction: a miss you can name vs. one you can't

Step back and notice something about the three failure modes you've just learned, compared to Session 3.1's original warning about hallucination. A chunking error, a retrieval miss, and context stuffing are all failures with a discoverable cause and a specific, targeted fix. You can point at exactly what went wrong and exactly what to change.

This matters because it draws a sharp line between two very different kinds of problems that can produce the same symptom — a wrong or unhelpful answer. One kind is a *pipeline* problem: something in chunking, retrieval, or context assembly didn't do its job well, and fixing that specific stage fixes the symptom. The other kind, which you'll meet properly in Week 5, is closer to a *trust* problem: even with a well-functioning pipeline, you still need systematic evaluation to catch cases where everything technically worked but the answer was still subtly wrong in a way no single component failure explains. Today's session is squarely about the first kind — and learning to recognize and name pipeline failures is itself the prerequisite for telling the two kinds apart, rather than throwing every bad answer into one undifferentiated "the AI was wrong" bucket.

---

---

### A worked example: diagnosing one failure mode from its symptom alone

It's worth walking through, once, exactly how this diagnostic process plays out, because the skill is in the *order* you check things, not just in knowing the three names.

Suppose a user asks your handbook bot: "How many sick days do I get and do they carry over?" — your exact Session 3.3 test case — and the system answers confidently with the PTO carryover policy (10-day cap, paid out on separation) instead of the sick-leave policy (no carryover, never paid out). The answer is fluent, specific, and entirely wrong for this question. Where do you look first?

Not at the answer's wording — you already know from Session 3.4 that fluency tells you nothing about correctness. You look at what was actually retrieved. If you inspect the top-k chunks handed to the model and the correct sick-leave chunk simply isn't there at all, you're looking at a retrieval miss (or, if you can trace it specifically to chunk boundaries cutting awkwardly through the sick-leave section, a chunking error — the two often travel together). If the correct chunk *is* present somewhere in what was retrieved, but it's buried as the eighth of ten chunks handed to the model alongside a lot of other material, that's context stuffing — the information was technically available to the model, just poorly surfaced. Each of these produces the identical symptom (a wrong answer about sick leave) but points to a different stage of the pipeline and a different fix. Skipping straight to "the model is bad at following instructions" — without first checking what it was actually given to work with — is the single most common mistake at this stage, and it's the mistake today's exercise is specifically designed to train you out of.

---

### What today's exercise will ask of you

You'll be handed a RAG pipeline today, not one you build from scratch — a working but deliberately broken system, with one or more of today's three failure modes built into it on purpose. Your job is diagnostic: given a real question and a real wrong (or weak) answer, figure out *which* failure mode is responsible, using the same kind of direct inspection you practiced in Sessions 3.3 and 3.4 — looking at what was actually retrieved, not just trusting that the final answer's fluency means the pipeline worked.

This is a different skill than the building you've done all week, and it's worth taking seriously as its own skill. Building a RAG pipeline that works on your test questions is necessary but not sufficient for production use — the real test is whether you, or someone on your team, can diagnose it quickly and correctly when a user reports that it gave a bad answer on a question you never thought to test yourself. That diagnostic instinct — check the retrieved chunks first, not the final answer's tone — is the single most transferable thing this entire session has to teach, and it's exactly what tomorrow's Week 3 lab will ask you to apply, unprompted, while building something new.

---

## Points to Remember

- **A chunking error, a retrieval miss, and context stuffing can all produce the identical visible symptom** — a wrong or weak final answer — but they point to different stages of the pipeline and require different fixes.
- **The diagnostic move is always the same: inspect what was actually retrieved, not just whether the final answer sounds right.** Fluency tells you nothing about which failure mode (if any) you're looking at.
- **Retrieval misses and context stuffing call for opposite fixes.** One needs more or better-targeted retrieval; the other needs less, more precisely chosen context. Reaching for "just increase k" without diagnosing first risks trading one failure mode for the other.
- **Re-ranking helps with both misses and stuffing at once**: cast a wider initial net (so near-misses survive the first cutoff), then apply a more expensive, more precise second-pass comparison to keep only the genuinely best few before generation.
- **A pipeline failure and a trust/evaluation failure are different categories of problem**, even though both can produce a wrong answer. Today is about the first category; Week 5 covers the second.
- **The same symptom can have more than one cause traveling together** — a chunking error and a retrieval miss often show up hand in hand, since awkward chunk boundaries are one common cause of a chunk failing to be retrieved at all.

---

## Quick Check: Fill in the Blanks

1. A __________ error happens when the way a document is split actively works against retrieval — either orphaning an idea across a boundary, or diluting a fact inside an overly broad chunk.
2. A retrieval __________ means the correct chunk exists somewhere in the document set, but it didn't make it into the top-k results at all.
3. __________ is what happens when a generously high k buries the one genuinely relevant chunk inside a large pile of weakly relevant or irrelevant ones.
4. Re-ranking works by retrieving a larger __________ pool of candidates first, then applying a more careful, more expensive comparison to keep only the best few.
5. When diagnosing a wrong answer, the correct first move is to inspect the actual __________, not the fluency or tone of the final answer.

**Answers:** 1. chunking — 2. miss — 3. Context stuffing — 4. initial / candidate — 5. retrieved chunks

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-03/session-3.5-quiz.md`](../../assessments/quizzes/week-03/session-3.5-quiz.md) · Answer key: [`assessments/answer-keys/week-03/session-3.5-quiz-answers.md`](../../assessments/answer-keys/week-03/session-3.5-quiz-answers.md)

Interview-style questions for this topic:

1. *"A RAG system gives a wrong answer. Walk me through exactly what you'd check first, second, and third."*
2. *"Explain why 'just increase k' can sometimes make a RAG system worse, not better."*
3. *"How does re-ranking address both retrieval misses and context stuffing with a single mechanism?"*
4. *"What's the difference between a pipeline failure and a trust/evaluation failure in a RAG system, and why does the distinction matter?"*

---

## Core path — guided activity

**Debug a Broken RAG Pipeline (Given).** You'll be handed `broken_pipeline.py` — a working RAG pipeline with three bugs planted on purpose, one per failure mode from this session. Your job is purely diagnostic: run it against the provided test questions, inspect the actual retrieved chunks for each, and record your diagnosis (which failure mode, and your evidence for it) in `diagnosis_worksheet.py`. You are not asked to fix the bugs — only to correctly name what's wrong and show the retrieval-level evidence that proves it. Full instructions: [`codebase/exercises/week-03/session-3.5/`](../../codebase/exercises/week-03/session-3.5/).

## Pro path — extended challenge

For the retrieval-miss case specifically, don't just confirm the correct chunk is absent from the top-k — look at what *did* get retrieved instead, and check whether any of those chunks contain a surface-level word overlap with the query that explains why they outranked the actually-correct chunk. Real retrieval misses are rarely "nothing relevant came back" — they're usually "something plausible-looking but wrong came back instead," and learning to spot the specific shared vocabulary that caused the confusion is a sharper diagnostic skill than just confirming absence.

## What's next

Session 3.6 — **Week 3 Lab: Mini Build Day** — building a company policy Q&A bot, integrating everything from this week, with no failure mode handed to you this time. You'll need to apply today's diagnostic instinct yourself, unprompted, the moment something looks off.
