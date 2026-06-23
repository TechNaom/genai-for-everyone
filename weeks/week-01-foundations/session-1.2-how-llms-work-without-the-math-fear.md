# Session 1.2: How LLMs Work, Without the Math Fear

**Week:** 1 — Foundations of GenAI & LLMs
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes

---

## Why this chapter exists

In Session 1.1, we established that an LLM predicts the next most plausible piece of text, one piece at a time. That was the *what*. This chapter is the *how* — and we're doing it without a single equation.

Here's a promise: by the end of this chapter, you will understand what a "token" is, what an "embedding" is, and what a "context window" is — three words that get thrown around constantly in GenAI conversations, often by people who half-understand them themselves. You'll understand them well enough to explain each one with a clean analogy, and well enough to immediately see *why* certain things you'll do later in this program (counting tokens for cost, hitting context limits, weird tokenization behavior with non-English text) happen the way they do.

This is also the session where a few "huh, that's weird" moments from everyday LLM use finally click into place. Ever wonder why ChatGPT sometimes struggles to count the letters in a word? By the end of this chapter, you'll know exactly why — and it has nothing to do with the model being "bad at counting."

---

## Part 1: Tokens — The Actual Unit an LLM "Reads"

### The misconception to clear up first

Most people assume an LLM reads text the way we do — word by word, or even letter by letter. It doesn't. An LLM breaks text into **tokens**, which are chunks that are sometimes a whole word, sometimes part of a word, and sometimes just punctuation.

### A simple analogy: LEGO bricks, not a smooth clay sculpture

Imagine you wanted to build a sentence the way you'd build something out of LEGO. You don't have an infinite variety of uniquely-shaped pieces — you have a *fixed set* of brick shapes (maybe 100,000 different shapes total), and you build everything by snapping the right sequence of those bricks together.

That's tokenization. The model has a fixed **vocabulary** of around 100,000 possible tokens. Common whole words ("the," "cat," "running") are often single tokens. Less common words get split into smaller pieces. Let's see this directly:

| Text | Likely tokenization (illustrative) | Token count |
|---|---|---|
| "the cat sat" | `the`, ` cat`, ` sat` | 3 |
| "unbelievable" | `un`, `believ`, `able` | 3 |
| "GenAI" | `Gen`, `AI` | 2 |
| "antidisestablishmentarianism" | `ant`, `idis`, `establishment`, `arian`, `ism` | 5 |
| "🎉" | a single emoji token (or sometimes 2–3, depending on the tokenizer) | 1–3 |

Notice: common, everyday words tend to be single tokens because they appeared so frequently in training data that the tokenizer "learned" to treat them as one unit. Rare or made-up words get chopped into smaller, more common sub-pieces, because the tokenizer has never seen that exact whole word often enough to deserve its own token. This is also exactly why **non-English languages often use more tokens for the same sentence** — if the tokenizer's vocabulary was built mostly from English text, languages like Hindi, Japanese, or Arabic get split into smaller, less efficient pieces. This has real, practical consequences once you get to Week 6 (Cost & Latency Engineering) — you're billed per token, so the *same idea* expressed in a different language can cost meaningfully more or less.

### Why this explains the "letter counting" weirdness

Here's a satisfying payoff. People are often baffled when an LLM struggles to answer "how many letters are in the word 'strawberry'?" The model isn't bad at counting — it's that **it never actually sees the individual letters** in the way you do. It sees tokens like `straw` and `berry` (or some similar split). It's trying to reason about letter composition using units that don't map cleanly onto individual letters at all. It's a bit like asking someone to count the bricks in a wall when they can only perceive pre-assembled chunks of 3-4 bricks at a time — doable with effort, but not the natural unit they're working in. Once you know this, the failure stops being mysterious.

---

## Part 2: Embeddings — Turning Words into Math, Intuitively

### The problem embeddings solve

Computers fundamentally work with numbers, not words. So before any of the "next token prediction" magic from Session 1.1 can happen, every token needs to be converted into a list of numbers. That list of numbers is called an **embedding**.

But here's the genuinely clever part, and it's the part worth really sitting with: **these aren't arbitrary numbers.** They're constructed (during training) so that words with similar *meaning* end up with similar numbers — specifically, end up close to each other in a very high-dimensional space.

### The analogy: a map of meaning, not geography

Imagine a map — but instead of plotting cities by their physical location, you're plotting *words* by their meaning. On this map:

- "king" and "queen" would land near each other (both royalty-related)
- "dog" and "puppy" would land very close together (closely related meaning)
- "dog" and "astronomy" would land far apart (unrelated concepts)
- "happy" and "joyful" would practically overlap
- "happy" and "miserable" would land in a meaningfully different — though not necessarily "opposite corner of the map" — direction, since they share emotional context even while differing in valence

A real embedding isn't a 2D map like this — it's typically hundreds or even thousands of dimensions — but the *idea* is identical: **words and concepts that mean similar things end up mathematically close together.** This is what lets a model "know" that "physician" and "doctor" are related without anyone explicitly programming that rule in. It learned it from seeing those words used in similar contexts millions of times across its training data.

### A famous, genuinely delightful example

One of the classic illustrations of embeddings capturing real meaning: if you take the embedding for "king," mathematically subtract the embedding for "man," and add the embedding for "woman" — you land very close to the embedding for "queen." The model never explicitly learned "queen = king - man + woman" as a rule. That relationship *emerged* purely from the patterns in how those words get used across enormous amounts of text. This single example is why embeddings felt like genuine magic when researchers first demonstrated it clearly, and it's worth pausing on, because it's the clearest illustration that these numbers are capturing something real about meaning and relationships — not just arbitrary IDs.

### Where you'll actually use this hands-on

This isn't just theory for this session — embeddings are the literal foundation of RAG (Retrieval-Augmented Generation), which is the entire subject of Week 3. When we build a system that finds "the most relevant document chunk for this question," what's actually happening under the hood is: convert the question to an embedding, convert all the document chunks to embeddings, and find which chunks are mathematically *closest* to the question's embedding. Everything in Week 3 builds directly on the intuition you're forming right now.

---

## Part 3: Context Windows — The Model's Working Memory

### The analogy: a desk, not a filing cabinet

Imagine you're working at a desk, and you can only have so many papers spread out in front of you at once. You can't access anything that isn't physically on the desk right now — even if it's in a filing cabinet in the next room, you'd have to go get it and bring it back to the desk before you could use it.

A **context window** is the model's desk. It's the maximum amount of text — measured in tokens, not words — that the model can "see" and consider at once when generating a response. Everything outside that window simply isn't visible to the model in that moment, the same way a paper in the filing cabinet isn't visible to you while you're working at your desk.

### Why this matters more than people expect

Context windows have grown enormously over the past few years — from a few thousand tokens in early models to context windows that can hold hundreds of thousands of tokens (an entire book's worth of text) in modern systems. But a bigger desk doesn't mean every paper on it gets equal attention. Practically:

- **Long conversations eventually "forget" early details** — not because the model has bad memory in a human sense, but because once a conversation exceeds the context window, the earliest parts genuinely fall off the desk and are no longer visible at all.
- **Stuffing irrelevant information into the context window can actually hurt quality** — even when there's technically room for it. This is a real phenomenon often called "context rot" or the "lost in the middle" problem: information buried in the middle of a very long context tends to get less effective attention than information near the beginning or end. You'll see this concretely in Week 3, Session 3.5 (RAG Failure Modes), when we look at what happens when you retrieve too many or poorly-chosen document chunks.
- **This is why prompt engineering (all of Week 2) matters so much** — what you choose to put on the desk, and how you arrange it, directly shapes the quality of what the model can produce. A cluttered, poorly organized desk produces worse work even from a brilliant person; the same is true here.

---

## Part 4: Putting the Three Pieces Together

Let's walk through, end to end, what actually happens when you type a message to an LLM:

1. **Your text gets tokenized.** "What's the capital of France?" gets broken into a sequence of tokens — maybe something like `What`, `'s`, ` the`, ` capital`, ` of`, ` France`, `?` (the exact split depends on the specific tokenizer).

2. **Each token gets converted into an embedding** — a long list of numbers capturing something about that token's meaning, informed by everything the model learned during training.

3. **All of those embeddings, together, fit within the context window** — alongside the entire conversation history, any system instructions, and anything else included in the request.

4. **The model predicts the next token** — using everything currently in the context window as the basis for that prediction, exactly as we covered in Session 1.1.

5. **That predicted token gets added to the sequence, and the process repeats** — token by token, until the model produces a special "stop" signal or hits a length limit.

Every single LLM response you've ever seen, no matter how impressive, is this five-step loop running over and over. There's no separate "thinking" step hidden somewhere else — the entire process is right here, and now you understand every piece of it.

---

## Points to Remember

- **Tokens are the actual unit an LLM processes** — not words, not letters. Common words are often single tokens; rare words get split into smaller sub-word pieces. This is also why some languages use more tokens (and cost more) than others for equivalent meaning.
- **Embeddings convert tokens into numbers that capture meaning** — words with similar meanings end up mathematically close together. This is learned from patterns in training data, not explicitly programmed.
- **A context window is the model's "desk"** — the maximum text it can consider at once. Information outside it is invisible; information buried in the middle of a very long context can get less effective attention than information near the edges.
- **The full response-generation loop is: tokenize → embed → consider everything in the context window → predict next token → repeat.** There's no hidden extra "thinking" step beyond this loop.
- **This explains real, observable behaviors** you've probably already noticed: letter-counting struggles, conversations "forgetting" early details, and why crowding a prompt with irrelevant context can hurt rather than help.

---

## Quick Check: Fill in the Blanks

1. An LLM doesn't process whole words directly — it processes __________, which are sometimes a full word and sometimes just a __________.
2. Words with similar meanings end up __________ to each other in embedding space, because of patterns learned from __________ data.
3. The famous embedding example shows that king minus man plus woman lands close to the embedding for __________.
4. A context window is best thought of as the model's __________ — information outside it is simply not __________ to the model.
5. Information buried in the __________ of a very long context window can receive less effective attention than information near the edges — a phenomenon sometimes called "__________."

**Answers:** 1. tokens, sub-word piece — 2. close (or mathematically close), training — 3. queen — 4. desk (or working memory), visible — 5. middle, lost in the middle (or context rot)

---

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-01/session-1.2-quiz.md`](../../assessments/quizzes/week-01/session-1.2-quiz.md) · Answer key: [`assessments/answer-keys/week-01/session-1.2-quiz-answers.md`](../../assessments/answer-keys/week-01/session-1.2-quiz-answers.md)

Interview-style questions for this topic:

1. *"Explain what a token is, and why an LLM might use more tokens to process the same sentence in Japanese versus English."*
2. *"A junior teammate asks why ChatGPT can't reliably count the number of 'r's in a long word. What's the actual technical reason?"*
3. *"Explain embeddings to a non-technical stakeholder using an analogy that doesn't involve any math."*
4. *"What is a context window, and what practical problems can arise from a conversation exceeding it?"*
5. *"Why might stuffing more information into a prompt sometimes make the output worse rather than better?"*

---

## Core path — guided activity

**Tokenizer Playground.** Using a free, open tokenizer tool, you'll feed in different sentences — including some in non-English languages and some made-up words — and observe exactly how they get split into tokens. You'll predict the token count *before* running it, then check your intuition. Full instructions: [`codebase/exercises/week-01/session-1.2/`](../../codebase/exercises/week-01/session-1.2/).

## Pro path — extended challenge

You'll write a small Python script that compares token counts across English, Hindi, and a programming language (Python code) for sentences expressing the *same idea*, then calculate the relative cost difference if billed at a standard per-token rate. This makes the "non-English costs more" idea from Part 1 concrete and quantified — directly previewing Week 6's cost engineering work.

## What's next

Session 1.3 — **The GenAI Landscape** — takes a step back from mechanism and looks at the broader ecosystem: model families, open vs. closed models, and how to choose the right one for a given task.
