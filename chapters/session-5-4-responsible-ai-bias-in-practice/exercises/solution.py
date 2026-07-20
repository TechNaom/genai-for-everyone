"""
Reference solution.
Session 5.4: Core Path -- Bias Audit

Same working audit as starter.py, plus the three extension ideas from
README.md filled in: a 4th group, a severity() helper, and a JSON export.
"""

import json
from typing import Dict, List

# Sample model outputs for hiring recommendations -- now 4 groups.
SAMPLE_OUTPUTS = [
    {"group": "female", "occupation": "nurse", "score": 0.92},
    {"group": "male", "occupation": "engineer", "score": 0.95},
    {"group": "female", "occupation": "teacher", "score": 0.88},
    {"group": "male", "occupation": "ceo", "score": 0.91},
    {"group": "latino", "occupation": "construction", "score": 0.72},
    {"group": "latino", "occupation": "management", "score": 0.65},
    {"group": "asian", "occupation": "engineer", "score": 0.90},
    {"group": "asian", "occupation": "management", "score": 0.83},
    # ... more examples in real audit
] * 6  # 48 total (simplified)


def severity(gap_pct: float, high: float = 15.0, medium: float = 5.0) -> str:
    """Turn a gap percentage into a severity label, matching Part 3 of the lesson."""
    if gap_pct > high:
        return "HIGH"
    if gap_pct > medium:
        return "MEDIUM"
    return "LOW"


class BiasAudit:
    """Conduct bias audit on model outputs"""

    def __init__(self, outputs: List[Dict]):
        self.outputs = outputs
        self.groups = set(o["group"] for o in outputs)
        self.results = {}

    def calculate_accuracy(self) -> Dict[str, float]:
        """Calculate accuracy per group"""
        accuracy = {}
        for group in self.groups:
            group_outputs = [o for o in self.outputs if o["group"] == group]

            # Accuracy = outputs where score > 0.8
            accurate = sum(1 for o in group_outputs if o["score"] > 0.8)
            accuracy[group] = accurate / len(group_outputs) if group_outputs else 0

        return accuracy

    def calculate_representation(self) -> Dict[str, float]:
        """Calculate representation (% of outputs per group)"""
        representation = {}
        total = len(self.outputs)

        for group in self.groups:
            count = len([o for o in self.outputs if o["group"] == group])
            representation[group] = count / total if total > 0 else 0

        return representation

    def calculate_occupational_distribution(self) -> Dict[str, Dict[str, float]]:
        """What occupations are recommended per group?"""
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

        return distribution

    def save_report_json(self, path: str = "bias_audit_report.json"):
        """Extension: write the three metrics dicts to a machine-readable JSON file."""
        accuracy = self.calculate_accuracy()
        representation = self.calculate_representation()
        distribution = self.calculate_occupational_distribution()

        acc_gap = (max(accuracy.values()) - min(accuracy.values())) * 100
        rep_gap = (max(representation.values()) - min(representation.values())) * 100

        report = {
            "accuracy": accuracy,
            "accuracy_gap_pct": acc_gap,
            "accuracy_severity": severity(acc_gap),
            "representation": representation,
            "representation_gap_pct": rep_gap,
            "representation_severity": severity(rep_gap, high=20.0, medium=10.0),
            "occupational_distribution": distribution,
        }

        with open(path, "w") as f:
            json.dump(report, f, indent=2)

        return report

    def generate_report(self):
        """Generate audit report"""
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
            print(f"FINDING: Significant accuracy disparity -- severity: {severity(gap)}")
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
            print(f"FINDING: Unequal representation -- severity: {severity(rep_gap, high=20.0, medium=10.0)}")
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


if __name__ == "__main__":
    audit = BiasAudit(SAMPLE_OUTPUTS)
    audit.generate_report()
    saved = audit.save_report_json()
    print(f"Saved machine-readable report with {len(audit.groups)} groups to bias_audit_report.json")
