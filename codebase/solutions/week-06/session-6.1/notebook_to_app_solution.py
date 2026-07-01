"""
Reference solution — Session 6.1: From Notebook to Application

Core path: single /ask endpoint, config from environment variables.
Pro path additions: /health endpoint, fail-fast startup check, proper error codes.

Run: python3 notebook_to_app_solution.py
Test: curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" \
        -d '{"question": "What is RAG?"}'
"""

import os
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_NAME = os.environ.get("MODEL_NAME", "claude-3-5-haiku-20241022")

# Pro path: fail fast at startup if a required config value is missing, rather
# than crashing confusingly on the first real request. For the free/open path
# no key is actually required (call_llm is mocked), but this shows the pattern
# you'd use once you swap in a real API call.
REQUIRE_API_KEY = os.environ.get("REQUIRE_API_KEY", "false").lower() == "true"
if REQUIRE_API_KEY and not os.environ.get("ANTHROPIC_API_KEY"):
    print("FATAL: REQUIRE_API_KEY is set but ANTHROPIC_API_KEY is missing from the environment.", file=sys.stderr)
    sys.exit(1)


def call_llm(question: str) -> str:
    """Mock LLM call. Swap for a real Anthropic call by uncommenting below."""
    # from anthropic import Anthropic
    # client = Anthropic()
    # response = client.messages.create(
    #     model=MODEL_NAME, max_tokens=300,
    #     messages=[{"role": "user", "content": question}],
    # )
    # return response.content[0].text
    return f"[{MODEL_NAME}] Mock answer to: {question}"


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True)
    if not data or not data.get("question"):
        return jsonify({"error": "question is required"}), 400

    question = data["question"]
    answer = call_llm(question)
    return jsonify({"answer": answer})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": MODEL_NAME})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
