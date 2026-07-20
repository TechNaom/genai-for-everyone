"""
Session 6.1: Core Path — reference solution.

A single /ask endpoint, config read from environment variables, and no
crashes on a malformed request.

Run: python3 solution.py
Test: curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" \
        -d '{"question": "What is RAG?"}'
Test the error path: curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" -d '{}'
"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_NAME = os.environ.get("MODEL_NAME", "claude-3-5-haiku-20241022")


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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
