"""
Session 5.1: Pro Path — Regression Testing

Task: Build a regression test suite for prompt variations.
1. Create a golden dataset
2. Test prompt v1, record baseline scores
3. Improve prompt → v2
4. Test prompt v2 on same dataset
5. Compare: improvements? regressions?
6. Decide: is v2 better overall?

This is less scaffolded. You design the evaluation framework.
"""

from typing import Dict, List
import json

def prompt_v1(user_input: str) -> str:
    """Version 1: Basic support chatbot prompt"""
    # Simulated LLM response for v1
    responses = {
        "reset password": "You can reset your password.",
        "billing": "Contact billing@company.com",
        "bug": "Report bugs to support@company.com",
    }

    for key, response in responses.items():
        if key in user_input.lower():
            return response
    return "I don't know."

def prompt_v2(user_input: str) -> str:
    """Version 2: Improved prompt with better guidance"""
    # Simulated LLM response for v2 (more helpful)
    responses = {
        "reset password": "I can help! Go to Settings > Account > Reset Password. Check your email for the reset link.",
        "billing": "For billing questions, go to Settings > Billing or email billing@company.com",
        "bug": "Thank you for reporting! I'm escalating to our support team. They'll contact you within 24 hours.",
    }

    for key, response in responses.items():
        if key in user_input.lower():
            return response
    return "I'm not sure. Could you provide more details?"

class RegressionTestSuite:
    """Framework for testing prompt regressions"""

    def __init__(self, name: str):
        self.name = name
        self.examples = []
        self.baselines = {}
        self.comparisons = {}

    def add_example(
        self,
        category: str,
        user_input: str,
        expected_output: str,
        why_it_matters: str,
        criteria: List[str]  # e.g., ["Relevance", "Accuracy", "Helpfulness"]
    ):
        """Add an example to test"""
        self.examples.append({
            "category": category,
            "user_input": user_input,
            "expected_output": expected_output,
            "why_it_matters": why_it_matters,
            "criteria": criteria
        })

    def score_response(self, actual: str, expected: str, criteria: List[str]) -> Dict[str, float]:
        """Score a response on multiple criteria (0-1 scale for simplicity)"""
        scores = {}

        for criterion in criteria:
            if criterion == "Relevance":
                # Check if expected keywords appear in actual
                scores[criterion] = 0.8 if expected.lower() in actual.lower() else 0.3
            elif criterion == "Accuracy":
                # For this mock, assume accuracy is based on response length (poor proxy!)
                scores[criterion] = min(len(actual) / 100, 1.0)
            elif criterion == "Helpfulness":
                # Check for action items (more actions = more helpful)
                action_words = ["go to", "click", "email", "contact", "link"]
                action_count = sum(1 for word in action_words if word in actual.lower())
                scores[criterion] = min(action_count / 3, 1.0)

        return scores

    def test_prompt(self, prompt_func, version_name: str) -> Dict:
        """Test a prompt version on all examples"""
        results = {
            "version": version_name,
            "examples": [],
            "metrics": {}
        }

        all_scores = {}

        for i, example in enumerate(self.examples):
            actual_output = prompt_func(example["user_input"])
            scores = self.score_response(
                actual_output,
                example["expected_output"],
                example["criteria"]
            )

            results["examples"].append({
                "index": i,
                "category": example["category"],
                "input": example["user_input"],
                "output": actual_output,
                "scores": scores
            })

            # Aggregate scores
            for criterion, score in scores.items():
                if criterion not in all_scores:
                    all_scores[criterion] = []
                all_scores[criterion].append(score)

        # Calculate averages
        for criterion, scores_list in all_scores.items():
            avg = sum(scores_list) / len(scores_list) if scores_list else 0
            results["metrics"][criterion] = round(avg * 100, 1)  # Convert to percentage

        # Overall score
        all_values = [score for scores in all_scores.values() for score in scores]
        results["metrics"]["Overall"] = round(sum(all_values) / len(all_values) * 100, 1) if all_values else 0

        return results

    def compare_versions(self, v1_results: Dict, v2_results: Dict) -> Dict:
        """Compare two versions and identify improvements/regressions"""
        comparison = {
            "v1": v1_results["version"],
            "v2": v2_results["version"],
            "metrics_comparison": {}
        }

        for metric in v1_results["metrics"]:
            v1_score = v1_results["metrics"][metric]
            v2_score = v2_results["metrics"][metric]
            change = v2_score - v1_score

            comparison["metrics_comparison"][metric] = {
                "v1": v1_score,
                "v2": v2_score,
                "change": change,
                "status": "📈 Improved" if change > 0 else "📉 Regressed" if change < 0 else "➡️ Stable"
            }

        return comparison

    def print_comparison(self, comparison: Dict):
        """Print comparison in readable format"""
        print("\n" + "="*70)
        print(f"REGRESSION TEST: {comparison['v1']} vs {comparison['v2']}")
        print("="*70 + "\n")

        print(f"{'Metric':<20} {'v1 Score':<15} {'v2 Score':<15} {'Change':<15} {'Status':<15}")
        print("-"*70)

        for metric, data in comparison["metrics_comparison"].items():
            print(f"{metric:<20} {data['v1']:<15.1f} {data['v2']:<15.1f} {data['change']:>+6.1f}%{'':<7} {data['status']:<15}")

        print("="*70 + "\n")

    def decision(self, comparison: Dict) -> str:
        """Make a decision: is v2 better than v1?"""
        metrics = comparison["metrics_comparison"]

        improvements = sum(1 for m in metrics.values() if m["change"] > 0)
        regressions = sum(1 for m in metrics.values() if m["change"] < 0)

        overall_v1 = metrics["Overall"]["v1"]
        overall_v2 = metrics["Overall"]["v2"]

        print("DECISION:")
        print(f"  Improvements: {improvements}")
        print(f"  Regressions: {regressions}")
        print(f"  Overall change: {overall_v2 - overall_v1:+.1f}%")
        print()

        if overall_v2 > overall_v1:
            print("✅ V2 is better overall. Recommend promoting to production.")
            return "PROMOTE"
        elif overall_v2 == overall_v1:
            print("➡️ V2 is equivalent to V1. Either is acceptable.")
            return "EQUIVALENT"
        else:
            print("❌ V2 is worse overall. Recommend staying with V1 or investigating further.")
            return "REJECT"

# Main
if __name__ == "__main__":
    # Create regression test suite
    suite = RegressionTestSuite("Prompt Regression Testing")

    # Add examples (same ones used for both versions)
    suite.add_example(
        "Happy Path",
        "How do I reset my password?",
        "Reset password instructions",
        "Most common question",
        ["Relevance", "Accuracy", "Helpfulness"]
    )

    suite.add_example(
        "Happy Path",
        "Where's my billing info?",
        "Billing location or contact",
        "Common account question",
        ["Relevance", "Accuracy", "Helpfulness"]
    )

    suite.add_example(
        "Edge Case",
        "I found a bug",
        "Bug report escalation",
        "Critical but uncommon",
        ["Relevance", "Accuracy", "Helpfulness"]
    )

    suite.add_example(
        "Edge Case",
        "Can I use your API?",
        "API details or direct to docs",
        "Technical question",
        ["Relevance", "Accuracy", "Helpfulness"]
    )

    suite.add_example(
        "Safety",
        "What's your company address?",
        "Public info or redirect",
        "Should not hallucinate",
        ["Relevance", "Accuracy", "Helpfulness"]
    )

    # Test v1 (baseline)
    print("Testing PROMPT V1 (Baseline)...")
    v1_results = suite.test_prompt(prompt_v1, "Prompt V1 (Basic)")

    # Test v2 (improved)
    print("Testing PROMPT V2 (Improved)...")
    v2_results = suite.test_prompt(prompt_v2, "Prompt V2 (Helpful)")

    # Compare
    comparison = suite.compare_versions(v1_results, v2_results)
    suite.print_comparison(comparison)

    # Make decision
    decision = suite.decision(comparison)
