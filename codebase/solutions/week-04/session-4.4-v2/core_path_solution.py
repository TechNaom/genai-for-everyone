"""
Reference solution.
Session 4.4: Multi-Agent Patterns - Core Path Starter

Build a writer + critic two-agent system:
1. Writer creates an essay on a topic
2. Critic reviews and gives feedback
3. Writer revises once based on feedback
4. Return final essay

Complete the TODO sections to finish the loop.
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
    # TODO 1: Write the prompt for the writer agent
    # If previous_feedback is provided, ask the writer to revise based on it.
    # If not, ask the writer to write an initial essay.
    # Keep essays to 3-4 paragraphs.
    # TODO 1 START
    if previous_feedback:
        prompt = f"""TODO: Write a prompt asking the writer to revise their essay on "{topic}" 
based on this feedback:
{previous_feedback}"""
    else:
        prompt = f"""TODO: Write a prompt asking the writer to write an initial essay on: {topic}
Keep it to 3-4 paragraphs."""
    # TODO 1 END
    
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
    # TODO 2: Write the prompt for the critic agent
    # Ask the critic to review the essay and provide 2-3 specific, actionable pieces of feedback.
    # Focus on clarity, accuracy, impact, and engagement.
    # TODO 2 START
    prompt = f"""TODO: Write a prompt asking the critic to review this essay and provide feedback:

{essay}"""
    # TODO 2 END
    
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
    # TODO 3: Implement the multi-agent loop
    # 1. Writer creates initial essay
    # 2. For each revision:
    #    a. Critic reviews the essay
    #    b. Writer revises based on feedback
    # 3. Return a dict with "drafts", "feedback_rounds", "final_essay", "topic"
    # TODO 3 START
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
        
        # TODO: Critic reviews
        # Store feedback in result["feedback_rounds"]
        feedback = critic_agent(draft)
        result["feedback_rounds"].append(feedback)
        print(f"Feedback:\n{feedback}\n")
        
        # TODO: Writer revises
        # Store revised draft in result["drafts"]
        draft = writer_agent(topic, previous_feedback=feedback)
        result["drafts"].append(draft)
        print(f"Revised Draft:\n{draft}\n")
    
    result["final_essay"] = draft
    # TODO 3 END
    
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
