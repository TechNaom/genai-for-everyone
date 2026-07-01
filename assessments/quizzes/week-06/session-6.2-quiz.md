# Quiz — Session 6.2: Cost & Latency Engineering

_5-8 questions, mixed format. Answer key in `assessments/answer-keys/`._

1. Why are output tokens usually priced higher than input tokens?
2. Your prompt includes a 2,000-token system prompt on every single request, and you make 10,000 requests/day. What technique specifically targets this kind of repeated cost, and how does it help?
3. True or False: Batch APIs are a good fit for a live customer-facing chat interface.
4. **Scenario:** A support chatbot routes every request — from "yes/no" simple questions to complex multi-part troubleshooting — to your most expensive model. What's the first optimization you'd investigate, and why?
5. What are the three numbers you should measure per request *before* attempting any cost or latency optimization?
6. A teammate asks the model for "a summary" with no length constraint and gets back 400 words when 50 would do. Is this a cost issue, a latency issue, or both? Explain.
7. Why is "optimize before you measure" a risky habit specifically for cost/latency work, even for an experienced engineer?
