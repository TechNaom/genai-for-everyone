# Answer Key — Session 1.2 Quiz

**1.** B — Tokens can be whole words, sub-word pieces, or punctuation, depending on how common that exact chunk was in training data.

**2.** "The" is an extremely common word that appeared constantly in training data, so it earned its own dedicated token. "Supercalifragilisticexpialidocious" is rare enough that it was never common enough as a whole unit to deserve a single token — so the tokenizer breaks it into smaller, more frequently-seen sub-word pieces instead.

**3.** C. (A, B, and D describe surface-level properties of a word, not the deeper, learned relationship between meaning and numerical representation that embeddings actually capture.)

**4.** A context window is the maximum amount of text (measured in tokens) that a model can consider at once when generating a response. Information that falls outside the context window is not visible to the model at all in that moment — it's effectively "off the desk," even if it was part of the conversation earlier.

**5.** Korean (like many non-English languages) likely tokenizes less efficiently than English with a tokenizer primarily trained on English-heavy data — meaning the same sentence or idea takes more tokens to represent in Korean than in English. Since API pricing is typically per-token, the same conversation can cost more in Korean purely due to tokenization efficiency, not because the content itself is more complex.

**6.** The risk to flag: simply having more documents fit within the context window doesn't guarantee they'll all be used effectively. Information buried in the middle of a very long context can receive less effective attention than information near the beginning or end (the "lost in the middle" effect) — so stuffing in 15 documents could actually produce worse, less focused output than carefully selecting the 2-3 most relevant ones. This previews exactly what Week 3, Session 3.5 (RAG Failure Modes) covers in depth.
