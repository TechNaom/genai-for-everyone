# Session 1.1: What GenAI Actually Is (and Isn't)

**Week:** 1 — Foundations of GenAI & LLMs
**Format:** Live session + self-paced exercise + quiz
**Reading time:** ~25–30 minutes (this is your first real chapter — take your time with it)

---

## Why this chapter exists

Before you write a single prompt, before you touch an API, before you build anything — you need a model in your head that's actually *correct*. Not "AI is smart computers." Not "AI is going to replace everyone." Something you could explain to a curious 12-year-old and to a skeptical CFO, and have both of them walk away with an accurate picture.

Here's why this matters more than it sounds like it should: almost every bad GenAI project — the ones that get cancelled, the ones that embarrass companies, the ones that waste six months of engineering time — traces back to someone having the *wrong mental model* of what these systems do. They expected a database. They got an improviser. They expected a calculator. They got a poet who's sometimes right about math. The gap between expectation and reality is where projects die.

So this chapter has one job: give you a mental model so solid that you'll catch yourself, three weeks from now, thinking "wait, that's not how this actually works" when someone else gets it wrong. That instinct is worth more than any framework or tool you'll learn later in this program.

---

## Part 1: The Big Split — Predictive AI vs. Generative AI

### Start with a deliberately uncomfortable question

If you asked ten random people on the street "what is AI?", you'd get ten different — and mostly unhelpful — answers. "A robot." "A computer that thinks." "The thing that's going to take everyone's jobs." "Like in the movies." None of these are *exactly* wrong, but none of them tell you anything useful about what to expect when you actually sit down and use one of these tools.

Here's the distinction that will save you more confusion than anything else in this entire 7-week program: **there are really only two fundamentally different jobs that an AI system can be built to do.**

### Job #1: Predictive AI — "Which bucket does this belong in?"

Predictive AI looks at something — a transaction, an email, a photo, a customer's history — and answers a question that has a *fixed, finite set of possible answers*. It's not creating anything new. It's sorting, scoring, or labeling.

Think of predictive AI as an incredibly fast, incredibly well-trained sorting clerk. You hand it something, and it places it into one of a small number of bins, or it gives it a number on a scale.

**Concrete examples, with the actual input and output spelled out:**

| Scenario | Input | Output | Output type |
|---|---|---|---|
| Spam filter | An email's text and metadata | "Spam" or "Not spam" | Binary category |
| Fraud detection | A credit card transaction's details | A fraud-risk score from 0–100 | Continuous score |
| Netflix recommendations | Your watch history + similar users' history | A ranked list of *existing* titles | Ranking from a fixed catalog |
| Loan approval | Income, credit history, debt | "Approve," "Deny," or "Review" | Category from a fixed set |
| Medical imaging | A chest X-ray | "Pneumonia likely" or "Pneumonia unlikely" | Binary category + confidence |

Notice the pattern across every single row: **the output already existed as a possibility before the model ever ran.** A spam filter can never invent a third category nobody thought of. A recommendation engine can't recommend a movie that doesn't exist in its catalog — it can only re-rank what's already there. Predictive AI's entire job is *selection and scoring from a known set of options.*

This is also the oldest, most mature, most boring (in the best way — boring means reliable) form of AI. It's been quietly running in the background of banking, e-commerce, logistics, and healthcare for over a decade. Nobody calls it "AI" in headlines anymore because the novelty wore off years ago — it just became invisible infrastructure, the way electricity stopped being exciting once it was just always there.

### Job #2: Generative AI — "Create something new that fits"

Generative AI does something categorically different: it produces *new content that did not exist in any fixed list beforehand.* Text, images, audio, code — the output is assembled fresh, token by token (or pixel by pixel, or note by note), based on patterns the model learned during training.

**Concrete examples, same format:**

| Scenario | Input | Output | Why it's generative |
|---|---|---|---|
| Drafting an email | "Write a polite follow-up to a client who hasn't responded in 2 weeks" | A full email, freshly composed | The exact wording never existed before this moment |
| Code generation | "Write a Python function to validate email addresses" | Working code | The specific code is assembled new each time |
| Image creation | "A lighthouse at sunset, watercolor style" | A newly rendered image | No such image existed in any database to retrieve |
| Summarization | A 40-message support thread | A 3-bullet summary | The summary's exact phrasing is newly generated, not copy-pasted |
| Translation | A paragraph in English | The same meaning, in Japanese | The Japanese sentence structure is generated fresh, not looked up word-by-word |

This is the kind of AI that triggered the explosion of public interest starting around 2022–2023 (ChatGPT, Midjourney, and what followed). It's also the primary focus of this entire program — but understanding it *requires* understanding what it's not, which is predictive AI's job of picking from a known menu.

### The single sentence that separates them

If you remember nothing else from this section, remember this:

> **Predictive AI chooses from what already exists. Generative AI creates what didn't exist a moment ago.**

This sentence will help you instantly in your career. When a manager says "let's add AI to X," your very first move — before you write any code — is to figure out which of these two jobs they're actually describing. Often *they* don't know. Half of being good at this job is asking the clarifying question that surfaces that ambiguity before it becomes a wasted sprint.

---

## Part 2: How Generative AI (Specifically LLMs) Actually Works

You don't need to understand the underlying math to use these tools well — we're deliberately not going near calculus or linear algebra in Week 1. But you do need an accurate, intuitive picture of the *mechanism*, because that mechanism explains almost every quirk, strength, and failure you'll encounter for the rest of this program.

### The analogy: autocomplete, but extraordinarily scaled up

You've used predictive text on your phone keyboard. You start typing a sentence, and your phone suggests the next word.

Type: *"I'll see you at the"* — and your keyboard might suggest "store," "park," or "office."

This is a tiny, weak version of exactly the mechanism that powers ChatGPT, Claude, and every other large language model (LLM). Seriously — same underlying idea. Let's compare them side by side so you can see exactly where the "scaling up" happens.

| | Your phone's autocomplete | A large language model |
|---|---|---|
| **Context it looks at** | The last 2–3 words you typed | The *entire* conversation — potentially tens of thousands of words |
| **Vocabulary it picks from** | A few thousand common words | ~100,000+ "tokens" (words and word-pieces) |
| **What it learned from** | A relatively small dataset of common phrases | A vast slice of human-written text — books, articles, code, conversations, websites |
| **What it can produce** | One or two plausible next words | Coherent paragraphs, working code, structured arguments, multi-step explanations |
| **How it decides** | Simple statistical pattern matching | The same fundamental idea — predicting the most statistically plausible next token — but learned through a vastly more sophisticated process |

The mechanism, underneath everything, is: **given everything that came before, predict what comes next — one small piece at a time.** The model does this once, gets a result, appends it to what it has so far, and does it again. And again. Thousands of times per response, each time conditioning on everything generated so far. That iterative process is *why* a response can stay coherent across paragraphs — it's not planning the whole essay in advance; it's building it one token at a time, each token informed by everything before it.

### Why this single fact explains almost everything else you'll learn

Once this mechanism clicks, a huge number of "weird" LLM behaviors stop being weird and start being *predictable*:

- **Why models hallucinate** (Session 1.5, later this week): if there's no real fact retrieval happening — just statistical pattern continuation — then a model can produce a wildly confident, fluent, *completely false* sentence, because fluency and factual accuracy are two entirely separate properties. The model isn't "lying"; it's continuing a pattern, and sometimes the most statistically plausible continuation is wrong.
- **Why longer context helps**: more context means more signal for predicting what should come next, which is why giving an LLM relevant background information (Week 2's prompting techniques, Week 3's RAG) dramatically improves output quality.
- **Why models are sensitive to how you phrase things**: since the model is predicting based on patterns in its training data, the *way* you phrase a request shifts which patterns get activated, which is the entire premise behind prompt engineering (all of Week 2).
- **Why models can write code, poetry, and legal summaries with the same underlying mechanism**: it's all just "predict the next token" — applied to a training set broad enough to include code repositories, poetry anthologies, and legal documents alike.

### An important, honest caveat

Whether this "predict the next token" mechanism constitutes real understanding, reasoning, or anything resembling human cognition is a genuinely open question — among AI researchers, philosophers, and the people who build these systems. We're not going to resolve that debate in Week 1 (or possibly ever). What we *can* say with confidence, and what matters for using these tools well, is purely behavioral: **the model's confidence in its own output is not a reliable signal of that output's correctness.** That's true regardless of how the philosophical debate eventually settles, and it's the operating principle you should carry through this entire program.

---

## Part 3: Three Myths That Cause Real Problems

These aren't abstract misunderstandings — each one has caused actual, costly mistakes in real companies. Let's take them one at a time.

### Myth #1: "It looked that fact up."

**The myth:** When an LLM states a fact — a date, a statistic, a citation — it found that fact somewhere, the way a search engine would.

**The reality:** Unless the model has been explicitly given a tool to search the web or a database (which we'll build ourselves in Week 4), it is not looking anything up in the moment you ask. It is generating the most statistically plausible continuation of text, based on patterns absorbed during training. Sometimes that continuation happens to be factually correct (often it is, especially for well-known facts that appeared frequently in training data). Sometimes it isn't — and the model has no internal alarm bell that goes off when it's about to say something false, because from the model's "perspective" (a loose word here, deliberately), generating a false-but-fluent sentence and a true-but-fluent sentence feel identical.

**Why this matters practically:** this is the entire root cause of *hallucination* — confidently stated, fluent, wrong information. You'll get a full session on this Thursday (Session 1.5), but the seed of the explanation is right here: no retrieval happened, so there was never a fact-check step to begin with.

### Myth #2: "It's reasoning, just like a human would."

**The myth:** When a model writes out a step-by-step explanation — "First, I'll consider X. Then, given Y, it follows that Z" — it's performing the same kind of internal reasoning process a human would.

**The reality:** The model is producing text that *resembles* reasoning, because step-by-step reasoning patterns appeared abundantly in its training data (math textbooks, tutoring transcripts, technical explanations). Whether something resembling actual reasoning happens "underneath" — in whatever sense that phrase even means for a system like this — is genuinely unresolved, even among the researchers who build these models.

**The practical takeaway, which matters far more than the philosophical question:** the *tone* of confidence in a model's explanation tells you nothing reliable about whether the conclusion is correct. A model can produce a beautifully structured, perfectly confident, entirely wrong chain of reasoning. Don't let polished presentation substitute for verification — this becomes a major theme again in Week 5 (Evaluation & Safety).

### Myth #3: "AI is one single thing."

**The myth:** "AI" refers to one technology, one capability, one kind of system.

**The reality:** "AI" is an umbrella term stretched across wildly different systems: predictive classifiers, recommendation engines, generative text/image/audio models, computer vision systems, robotics control systems, and more. They have different architectures, different training methods, different failure modes, and are suited to entirely different problems.

**Why this matters practically:** when someone in a meeting says "let's use AI for this," that sentence is, by itself, almost meaningless. It could mean four or five completely different engineering projects. The single highest-value habit you can build in this entire career is pausing on that sentence and asking: *which specific kind of AI problem is this, actually?*

---

## Part 4: A Real-World Scenario, Worked Through

Let's make this concrete with a situation you will absolutely encounter in a real job.

**The setup:** You work at a mid-size retail company. Customer support is drowning — too many tickets, not enough agents. In an all-hands meeting, the VP of Customer Experience says: *"We need to put AI on this. Can your team look into it?"*

That single sentence is hiding at least four genuinely different projects:

1. **An AI that drafts reply suggestions** for human agents to review and send. *(Generative — produces new text from the ticket content.)*
2. **An AI that automatically routes tickets** to the correct team (billing, technical, shipping). *(Predictive — classifies into a fixed set of categories.)*
3. **An AI that predicts which tickets are likely to escalate** into an angry, churn-risk situation, so a senior agent can intervene early. *(Predictive — outputs a risk score.)*
4. **An AI that summarizes long, multi-message ticket threads** into 2-3 sentences so agents don't have to re-read everything. *(Generative — produces new condensed text.)*

Each of these is a different build. Different data requirements. Different evaluation approach (how do you even measure if a "draft reply" is good, versus measuring if a "ticket router" is accurate — these are completely different evaluation problems, which is the entire subject of Week 5). Different rollout risk (a wrong ticket routing is annoying; a wrong escalation prediction could mean a furious customer slips through unnoticed).

**The single highest-leverage move in this entire scenario** is not writing any code. It's going back to the VP and asking: *"When you say 'put AI on this' — are we talking about helping agents respond faster, routing tickets more accurately, catching angry customers before they escalate, or something else? These are different projects with different timelines."*

That question, asked at the right moment, is worth more than a week of engineering work done on the wrong target.

---

## Points to Remember

- **AI splits into two fundamentally different jobs:** predictive AI selects/scores from a fixed set of existing options; generative AI creates new content that didn't exist a moment before.
- **LLMs work by predicting the next most statistically plausible token**, one piece at a time, conditioned on everything that came before — the same core mechanism as your phone's autocomplete, just radically scaled up in context length, vocabulary, and training data.
- **Fluency is not the same as accuracy.** A model's confidence in tone tells you nothing reliable about whether its output is actually correct — this single idea underlies hallucination (1.5), evaluation (Week 5), and safety (Week 5) for the rest of this program.
- **"AI" is an umbrella term, not one technology.** Before building anything, identify precisely which kind of AI problem you're actually solving.
- **The most valuable habit you can build this week:** when someone says "let's use AI," pause and ask which specific job — predictive or generative, and doing exactly what — they actually mean.

---

## Quick Check: Fill in the Blanks

Try filling these in from memory before checking the answers — that's the whole point of a recall check.

1. Predictive AI selects from a __________ set of existing options, while generative AI produces __________ content.
2. The core mechanism behind an LLM is predicting the next most statistically __________ token, based on everything that came __________ it.
3. A model's __________ in its own output is not a reliable signal of that output's __________.
4. Your phone's autocomplete looks at only the last __________ words, while an LLM can consider __________ of words of context.
5. The root cause of hallucination is that, unless a model is explicitly using a __________ tool, it never actually __________ a fact — it generates a plausible continuation instead.

**Answers:** 1. fixed/finite, new (or newly-generated) — 2. plausible, before — 3. confidence, correctness — 4. 2–3, thousands — 5. search/retrieval, looked up (or verified)

---

## Quiz and Interview Questions

This chapter's full quiz lives in [`assessments/quizzes/week-01/session-1.1-quiz.md`](../../assessments/quizzes/week-01/session-1.1-quiz.md), and the answer key is in [`assessments/answer-keys/week-01/session-1.1-quiz-answers.md`](../../assessments/answer-keys/week-01/session-1.1-quiz-answers.md).

Interview-style questions for this specific topic (useful for self-testing or mock interviews):

1. *"Explain the difference between predictive and generative AI to someone with no technical background, using an example from everyday life."*
2. *"A non-technical stakeholder says, 'Our chatbot should just know the answer to anything.' How would you respond, and what would you ask them next?"*
3. *"Why can a large language model write a confident, detailed, completely incorrect answer to a factual question? Explain the mechanism, not just the symptom."*
4. *"Give an example of a business problem that sounds like it needs generative AI but is actually better solved with a simpler, non-AI approach."*
5. *"How would you explain 'hallucination' to a product manager who is panicking after seeing a wrong answer from your company's new AI feature?"*

The full Week 1 interview-question set (covering all six sessions) is in [`assessments/interview-questions/week-01-interview-qs.md`](../../assessments/interview-questions/week-01-interview-qs.md).

---

## Core path — guided activity

**The AI Capability Map.** You'll classify 12 real-world scenarios as predictive or generative, describe the input → output relationship, and name a real tool that does each. Full instructions and starter code: [`codebase/exercises/week-01/session-1.1/`](../../codebase/exercises/week-01/session-1.1/).

## Pro path — extended challenge

You're handed three real (anonymized) internal requests like "can we use AI to help with X." For each, you'll determine whether it's genuinely a GenAI problem, a predictive-AI problem, simple automation with no AI needed at all, or too vague to start — and write the one clarifying question you'd ask before doing any work. Instructions in the same exercise folder.

## What's next

Session 1.2 — **How LLMs Work, Without the Math Fear** — goes one level deeper into the mechanism we sketched in Part 2: tokens, embeddings, and what a "context window" really is.
