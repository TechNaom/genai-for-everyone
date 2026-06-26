# Session 3.1 Quiz — Answer Key

---

**1. Answer: C**

The knowledge cutoff is the point in time where the training data snapshot ends. The model can reliably discuss things that were true and well-documented before that date; for anything that depends on what's true *now* — current events, current holders of a role, anything created or changed after the cutoff — the model is working from a frozen snapshot, not live knowledge. It has nothing to do with token limits, refusal behavior, or content filtering.

---

**2. Answer: B**

A language model produces text by predicting the most statistically plausible next tokens given everything before them, including the question itself. When training data on a topic is thin, ambiguous, or absent, the model still has to produce *some* continuation — there's no separate "knowledge confidence meter" wired into the generation process that halts output when certainty is low. The result can be a fully fluent, confidently worded, completely fabricated answer that is mechanically indistinguishable, from the outside, from a correct one. This isn't about deliberate dishonesty, model size, or only happening in creative contexts — it's a structural property of how next-token prediction works.

---

**3. Answer: False**

More frequent retraining narrows the cutoff gap, but it doesn't solve the deeper reason RAG exists: a huge amount of information was *never going to be in a general-purpose model's training data at all*, no matter how recently trained — private company documents, a specific customer's account data, internal records, anything proprietary or freshly created. No retraining schedule, however frequent, puts your company's internal NDA template or a specific employee's sick-day balance into a general-purpose model's weights. RAG addresses that structural gap, not just the time-lag gap.

---

**4. Sample answer:**

A model's confidence is just a property of how fluently and assertively it phrases an answer — it comes from the same next-token-prediction process whether the underlying information is rock-solid or completely fabricated. In the consultant analogy, the consultant is just as articulate and certain-sounding when confidently inventing details about a meeting they were never in as they are when accurately summarizing a topic they deeply know. There's no second signal that leaks through to tell you which case you're in — both arrive in the same calm, complete, confident sentences. That's exactly why you can't use "the model sounded sure" as a substitute for actually verifying a factual claim, especially on anything time-sensitive, private, or niche.

---

**5. Answer: C**

This scenario hits two of the three criteria directly: it's time-sensitive (the policy is "updated occasionally," so a frozen training snapshot can't be trusted to reflect the current version) and it benefits heavily from source traceability (a wrong answer about a refund policy has real consequences, so grounding the answer in the actual current policy text matters). World War I causes (A) and a haiku (D) are timeless/creative tasks with no retrieval need. Rewriting a paragraph (B) is a pure transformation task — all needed information is already in the prompt.

---

**6. Sample answer:**

Before reaching for RAG, I'd want to check: (1) Is the chatbot actually missing access to information it would need — i.e., is this really a training-data gap, or could a clearer, better-constrained prompt (Session 2.1) already fix it without adding retrieval infrastructure? (2) Is the "niche technical" information genuinely something a general-purpose model would never reliably know (private, very obscure, or post-cutoff), or is it actually fairly well-documented public knowledge that the model should know, in which case the bug might be in *how* the question is being asked, not in what the model knows? Jumping straight to "add RAG" without checking these first risks building real retrieval infrastructure — with its own latency, chunking, and failure-mode complexity — to fix a problem that a better prompt could have solved directly, which is exactly the "wrong layer" mistake the session warned about.
