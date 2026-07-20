"""
Session 6.4 Project (Pro path): Feedback Loop + Drift Check

Extends a small Flask service (same shape as Session 6.1) with:
  - structured request logging + a /stats summary (already wired up for you)
  - POST /feedback  -- log a thumbs up/down against a request ID
  - GET  /drift     -- re-score a golden dataset and flag a pass-rate drop
                        compared to the PREVIOUS drift check, not just a
                        fixed absolute threshold

Fully offline: call_llm() below is a mock -- no API key, no network calls.
A /simulate-policy-update endpoint lets you manufacture drift on demand so
you can watch the /drift check actually catch it.

Run:    python3 starter.py
Test:   curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" \\
          -d '{"question": "remote work policy"}'
        curl -X POST http://localhost:5000/feedback -H "Content-Type: application/json" \\
          -d '{"request_id": "<id from /ask response>", "thumbs_up": true}'
        curl http://localhost:5000/drift
        curl -X POST http://localhost:5000/simulate-policy-update
        curl http://localhost:5000/drift
"""

import os
import time
import uuid
from typing import Dict, List

from flask import Flask, jsonify, request

app = Flask(__name__)

REQUEST_LOG: List[Dict] = []
FEEDBACK_LOG: List[Dict] = []
DRIFT_HISTORY: List[Dict] = []

# A tiny "golden dataset" of known-good question/answer pairs, same shape as
# Week 5's evaluation sets. KNOWLEDGE_BASE stands in for a RAG index: it's
# what call_llm() actually consults to answer.
GOLDEN_DATASET = [
    {"id": "g1", "input": "vacation days after 2 years", "expected": "18 days"},
    {"id": "g2", "input": "parental leave policy", "expected": "12 weeks paid"},
    {"id": "g3", "input": "remote work policy", "expected": "hybrid, 3 days in office"},
]
KNOWLEDGE_BASE: Dict[str, str] = {item["input"]: item["expected"] for item in GOLDEN_DATASET}

DRIFT_DROP_THRESHOLD = 0.15  # flag if pass rate falls more than 15 points vs. the last check


def call_llm(question: str) -> str:
    """Mock LLM call, grounded in KNOWLEDGE_BASE (stands in for retrieval).

    Swap for a real API call if you like:

    from anthropic import Anthropic
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment automatically
    response = client.messages.create(
        model="claude-3-5-haiku-latest", max_tokens=200,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text
    """
    if question in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[question]
    return f"I don't have information about: {question}"


def logged_ask(question: str) -> Dict:
    """Calls call_llm, logs a structured entry, and returns it with a request_id.

    Already implemented -- this is the Core-path pattern from the exercises,
    reused here as the foundation the Pro-path tasks build on.
    """
    start = time.time()
    answer = call_llm(question)
    latency_ms = round((time.time() - start) * 1000, 2)
    entry = {
        "request_id": str(uuid.uuid4()),
        "input": question,
        "output": answer,
        "latency_ms": latency_ms,
        "input_tokens": len(question.split()) * 2,
        "output_tokens": len(answer.split()) * 2,
    }
    REQUEST_LOG.append(entry)
    return entry


def score_fn(user_input: str, expected: str) -> bool:
    """Already implemented: does the live service still return the expected answer?"""
    return call_llm(user_input) == expected


@app.route("/ask", methods=["POST"])
def ask():
    """Already implemented: validates the body, calls logged_ask, returns the result."""
    body = request.get_json(silent=True) or {}
    question = body.get("question", "").strip()
    if not question:
        return jsonify({"error": "question is required"}), 400
    entry = logged_ask(question)
    return jsonify({"request_id": entry["request_id"], "answer": entry["output"]})


@app.route("/stats", methods=["GET"])
def stats():
    """Already implemented: aggregate metrics from REQUEST_LOG."""
    if not REQUEST_LOG:
        return jsonify({"total_requests": 0})
    total = len(REQUEST_LOG)
    avg_latency = sum(r["latency_ms"] for r in REQUEST_LOG) / total
    total_tokens = sum(r["input_tokens"] + r["output_tokens"] for r in REQUEST_LOG)
    return jsonify({
        "total_requests": total,
        "average_latency_ms": round(avg_latency, 2),
        "total_tokens": total_tokens,
    })


@app.route("/feedback", methods=["POST"])
def feedback():
    """
    TODO 1: Read the JSON body. It should contain "request_id" (a string that
    must match a request_id already present in REQUEST_LOG) and "thumbs_up"
    (a bool). If request_id is missing, not a string, or doesn't match any
    logged request, return a 400 with a JSON error body -- do not crash.
    If thumbs_up is missing or not a bool, return a 400 too.
    On success, append {"request_id": ..., "thumbs_up": ...} to FEEDBACK_LOG
    and return the same object with a 200.
    """
    raise NotImplementedError


def check_drift(threshold: float = DRIFT_DROP_THRESHOLD) -> Dict:
    """
    TODO 2: Re-score every item in GOLDEN_DATASET using score_fn(item["input"],
    item["expected"]), and compute pass_rate = passed / total.

    Append a record to DRIFT_HISTORY: {"timestamp": time.time(), "pass_rate": pass_rate}.

    Compare against the PREVIOUS entry in DRIFT_HISTORY (the one before the
    one you just appended), if any:
      - If there is no previous entry, this is the first run -- not drift,
        just a baseline.
      - If there IS a previous entry, compute drop = previous_pass_rate - pass_rate.
        Flag drift (drifted=True) if drop > threshold.

    Return a dict with at least: pass_rate, drifted (bool), and a short
    message explaining the result (e.g. "first run, baseline recorded" or
    "pass rate dropped 33 points since last check").
    """
    raise NotImplementedError


@app.route("/drift", methods=["GET"])
def drift():
    """Already implemented: exposes check_drift() as an on-demand endpoint."""
    return jsonify(check_drift())


@app.route("/simulate-policy-update", methods=["POST"])
def simulate_policy_update():
    """Demo-only: corrupts one KNOWLEDGE_BASE entry to manufacture drift,
    the same way an un-refreshed RAG index would silently go stale after a
    real policy change. Call /drift before and after to see the effect."""
    KNOWLEDGE_BASE["remote work policy"] = "fully remote, no office requirement"
    return jsonify({"message": "Simulated a stale knowledge base entry. Call /drift again."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
