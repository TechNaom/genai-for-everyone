# Session 3.6 Quiz — Answer Key

1. **B.** Retrieval can now confidently return the wrong *document*, not
   just an imperfect chunk within the right one. With a single source
   document, every retrieved chunk is at least from the "right" place by
   definition — the worst case is an imprecise or overly broad chunk.
   With multiple documents, retrieval can return a confident, high-scoring
   chunk from an entirely wrong document, which is a more dangerous and
   harder-to-spot failure.

2. **B.** Blank-line-based chunking finds only one giant "paragraph" in
   the PDF-extracted text, so the whole multi-section document becomes
   one diluted chunk. PDF text extraction does not reliably preserve the
   blank lines that visually separated sections in the original layout,
   so `re.split(r"\n\s*\n", text)` finds nothing to split on, and the
   entire document collapses into a single oversized chunk regardless of
   the target word count.

3. **Sample answer:** The bug is upstream of `target_words` entirely.
   The chunker only considers splitting into a new chunk once it has
   *another paragraph* to start that new chunk with — but because the
   blank-line split finds just one giant paragraph for the whole
   document, there's no second paragraph available to even try starting
   a new chunk. `target_words` controls *when* to close a chunk once
   you're accumulating paragraphs, but if the paragraph-splitting step
   itself returns only one paragraph, there's nothing for `target_words`
   to act on — so changing it from 80 to 25 (or any other value) doesn't
   change the chunk boundaries at all.

4. **B.** Splitting on the document's numbered section headers, since
   that pattern survives PDF text extraction even when blank lines
   don't. The numbered headers ("1. Eligibility", "2. Remote Work Days",
   etc.) are literal text content, not formatting whitespace, so they
   survive the PDF-to-text conversion intact and can be used as reliable
   split points.

5. **Sample answer:** With multiple source documents, a citation number
   like `[1]` alone doesn't tell a human (or a QA reviewer) *which
   document* the answer is actually grounded in. If a question about VPN
   requirements gets answered with `[1]` and `[1]` is silently from the
   Leave Policy instead of the IT Security Policy, nobody reading the
   raw citation number would catch that without manually cross-checking
   the retrieved chunk text. Adding a human-readable source label (e.g.
   "Source: IT Security Policy") makes a wrong-document retrieval
   immediately visible at a glance, without requiring anyone to dig
   through the underlying chunk text to sanity-check it.

6. **Sample answer:** One real downside: very small chunks lose
   surrounding context that may be necessary to correctly interpret a
   fact. For example, a chunk that just says "up to $500" with no
   surrounding sentence about what it applies to (a home office stipend
   vs. some other reimbursement) becomes ambiguous or even misleading on
   its own. Smaller chunks can also multiply retrieval noise — with many
   tiny, narrowly-scoped chunks, more of them may score similarly for a
   given query, making it harder for the top-k results to reliably
   surface the single best answer. The real takeaway from this lab isn't
   "always go smaller" — it's that chunk size and chunking strategy need
   to match the actual structure of the source document. For these
   PDFs, that means splitting on numbered sections (which happen to
   produce moderately small, topic-coherent chunks), not "always use the
   smallest size possible" as a universal rule applied without
   inspecting what's actually in the documents.
