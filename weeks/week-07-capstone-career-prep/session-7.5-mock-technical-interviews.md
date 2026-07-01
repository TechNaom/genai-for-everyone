# Session 7.5: Mock Technical Interviews

**Week:** 7 (Capstone Career Prep)
**Format:** Live session + self-paced exercise + quiz

## Learning objective

Answer real GenAI interview formats — system design, live problem-solving, and "walk me through your project" — using the vocabulary and judgment built across this entire program, and give/receive structured feedback on interview performance.

## Concept (shared by everyone)

A GenAI interview isn't one format — it's usually a mix of three, and each rewards a different kind of preparation.

### Format 1: "Walk me through a project you built"

This is where your capstone (and your Session 7.1 proposal discipline) pays off directly. A strong answer follows a clear shape: the problem and user (not "I built a RAG thing"), the approach and *why* that approach over alternatives, one specific hard decision or trade-off you made, and how you know it works (your actual success criteria, not "it seemed to work"). Interviewers are listening for judgment, not just that you can list technologies you used.

### Format 2: System design ("design a GenAI feature for X")

These questions are rarely testing whether you know a specific API. They're testing whether you reach for the right *questions* before designing: What's the actual user and problem? Does this need retrieval, or is it a pure prompting problem (Session 3.1's "RAG or not?")? What's the eval plan — how would you know if this design is working (Week 5)? What breaks at scale, and what's the cost model (Week 6)? A candidate who immediately starts describing an architecture without first asking these questions is optimizing for the wrong signal.

### Format 3: Live problem-solving

"Here's a broken prompt/pipeline, fix it" or "here's an eval showing 60% accuracy, diagnose why." This tests the debugging instincts from Sessions 2.1-2.3 and 3.5 directly — reading an example and its failure output for the *pattern* (formatting issue? missing context? wrong retrieval? ambiguous instructions?) rather than guessing at random fixes.

### Giving and receiving feedback well

A mock interview is only useful if the feedback afterward is specific. "That was good" teaches nothing. "You jumped straight to describing your architecture before asking who the user was — that's the first thing a real interviewer would want to hear" is feedback someone can actually act on. When you're the interviewer in a mock session, hold yourself to that same standard.

## Core path — guided activity

Practice a "walk me through your project" answer for your own capstone using the structure above (problem/user, approach + why, one hard trade-off, success criteria), then run it against the self-check script that flags whether each element is present. Full instructions: [`codebase/exercises/week-07/session-7.5/`](../../codebase/exercises/week-07/session-7.5/).

## Pro path — extended challenge

Do a full mock interview with a peer (or self-run using the provided question bank): one system design question and one live-debugging question from the provided sets, timed at 15 minutes each, then write structured feedback for the other person (or yourself) following the "specific, actionable" standard above.

## Real-world scenario

Two candidates both built a similar RAG project. Candidate A describes it as "I used LangChain and a vector database to build a chatbot." Candidate B describes it as "Support agents were spending 12 minutes per ticket searching docs manually; I built a retrieval system over the internal wiki, chose chunking by section rather than fixed-size because the wiki's structure made that more accurate, and validated it against a 15-question golden set before considering it done." Candidate B is describing judgment; Candidate A is describing a tech stack. Interviewers remember the difference.

## Key takeaways

- "Walk me through your project" rewards judgment and trade-offs, not a list of technologies used — lead with the problem and the *why* behind your decisions.
- System design questions are testing whether you ask the right questions first (RAG or not, eval plan, cost/scale) before describing an architecture.
- Live debugging questions test pattern recognition in failures — read the specific symptom before guessing at a fix.
- Feedback is only useful if it's specific and actionable — practice giving feedback you could actually act on, not just "that was good."

## Quiz

See [`assessments/quizzes/week-07/session-7.5-quiz.md`](../../assessments/quizzes/week-07/session-7.5-quiz.md)

## Slide deck

See `assets/slides/week-07/session-7.5.pptx`
