"""
Session 5.2: Core Path — Evaluation Harness

Build an evaluation harness that:
1. Takes 3 prompt variants (v1, v2, v3)
2. Runs each on golden dataset examples
3. Scores using: manual rubric + semantic similarity
4. Compares results: which variant wins?

Complete the TODO sections.
"""

from typing import Dict, List
import math

# Mock semantic similarity (replace with real embeddings in production)
def mock_semantic_similarity(actual: str, expected: str) -> float:
    """Mock semantic similarity (0-1 scale)"""
    # In production, use sentence-transformers or OpenAI embeddings
    # For now, simple word overlap as proxy
    actual_words = set(actual.lower().split())
    expected_words = set(expected.lower().split())
    
    if not expected_words:
        return 1.0
    
    overlap = len(actual_words & expected_words)
    similarity = overlap / len(expected_words)
    return min(similarity, 1.0)

# Three prompt variants to evaluate
def prompt_variant_v1(user_input: str) -> str:
    """Version 1: Basic responses"""
    responses = {
        "reset password": "You can reset your password.",
        "billing": "Contact billing for help.",
        "bug": "Report the bug to support.",
    }
    for key, response in responses.items():
        if key in user_input.lower():
            return response
    return "I don't know."

def prompt_variant_v2(user_input: str) -> str:
    """Version 2: More helpful"""
    responses = {
        "reset password": "Go to Settings > Account > Reset Password to reset your password.",
        "billing": "You can view billing in Settings > Billing or contact billing@company.com.",
        "bug": "Thank you for reporting. Please contact support@company.com with details.",
    }
    for key, response in responses.items():
        if key in user_input.lower():
            return response
    return "I'm not sure. Could you provide more details?"

def prompt_variant_v3(user_input: str) -> str:
    """Version 3: Most helpful (but maybe too verbose)"""
    responses = {
        "reset password": "I can help you reset your password! Here are the steps: (1) Go to Settings, (2) Click Account tab, (3) Select Reset Password, (4) Check your email for the reset link, (5) Follow the link and create a new password.",
        "billing": "To manage your billing, log into your account and go to Settings > Billing. There you can view invoices, update payment methods, and manage your subscription. If you have questions, email billing@company.com.",
        "bug": "I'm sorry you encountered a bug! Please report it to support@company.com with: the steps to reproduce, your browser/OS, and any error messages. Our team will investigate within 24 hours.",
    }
    for key, response in responses.items():
        if key in user_input.lower():
            return response
    return "I'm not sure. Could you provide more details about your issue?"

class EvaluationHarness:
    """Evaluate multiple prompt variants"""
    
    def __init__(self, golden_dataset: List[Dict]):
        self.dataset = golden_dataset
        self.results = {}
    
    def grade_rubric(self, actual: str, expected: str) -> int:
        """
        TODO 1: Implement manual rubric grading
        Score 0-7 based on:
        - Relevance: expected content in actual? (0-2)
        - Accuracy: info correct? (0-2)
        - Helpfulness: can user act on this? (0-2)
        - Conciseness: not too long? (0-1)
        """
        # TODO 1 START
        
        # Relevance
        relevance = 2 if expected.lower() in actual.lower() else 1
        
        # Accuracy (assume correct for mocked responses)
        accuracy = 2
        
        # Helpfulness (more action items = more helpful)
        action_words = ["click", "go to", "email", "contact", "link", "follow"]
        helpfulness = min(2, len([w for w in action_words if w in actual.lower()]))
        
        # Conciseness (shorter is better, but not too short)
        conciseness = 1 if 20 < len(actual) < 300 else 0
        
        # TODO 1 END
        
        return relevance + accuracy + helpfulness + conciseness
    
    def eval_prompt_variant(self, prompt_func, variant_name: str) -> Dict:
        """
        TODO 2: Evaluate a single prompt variant
        For each example in golden dataset:
          - Run prompt on input
          - Score with rubric
          - Score with semantic similarity
          - Record both scores
        Calculate averages
        """
        # TODO 2 START
        
        rubric_scores = []
        semantic_scores = []
        
        for example in self.dataset:
            actual = prompt_func(example["input"])
            expected = example["expected"]
            
            # Score with rubric
            rubric_score = self.grade_rubric(actual, expected)
            rubric_scores.append(rubric_score)
            
            # Score with semantic similarity
            semantic_score = mock_semantic_similarity(actual, expected)
            semantic_scores.append(semantic_score)
        
        # Calculate averages
        avg_rubric = sum(rubric_scores) / len(rubric_scores) if rubric_scores else 0
        avg_semantic = sum(semantic_scores) / len(semantic_scores) if semantic_scores else 0
        
        result = {
            "variant": variant_name,
            "rubric_scores": rubric_scores,
            "semantic_scores": semantic_scores,
            "avg_rubric": avg_rubric,
            "avg_semantic": avg_semantic,
        }
        
        self.results[variant_name] = result
        
        # TODO 2 END
        
        return result
    
    def compare(self, variant_names: List[str]) -> None:
        """
        TODO 3: Compare prompt variants
        Print results in readable format
        Show: rubric score, semantic score, which variant wins
        """
        # TODO 3 START
        
        print("\n" + "="*70)
        print("EVALUATION HARNESS RESULTS")
        print("="*70 + "\n")
        
        print(f"{'Variant':<20} {'Rubric (0-7)':<20} {'Semantic (0-1)':<20} {'Average':<10}")
        print("-"*70)
        
        best_variant = None
        best_avg = -1
        
        for name in variant_names:
            result = self.results[name]
            avg = (result["avg_rubric"] / 7 + result["avg_semantic"]) / 2  # Normalize and average
            
            print(f"{name:<20} {result['avg_rubric']:<20.2f} {result['avg_semantic']:<20.2f} {avg:<10.3f}")
            
            if avg > best_avg:
                best_avg = avg
                best_variant = name
        
        print("="*70)
        print(f"\n✅ Best variant: {best_variant}")
        print()
        
        # TODO 3 END

# Main
if __name__ == "__main__":
    # Golden dataset
    golden_dataset = [
        {
            "input": "How do I reset my password?",
            "expected": "Password reset instructions"
        },
        {
            "input": "Where's my billing?",
            "expected": "Billing info location or contact"
        },
        {
            "input": "I found a bug",
            "expected": "Bug report instructions"
        },
        {
            "input": "Can't log in",
            "expected": "Password reset or help"
        },
        {
            "input": "Need support",
            "expected": "Support contact info"
        },
    ]
    
    # Create eval harness
    harness = EvaluationHarness(golden_dataset)
    
    print("Evaluating 3 prompt variants...")
    print()
    
    # Evaluate each variant
    harness.eval_prompt_variant(prompt_variant_v1, "Variant V1 (Basic)")
    harness.eval_prompt_variant(prompt_variant_v2, "Variant V2 (Helpful)")
    harness.eval_prompt_variant(prompt_variant_v3, "Variant V3 (Verbose)")
    
    # Compare results
    harness.compare(["Variant V1 (Basic)", "Variant V2 (Helpful)", "Variant V3 (Verbose)"])
