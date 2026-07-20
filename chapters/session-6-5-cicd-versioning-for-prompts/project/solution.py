"""
Session 6.5 Project: Prompt Version History & Rollback -- reference solution.

Run: python3 solution.py
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PromptVersion:
    name: str
    score: float
    timestamp: str
    note: str = ""


class PromptVersionHistory:
    def __init__(self, regression_threshold: float = 0.05):
        self.versions: List[PromptVersion] = []
        self.current_index: int = -1
        self.regression_threshold = regression_threshold

    def add_version(self, name: str, score: float, timestamp: str, note: str = "") -> None:
        self.versions.append(PromptVersion(name=name, score=score, timestamp=timestamp, note=note))
        self.current_index = len(self.versions) - 1

    def current(self) -> Optional[PromptVersion]:
        if 0 <= self.current_index < len(self.versions):
            return self.versions[self.current_index]
        return None

    def rollback(self) -> PromptVersion:
        if self.current_index <= 0:
            raise IndexError("No earlier version to roll back to.")
        self.current_index -= 1
        return self.versions[self.current_index]

    def first_regression(self) -> Optional[PromptVersion]:
        for i in range(1, len(self.versions)):
            prev_score = self.versions[i - 1].score
            this_score = self.versions[i].score
            if prev_score - this_score > self.regression_threshold:
                return self.versions[i]
        return None

    def changelog(self) -> str:
        lines = ["=== PROMPT VERSION CHANGELOG ==="]
        regression = self.first_regression()
        prev_score = None

        for i, v in enumerate(self.versions):
            change = "" if prev_score is None else f"  ({v.score - prev_score:+.0%})"

            flags = []
            if regression is not None and v.name == regression.name:
                flags.append("<-- regression started here")
            if i == self.current_index:
                flags.append("(current)")
            flag_str = "  " + "  ".join(flags) if flags else ""

            lines.append(
                f"{v.name:<22}{v.score:>5.0%}  {v.timestamp}{change}{flag_str}"
                + (f"  -- {v.note}" if v.note else "")
            )
            prev_score = v.score

        return "\n".join(lines)


if __name__ == "__main__":
    history = PromptVersionHistory(regression_threshold=0.05)
    history.add_version("v1_baseline", 0.92, "2026-01-05", note="Initial support bot prompt")
    history.add_version("v2_friendlier_tone", 0.78, "2026-01-12", note="Reworded for a friendlier tone")
    history.add_version("v3_friendlier_fixed", 0.90, "2026-01-14", note="Kept tone, restored refund-policy precision")
    history.add_version("v4_shorter_answers", 0.91, "2026-01-20", note="Trimmed answers to cut cost")

    print(history.changelog())

    regression = history.first_regression()
    if regression is not None:
        print(f"\nFirst regression detected at: {regression.name} ({regression.timestamp}) -- {regression.note}")

    print(f"\nCurrent version: {history.current().name}")
    print("A production issue just came in -- rolling back...")
    rolled_back_to = history.rollback()
    print(f"Now on: {rolled_back_to.name} ({rolled_back_to.score:.0%})")
