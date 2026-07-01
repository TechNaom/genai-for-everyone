# Session 6.1: From Notebook to Application

**Week:** 6 (Deployment Scaling)
**Format:** Live session + self-paced exercise + quiz

## Learning objective

Turn a script or notebook that calls an LLM into a small, real HTTP service: a proper entry point, environment-based configuration, and secrets that never touch source control.

## Concept (shared by everyone)

Every project so far in this program has run the same way: you execute a Python file top to bottom, and it prints a result. That's fine for learning, and it's how most GenAI prototypes are actually built. But nobody using your product runs `python my_script.py` themselves — they hit a URL, or tap a button in an app, and something on a server handles the request.

The gap between "a script that works on my machine" and "a service other people can call" is smaller than it looks, and it comes down to three changes:

1. **An entry point that accepts requests, not just runs once.** Instead of `if __name__ == "__main__":` running your logic once and exiting, you wrap the logic in a function that a web framework calls every time a request comes in.
2. **Configuration that isn't hard-coded.** Your model name, temperature, and any tunable values should be read from environment variables or a config file — not typed directly into the code — so you can change behavior without redeploying.
3. **Secrets that live outside the code.** Your API key was probably sitting in a variable or a `.env` file you load locally. In a real service, that same `.env` pattern extends to how the *deployed* service gets its secrets — read from the environment, never committed, never printed in logs.

None of this requires new AI concepts. It's plain software engineering, applied to the GenAI project you already built. That's exactly why most GenAI courses skip it — and exactly why it matters for actually getting hired to build this stuff.

### The shape of a minimal service

```python
from flask import Flask, request, jsonify
import os

app = Flask(__name__)
MODEL_NAME = os.environ.get("MODEL_NAME", "claude-3-5-haiku-20241022")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "question is required"}), 400
    answer = call_llm(question)  # your existing logic, unchanged
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(port=int(os.environ.get("PORT", 5000)))
```

Notice what didn't change: `call_llm()` is the same function you already wrote in Week 1-5. Wrapping it in a route doesn't touch the GenAI logic at all — it just gives the outside world a way to call it.

### Why environment variables, specifically

A hard-coded API key or model name means every change requires editing code and redeploying. An environment variable means you can point the exact same code at a different model, a different rate limit, or a staging vs. production API key just by changing how the process is started — no code change, no redeploy. This is the single habit that separates "prototype" from "operable service."

## Core path — guided activity

Wrap your Week 3 policy Q&A bot (or Week 4 research agent, or any project from this program) in a minimal Flask service with one `/ask` endpoint. Read the model name and API key from environment variables, never hard-code them. Full instructions: [`codebase/exercises/week-06/session-6.1/`](../../codebase/exercises/week-06/session-6.1/).

## Pro path — extended challenge

Same service, but add: a `/health` endpoint for uptime checks, input validation that returns proper 4xx errors (not a stack trace) for malformed requests, and a startup check that fails fast with a clear error message if a required environment variable is missing — rather than crashing confusingly on the first real request.

## Real-world scenario

A hiring manager asks you to demo your Week 3 RAG project live, over a video call, from your own laptop. If it only runs as `python build_rag_pipeline.py` in a terminal, that's a fine demo. But if you can say "here's the same thing running as a service — let me `curl` it from my phone," you've just demonstrated a materially different skill: the same GenAI knowledge, packaged the way it's actually used at a company.

## Key takeaways

- The AI logic doesn't change when you deploy it — only how it's *invoked* changes, from a script running once to a service handling requests.
- Environment variables (not hard-coded values) are what let the same code run correctly in different environments (local, staging, production) with different secrets and settings.
- Fail fast and clearly on missing configuration — a confusing crash on request #1 is worse than a clear startup error.

## Quiz

See [`assessments/quizzes/week-06/session-6.1-quiz.md`](../../assessments/quizzes/week-06/session-6.1-quiz.md)

## Slide deck

See `assets/slides/week-06/session-6.1.pptx`
