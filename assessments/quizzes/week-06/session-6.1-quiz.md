# Quiz — Session 6.1: From Notebook to Application

_5-8 questions, mixed format. Answer key in `assessments/answer-keys/`._

1. What are the three changes that turn a one-off script into a callable service? Name them.
2. Why should a model name or API key be read from an environment variable instead of hard-coded?

A) It makes the code shorter
B) It lets the same code run with different config/secrets in different environments without a code change
C) Environment variables are faster than string literals
D) It's required by the Python language

3. Your Flask route crashes with a raw Python stack trace when a client sends a request with no `question` field. What should happen instead?
4. True or False: Wrapping an existing `call_llm()` function in a Flask route requires rewriting the GenAI logic itself.
5. What's the risk of printing the value of an API key to the server logs for "debugging," and what should you do instead?
6. **Scenario:** Your service works fine locally but crashes on the deployed server with `KeyError: 'ANTHROPIC_API_KEY'` on the very first request. What's the better failure mode, and why?
7. Why is a dedicated `/health` endpoint useful for a deployed service, separate from the actual functional endpoint(s)?
