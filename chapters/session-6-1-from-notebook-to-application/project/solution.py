"""
Session 6.1 Project: Health, Validation & Fail-Fast Startup — reference solution.

Pro path build: adds a /health endpoint, real input validation with proper
4xx errors, and a startup check that fails fast if a required env var is
missing, on top of the Core path /ask service.

Run: python3 solution.py
Test: curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" \
        -d '{"question": "What is RAG?"}'
Try the fail-fast path: REQUIRE_API_KEY=true python3 solution.py
Try it with the key present: REQUIRE_API_KEY=true ANTHROPIC_API_KEY=sk-test python3 solution.py
"""

import os
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_NAME = os.environ.get("MODEL_NAME", "claude-3-5-haiku-20241022")

# Startup check: fail fast and clearly if a required env var is missing,
# rather than crashing confusingly on the first real request. Defaults to
# "false" so this project is fully testable with zero API cost -- call_llm()
# below is mocked either way.
REQUIRE_API_KEY = os.environ.get("REQUIRE_API_KEY", "false").lower() == "true"
if REQUIRE_API_KEY and not os.environ.get("ANTHROPIC_API_KEY"):
    print(
        "FATAL: REQUIRE_API_KEY is set but ANTHROPIC_API_KEY is missing from the environment.",
        file=sys.stderr,
    )
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
    if not data:
        return jsonify({"error": "request body must be valid JSON"}), 400

    question = data.get("question")
    if question is None:
        return jsonify({"error": "question is required"}), 400
    if not isinstance(question, str) or not question.strip():
        return jsonify({"error": "question must be a non-empty string"}), 400

    answer = call_llm(question)
    return jsonify({"answer": answer})


@app.route("/health", methods=["GET"])
def health():
    # Deliberately does not call call_llm() -- infrastructure should be able
    # to check "is this process alive" cheaply, without depending on whether
    # a downstream LLM API is having a bad day.
    return jsonify({"status": "ok", "model": MODEL_NAME})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
