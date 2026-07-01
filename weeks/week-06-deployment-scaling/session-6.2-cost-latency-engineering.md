# Session 6.2: Cost & Latency Engineering

**Week:** 6 (Deployment Scaling)
**Format:** Live session + self-paced exercise + quiz

## Learning objective

Estimate and reduce the real dollar cost and response time of a GenAI feature, using token economics, caching, model selection, and batching — before a surprise bill or a slow demo forces the issue.

## Concept (shared by everyone)

Every LLM API call has two costs that matter in production: **money** (you pay per token, in and out) and **time** (the user waits for tokens to stream back). Both are controllable, and both are usually ignored until they become a problem — a $4,000 monthly bill, or a chatbot that takes 8 seconds to answer "hello."

### Token economics, in practice

Providers price per million tokens, input and output priced separately (output is usually 3-5x more expensive than input, because generating text costs more compute than reading it). Three levers matter:

1. **Input size.** A RAG pipeline that stuffs 10 retrieved chunks into every prompt when 3 would do is paying for 7 chunks of pure waste, every single request.
2. **Output length.** Asking for "a one-paragraph summary" versus not constraining length at all can be a 5-10x difference in output tokens, and output tokens are the expensive ones.
3. **Model choice.** A smaller/cheaper model correctly handles a large fraction of real traffic (simple classification, short replies); routing only the genuinely hard cases to an expensive model can cut cost dramatically with no quality loss on the easy cases.

### Caching: paying once instead of every time

If many requests share the same prefix (a long system prompt, a large retrieved document, a big set of tool definitions), prompt caching lets you pay full price once and a fraction of the price on repeat calls that reuse that prefix. This is a pure latency *and* cost win with no quality trade-off — always worth checking whether your provider supports it and whether your prompt structure takes advantage of it.

### Batching: trading latency for cost

If a workload doesn't need an instant response — nightly report generation, bulk classification of a backlog — batch APIs process requests asynchronously at a steep discount (often 50%) in exchange for a turnaround measured in minutes-to-hours instead of seconds. Never use this for a live chat interface; always consider it for anything that runs on a schedule.

### The core discipline: measure before you optimize

The single biggest mistake is optimizing before measuring. Before changing anything, know: tokens in and out per request, dollar cost per request, and latency per request, broken down by *where the time goes* (network, model inference, your own processing). Optimizing the wrong 80% wastes effort the same way it does anywhere else in engineering.

## Core path — guided activity

Build a cost calculator that takes a workload description (requests/day, average input/output tokens) and computes daily/monthly cost for a few model options, plus one concrete optimization (e.g., trimming average input tokens, switching model tier) with its cost impact shown side by side. Full instructions: [`codebase/exercises/week-06/session-6.2/`](../../codebase/exercises/week-06/session-6.2/).

## Pro path — extended challenge

Given a realistic mixed workload (some requests need the expensive model, most don't), design and implement a **routing strategy**: cheap model handles requests below a complexity/length threshold, expensive model handles the rest, and your report shows the blended cost versus an "everything goes to the expensive model" baseline.

## Real-world scenario

Your team ships a support chatbot. Week 1 it handles 500 conversations and everyone's thrilled. Month 2, it's handling 50,000 conversations and finance asks why the API bill is $12,000 — nobody modeled cost at scale before shipping. Cost engineering isn't a nice-to-have optimization pass; it's the difference between a project that survives its first real month of traffic and one that gets pulled.

## Key takeaways

- Output tokens are the expensive ones — constrain length deliberately, don't just hope the model is terse.
- Prompt caching turns a repeated large prefix (system prompt, long context) from a recurring cost into a one-time cost.
- Not every request needs your most expensive model — routing by complexity is often the single biggest cost lever available.
- Measure tokens, cost, and latency per request *before* optimizing anything — guessing wastes effort on the wrong fix.

## Quiz

See [`assessments/quizzes/week-06/session-6.2-quiz.md`](../../assessments/quizzes/week-06/session-6.2-quiz.md)

## Slide deck

See `assets/slides/week-06/session-6.2.pptx`
