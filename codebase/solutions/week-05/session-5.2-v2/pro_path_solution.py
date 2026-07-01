"""
Reference solution.
Session 5.2 (v2): Pro Path — Routing Logic Stress Test

Build the full needs_human_review() routing system and PROVE it catches
omission failures that a naive "flag anything below 0.5" threshold
would miss.

This is less scaffolded. You design the comparison.
"""

from typing import Dict, List, Tuple

# Extended test set: 8 clause/summary pairs, deliberately including
# several that hit the deceptive 0.70-0.85 similarity band while still
# omitting something legally significant.
TEST_CASES = [
    # (clause_id, clause_type, semantic_sim, llm_score, actually_omits_detail)
    ("case_1", "arbitration",      0.95, 9, False),  # genuinely complete, high score
    ("case_2", "arbitration",      0.75, 5, True),   # THE problem case: mid-similarity, omits detail
    ("case_3", "notice_period",    0.40, 3, True),   # obviously bad, easy to catch
    ("case_4", "indemnification",  0.80, 6, True),   # another mid-band omission
    ("case_5", "notice_period",    0.92, 9, False),  # genuinely complete
    ("case_6", "arbitration",      0.30, 2, True),   # obviously bad, easy to catch
    ("case_7", "indemnification",  0.78, 5, True),   # another mid-band omission
    ("case_8", "notice_period",    0.88, 8, False),  # genuinely complete, slightly stylistic difference
]


def naive_threshold_review(semantic_sim: float) -> bool:
    """The WRONG way: flag only low scores."""
    return semantic_sim < 0.5


def proper_routing_review(llm_score: int, semantic_sim: float, clause_type: str) -> bool:
    """
    TODO 1: Implement the chapter's full routing logic (Part 4):
      - high-risk clause type (arbitration, indemnification) -> always flag
      - llm_score in the uncertain middle (4-7) -> flag
      - semantic_sim in the deceptive middle band (0.70-0.85) -> flag
    """
    # TODO 1 START

    HIGH_RISK_TYPES = {"arbitration", "indemnification"}

    if clause_type in HIGH_RISK_TYPES:
        return True
    if 4 <= llm_score <= 7:
        return True
    if 0.70 <= semantic_sim <= 0.85:
        return True
    return False

    # TODO 1 END


def evaluate_routing_strategy(strategy_fn, strategy_name: str, use_full_args: bool):
    """
    TODO 2: Run a routing strategy against all 8 test cases.
    Compute:
      - false negative rate AMONG OMISSION CASES SPECIFICALLY: of the
        cases where actually_omits_detail is True, what fraction did
        this strategy FAIL to flag?
      - overall flag rate (for context — flagging everything trivially
        gets 0% false negatives but isn't useful)
    """
    # TODO 2 START

    omission_cases = [c for c in TEST_CASES if c[4]]  # actually_omits_detail == True
    missed_omissions = 0

    print(f"\n--- {strategy_name} ---")

    for clause_id, clause_type, sem_sim, llm_score, omits in TEST_CASES:
        if use_full_args:
            flagged = strategy_fn(llm_score, sem_sim, clause_type)
        else:
            flagged = strategy_fn(sem_sim)

        miss_marker = ""
        if omits and not flagged:
            missed_omissions += 1
            miss_marker = "  🚨 MISSED OMISSION"

        flag_str = "FLAGGED" if flagged else "not flagged"
        print(f"  {clause_id} (sim={sem_sim:.2f}, llm={llm_score}, "
              f"omits={omits}): {flag_str}{miss_marker}")

    fn_rate = (missed_omissions / len(omission_cases)) * 100 if omission_cases else 0
    total_flagged = sum(
        1 for c in TEST_CASES
        if (strategy_fn(c[3], c[2], c[1]) if use_full_args else strategy_fn(c[2]))
    )
    flag_rate = (total_flagged / len(TEST_CASES)) * 100

    print(f"\n  False negative rate (among omission cases): {fn_rate:.0f}% "
          f"({missed_omissions}/{len(omission_cases)} omissions missed)")
    print(f"  Overall flag rate: {flag_rate:.0f}%")

    return fn_rate, flag_rate

    # TODO 2 END


if __name__ == "__main__":
    print("=" * 70)
    print("ROUTING STRATEGY COMPARISON")
    print("=" * 70)

    naive_fn, naive_flag = evaluate_routing_strategy(
        naive_threshold_review, "NAIVE: flag only if similarity < 0.5", use_full_args=False
    )

    proper_fn, proper_flag = evaluate_routing_strategy(
        proper_routing_review, "PROPER: high-risk type OR mid-band score", use_full_args=True
    )

    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)
    print(f"Naive threshold:  {naive_fn:.0f}% of real omissions missed, "
          f"{naive_flag:.0f}% overall flag rate")
    print(f"Proper routing:   {proper_fn:.0f}% of real omissions missed, "
          f"{proper_flag:.0f}% overall flag rate")

    if proper_fn < naive_fn:
        print(f"\n✅ Proper routing catches {naive_fn - proper_fn:.0f} percentage "
              f"points MORE of the real omission failures, at the cost of a "
              f"{proper_flag - naive_flag:.0f} point higher flag rate.")
        print("   That trade — more human review time, for catching the failures")
        print("   that actually matter — is the right one for a legal tool.")
