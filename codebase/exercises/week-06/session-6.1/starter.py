"""
Session 6.1: Core Path — Wrap an LLM call in a Flask service.

Run: python3 starter.py
Test: curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" \
        -d '{"question": "What is RAG?"}'
"""

import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# TODO 1: read the model name from an environment variable, with a sensible default.
# Do not hard-code the model name directly in call_llm().
MODEL_NAME = None  # TODO


def call_llm(question: str) -> str:
    """Mock LLM call for the free/open path. Swap for a real API call if you like:

    from anthropic import Anthropic
    client = Anthropic()  # reads ANTHROPIC_API_KEY from the environment automatically
    response = client.messages.create(
        model=MODEL_NAME, max_tokens=300,
        messages=[{"role": "user", "content": question}],
    )
    return response.content[0].text
    """
    return f"[{MODEL_NAME}] Mock answer to: {question}"


@app.route("/ask", methods=["POST"])
def ask():
    # TODO 2: get the JSON body, validate that "question" is present and non-empty.
    # If it's missing, return a 400 with a JSON error body — do not let this crash.
    raise NotImplementedError


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
