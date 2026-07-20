"""
Session 4.4: Multi-Agent Patterns - Pro Path

Build a multi-reviewer system:
1. Writer creates an essay
2. Three independent reviewers (fact-checker, style-checker, impact-checker) review
3. Writer synthesizes feedback from all three
4. Implement a "convergence" check — when do we stop revising?
5. Return final essay + review history

This is less scaffolded than the Core Path. The three reviewers are already
implemented for you below -- run this file as-is first, then work through the
challenges in README.md (changing convergence_threshold, adding a 4th
reviewer, replacing similarity_score with an LLM-based check).

Requires the `anthropic` package and an ANTHROPIC_API_KEY environment
variable (this makes real model calls).
"""

from anthropic import Anthropic
from typing import Dict, List
import json

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

def writer_agent(topic: str, all_feedback: List[Dict] = None) -> str:
    """
    Writer: Creates or revises essay based on feedback from multiple reviewers.

    Args:
        topic: Essay topic
        all_feedback: List of dicts, each with "reviewer" and "feedback" keys

    Returns:
        Essay text
    """
    if all_feedback:
        feedback_str = "\n".join([
            f"- {fb['reviewer']}: {fb['feedback']}"
            for fb in all_feedback
        ])
        prompt = f"""You are a skilled writer revising an essay.

Topic: {topic}

You received feedback from multiple reviewers:
{feedback_str}

Revise your essay to address the most important feedback points.
Keep it to 3-4 paragraphs."""
    else:
        prompt = f"""Write a clear, engaging essay on: {topic}
Keep it to 3-4 paragraphs. Use accessible language."""

    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        messages=messages
    )

    return "".join([block.text for block in response.content if hasattr(block, "text")])

def fact_checker_agent(essay: str) -> str:
    """
    Reviewer 1: Checks factual accuracy.
    """
    prompt = f"""You are a fact-checker. Review this essay for accuracy.

{essay}

Provide specific feedback on:
1. Factual claims that need verification
2. Missing context or nuance
3. Any questionable statistics or dates

Be concise and direct."""

    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=256,
        messages=messages
    )

    return "".join([block.text for block in response.content if hasattr(block, "text")])

def style_checker_agent(essay: str) -> str:
    """
    Reviewer 2: Checks writing style and clarity.
    """
    prompt = f"""You are a writing style expert. Review this essay for clarity and flow.

{essay}

Provide specific feedback on:
1. Clarity: Is the writing easy to understand?
2. Tone: Is it appropriate for the audience?
3. Flow: Do paragraphs connect logically?

Be concise and direct."""

    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=256,
        messages=messages
    )

    return "".join([block.text for block in response.content if hasattr(block, "text")])

def impact_checker_agent(essay: str) -> str:
    """
    Reviewer 3: Checks impact and engagement.
    """
    prompt = f"""You are a communication strategist. Review this essay for impact and engagement.

{essay}

Provide specific feedback on:
1. Hook: Does it grab the reader's attention?
2. Relevance: Does it address the reader's concerns?
3. Call-to-action: Does it inspire action or thought?

Be concise and direct."""

    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=256,
        messages=messages
    )

    return "".join([block.text for block in response.content if hasattr(block, "text")])

def similarity_score(feedback1: str, feedback2: str) -> float:
    """
    Simple convergence check: Do two feedback strings mention similar issues?
    Returns a score 0.0-1.0 (1.0 = identical).

    For production, you'd use embeddings or LLM-based similarity.
    This is a placeholder.
    """
    # Simple: count common words
    words1 = set(feedback1.lower().split())
    words2 = set(feedback2.lower().split())

    if not words1 or not words2:
        return 0.0

    intersection = len(words1 & words2)
    union = len(words1 | words2)

    return intersection / union if union > 0 else 0.0

def multi_agent_multi_reviewer_loop(topic: str, max_revisions: int = 3, convergence_threshold: float = 0.7) -> dict:
    """
    Multi-reviewer loop with convergence checking.

    Args:
        topic: Essay topic
        max_revisions: Maximum number of revision cycles
        convergence_threshold: If feedback similarity > this, stop revising

    Returns:
        Dict with all drafts, feedback, and revision history
    """
    result = {
        "topic": topic,
        "drafts": [],
        "feedback_history": [],  # List of dicts with reviewer feedback
        "convergence_scores": [],
        "final_essay": None,
        "final_feedback": None,
        "stopped_reason": None
    }

    print(f"Topic: {topic}\n")

    # Step 1: Initial draft
    print("=== Step 1: Initial Draft ===")
    draft = writer_agent(topic)
    result["drafts"].append(draft)
    print(f"Draft ({len(draft)} chars):\n{draft[:200]}...\n")

    # Step 2-N: Multi-reviewer + revision loop
    previous_feedback_str = ""

    for revision_num in range(max_revisions):
        print(f"=== Revision Round {revision_num + 1} ===")

        # Collect feedback from all three reviewers
        feedback_dict = {
            "iteration": revision_num,
            "reviews": {}
        }

        print("Fact-checking...")
        fact_feedback = fact_checker_agent(draft)
        feedback_dict["reviews"]["fact-checker"] = fact_feedback
        print(f"  → {fact_feedback[:80]}...\n")

        print("Checking style...")
        style_feedback = style_checker_agent(draft)
        feedback_dict["reviews"]["style-checker"] = style_feedback
        print(f"  → {style_feedback[:80]}...\n")

        print("Checking impact...")
        impact_feedback = impact_checker_agent(draft)
        feedback_dict["reviews"]["impact-checker"] = impact_feedback
        print(f"  → {impact_feedback[:80]}...\n")

        result["feedback_history"].append(feedback_dict)

        # Check convergence: are we getting the same feedback?
        current_feedback_str = fact_feedback + " " + style_feedback + " " + impact_feedback
        if previous_feedback_str:
            conv_score = similarity_score(previous_feedback_str, current_feedback_str)
            result["convergence_scores"].append(conv_score)
            print(f"Convergence score: {conv_score:.2f}")

            if conv_score > convergence_threshold:
                print(f"Feedback converged (> {convergence_threshold}). Stopping.")
                result["stopped_reason"] = "convergence"
                result["final_feedback"] = feedback_dict
                break

        previous_feedback_str = current_feedback_str

        # Writer revises based on all feedback
        print(f"Writer revising...")
        all_feedback = [
            {"reviewer": "Fact-Checker", "feedback": fact_feedback},
            {"reviewer": "Style-Checker", "feedback": style_feedback},
            {"reviewer": "Impact-Checker", "feedback": impact_feedback},
        ]

        draft = writer_agent(topic, all_feedback=all_feedback)
        result["drafts"].append(draft)
        print(f"Revised draft ({len(draft)} chars):\n{draft[:200]}...\n")

    if result["stopped_reason"] is None:
        result["stopped_reason"] = "max_revisions_reached"

    result["final_essay"] = draft
    return result

# Test the system
if __name__ == "__main__":
    topic = "The ethics of AI in hiring"
    result = multi_agent_multi_reviewer_loop(
        topic,
        max_revisions=3,
        convergence_threshold=0.65
    )

    print("\n" + "="*60)
    print("RESULTS SUMMARY")
    print("="*60)
    print(f"Topic: {result['topic']}")
    print(f"Total revisions: {len(result['drafts']) - 1}")
    print(f"Feedback rounds: {len(result['feedback_history'])}")
    print(f"Stopped because: {result['stopped_reason']}")
    print(f"Convergence scores: {[f'{s:.2f}' for s in result['convergence_scores']]}")

    print("\n" + "="*60)
    print("FINAL ESSAY")
    print("="*60)
    print(result["final_essay"])

    print("\n" + "="*60)
    print("FINAL FEEDBACK")
    print("="*60)
    if result["final_feedback"]:
        for reviewer, feedback in result["final_feedback"]["reviews"].items():
            print(f"\n{reviewer.upper()}:\n{feedback}")
