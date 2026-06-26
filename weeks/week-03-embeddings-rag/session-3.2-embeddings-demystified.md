# Session 3.2 — Embeddings Demystified

## Vector Representations, Semantic Similarity, and Cosine Distance

---

### The librarian who doesn't read English

Picture a librarian working in a library where every book has had its title and cover torn off. She can't read a single word of any language. And yet, somehow, she's astonishingly good at her job: hand her any book, and she'll correctly shelve it near other books about similar topics. Cooking books end up together. So do mysteries, gardening guides, and books about the French Revolution. Ask her to find "something like this book about volcanoes," and she'll walk straight to a shelf of books about earthquakes and tectonic plates — not because she read the word "volcano," but because of something else entirely: the books *feel* alike to her, in some way she can sense but not name in words.

How? She's not reading content. She's measuring *shape* — the weight of the book, the texture of the paper, the number of pages, the density of diagrams versus paragraphs, dozens of physical properties she's learned to associate with different subjects after shelving a million books. Two books about volcanoes tend to have a similar shape, even with their covers gone. A cookbook and a physics textbook do not.

This is, almost exactly, what an embedding is. An embedding takes a piece of text — a word, a sentence, a whole paragraph — and converts it into a list of numbers, a **vector**, that captures something about its *meaning*, without "reading" it the way you do. Texts with similar meaning end up with similar-looking vectors. Texts with different meaning end up with vectors that look very different. Once meaning has been converted into numbers this way, something remarkable becomes possible: you can use ordinary math — the same kind you'd use to measure distances between points in space — to find which pieces of text are "close" to each other in meaning. This is the actual mechanism underneath every "find the relevant text" step you learned you'd need in Session 3.1. Today you learn how it works.

---

### From words to numbers: what a vector actually is

Strip away the jargon for a second. A vector, in this context, is just an ordered list of numbers — something like `[0.2, -1.4, 0.8, 0.1, ...]`. Real embedding models produce vectors with hundreds or even thousands of numbers in them, but the *idea* is identical to something far simpler you already know: coordinates.

You know how to plot a point on a 2D graph using two numbers, `(x, y)`. A point at `(2, 3)` is close to a point at `(2.1, 3.2)` and far from a point at `(50, -30)`. An embedding does exactly this, except instead of 2 numbers describing a point in physical space, it uses hundreds of numbers describing a point in *meaning space*. Each number in the vector doesn't correspond to something as clean and human-readable as "x-coordinate" or "y-coordinate" — you can't point at position #47 in the vector and say "that's the 'royalty-ness' score." But across the *whole* vector, the pattern of numbers ends up encoding real semantic properties, learned automatically from massive amounts of text during training, the same general family of process you learned about in Week 1.

Here's the property that makes this genuinely useful, not just a neat trick: **words and sentences with similar meaning end up as nearby points in this high-dimensional space, and words and sentences with different meaning end up far apart.** "The cat sat on the mat" and "A feline rested on the rug" will produce vectors that are close to each other, even though they don't share almost any of the same words — because an embedding model captures *meaning*, not just spelling or vocabulary overlap. Meanwhile, "The cat sat on the mat" and "Quarterly earnings rose 4 percent" will land far apart, because they're about genuinely different things.

This is the single idea the entire rest of RAG is built on top of. Once meaning becomes geometry, *finding relevant information* becomes *finding nearby points* — a problem computers are extremely good at solving quickly, even across millions of candidates.

---

### Why this is a leap beyond matching keywords

It's worth pausing on why this matters, because the alternative — the thing embeddings replace — is more familiar and more limited than people expect.

Before embeddings, "search" mostly meant **keyword matching**: does this document contain the literal words in the query? This works fine when people phrase things the same way the document does, and falls apart the moment they don't. Someone searching a company's internal wiki for "how do I get reimbursed for travel" will get nothing useful from a keyword search if the actual policy document is titled "Expense Submission Procedures" and never uses the word "reimbursed" or "travel" in those exact forms. The *meaning* overlaps almost completely. The *words* barely overlap at all.

Embeddings solve exactly this gap. Because the comparison happens in meaning-space rather than word-space, a query about "getting reimbursed for travel" and a document about "expense submission procedures" can end up as nearby vectors, because they're about closely related concepts — even with close to zero vocabulary overlap. This is why embeddings are the foundational building block beneath modern semantic search and RAG: they let you search by *what something means*, not just *what words it happens to use*.

---

### Measuring "closeness": introducing cosine similarity

So embeddings turn text into points in space, and similar meaning produces nearby points. But "nearby" needs a precise mathematical definition if a computer is going to use it — you can't tell a program "just eyeball which ones look close together" the way you might glance at a 2D scatter plot.

The most common way to measure closeness between two embedding vectors is **cosine similarity**, and the intuition behind it is more approachable than the name suggests. Imagine each vector as an arrow shooting out from the same starting point, in some direction, out into that high-dimensional meaning-space. Cosine similarity asks one specific question: *how similar is the direction these two arrows are pointing in?* — completely ignoring how long either arrow is.

This produces a single number, almost always somewhere between -1 and 1, with very intuitive landmarks:

- **1** means the two vectors point in *exactly* the same direction — maximally similar meaning.
- **0** means the vectors are at a right angle to each other — essentially unrelated.
- **-1** means they point in *completely opposite* directions — maximally dissimilar (this is rare in practice with real text embeddings, but it's the theoretical floor).

In practice, when you compare real sentence embeddings, you'll mostly see values clustered in the upper range — two sentences about completely different topics might land around 0.1–0.3, while two paraphrases of the same idea might land at 0.85–0.95. There's no universal hard cutoff for "similar enough" — what counts as a good match depends on your embedding model and your use case, which is exactly the kind of practical calibration you'll wrestle with in Session 3.3 when you're choosing a top-k retrieval threshold for a real vector store.

Why direction, specifically, and not straight-line distance? Because for text embeddings, the *direction* a vector points in tends to capture meaning far more reliably than its raw length, which can vary for reasons unrelated to semantic content (like sentence length or word frequency quirks). Two ways of saying "I love this restaurant" should be considered highly similar regardless of small differences in vector magnitude — and cosine similarity, by ignoring magnitude entirely and focusing purely on direction, captures exactly that intuition. This is why it's the dominant similarity measure used across nearly every real-world embedding and vector-search system you'll encounter.

---

### A concrete walk-through, by hand

Let's make this fully concrete with numbers small enough to actually compute, rather than leaving "vectors" as an abstract idea. Real embeddings have hundreds of dimensions, but the math works identically in 2 dimensions, where you can actually see it.

Suppose, in some simplified 2D meaning-space, three sentences produced these embeddings:

- "I adopted a puppy" → `(4, 3)`
- "I got a new dog" → `(5, 2)`
- "Stock prices fell sharply" → `(-2, 4)`

Cosine similarity between two vectors `A` and `B` is computed as:

```
cosine_similarity(A, B) = (A · B) / (|A| × |B|)
```

where `A · B` is the dot product (multiply matching components, then add them up) and `|A|`, `|B|` are each vector's length (the square root of the sum of its squared components).

Comparing "I adopted a puppy" `(4, 3)` and "I got a new dog" `(5, 2)`:

- Dot product: `(4 × 5) + (3 × 2) = 20 + 6 = 26`
- Length of `(4, 3)`: `√(16 + 9) = √25 = 5`
- Length of `(5, 2)`: `√(25 + 4) = √29 ≈ 5.39`
- Cosine similarity: `26 / (5 × 5.39) ≈ 26 / 26.93 ≈ 0.97`

That's a very high similarity score — which makes sense, since both sentences are about the same real-world idea (getting a dog), even though they don't share a single word in common.

Now compare "I adopted a puppy" `(4, 3)` and "Stock prices fell sharply" `(-2, 4)`:

- Dot product: `(4 × -2) + (3 × 4) = -8 + 12 = 4`
- Length of `(4, 3)`: `5` (from before)
- Length of `(-2, 4)`: `√(4 + 16) = √20 ≈ 4.47`
- Cosine similarity: `4 / (5 × 4.47) ≈ 4 / 22.36 ≈ 0.18`

A score near zero — these two sentences are about essentially unrelated topics, and the math reflects that directly. You just hand-verified, with arithmetic anyone can check, the exact computation that powers every "find the most relevant document" step in a real RAG system. Sessions 3.3 and 3.4 scale this idea up from 3 sentences in 2 dimensions to thousands of documents in hundreds of dimensions — but the underlying operation, the dot-product-over-magnitudes formula you just computed by hand, doesn't change at all.

---

### What "20 sentences in 2D" is actually showing you

Today's exercise asks you to take 20 real sentences, turn them into embedding-style vectors, and visualize them in 2D. Two things are worth understanding about this *before* you do it, so the result means something rather than just looking like a pretty scatter plot.

First, an honest note about the vectors themselves: a real production embedding model learns its sense of meaning from a staggering amount of text — far more than 20 short sentences could ever provide. Building one from scratch isn't something you'll do today (or, frankly, something almost anyone builds from scratch at all — you'll typically call an existing embedding model, the way you called LLM APIs in Week 1). So today's exercise uses a small, deliberately transparent stand-in: a "concept anchor" score that checks which of a handful of hand-picked topic words appear in each sentence, combined with each sentence's own raw word counts for added texture. You can read every line of how it's built. It is, candidly, a simplification of what a real embedding model does *automatically* — but the geometry it produces, and the math you apply to it, work in exactly the same way a real embedding's geometry would.

Second: real embeddings — toy or production-grade — live in many dimensions, not 2. To draw them on a flat 2D plot at all, you need a **dimensionality reduction** technique (the exercise uses a standard, widely-available one) that tries to preserve relative distances as it flattens many dimensions down into 2 — a bit like trying to flatten a globe into a 2D map. Some distortion is inevitable, exactly the way Greenland looks enormous on a flat world map despite being much smaller in reality. So the 2D plot you produce today is a *useful approximation* of the underlying similarity structure, not a perfectly faithful picture of it.

Watch for **clustering** in your plot: sentences about pets should visually group together, separately from sentences about cooking, finance, or space. With today's toy embedding, that clustering is partly *engineered* — the concept-anchor scores are organized by topic on purpose, since there isn't enough raw text here for topic structure to emerge from word statistics alone (try building vectors from nothing but raw word counts, with no concept anchors, and you'll see this directly: the clustering you'd expect barely appears, because these sentences were written to share almost no literal vocabulary even within a topic). A real production embedding model doesn't need that engineered help — it has *learned*, from enormous amounts of text, which words and concepts relate to each other, so clustering by meaning emerges automatically from text alone, with no human ever telling it "these five sentences are about pets." That automatic emergence — meaning organizing itself into visible structure purely from learned patterns, no labels required — is the real foundation that semantic search and RAG retrieval are built on. Today's exercise lets you see the *shape* of that idea concretely, even though the specific vectors you're plotting got a deliberate hand from the seed list rather than learning topic structure unsupervised.

---

### Where this is headed

You now understand the actual computational substance behind "find the relevant text," which is the load-bearing idea inside every RAG system you'll build from here on. But notice what today's exercise *doesn't* yet do: it doesn't organize a large real-world document collection, it doesn't handle the question of how to split long documents into the right-sized pieces before embedding them, and it doesn't yet retrieve anything in response to a live user question.

Those are exactly the problems Session 3.3 takes on — chunking strategies for breaking documents into sensible pieces, vector databases for storing and searching embeddings efficiently at scale, and top-k retrieval for actually pulling back the most relevant matches to a query. You've built the conceptual engine today. Next session, you put it in a car.
