"""
Reference solution.
Session 4.4: Multi-Agent Patterns - Core Path

Build a writer + critic two-agent system:
1. Writer creates an essay on a topic
2. Critic reviews and gives feedback
3. Writer revises once based on feedback
4. Return final essay

Requires the `anthropic` package and an ANTHROPIC_API_KEY environment
variable (this exercise makes real model calls -- see README.md for setup).
"""

from anthropic import Anthropic

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

def writer_agent(topic: str, previous_feedback: str = None) -> str:
    """
    Agent 1: Writer. Writes or revises an essay.

    Args:
        topic: The essay topic
        previous_feedback: Optional feedback to incorporate in revision

    Returns:
        Essay text
    """
    # TODO 1 (solved): the writer either revises based on feedback, or writes
    # a fresh essay if this is the first draft.
    if previous_feedback:
        prompt = f"""You are an expert writer.
Topic: {topic}

Here is previous feedback on your draft:
{previous_feedback}

Please revise your essay addressing this feedback. Keep it to 3-4 paragraphs."""
    else:
        prompt = f"""You are an expert writer.
Write a clear, engaging essay on: {topic}
Keep it to 3-4 paragraphs. Use accessible language."""

    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        messages=messages
    )

    return "".join([block.text for block in response.content if hasattr(block, "text")])

def critic_agent(essay: str) -> str:
    """
    Agent 2: Critic. Reviews an essay and provides feedback.

    Args:
        essay: The essay to review

    Returns:
        Feedback text (not a revised essay, just feedback)
    """
    # TODO 2 (solved): the critic gives feedback only, never a rewrite --
    # that separation of concerns is the entire point of a two-agent system.
    prompt = f"""You are a harsh but fair critic. Your job is to improve writing.

Read this essay:
{essay}

Provide 2-3 specific, actionable pieces of feedback. Be constructive but direct.
Focus on: clarity, accuracy, impact, and engagement."""

    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=512,
        messages=messages
    )

    return "".join([block.text for block in response.content if hasattr(block, "text")])

def multi_agent_loop(topic: str, num_revisions: int = 1) -> dict:
    """
    Two-agent loop: Writer → Critic → Revision.

    Args:
        topic: The essay topic
        num_revisions: How many times the writer revises (default 1)

    Returns:
        Dict with drafts, feedback, and final essay
    """
    result = {
        "topic": topic,
        "drafts": [],
        "feedback_rounds": [],
        "final_essay": None
    }

    # Step 1: Initial draft
    print(f"Topic: {topic}\n")
    print("=== Step 1: Initial Draft ===")
    draft = writer_agent(topic)
    result["drafts"].append(draft)
    print(f"Draft:\n{draft}\n")

    # Step 2-N: Feedback + Revision loop
    for revision_num in range(num_revisions):
        print(f"=== Step {revision_num + 2}: Feedback & Revision ===")

        feedback = critic_agent(draft)
        result["feedback_rounds"].append(feedback)
        print(f"Feedback:\n{feedback}\n")

        draft = writer_agent(topic, previous_feedback=feedback)
        result["drafts"].append(draft)
        print(f"Revised Draft:\n{draft}\n")

    result["final_essay"] = draft

    return result

# Test the system
if __name__ == "__main__":
    topic = "The role of AI in climate change solutions"
    result = multi_agent_loop(topic, num_revisions=1)

    print("\n" + "="*60)
    print("FINAL RESULT")
    print("="*60)
    print(f"Topic: {result['topic']}")
    print(f"Revisions: {len(result['feedback_rounds'])}")
    print(f"\n{result['final_essay']}")
