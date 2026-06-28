# Session 3.6 Quiz — Week 3 Lab: Campus Student Services Q&A Bot

1. (Multiple choice) Why does retrieval over four cross-referencing campus documents introduce a failure mode that a single-document system doesn't have?

   A. Cosine similarity cannot be computed when there is more than one document
   B. Retrieval can confidently return a chunk from the *wrong document entirely*, not just an imprecise chunk from the right one
   C. PDFs cannot be loaded into the same Python program as each other
   D. Vector stores have a hard limit of one document per store

2. (Multiple choice) What is the root cause of this lab's chunking bug?

   A. The PDF files are corrupted and cannot be read at all
   B. Blank-line-based chunking merges an entire multi-section document into one diluted chunk, because PDF text extraction doesn't reliably preserve blank lines between sections
   C. Cosine similarity cannot handle questions phrased as "what happens if"
   D. The vector store only stores the first chunk of each document

3. (Short answer) A teammate suggests reusing the exact same "split on numbered headers" fix that worked on a different document set. Explain why that fix might not work on this lab's documents, and what you'd check before assuming any fix transfers.

4. (Multiple choice) What pattern does the actual fix in this lab split on?

   A. Blank lines, but with a smaller target word count
   B. Lines that are entirely uppercase, since that's how this corpus's section headers are written
   C. The word "Section" appearing anywhere in the text
   D. Page breaks in the original PDF

5. (Short answer) Why does the merged Registration Guide chunk score deceptively well against questions about academic probation and housing eligibility, even though it isn't the right answer to either one?

6. (Short answer) What is the actual transferable lesson of this lab — not the specific regex used, but the underlying principle? Explain it in your own words.
