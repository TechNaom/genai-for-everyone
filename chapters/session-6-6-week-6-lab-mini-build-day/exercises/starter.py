"""
Session 6.6: Week 6 Lab — Combine service + logging + fallback + regression gate

Run: python3 starter.py
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
    """
    TODO 1: call _call_primary; on ConnectionError, call _call_fallback instead.
    """
    raise NotImplementedError


def run_regression_check() -> bool:
    """
    TODO 2 (Pro path): score GOLDEN_DATASET against call_model_with_fallback
    (a simple substring/keyword check is fine), compute pass rate, print it,
    and return True only if pass rate >= REGRESSION_THRESHOLD.
    """
    raise NotImplementedError


@app.route("/ask", methods=["POST"])
def ask():
    # TODO 3: validate input, call call_model_with_fallback, log the request
    # (input, output, latency) to REQUEST_LOG, return the answer as JSON.
    raise NotImplementedError


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "requests_served": len(REQUEST_LOG)})


if __name__ == "__main__":
    # Pro path: startup-time regression gate — refuse to start if it fails.
    if not run_regression_check():
        print("FATAL: regression check failed at startup. Refusing to start.", file=sys.stderr)
        sys.exit(1)

    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
