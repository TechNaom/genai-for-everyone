"""
Session 4.3: Multi-Step Task Agent (Core Path Starter)

Build a research agent that:
1. Plans a strategy
2. Executes searches
3. Stops when done
4. Returns a summary

Complete the TODO sections to finish the agent loop.

Setup:
    pip install anthropic
    export ANTHROPIC_API_KEY="your-api-key-here"
"""

from anthropic import Anthropic

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

# Tools available to the agent
TOOLS = [
    {
        "name": "search_web",
        "description": "Search the web for information. Returns results as plain text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        }
    }
]

# Simulated search results (in production, call a real search API)
SEARCH_RESULTS = {
    "python vs javascript performance": "Python is generally slower for compute-heavy tasks (10-100x slower) but better for data science. JavaScript is faster for web apps.",
    "machine learning frameworks python": "PyTorch (59% market share), TensorFlow (38%), JAX, scikit-learn. PyTorch dominates for deep learning.",
    "how to learn machine learning": "Start with Python + NumPy. Take Andrew Ng's courses. Build projects on Kaggle. Read papers. Practice.",
    "artificial intelligence applications 2024": "LLMs (ChatGPT, Claude), computer vision, robotics, autonomous vehicles, healthcare diagnostics.",
}

def search_web(query: str) -> str:
    """Simulate a web search. In production, call a real search API."""
    query_lower = query.lower()
    for key, value in SEARCH_RESULTS.items():
        if any(word in query_lower for word in key.split()):
            return value
    return f"No results found for '{query}'. (In production, this would return real search results.)"

def process_tool_call(tool_name: str, tool_input: dict) -> str:
    """Process a tool call and return the result."""
    if tool_name == "search_web":
        return search_web(tool_input["query"])
    else:
        return f"Unknown tool: {tool_name}"

def run_research_agent(user_task: str) -> dict:
    """
    Run a multi-step research agent.

    Args:
        user_task: The research task (e.g., "Research machine learning frameworks and pick the best one")

    Returns:
        A dict with keys: plan, findings, final_result, status
    """

    messages = []
    working_memory = {
        "task": user_task,
        "plan": None,
        "findings": [],
        "final_result": None,
        "status": "in_progress"
    }

    # TODO 1: Create the planning prompt
    # Write a prompt that asks the agent to plan 3 research steps WITHOUT executing yet.
    # Store the prompt in a variable `plan_prompt`.
    # Hint: See Session 4.3 Part 3 for the pattern.
    # TODO 1 START
    plan_prompt = f"""TODO: Write a prompt that asks the LLM to plan 3 research steps for the task: {user_task}
Make it clear the agent should NOT execute yet, just plan."""
    # TODO 1 END

    messages.append({"role": "user", "content": plan_prompt})

    # Get the plan from the LLM
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        tools=TOOLS,
        messages=messages
    )

    # Extract plan text
    plan_text = "".join([block.text for block in response.content if hasattr(block, "text")])
    working_memory["plan"] = plan_text
    print(f"Agent's plan:\n{plan_text}\n")

    # Add assistant response to messages
    messages.append({"role": "assistant", "content": response.content})

    # TODO 2: Add the execution prompt
    # Tell the agent to now execute the plan step by step using tools.
    # Append this to `messages`.
    # TODO 2 START
    execution_prompt = "TODO: Write a prompt telling the agent to execute the plan"
    messages.append({"role": "user", "content": execution_prompt})
    # TODO 2 END

    # TODO 3: Implement the execution loop
    # Loop (max 10 iterations):
    #   1. Call client.messages.create() with messages and tools
    #   2. Extract tool calls from response
    #   3. If NO tool calls: agent is done. Extract text and return.
    #   4. If tool calls exist: process each one, add results to messages, continue.
    # TODO 3 START
    max_iterations = 10
    for iteration in range(max_iterations):
        print(f"--- Iteration {iteration + 1} ---")

        # Call the LLM
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=2048,
            tools=TOOLS,
            messages=messages
        )

        # TODO: Extract tool calls from response.content
        # Hint: Check if block.type == "tool_use"
        tool_calls = []  # TODO: Implement

        # TODO: Extract text blocks
        text_blocks = []  # TODO: Implement

        # TODO: Check stopping condition
        # If no tool calls, agent is done.
        if not tool_calls:
            print("Agent determined it's done.")
            final_text = " ".join([block.text for block in text_blocks])
            working_memory["final_result"] = final_text
            working_memory["status"] = "completed"
            return working_memory

        # Add assistant response to messages
        messages.append({"role": "assistant", "content": response.content})

        # Process tool calls
        tool_results = []
        for tool_call in tool_calls:
            print(f"  Agent calling: {tool_call.name}")
            result = process_tool_call(tool_call.name, tool_call.input)
            working_memory["findings"].append({
                "tool": tool_call.name,
                "query": tool_call.input.get("query", "N/A"),
                "result": result
            })
            print(f"    Result: {result[:80]}...")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result
            })

        # Add tool results back to messages
        messages.append({"role": "user", "content": tool_results})

    # TODO 3 END

    # If we get here, max iterations reached
    working_memory["status"] = "max_iterations_reached"
    return working_memory

# Test the agent
if __name__ == "__main__":
    # Test task
    task = "Research machine learning frameworks for Python. What are the top 3? Why?"

    print(f"Task: {task}\n")
    result = run_research_agent(task)

    print("\n=== RESULTS ===")
    print(f"Status: {result['status']}")
    print(f"\nPlan:\n{result['plan']}")
    print(f"\nFindings ({len(result['findings'])} searches):")
    for i, finding in enumerate(result['findings'], 1):
        print(f"  {i}. {finding['query']}")
    print(f"\nFinal Summary:\n{result['final_result']}")
