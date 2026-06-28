# Session 3.6 — Week 3 Lab: Building a Campus Student Services Q&A Bot

## The question nobody can answer fast

Picture a college sophomore, mid-semester, trying to figure out something urgent: she just dropped a class and fell below full-time enrollment, and she lives in a dorm. Does that put her housing at risk? Does it affect the financial aid she's counting on for next semester? She doesn't know which office to call, doesn't know which of four different PDFs scattered across the university's website actually has the answer, and the people staffing the help desk are juggling forty other students with forty other questions.

This is the scenario behind today's lab, and it's also, not coincidentally, close to the single most common real-world reason organizations build a RAG system in the first place: a question that has a real, correct, document-backed answer — but that answer is buried across more than one document, written by more than one office, on more than one schedule, and nobody wants to make a student (or an employee, or a customer) hunt for it themselves.

Today you build that system. Not a new concept — you've already learned every piece this week. Today is about putting them together, over a genuinely messier set of documents than you've worked with before, and discovering exactly where that extra messiness breaks something you'd otherwise have assumed was solid.

## What you already know, applied to something harder

Quick recap of the arc that gets you here: **3.2** showed you that text becomes a vector, and that similar meaning produces similar vectors. **3.3** showed you how to chunk a document and search those chunks. **3.4** showed you how to hand retrieved chunks to a model with strict citation instructions, so you can verify what it actually used. **3.5** showed you the named ways this breaks — chunking errors, retrieval misses, context stuffing — and how to diagnose each one from its symptom.

Sessions 3.3 and 3.4 deliberately used a single, self-contained document to teach those ideas cleanly. Today's lab does something different on purpose: it gives you **four separate documents** — a Registration Guide, a Financial Aid Handbook, an Academic Standing Policy, and a Housing Handbook — that were clearly written by different offices, at different times, and that genuinely cross-reference each other the way real institutional documents do. The Registration Guide mentions financial aid holds. The Housing Handbook mentions full-time enrollment status. The Academic Standing Policy mentions both financial aid suspension and course load limits. None of this overlap is an accident in the writing — it's exactly how real policy documents actually behave, because the topics genuinely are connected to each other in the real world, even though they live in separate files.

That overlap is precisely what makes multi-document retrieval harder than single-document retrieval. With one document, every retrieved chunk is at least from "the right place" by definition — the worst case is an imprecise match. With four overlapping documents, retrieval can confidently hand back a chunk from the *wrong document entirely*, and that chunk might even look like a strong match, because it touches the right topic in passing without actually containing the right answer.

## The bug you're going to find

Here are the two questions that break things, and they break in the same way for a connected reason:

> "What is the maximum course load for a student on probation?"
> "What happens if I drop below full-time enrollment while living in a dorm?"

The first question's real answer — 13 credit hours — lives in the Academic Standing Policy, under a section called "Academic Probation." The second question's real answer lives in the Housing Handbook, under "Housing Eligibility and Course Load." Both are clearly written, clearly labeled, easy for a human to find.

But if you chunk these documents the way you did in Session 3.3 — splitting on blank lines between paragraphs — both questions get answered from the wrong document. Both retrieve the **Registration Guide** instead, specifically its course-load and enrollment-status sections, which mention "course load" and "full-time" in passing while cross-referencing the Academic Standing Policy and discussing on-campus housing eligibility — without actually containing the specific facts either question is asking about.

Why? The same upstream mechanism you may already be alert to: PDF text extraction does not reliably preserve the blank lines that visually separated sections on the page. The Registration Guide has five sections — Add/Drop Deadlines, Course Load Requirements, Waitlists, Registration Holds, Transfer Credit — and when extracted as text, there's no blank line anywhere between them. A blank-line-based chunker finds exactly one giant "paragraph" for the entire document, and the whole 240-word block becomes a single chunk. Inside that one chunk, words like "course load," "full-time," "financial aid," and "Academic Standing Policy" all appear together — not because that section is actually about probation or housing, but because policy writers naturally cross-reference related topics in passing. That cross-referencing language is exactly what makes the merged chunk score deceptively well against questions that are really about *other* documents.

## Why the earlier fix doesn't just transfer over

If you've worked with a different RAG corpus before today, you might already know a fix for "blank lines don't survive PDF extraction": split on the document's own section headers instead. That instinct is correct — but notice that it isn't a fact about *this specific fix*, it's a fact about *needing a fix that matches your document's structure*. And this corpus's documents don't number their sections. They use headers written in ALL CAPS on their own line — "COURSE LOAD REQUIREMENTS," "ACADEMIC PROBATION," "HOUSING ELIGIBILITY AND COURSE LOAD." A splitting rule built for numbered headers would find nothing to split on here at all.

This is the actual lesson underneath today's lab, stated as plainly as possible: **there is no universal chunking fix, only a universal chunking *principle*** — look at how your real documents are actually structured, and split on whatever pattern reliably survives whatever transformation your text went through to reach you. For numbered documents, that's the numbering. For documents like these, written by people who format with capitalized headers instead, the fix is to split on lines that are entirely uppercase. The code is different. The principle — match your strategy to your actual documents, verified by actually running it, not assumed from a previous success — is identical.

## Multi-document citation labeling, carried forward

Just as in earlier multi-document work, every retrieved chunk in today's pipeline carries a source-document label, surfaced directly in the citation: "[1] (Source: Housing Handbook)," not just "[1]." This is what makes a wrong-document retrieval visible at a glance instead of something you'd only discover by manually re-reading the chunk text behind every citation. If a student asks about dorm eligibility and the answer is grounded in the Registration Guide instead of the Housing Handbook, that mismatch should be obvious the instant you look at the citation — not something a reviewer has to go digging for.

## Points to remember

- Multi-document RAG systems fail in a way single-document systems structurally can't: retrieval can confidently return the *wrong document*, not just an imprecise chunk from the right one.
- Real institutional documents — policies, handbooks, guides — genuinely cross-reference each other, and that overlap is exactly what makes a merged, overly broad chunk look deceptively relevant to questions it can't actually answer.
- PDF text extraction unreliably preserves blank lines between sections, which can silently break blank-line-based chunking regardless of `target_words` — the failure is upstream of chunk size entirely.
- A chunking fix that worked for one document's structure (e.g. numbered sections) does not automatically transfer to a different document's structure (e.g. all-caps headers). The fix has to match the actual document.
- The universal lesson is a *principle*, not a specific regex: inspect how your real documents are structured, and split on whatever survives extraction intact — verified by running it, not assumed from a previous fix that worked elsewhere.
- Source-document labels on every citation make a wrong-document retrieval visible at a glance, rather than something a reviewer has to manually dig for.

## Fill in the blanks

1. Real institutional documents often __________ each other, which is exactly what makes an overly broad, merged chunk look deceptively relevant to questions it can't actually answer.
2. PDF text extraction does not reliably preserve __________ between sections, which can break a blank-line-based chunker no matter what `target_words` is set to.
3. This lab's documents use __________ headers on their own line, instead of numbered headers, which means a numbered-section chunking fix would not work here.
4. The real, transferable lesson of this lab is a __________, not a specific regex: match your chunking strategy to how your actual documents are structured.
5. A __________ label on every citation makes a wrong-document retrieval visible at a glance, rather than requiring a reviewer to manually re-check the chunk text.

*(Answers: 1. cross-reference, 2. blank lines, 3. ALL-CAPS / all-caps, 4. principle, 5. source document / source)*

## Quiz and Interview Questions

Full quiz: [`assessments/quizzes/week-03/session-3.6-quiz.md`](../../assessments/quizzes/week-03/session-3.6-quiz.md) · Answer key: [`assessments/quizzes/week-03/session-3.6-quiz-answers.md`](../../assessments/quizzes/week-03/session-3.6-quiz-answers.md)

Interview-style questions for this topic:

1. "Why can real institutional documents that cross-reference each other be *harder* for retrieval than documents that don't overlap at all?"
2. "You fix a chunking bug for one document type by splitting on numbered headers. A new document type uses different formatting entirely. Walk me through how you'd approach it."
3. "What's the difference between a chunking error and a retrieval miss, and how would you tell which one you're looking at from a wrong answer alone?"
4. "How would you design a multi-document RAG system's citations so a wrong-document retrieval is obvious without reading the model's full answer?"

## Core path — guided activity

**Campus Student Services Q&A Bot.** You'll integrate chunking, embeddings, a multi-document vector store, and citation-grounded generation into a bot that answers student questions over four real campus PDFs, tagging every retrieved chunk with its source document. Full instructions: [`codebase/exercises/week-03/session-3.6/`](../../codebase/exercises/week-03/session-3.6/).

## Pro path — extended challenge

Before reading the solution's diagnosis, find both chunking bugs yourself: run the Core path pipeline against both failing questions and confirm they retrieve the wrong document. Then inspect the actual chunk boundaries for `registration_guide.pdf` — print them out, try a few different `target_words` values, and confirm the boundaries don't move no matter what you set. That's your evidence the bug is upstream of chunk size. Only then look at how the section headers are actually written in the extracted text, and design your own fix before checking it against the reference solution.

## What's next

Week 4 — **Tool Use, Agents & Automation**. You've spent this week teaching a model to *find and use* the right information, even when that information is scattered across documents that don't agree on how to organize themselves. Next week, you'll teach it to *take actions* in the world based on what it finds.
