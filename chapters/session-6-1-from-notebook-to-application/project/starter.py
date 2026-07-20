"""
Session 6.1 Project: Health, Validation & Fail-Fast Startup
See README.md in this folder for the full brief and an example run.

Pro path build for Session 6.1 -- takes the Core path /ask service and makes
it operable: a /health endpoint, real input validation with proper 4xx
errors, and a startup check that fails fast if a required env var is missing.

No real API key is needed to complete this project -- call_llm() stays
mocked. REQUIRE_API_KEY defaults to "false" so the fail-fast check is
inert by default; flip it on to see the startup behavior.

Run: python3 starter.py
Test: curl -X POST http://localhost:5000/ask -H "Content-Type: application/json" \
        -d '{"question": "What is RAG?"}'
Try the fail-fast path: REQUIRE_API_KEY=true python3 starter.py
"""

import os
import sys
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_NAME = os.environ.get("MODEL_NAME", "claude-3-5-haiku-20241022")

# TODO 1: Startup check -- fail fast if a required env var is missing.
#
# If os.environ.get("REQUIRE_API_KEY", "false").lower() == "true" AND
# "ANTHROPIC_API_KEY" is not in os.environ, print a message to stderr in the
# form "FATAL: REQUIRE_API_KEY is set but ANTHROPIC_API_KEY is missing from
# the environment." and exit with sys.exit(1) -- before app.run() ever runs.
#
# REQUIRE_API_KEY = os.environ.get("REQUIRE_API_KEY", "false").lower() == "true"
# if REQUIRE_API_KEY and not os.environ.get("ANTHROPIC_API_KEY"):
#     ...


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
    # TODO 2: real input validation, not just "is it missing".
    #
    # Reject, each with a 400 and a specific "error" message:
    #   - a missing/invalid JSON body
    #   - a missing "question" field
    #   - a "question" that is present but not a string
    #   - a "question" that is a string but empty/whitespace-only
    #
    # data = request.get_json(silent=True)
    # if not data:
    #     return jsonify({"error": "request body must be valid JSON"}), 400
    # question = data.get("question")
    # if question is None:
    #     return jsonify({"error": "question is required"}), 400
    # if not isinstance(question, str):
    #     return jsonify({"error": "question must be a non-empty string"}), 400
    # if not question.strip():
    #     return jsonify({"error": "question must be a non-empty string"}), 400
    raise NotImplementedError


# TODO 3: a /health endpoint.
#
# Add a GET /health route that returns {"status": "ok", "model": MODEL_NAME}
# with a 200. It must NOT call call_llm() or do anything expensive -- it
# should answer "is this process alive" independent of whether the LLM logic
# works.


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
