"""
Reference solution — Session 7.3: Capstone Build Day I — Checkpoint Tracker

Run: python3 solution.py
"""

import time
from typing import Dict, List, Optional

CHECKPOINTS = [
    "Checkpoint 1: thinnest end-to-end pipeline",
    "Checkpoint 2: core path works on golden dataset",
    "Checkpoint 3: eval pass completed",
    "Checkpoint 4: pro path or conscious scope cut",
]


class BuildDayTracker:
    def __init__(self, total_minutes: int):
        self.total_minutes = total_minutes
        self.start_time = time.time()
        self.log: List[Dict] = []

    def elapsed_minutes(self) -> float:
        return (time.time() - self.start_time) / 60

    def elapsed_percent(self) -> float:
        return min(self.elapsed_minutes() / self.total_minutes * 100, 100)

    def complete_checkpoint(self, checkpoint: str, justification: Optional[str] = None):
        self.log.append({
            "checkpoint": checkpoint,
            "elapsed_percent": round(self.elapsed_percent(), 1),
            "justification": justification,
        })

    def status_report(self) -> str:
        lines = ["=== BUILD DAY STATUS ==="]
        for entry in self.log:
            lines.append(f"{entry['checkpoint']} — completed at {entry['elapsed_percent']}% elapsed")
            if entry["justification"]:
                lines.append(f"    justification: {entry['justification']}")
            if entry["checkpoint"] == CHECKPOINTS[0] and entry["elapsed_percent"] > 25:
                lines.append("    ⚠️  Checkpoint 1 completed after 25% of build time — "
                              "consider simplifying scope going forward.")
        return "\n".join(lines)


if __name__ == "__main__":
    tracker = BuildDayTracker(total_minutes=90)

    tracker.complete_checkpoint(CHECKPOINTS[0], justification="Hard-coded 3 docs, crude prompt, prints an answer.")
    tracker.complete_checkpoint(CHECKPOINTS[1], justification="All 6 golden-dataset questions run through the pipeline.")

    print(tracker.status_report())
