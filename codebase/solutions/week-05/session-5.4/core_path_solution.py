"""
Reference solution.
Session 5.4: Core Path — Bias Audit

Conduct a bias audit on model outputs:
1. Load sample outputs (50 examples)
2. Audit for bias across 3 groups
3. Calculate metrics
4. Document findings
5. Suggest mitigations

Complete TODOs.
"""

import json
from typing import Dict, List

# Sample model outputs for hiring recommendations
SAMPLE_OUTPUTS = [
    {"group": "female", "occupation": "nurse", "score": 0.92},
    {"group": "male", "occupation": "engineer", "score": 0.95},
    {"group": "female", "occupation": "teacher", "score": 0.88},
    {"group": "male", "occupation": "ceo", "score": 0.91},
    {"group": "latino", "occupation": "construction", "score": 0.72},
    {"group": "latino", "occupation": "management", "score": 0.65},
    # ... more examples in real audit
] * 8  # 48 total (simplified)

class BiasAudit:
    """Conduct bias audit on model outputs"""
    
    def __init__(self, outputs: List[Dict]):
        self.outputs = outputs
        self.groups = set(o["group"] for o in outputs)
        self.results = {}
    
    def calculate_accuracy(self) -> Dict[str, float]:
        """TODO 1: Calculate accuracy per group"""
        # TODO 1 START
        
        accuracy = {}
        for group in self.groups:
            group_outputs = [o for o in self.outputs if o["group"] == group]
            
            # Accuracy = outputs where score > 0.8
            accurate = sum(1 for o in group_outputs if o["score"] > 0.8)
            accuracy[group] = accurate / len(group_outputs) if group_outputs else 0
        
        # TODO 1 END
        
        return accuracy
    
    def calculate_representation(self) -> Dict[str, float]:
        """TODO 2: Calculate representation (% of outputs per group)"""
        # TODO 2 START
        
        representation = {}
        total = len(self.outputs)
        
        for group in self.groups:
            count = len([o for o in self.outputs if o["group"] == group])
            representation[group] = count / total if total > 0 else 0
        
        # TODO 2 END
        
        return representation
    
    def calculate_occupational_distribution(self) -> Dict[str, Dict[str, float]]:
        """TODO 3: What occupations are recommended per group?"""
        # TODO 3 START
        
        distribution = {}
        
        for group in self.groups:
            group_outputs = [o for o in self.outputs if o["group"] == group]
            
            occupations = {}
            for output in group_outputs:
                occ = output["occupation"]
                occupations[occ] = occupations.get(occ, 0) + 1
            
            # Convert to percentages
            total = len(group_outputs)
            distribution[group] = {
                occ: count / total for occ, count in occupations.items()
            }
        
        # TODO 3 END
        
        return distribution
    
    def generate_report(self):
        """TODO 4: Generate audit report"""
        # TODO 4 START
        
        print("\n" + "="*70)
        print("BIAS AUDIT REPORT")
        print("="*70 + "\n")
        
        # Accuracy
        print("1. ACCURACY DISPARITY")
        print("-"*70)
        accuracy = self.calculate_accuracy()
        for group, acc in accuracy.items():
            print(f"{group.upper():<15} Accuracy: {acc*100:.1f}%")
        
        max_acc = max(accuracy.values())
        min_acc = min(accuracy.values())
        gap = (max_acc - min_acc) * 100
        print(f"\nAccuracy gap: {gap:.1f}% (target: <5%)")
        if gap > 5:
            print("FINDING: Significant accuracy disparity ⚠️")
        print()
        
        # Representation
        print("2. REPRESENTATION")
        print("-"*70)
        representation = self.calculate_representation()
        for group, rep in representation.items():
            print(f"{group.upper():<15} Representation: {rep*100:.1f}%")
        
        max_rep = max(representation.values())
        min_rep = min(representation.values())
        rep_gap = (max_rep - min_rep) * 100
        print(f"\nRepresentation gap: {rep_gap:.1f}% (target: <10%)")
        if rep_gap > 10:
            print("FINDING: Unequal representation ⚠️")
        print()
        
        # Occupational distribution
        print("3. OCCUPATIONAL DISTRIBUTION")
        print("-"*70)
        distribution = self.calculate_occupational_distribution()
        for group, occupations in distribution.items():
            print(f"\n{group.upper()}:")
            for occ, pct in sorted(occupations.items(), key=lambda x: x[1], reverse=True):
                print(f"  {occ}: {pct*100:.1f}%")
        
        print()
        print("="*70)
        print("MITIGATIONS")
        print("="*70)
        print("1. Audit training data: Are all groups equally represented?")
        print("2. Oversample underrepresented groups in training")
        print("3. Add fairness constraints during model training")
        print("4. Adjust decision thresholds to equalize accuracy across groups")
        print("5. Use human review for high-stakes decisions")
        print()
        
        # TODO 4 END

if __name__ == "__main__":
    audit = BiasAudit(SAMPLE_OUTPUTS)
    audit.generate_report()
