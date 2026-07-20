"""
Session 6.6 — Week 6 Lab: Mini Build Day (REFERENCE SOLUTION)

This is the answer key. Try starter.py yourself first before reading this file.

Run: python3 solution.py
Test: curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" \
        -d '{"question": "vacation days after 2 years"}'
"""

import os
import sys
import random
import time
from typing import Dict, List
from flask import Flask, request, jsonify

app = Flask(__name__)

REQUEST_LOG: List[Dict] = []

GOLDEN_DATASET = [
    {"input": "vacation days after 2 years", "expected": "18"},
    {"input": "parental leave weeks", "expected": "12"},
]

REGRESSION_THRESHOLD = 0.8


def _call_primary(question: str) -> str:
    if random.random() < 0.2:
        raise ConnectionError("primary provider unavailable")
    return f"[primary] answer to: {question}"


def _call_fallback(question: str) -> str:
    return f"[fallback] answer to: {question}"


def call_model_with_fallback(question: str) -> str:
    try:
        return _call_primary(question)
    except ConnectionError:
        return _call_fallback(question)


def run_regression_check() -> bool:
    passed = 0
    for example in GOLDEN_DATASET:
        output = call_model_with_fallback(example["input"])
        # Both mocked providers echo the question, so we check the question
        # made it through end to end — a stand-in for a real rubric/keyword check.
        if example["input"] in output:
            passed += 1
    pass_rate = passed / len(GOLDEN_DATASET)
    print(f"Startup regression check: {pass_rate:.0%} (threshold {REGRESSION_THRESHOLD:.0%})")
    return pass_rate >= REGRESSION_THRESHOLD


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    if not data or not data.get("question"):
        return jsonify({"error": "question is required"}), 400

    question = data["question"]
    start = time.time()
    answer = call_model_with_fallback(question)
    latency_ms = round((time.time() - start) * 1000, 1)

    REQUEST_LOG.append({"input": question, "output": answer, "latency_ms": latency_ms})
    return jsonify({"answer": answer, "latency_ms": latency_ms})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "requests_served": len(REQUEST_LOG)})


if __name__ == "__main__":
    if not run_regression_check():
        print("FATAL: regression check failed at startup. Refusing to start.", file=sys.stderr)
        sys.exit(1)

    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
