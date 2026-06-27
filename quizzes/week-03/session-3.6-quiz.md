# Session 3.6 Quiz — Week 3 Lab: Company Policy Q&A Bot

1. (Multiple choice) In this lab's policy Q&A bot, why does adding a
   second source document introduce a new failure mode that a single-
   document system (like Session 3.3/3.4's handbook) doesn't have?

   A. More documents always mean more total information, which always
      improves answer quality
   B. Retrieval can now confidently return the wrong *document*, not
      just an imperfect chunk within the right one
   C. Multiple PDFs cannot be loaded by the same Python program
   D. Cosine similarity only works correctly with exactly one source
      document

2. (Multiple choice) The lab's chunking bug causes the system to
   retrieve the wrong document for "What is the home office equipment
   stipend amount?" What is the root cause?

   A. The dollar amount $500 is written in a font the PDF parser can't read
   B. Blank-line-based chunking finds only one giant "paragraph" in the
      PDF-extracted text, so the whole multi-section document becomes one
      diluted chunk
   C. The vector store has a hard limit of 4 chunks per document
   D. Cosine similarity cannot handle numbers in queries

3. (Short answer) Explain, in your own words, why simply lowering
   `target_words` (e.g. from 80 to 25) does NOT fix the chunking bug
   in this lab, even though smaller target word counts usually produce
   smaller chunks.

4. (Multiple choice) What was the actual fix applied to
   `chunk_text_by_section()` to resolve the retrieval bug?

   A. Splitting on blank lines with a smaller target word count
   B. Splitting on the document's numbered section headers, since that
      pattern survives PDF text extraction even when blank lines don't
   C. Removing the word "stipend" from the query before searching
   D. Increasing `k` so more chunks are retrieved

5. (Short answer) Why does the lab add a human-readable "Source:
   <document name>" label to every retrieved chunk in `format_context()`,
   instead of just numbering chunks `[1]`, `[2]`, `[3]` like Session 3.4
   did?

6. (Short answer) A teammate suggests: "Let's just always use the
   smallest possible chunk size everywhere, so we never run into a
   chunking bug like this again." Give one real downside of always
   using very small chunks, and explain why "smaller is always safer"
   is not the right takeaway from this lab.
