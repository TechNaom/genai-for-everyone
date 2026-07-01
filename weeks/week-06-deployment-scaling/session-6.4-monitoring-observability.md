# Session 6.4: Monitoring & Observability

**Week:** 6 (Deployment Scaling)
**Format:** Live session + self-paced exercise + quiz

## Learning objective

Add logging, drift detection, and a user feedback loop to a GenAI service so problems in production are visible instead of invisible.

## Concept (shared by everyone)

Session 5.1-5.2 taught you to evaluate before shipping, against a fixed golden dataset. Monitoring is the same discipline, continued *after* shipping — because real users ask things your golden dataset never anticipated, and a system that scored 95% in testing can quietly degrade in production without a single alert firing, unless you built the visibility in.

### What to log, specifically

For every request to a GenAI feature, logging the following is the minimum bar:
- The prompt/input (redacting anything sensitive — see Session 5.3-5.5's safety lessons; logs are still a data-leak surface)
- The model's output
- Model/version used, token counts, latency, and cost
- Any downstream signal you have: did the user thumbs-up/down it, retry the request, abandon the session?

Without this, "the bot got worse last week" is a feeling, not a fact you can investigate.

### Drift: why a system that never changed can still get worse

Nothing about your code has to change for quality to degrade in production:
- **Input drift:** the questions users actually ask shift over time (new product launches, new policy, new slang) — your golden dataset from Session 5.1 was accurate the day you wrote it, not forever
- **Silent upstream changes:** your provider updates a model version behind an alias you're using, and its behavior shifts slightly
- **Retrieval drift** (for RAG systems): the underlying documents get updated or removed, and retrieval that used to work now returns stale or missing chunks

Monitoring for drift means periodically re-running your golden dataset in production (or a sample of real traffic scored the same way) and watching the trend line, not just checking it once at launch.

### The feedback loop

A simple thumbs-up/thumbs-down button on every response, logged with the input/output pair, is disproportionately valuable: it's the cheapest way to build a stream of real, labeled examples of what's actually failing for actual users — which becomes next month's additions to your golden dataset (closing the loop back to Session 5.1).

## Core path — guided activity

Add structured logging to your Week 6.1 Flask service: every request logs input, output, latency, and token counts to a file (or in-memory list for the exercise) in a consistent format, and a `/stats` endpoint reports aggregate metrics (average latency, total requests, error rate) from the logged data. Full instructions: [`codebase/exercises/week-06/session-6.4/`](../../codebase/exercises/week-06/session-6.4/).

## Pro path — extended challenge

Add a feedback endpoint (`POST /feedback` with a request ID and thumbs up/down) and a simple drift check: re-score a fixed golden dataset against the live service on a schedule (or on demand for the exercise) and flag if the pass rate drops below a threshold compared to the last run.

## Real-world scenario

A support chatbot silently starts giving worse answers after the company's return policy changes, because the RAG index wasn't refreshed. Nobody notices for three weeks — until customer complaints spike and someone finally checks. A basic feedback button and a weekly re-run of the golden dataset would have caught this on day one, not week three.

## Key takeaways

- Log input, output, model/version, tokens, latency, and cost for every request — this is the minimum bar for being able to investigate "did something get worse."
- Systems can degrade without any code changing: input patterns shift, provider models update silently, retrieved documents go stale.
- Re-running your golden dataset periodically in production is how you catch drift instead of just hoping you don't have any.
- A cheap feedback mechanism (thumbs up/down) is one of the highest-value additions to a shipped GenAI feature — it directly feeds your next eval dataset.

## Quiz

See [`assessments/quizzes/week-06/session-6.4-quiz.md`](../../assessments/quizzes/week-06/session-6.4-quiz.md)

## Slide deck

See `assets/slides/week-06/session-6.4.pptx`
