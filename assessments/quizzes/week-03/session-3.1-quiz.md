# Session 3.1 Quiz — Why LLMs Need External Knowledge

*6 questions. Mixed multiple-choice and short-answer.*

---

**1.** What is a model's "knowledge cutoff"?

A) The maximum number of tokens it can process in one request
B) The date after which the model refuses to answer questions
C) The point in time after which no training data was included, so the model has no reliable knowledge of events or facts after that point
D) A safety filter that blocks certain topics

---

**2.** A model confidently states a specific, detailed, but completely fabricated answer to a factual question it doesn't actually have reliable information about. Why doesn't the model instead say "I don't know"?

A) The model is deliberately programmed to lie when convenient
B) The model generates the most statistically plausible continuation of the prompt; it has no built-in mechanism that reliably detects "I lack real knowledge here" and stops
C) The model only hallucinates when explicitly asked to be creative
D) This only happens with older or smaller models

---

**3.** True or False: Retraining a model more frequently, so its knowledge cutoff is always very recent, fully solves the need for retrieval-augmented generation (RAG).

---

**4. Short answer.** Explain, in your own words, why a model's *confidence* in an answer is not a reliable signal of that answer's *accuracy*. Use the consultant analogy or your own example.

---

**5.** Which of the following scenarios is the *strongest* candidate for RAG, based on the three criteria from the session (training-data gap, source traceability, time-sensitivity)?

A) "Explain the causes of World War I."
B) "Rewrite this paragraph to sound friendlier."
C) "What's our current refund policy for orders placed more than 30 days ago?" (where the policy is on a company webpage that's updated occasionally)
D) "Write a haiku about autumn."

---

**6. Short answer.** A teammate says: "Our chatbot keeps giving wrong answers about niche technical questions, so let's add RAG to fix it." Before agreeing, what would you want to know first? Name at least two things you'd want to check, and explain why simply "adding RAG" might not be the right first move.
