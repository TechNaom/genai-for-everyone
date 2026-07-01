"""
Reference solution.
Session 5.2 (v2): Core Path — Eval Harness for a Contract Clause Summarizer

Build an evaluation harness that scores 3 prompt variants using:
1. LLM-as-judge (mocked, with an explicit partial-failure cap)
2. Semantic similarity (mocked via word overlap, since real embeddings
   aren't available in this environment — but the SAME blind spot shows up)

Complete the TODOs.
"""

from typing import Dict, List

# A small golden dataset: clause text (summarized for brevity), the
# human-verified reference summary, and clause risk type.
GOLDEN_DATASET = [
    {
        "id": "arb_1",
        "type": "arbitration",
        "clause_summary_of_clause": "binding arbitration clause that also "
                                     "waives the right to join a class action",
        "reference": "You agree to arbitration and waive your right to "
                      "join a class action lawsuit.",
    },
    {
        "id": "notice_1",
        "type": "notice_period",
        "clause_summary_of_clause": "30-day written notice required to "
                                     "terminate the agreement",
        "reference": "You must give 30 days written notice to end this "
                      "agreement.",
    },
    {
        "id": "indem_1",
        "type": "indemnification",
        "clause_summary_of_clause": "you indemnify the company for any "
                                     "claims arising from your use of the "
                                     "product, with no cap on liability",
        "reference": "You agree to cover the company's legal costs for "
                      "claims related to your use of the product, with no "
                      "limit on how much you could owe.",
    },
]

# Mock outputs from 3 prompt variants for each clause in the dataset.
# Variant A: concise (drops secondary details to stay short)
# Variant B: thorough (catches everything)
# Variant C: plain language (casual tone, but actually complete)
VARIANT_OUTPUTS = {
    "Variant A (concise)": {
        "arb_1": "You agree to settle disputes through arbitration instead of court.",  # omits class action waiver!
        "notice_1": "Give 30 days notice to cancel.",
        "indem_1": "You agree to cover the company's legal costs for any claim tied to your use of the product.",  # omits "no cap"!
    },
    "Variant B (thorough)": {
        "arb_1": "You agree to arbitration instead of court, and you give "
                  "up the right to join a class action lawsuit.",
        "notice_1": "You need to give 30 days written notice before "
                     "ending this agreement.",
        "indem_1": "You agree to cover the company's legal costs for "
                     "claims tied to your product use — and there's no "
                     "cap on how much that could cost you.",
    },
    "Variant C (plain language)": {
        "arb_1": "Basically, if there's a dispute, you're going to "
                  "arbitration, not court — and you can't team up with "
                  "other customers to sue as a group.",
        "notice_1": "Just give a month's heads up in writing if you want "
                      "to cancel.",
        "indem_1": "Heads up: if your use of the product causes a claim "
                     "against the company, you're on the hook for their "
                     "legal costs, and there's no maximum on that.",
    },
}


def mock_semantic_similarity(summary: str, reference: str) -> float:
    """
    Mock semantic similarity using KEY-CONCEPT overlap rather than raw
    word overlap. Real sentence embeddings capture meaning, not exact
    words — so "give a month's heads up" and "give 30 days written
    notice" should score similarly high despite sharing almost no words.
    This mock approximates that by checking for the presence of a small
    set of meaning-bearing concepts per clause, rather than literal
    string overlap. This reproduces the SAME blind spot real embeddings
    have for this task: it rewards covering the gist, even when a
    specific legally significant detail is the part that's missing.
    """
    text = summary.lower()

    # Each clause has 2-3 "concepts" a faithful summary should hit.
    # A summary that captures most of them reads as semantically close,
    # REGARDLESS of which exact words it uses.
    concept_checks = {
        "arb_1": {
            "arbitration": any(w in text for w in ["arbitration", "arbitrate"]),
            "not_court": any(w in text for w in ["court", "instead of court", "not court"]),
            "class_action_waiver": any(w in text for w in ["class action", "team up", "group", "join"]),
            "binding_nature": any(w in text for w in ["agree", "agreeing", "you're going", "you are going"]),
        },
        "notice_1": {
            "notice_period": any(w in text for w in ["notice", "heads up", "head's up"]),
            "duration": "30" in text or "month" in text,
            "termination": any(w in text for w in ["cancel", "end", "terminate"]),
        },
        "indem_1": {
            "indemnification": any(w in text for w in ["cover", "legal costs", "on the hook", "indemnif"]),
            "trigger": any(w in text for w in ["claim", "use of the product", "your use"]),
            "no_cap": any(w in text for w in ["no cap", "no limit", "no maximum", "however much", "any amount"]),
            "binding_nature": any(w in text for w in ["agree", "agreeing", "you're on", "you are on"]),
        },
    }

    # Find which clause this reference belongs to by checking known text
    if "arbitration" in reference.lower() or "class action" in reference.lower():
        checks = concept_checks["arb_1"]
    elif "notice" in reference.lower():
        checks = concept_checks["notice_1"]
    else:
        checks = concept_checks["indem_1"]

    hits = sum(1 for present in checks.values() if present)
    return round(hits / len(checks), 2)


def llm_judge_score(summary: str, reference: str, omits_detail: bool) -> int:
    """
    TODO 1: Mock an LLM-as-judge score (0-10) with an explicit
    partial-failure cap, as described in the chapter (Part 2).

    Rules to implement:
      - Start from a base score reflecting word overlap with the reference
        (use mock_semantic_similarity() scaled to 0-10) as a rough proxy
        for "how much did it get right"
      - BUT: if omits_detail is True (a legally significant detail was
        left out), CAP the score at 5, regardless of how high the overlap
        score would otherwise be. This is the explicit anti-generosity
        rule from the chapter.
    """
    # TODO 1 START

    base_score = round(mock_semantic_similarity(summary, reference) * 10)

    if omits_detail:
        return min(base_score, 5)

    return base_score

    # TODO 1 END


# Ground truth: does each variant's summary for each clause omit a
# legally significant detail? (In production, a human determines this
# during the golden dataset build — see Session 5.1.)
OMITS_DETAIL = {
    "Variant A (concise)": {"arb_1": True, "notice_1": False, "indem_1": True},
    "Variant B (thorough)": {"arb_1": False, "notice_1": False, "indem_1": False},
    "Variant C (plain language)": {"arb_1": False, "notice_1": False, "indem_1": False},
}


def needs_human_review(llm_score: int, semantic_sim: float, clause_type: str) -> bool:
    """
    TODO 2: Implement the routing logic from the chapter (Part 4).
    Flag for review if:
      - clause_type is high-risk (arbitration, indemnification), OR
      - llm_score is in the uncertain middle (4-7), OR
      - semantic_sim is in the omission-prone middle band (0.70-0.85)
    """
    # TODO 2 START

    HIGH_RISK_TYPES = {"arbitration", "indemnification"}

    if clause_type in HIGH_RISK_TYPES:
        return True
    if 4 <= llm_score <= 7:
        return True
    if 0.70 <= semantic_sim <= 0.85:
        return True
    return False

    # TODO 2 END


def eval_variant(variant_name: str) -> Dict:
    """
    TODO 3: Evaluate one variant across the full golden dataset.
    For each clause: compute semantic similarity, LLM-judge score, and
    whether it needs human review. Return averages + flag rate.
    """
    # TODO 3 START

    outputs = VARIANT_OUTPUTS[variant_name]
    omits = OMITS_DETAIL[variant_name]

    semantic_scores = []
    llm_scores = []
    flags = []

    for clause in GOLDEN_DATASET:
        clause_id = clause["id"]
        summary = outputs[clause_id]
        reference = clause["reference"]

        sem_sim = mock_semantic_similarity(summary, reference)
        llm_score = llm_judge_score(summary, reference, omits[clause_id])
        flagged = needs_human_review(llm_score, sem_sim, clause["type"])

        semantic_scores.append(sem_sim)
        llm_scores.append(llm_score)
        flags.append(flagged)

    return {
        "variant": variant_name,
        "avg_semantic": sum(semantic_scores) / len(semantic_scores),
        "avg_llm_judge": sum(llm_scores) / len(llm_scores),
        "pct_flagged": (sum(flags) / len(flags)) * 100,
        "per_clause": list(zip(
            [c["id"] for c in GOLDEN_DATASET], semantic_scores, llm_scores, flags
        )),
    }

    # TODO 3 END


def run_comparison():
    print("\n" + "=" * 70)
    print("CONTRACT SUMMARIZER — EVAL HARNESS")
    print("=" * 70 + "\n")

    for variant_name in VARIANT_OUTPUTS:
        result = eval_variant(variant_name)
        print(f"{variant_name}:")
        print(f"  Avg semantic similarity: {result['avg_semantic']:.2f}")
        print(f"  Avg LLM-judge score:     {result['avg_llm_judge']:.1f}/10")
        print(f"  % flagged for review:    {result['pct_flagged']:.0f}%")
        print(f"  Per-clause detail:")
        for clause_id, sem, llm, flagged in result["per_clause"]:
            flag_str = "🚩 FLAGGED" if flagged else "  ok"
            print(f"    {clause_id}: semantic={sem:.2f}, llm={llm}/10  {flag_str}")
        print()

    print("=" * 70)
    print("Notice: Variant A's arb_1 and indem_1 both omit a real detail.")
    print("Did semantic similarity alone catch that? Check the per-clause")
    print("scores above — a 0.7-0.85 'middle band' score on an omission")
    print("case looks deceptively reasonable without the LLM-judge cap.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    run_comparison()
