"""
Session 7.3: Capstone Build Day I — Checkpoint Tracker

Run: python3 starter.py
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
        """
        TODO 1: append {"checkpoint": checkpoint, "elapsed_percent": ...,
        "justification": justification} to self.log.
        """
        raise NotImplementedError

    def status_report(self) -> str:
        """
        TODO 2: return a formatted string showing, for each entry in self.log,
        the checkpoint name and elapsed_percent at the time it was completed.
        Also flag (in the string) if Checkpoint 1 was completed after 25%
        elapsed — the "you should have simplified" signal from the lesson.
        """
        raise NotImplementedError


if __name__ == "__main__":
    tracker = BuildDayTracker(total_minutes=90)

    # Simulate reaching checkpoints (in a real build day, call these as you go)
    tracker.complete_checkpoint(CHECKPOINTS[0])
    tracker.complete_checkpoint(CHECKPOINTS[1])

    print(tracker.status_report())
