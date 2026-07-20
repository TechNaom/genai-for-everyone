"""
Session 6.5 Project: Prompt Version History & Rollback

Extends the CI regression gate from the exercise into a small
version-history system: store each prompt version with its score and a
timestamp, support "rollback to the previous version," and produce a
changelog-style report showing score trends across versions -- enough to
answer "when did this start getting worse, and what changed?"

No API key, no internet access, no external libraries -- fully offline,
pure data/scoring logic that builds on the Session 6.5 lesson's regression
gate and Session 5.1's regression suite.

Run: python3 starter.py
"""

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class PromptVersion:
    name: str
    score: float
    timestamp: str      # a plain sortable string, e.g. "2026-01-05" -- no datetime needed
    note: str = ""       # what changed in this version, for the changelog


class PromptVersionHistory:
    """
    Tracks a sequence of prompt versions with scores and timestamps.
    Supports adding new versions, rolling back to the previous version, and
    generating a changelog report that flags where a regression began.
    """

    def __init__(self, regression_threshold: float = 0.05):
        self.versions: List[PromptVersion] = []
        self.current_index: int = -1
        self.regression_threshold = regression_threshold

    def add_version(self, name: str, score: float, timestamp: str, note: str = "") -> None:
        """
        TODO 1: Append a new PromptVersion(name, score, timestamp, note) to
        self.versions, then update self.current_index so it points at the
        version you just added (the newest version becomes "current").
        """
        raise NotImplementedError

    def current(self) -> Optional[PromptVersion]:
        """Return the currently active version, or None if there isn't one."""
        if 0 <= self.current_index < len(self.versions):
            return self.versions[self.current_index]
        return None

    def rollback(self) -> PromptVersion:
        """
        TODO 2: Move self.current_index back by one and return that
        PromptVersion. If there's no earlier version to roll back to
        (self.current_index is already 0 or the history is empty), raise
        IndexError with a clear message instead of moving past the start.
        """
        raise NotImplementedError

    def first_regression(self) -> Optional[PromptVersion]:
        """
        TODO 3: Walk through self.versions in the order they were added.
        Find the FIRST version whose score dropped by more than
        self.regression_threshold compared to the version immediately
        before it (prev_score - this_score > regression_threshold). Return
        that PromptVersion -- the one that introduced the regression -- or
        None if no version ever regressed beyond the threshold.
        """
        raise NotImplementedError

    def changelog(self) -> str:
        """
        TODO 4: Build and return a formatted, multi-line changelog string.
        For each version (in the order it was added), show at least: name,
        score (as a percentage), timestamp, and the score change versus the
        previous version (e.g. "+2%" or "-14%"; the first version has no
        change to show). Mark the version returned by first_regression()
        with a clear flag such as "<-- regression started here", and mark
        whichever version is at self.current_index with "(current)".

        Example line format (yours doesn't have to match exactly):
          v2_friendlier_tone   78%  2026-01-12  (-14%)  <-- regression started here
        """
        raise NotImplementedError


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
