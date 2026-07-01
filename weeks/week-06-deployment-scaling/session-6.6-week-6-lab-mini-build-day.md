# Session 6.6: Week 6 Lab — Mini Build Day

**Week:** 6 (Deployment Scaling)
**Format:** Live session + self-paced exercise + quiz

## Learning objective

Combine everything from Week 6 — service wrapper, cost awareness, model fallback, monitoring, and a regression gate — into one deployable project, and produce the artifacts a real team would require before calling it "shipped."

## Concept (shared by everyone)

Five sessions in, you've built each piece separately:
- **6.1:** Wrapped a project as an HTTP service with environment-based config
- **6.2:** Learned to calculate and reduce cost/latency
- **6.3:** Built a provider adapter with a fallback strategy
- **6.4:** Added logging, stats, and a feedback loop
- **6.5:** Built a regression gate that blocks a prompt change if it makes things worse

Today, these combine into one deployable artifact. "Deployable" here doesn't require an actual cloud account — it means: a service that starts with one command, reads its configuration from the environment, logs every request, degrades gracefully if its primary model provider fails, and has a passing regression check before you'd call it done. That is the actual bar most companies mean by "production-ready," regardless of which specific cloud host it eventually runs on.

### What "hosted demo" means for this lab

You don't need a paid cloud account to demonstrate this skill. A hosted demo can be:
- The Flask service from 6.1, running locally, callable via `curl` or a simple browser form — demoed live
- Deployed to a free tier of a platform like Render, Railway, Fly.io, or PythonAnywhere, if you want the "it has a real public URL" experience (all have generous free tiers as of this writing — check current terms before relying on one)

Either way, the artifact that matters for this lab is the same: a project with a clean `README` that lets someone else run `pip install -r requirements.txt`, set a couple of environment variables, and have it working in under 5 minutes. That's the actual definition of "deployable" a hiring manager cares about — not which specific host you happened to use.

## Core path — guided activity

Combine your Session 6.1 service with the Session 6.4 logging/stats and a `/health` endpoint into one project. Write a `DEPLOY.md` describing exactly how someone else would run it (setup, env vars, how to start it, how to verify it's healthy). Full instructions: [`codebase/exercises/week-06/session-6.6/`](../../codebase/exercises/week-06/session-6.6/).

## Pro path — extended challenge

Add the Session 6.3 fallback adapter and the Session 6.5 regression check as a pre-deploy gate: before the service "goes live" (starts accepting real traffic in the exercise's simulation), it runs the regression check against a golden dataset and refuses to start if the check fails — a startup-time safety gate, not just a CI-time one.

## Real-world scenario

A hiring manager says: "Show me something you built end to end." A folder of separate scripts from Weeks 1-5 is a portfolio of exercises. One project with a working service, a README that lets them run it themselves in 5 minutes, visible logging, and a passing eval gate is a demonstration of judgment — the exact difference this whole week has been building toward.

## Key takeaways

- "Deployable" means: one-command startup, config from the environment, logging, graceful degradation, and a passing regression check — not a specific cloud provider.
- A `DEPLOY.md` that lets a stranger run your project in under 5 minutes is itself a real skill worth demonstrating.
- A pre-deploy regression gate (checked at startup, not just in CI) is a stronger safety net than a CI check alone, because it catches bad configuration at the exact moment it would otherwise go live.
- Everything from Week 6 is meant to compose — none of these five sessions were meant to be used in isolation on a real project.

## Quiz

See [`assessments/quizzes/week-06/session-6.6-quiz.md`](../../assessments/quizzes/week-06/session-6.6-quiz.md)

## Slide deck

See `assets/slides/week-06/session-6.6.pptx`
