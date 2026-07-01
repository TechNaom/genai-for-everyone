# Session 7.3: Capstone Build Day I

**Week:** 7 (Capstone Career Prep)
**Format:** Live session + self-paced exercise + quiz

## Learning objective

Build a working v1 of your capstone using an MVP-first, milestone-driven approach — so that at the end of this session you have something that runs end to end, even if incomplete, rather than several unfinished pieces.

## Concept (shared by everyone)

The single biggest risk on a build day isn't running out of skill — it's running out of *time with nothing that runs*. The fix is a discipline borrowed directly from real engineering teams: build the thinnest possible end-to-end version first, then layer in depth, rather than perfecting one piece before touching the next.

### MVP-first, not perfect-first

For a RAG-based capstone, "thinnest possible end-to-end version" looks like: hard-code 3 documents, get retrieval-then-generation working with the ugliest possible prompt, and print an answer to the console. That is a complete pipeline, even though every piece of it is crude. Only after that works do you improve chunking, add more documents, improve the prompt, or add a UI. The alternative — perfecting your chunking strategy before you've ever generated a single answer — risks ending the day with a beautiful chunker and nothing that actually answers a question.

### Milestone checkpoints

Break the build into checkpoints with a rough time budget, and treat each checkpoint as a go/no-go decision point, not just a to-do list item:

1. **Checkpoint 1 (≈25% of build time):** Thinnest possible end-to-end pipeline runs, however crude
2. **Checkpoint 2 (≈50%):** Core path functionality from your proposal works on your golden dataset examples
3. **Checkpoint 3 (≈75%):** At least one Week 5 eval pass done (does it actually work, not just "did it run")
4. **Checkpoint 4 (≈100%):** Pro path extension attempted, or scope consciously cut if time ran short

If you're not at Checkpoint 1 by 25% of your time, that's the signal to simplify immediately — cut a feature, hard-code something you meant to make dynamic, use a smaller document set — rather than pushing forward on the original plan and hoping time works out.

### When to ask for help vs. push through

Two failure modes are equally costly on a build day: asking for help on something you could solve in 2 more minutes of debugging, and silently struggling for 40 minutes on something a mentor could unblock in 2. A reasonable rule: if you've been stuck on the *same* specific error for more than 10-15 minutes with no new information, that's the signal to ask — not a sign of failure, but time-management discipline.

## Core path — guided activity

Using your Session 7.1 proposal, build your capstone's thinnest possible end-to-end version first (Checkpoint 1), then work through Checkpoints 2-3 in order. Use the checkpoint tracker script to log your progress and time spent per checkpoint. Full instructions: [`codebase/exercises/week-07/session-7.3/`](../../codebase/exercises/week-07/session-7.3/).

## Pro path — extended challenge

At each checkpoint, before moving to the next, write one sentence justifying *why* you're moving on now rather than polishing further — practicing the scope-discipline judgment call a real engineering lead makes constantly under a deadline.

## Real-world scenario

A team building a demo for a Monday board meeting spends three days perfecting the retrieval quality for one document type, then discovers on Friday afternoon that the generation step, never tested end to end, produces malformed output for their actual use case. An MVP-first approach — thin pipeline working by day one — would have surfaced that problem three days earlier, when there was still time to fix it.

## Key takeaways

- Build the thinnest possible end-to-end pipeline first; only then improve individual pieces — a complete crude system beats a polished incomplete one, every time you're short on time.
- Treat checkpoints as go/no-go decision points: if you're behind schedule at a checkpoint, simplify immediately rather than hoping to catch up later.
- Getting unblocked quickly (asking after 10-15 minutes stuck) is a time-management skill, not a sign you're behind — silently struggling for 40 minutes is the actual failure mode to avoid.
- A capstone v1 that runs end to end, even simplified, is worth more at the end of a build day than several unfinished, individually-impressive pieces.

## Quiz

See [`assessments/quizzes/week-07/session-7.3-quiz.md`](../../assessments/quizzes/week-07/session-7.3-quiz.md)

## Slide deck

See `assets/slides/week-07/session-7.3.pptx`
