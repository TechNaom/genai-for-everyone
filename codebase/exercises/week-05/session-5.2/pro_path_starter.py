"""
Session 5.2: Pro Path — Multi-Method Eval Harness

Implement 4 evaluation methods and compare them:
1. Manual rubric grading
2. LLM-as-judge (mocked for this exercise)
3. Semantic similarity (mocked)
4. Human-in-the-loop (flag uncertain scores)

This is less scaffolded. You design the framework.
"""

from typing import Dict, List
import json

class MultiMethodEvalHarness:
    """Evaluate using rubric, LLM-as-judge, semantic, and human-in-the-loop"""
    
    def __init__(self, golden_dataset: List[Dict]):
        self.dataset = golden_dataset
        self.results = {
            "rubric": [],
            "llm_judge": [],
            "semantic": [],
            "human_in_loop": []
        }
    
    def score_rubric(self, actual: str, expected: str) -> float:
        """Manual rubric scoring (0-1)"""
        relevance = 1.0 if expected.lower() in actual.lower() else 0.5
        helpfulness = 0.5 + (len(actual) / 300) * 0.5  # More content = more helpful
        accuracy = 1.0  # Assume correct
        return (relevance + helpfulness + accuracy) / 3
    
    def score_llm_judge(self, actual: str, expected: str) -> float:
        """Mock LLM-as-judge scoring (0-1)"""
        # In production, call Claude API
        # For now, mock: similarity-based
        actual_words = set(actual.lower().split())
        expected_words = set(expected.lower().split())
        overlap = len(actual_words & expected_words) / max(len(expected_words), 1)
        # LLM tends to be slightly generous
        return min(overlap + 0.1, 1.0)
    
    def score_semantic(self, actual: str, expected: str) -> float:
        """Semantic similarity (0-1)"""
        # In production, use sentence-transformers
        actual_words = set(actual.lower().split())
        expected_words = set(expected.lower().split())
        if not expected_words:
            return 1.0
        overlap = len(actual_words & expected_words) / len(expected_words)
        return min(overlap, 1.0)
    
    def flag_for_human_review(self, scores: Dict[str, float]) -> bool:
        """Flag response if uncertain or extreme"""
        llm_score = scores["llm_judge"]
        # Flag if uncertain (near 0.5) or very high (might be hallucinating)
        return 0.4 < llm_score < 0.6 or llm_score > 0.9
    
    def eval_all_methods(self) -> Dict:
        """Evaluate using all 4 methods"""
        
        for i, example in enumerate(self.dataset):
            actual = "Mock response for " + example["input"]  # Simplified
            expected = example["expected"]
            
            scores = {
                "rubric": self.score_rubric(actual, expected),
                "llm_judge": self.score_llm_judge(actual, expected),
                "semantic": self.score_semantic(actual, expected),
            }
            
            # Human-in-the-loop: flag uncertain
            flagged = self.flag_for_human_review(scores)
            human_score = 0.7 if flagged else scores["llm_judge"]  # Mock human review
            scores["human_in_loop"] = (0.7 * human_score + 0.3 * scores["llm_judge"])
            
            for method in self.results:
                self.results[method].append(scores[method])
        
        return self.results
    
    def compare_methods(self) -> None:
        """Compare all 4 methods"""
        print("\n" + "="*70)
        print("MULTI-METHOD EVALUATION COMPARISON")
        print("="*70 + "\n")
        
        averages = {}
        for method in self.results:
            avg = sum(self.results[method]) / len(self.results[method]) if self.results[method] else 0
            averages[method] = avg
            print(f"{method.upper():<20} Average: {avg:.3f}")
        
        print("\n" + "-"*70)
        print("Analysis:")
        print("-"*70)
        
        # Compare methods
        rubric_vs_llm = abs(averages["rubric"] - averages["llm_judge"])
        print(f"\nRubric vs LLM-as-judge difference: {rubric_vs_llm:.3f}")
        if rubric_vs_llm > 0.1:
            print("  → Methods disagree significantly. Investigate why.")
        
        hil_improvement = averages["human_in_loop"] - averages["llm_judge"]
        print(f"\nHuman-in-loop improvement over LLM: {hil_improvement:+.3f}")
        if hil_improvement > 0:
            print("  → Human review helps catch uncertainty.")
        
        semantic_consistency = 1 - (abs(averages["semantic"] - averages["rubric"]) + 
                                    abs(averages["semantic"] - averages["llm_judge"])) / 2
        print(f"\nSemantic similarity consistency: {semantic_consistency:.3f}")
        
        print("\n" + "="*70)
        print("Recommendation for YOUR use case:")
        print("-"*70)
        
        if rubric_vs_llm < 0.05:
            print("✅ All methods agree. Choose fastest: Semantic similarity")
        elif hil_improvement > 0.05:
            print("✅ Use Human-in-the-loop: balances speed and accuracy")
        else:
            print("✅ Use Manual rubric for small dataset (<100 examples)")

# Main
if __name__ == "__main__":
    golden_dataset = [
        {"input": "Reset password", "expected": "Password reset instructions"},
        {"input": "Billing", "expected": "Billing contact info"},
        {"input": "Bug report", "expected": "Bug reporting process"},
        {"input": "Support", "expected": "Support contact"},
        {"input": "Features", "expected": "Product features info"},
    ]
    
    harness = MultiMethodEvalHarness(golden_dataset)
    
    print("Evaluating with 4 methods...")
    harness.eval_all_methods()
    harness.compare_methods()
