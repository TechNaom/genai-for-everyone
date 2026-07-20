"""
Reference solution -- Session 6.4 Project: Feedback Loop + Drift Check

Fully offline: call_llm() is a mock -- no API key, no network calls.

Run:    python3 solution.py
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

GOLDEN_DATASET = [
    {"id": "g1", "input": "vacation days after 2 years", "expected": "18 days"},
    {"id": "g2", "input": "parental leave policy", "expected": "12 weeks paid"},
    {"id": "g3", "input": "remote work policy", "expected": "hybrid, 3 days in office"},
]
KNOWLEDGE_BASE: Dict[str, str] = {item["input"]: item["expected"] for item in GOLDEN_DATASET}

DRIFT_DROP_THRESHOLD = 0.15  # flag if pass rate falls more than 15 points vs. the last check


def call_llm(question: str) -> str:
    """Mock LLM call, grounded in KNOWLEDGE_BASE (stands in for retrieval)."""
    if question in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[question]
    return f"I don't have information about: {question}"


def logged_ask(question: str) -> Dict:
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
    return call_llm(user_input) == expected


@app.route("/ask", methods=["POST"])
def ask():
    body = request.get_json(silent=True) or {}
    question = body.get("question", "").strip()
    if not question:
        return jsonify({"error": "question is required"}), 400
    entry = logged_ask(question)
    return jsonify({"request_id": entry["request_id"], "answer": entry["output"]})


@app.route("/stats", methods=["GET"])
def stats():
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


def _find_request(request_id: str) -> Dict:
    for entry in REQUEST_LOG:
        if entry["request_id"] == request_id:
            return entry
    return None


@app.route("/feedback", methods=["POST"])
def feedback():
    body = request.get_json(silent=True) or {}
    request_id = body.get("request_id")
    thumbs_up = body.get("thumbs_up")

    if not isinstance(request_id, str) or not request_id:
        return jsonify({"error": "request_id (string) is required"}), 400
    if _find_request(request_id) is None:
        return jsonify({"error": f"no logged request with request_id={request_id!r}"}), 400
    if not isinstance(thumbs_up, bool):
        return jsonify({"error": "thumbs_up (true/false) is required"}), 400

    record = {"request_id": request_id, "thumbs_up": thumbs_up}
    FEEDBACK_LOG.append(record)
    return jsonify(record), 200


def check_drift(threshold: float = DRIFT_DROP_THRESHOLD) -> Dict:
    results = [score_fn(item["input"], item["expected"]) for item in GOLDEN_DATASET]
    pass_rate = sum(results) / len(results)

    previous = DRIFT_HISTORY[-1] if DRIFT_HISTORY else None
    DRIFT_HISTORY.append({"timestamp": time.time(), "pass_rate": pass_rate})

    if previous is None:
        return {
            "pass_rate": pass_rate,
            "drifted": False,
            "message": "First run -- baseline recorded, nothing to compare against yet.",
        }

    drop = previous["pass_rate"] - pass_rate
    drifted = drop > threshold
    if drifted:
        message = (
            f"DRIFT DETECTED: pass rate dropped "
            f"{drop * 100:.0f} points since the last check "
            f"({previous['pass_rate']:.0%} -> {pass_rate:.0%})."
        )
    else:
        message = (
            f"No drift. Pass rate {pass_rate:.0%} "
            f"(previous check: {previous['pass_rate']:.0%})."
        )

    return {"pass_rate": pass_rate, "drifted": drifted, "message": message}


@app.route("/drift", methods=["GET"])
def drift():
    return jsonify(check_drift())


@app.route("/simulate-policy-update", methods=["POST"])
def simulate_policy_update():
    """Demo-only: corrupts one KNOWLEDGE_BASE entry to manufacture drift."""
    KNOWLEDGE_BASE["remote work policy"] = "fully remote, no office requirement"
    return jsonify({"message": "Simulated a stale knowledge base entry. Call /drift again."})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
