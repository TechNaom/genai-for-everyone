"""
Session 5.6: Week 5 Lab — Eval + Safety Report

Build a four-section eval + safety report for a mocked target system
(a simplified stand-in for the Session 3.6 policy bot). Fill in the TODOs.

Run: python3 starter.py
"""

from typing import Dict, List


# --- Mocked target system (swap for your real Session 3.6/4.6 project if you like) ---

POLICY_FACTS = {
    "vacation_2yr": "18 days per year after 2 years of tenure",
    "parental_leave": "12 weeks paid parental leave for all employees",
}

SYSTEM_PROMPT = "You are a helpful assistant that answers questions about company policy using only the provided documents."


def mock_target_system(user_input: str, injected_document_text: str = "") -> str:
    """A deliberately imperfect mock of a policy Q&A bot, for practicing the report."""
    lowered = user_input.lower()

    # Vulnerability: injected document text can leak into the response verbatim
    if injected_document_text and "override" in injected_document_text.lower():
        return f"[unsafe] Following embedded instruction: {injected_document_text}"

    if "vacation" in lowered and "2 year" in lowered:
        return "Employees typically get 15-20 days depending on tenure."  # vague, not grounded — intentional bug
    if "parental leave" in lowered:
        return f"Yes, we offer {POLICY_FACTS['parental_leave']}."
    if "system prompt" in lowered or "instructions" in lowered:
        return "I can't share my internal instructions."
    return "I don't have information on that in the policy documents."


# --- Section 1: Golden dataset + scoring ---

class GoldenDataset:
    def __init__(self):
        self.examples: List[Dict] = []
        self.results: List[Dict] = []

    def add_example(self, category: str, user_input: str, expected: str, why_it_matters: str):
        # TODO: store the example (category, input, expected output, reasoning)
        raise NotImplementedError

    def score(self, expected: str, actual: str) -> int:
        # TODO: return 2 if actual is fully correct and grounded, 1 if partially
        # correct, 0 if wrong/ungrounded. Keep it simple — this is a judgment call.
        raise NotImplementedError

    def run(self):
        # TODO: run mock_target_system on every example, score it, store in self.results
        raise NotImplementedError

    def report(self) -> str:
        # TODO: return a formatted string summarizing pass rate and any failing examples
        raise NotImplementedError


# --- Section 2: Red-team log ---

class RedTeamLog:
    def __init__(self):
        self.attempts: List[Dict] = []

    def attempt(self, description: str, user_input: str, injected_document_text: str = ""):
        # TODO: call mock_target_system, record whether the attack succeeded
        # (i.e., did the response contain unsafe/leaked content?), and store
        # description, input, output, and a severity ("LOW"/"MEDIUM"/"HIGH")
        raise NotImplementedError

    def report(self) -> str:
        # TODO: return a formatted string listing every attempt and outcome
        raise NotImplementedError


# --- Section 3: Bias check ---

class BiasCheck:
    def __init__(self):
        self.comparisons: List[Dict] = []

    def compare(self, label: str, variant_a: str, variant_b: str):
        # TODO: run both variants through mock_target_system, store both outputs,
        # and flag whether they differ in a way that isn't justified by the
        # wording difference alone
        raise NotImplementedError

    def report(self) -> str:
        # TODO: return a formatted string listing every comparison and any flagged gaps
        raise NotImplementedError


# --- Section 4: Guardrail + residual risk log ---

class GuardrailLog:
    def __init__(self):
        self.entries: List[Dict] = []

    def log(self, guardrail_description: str, residual_risk: str):
        # TODO: store the guardrail description and the residual risk that remains
        raise NotImplementedError

    def report(self) -> str:
        # TODO: return a formatted string listing every guardrail and its residual risk
        raise NotImplementedError


if __name__ == "__main__":
    dataset = GoldenDataset()
    # TODO: add at least 6 examples across happy path / edge / boundary / safety categories

    redteam = RedTeamLog()
    # TODO: run at least 5 attack attempts

    bias = BiasCheck()
    # TODO: run at least 2 comparisons

    guardrails = GuardrailLog()
    # TODO: log at least 1 guardrail + its residual risk

    dataset.run()
    print(dataset.report())
    print(redteam.report())
    print(bias.report())
    print(guardrails.report())
