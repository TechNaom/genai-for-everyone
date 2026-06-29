"""
Session 5.4: Pro Path — Comprehensive Bias Audit Framework

Design and implement a full bias audit:
1. Define audit scope
2. Collect/annotate sample data
3. Calculate metrics per group
4. Create model card
5. Identify mitigations

This is less scaffolded. You design the framework.
"""

import json
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class AuditConfig:
    """Configuration for bias audit"""
    groups: List[str]
    metrics: List[str]
    sample_size: int
    threshold_parity: float = 0.05
    threshold_representation: float = 0.1

class ComprehensiveBiasAudit:
    """Full bias audit framework"""
    
    def __init__(self, config: AuditConfig):
        self.config = config
        self.outputs = []
        self.annotations = {}
    
    def collect_sample_data(self, source_data: List[Dict]):
        """Step 1: Collect balanced sample"""
        # Ensure balanced representation
        per_group = self.config.sample_size // len(self.config.groups)
        
        self.outputs = []
        for group in self.config.groups:
            group_data = [d for d in source_data if d.get("group") == group]
            self.outputs.extend(group_data[:per_group])
    
    def annotate_outputs(self, human_labels: Dict):
        """Step 2: Annotate ground truth (simulated)"""
        self.annotations = human_labels
    
    def calculate_metrics(self) -> Dict:
        """Step 3: Calculate all metrics"""
        metrics = {}
        
        for metric in self.config.metrics:
            metrics[metric] = {}
            
            for group in self.config.groups:
                group_outputs = [o for o in self.outputs if o.get("group") == group]
                
                if metric == "accuracy":
                    # % where model output matches human annotation
                    matches = sum(
                        1 for o in group_outputs
                        if self.annotations.get(o.get("id")) == o.get("prediction")
                    )
                    metrics[metric][group] = matches / len(group_outputs) if group_outputs else 0
                
                elif metric == "representation":
                    # % of outputs from this group
                    metrics[metric][group] = len(group_outputs) / len(self.outputs)
                
                elif metric == "fairness_score":
                    # Simulated fairness score (0-1)
                    metrics[metric][group] = 0.85 + (hash(group) % 10) / 100
        
        return metrics
    
    def check_parity(self, metrics: Dict) -> Dict[str, bool]:
        """Step 4: Check if metrics meet parity thresholds"""
        parity_violations = {}
        
        for metric, group_scores in metrics.items():
            if isinstance(group_scores, dict) and len(group_scores) > 1:
                scores = list(group_scores.values())
                gap = max(scores) - min(scores)
                
                threshold = (self.config.threshold_parity 
                            if metric == "accuracy" 
                            else self.config.threshold_representation)
                
                parity_violations[metric] = gap > threshold
        
        return parity_violations
    
    def create_model_card(self, metrics: Dict, parity: Dict):
        """Step 5: Create model card documenting findings"""
        card = {
            "model_name": "Hiring Recommendation System",
            "overall_metrics": {
                "accuracy": sum(v for k, v in metrics.get("accuracy", {}).items()) / len(self.config.groups),
            },
            "group_performance": metrics,
            "parity_violations": parity,
            "limitations": [],
            "recommended_use": "",
        }
        
        # Document limitations
        for metric, violated in parity.items():
            if violated:
                card["limitations"].append(f"Significant disparity in {metric} across groups")
        
        # Recommend use
        if any(parity.values()):
            card["recommended_use"] = "Not recommended for high-stakes decisions. Use with human review."
        else:
            card["recommended_use"] = "Acceptable for medium-stakes decisions. Monitor continuously."
        
        return card
    
    def generate_full_report(self) -> str:
        """Generate comprehensive audit report"""
        metrics = self.calculate_metrics()
        parity = self.check_parity(metrics)
        card = self.create_model_card(metrics, parity)
        
        report = "\n" + "="*70 + "\n"
        report += "COMPREHENSIVE BIAS AUDIT REPORT\n"
        report += "="*70 + "\n\n"
        
        report += "MODEL CARD:\n"
        report += json.dumps(card, indent=2) + "\n\n"
        
        report += "METRICS BY GROUP:\n"
        for metric, groups in metrics.items():
            report += f"\n{metric.upper()}:\n"
            for group, score in groups.items():
                report += f"  {group}: {score:.3f}\n"
        
        report += "\nPARITY VIOLATIONS:\n"
        for metric, violated in parity.items():
            status = "⚠️ VIOLATED" if violated else "✅ PASS"
            report += f"  {metric}: {status}\n"
        
        report += "\n" + "="*70 + "\n"
        
        return report

# Example usage
if __name__ == "__main__":
    config = AuditConfig(
        groups=["male", "female", "latino"],
        metrics=["accuracy", "representation", "fairness_score"],
        sample_size=300,
    )
    
    audit = ComprehensiveBiasAudit(config)
    
    # Simulate data collection
    sample_data = [
        {"id": i, "group": "male", "prediction": "engineer"}
        for i in range(100)
    ] + [
        {"id": i+100, "group": "female", "prediction": "nurse"}
        for i in range(100)
    ] + [
        {"id": i+200, "group": "latino", "prediction": "construction"}
        for i in range(100)
    ]
    
    audit.collect_sample_data(sample_data)
    
    # Simulate annotations
    audit.annotations = {i: "engineer" if i < 50 else "nurse" for i in range(300)}
    
    # Generate report
    print(audit.generate_full_report())
