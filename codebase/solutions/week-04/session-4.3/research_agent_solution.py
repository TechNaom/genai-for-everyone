"""
Session 4.3: Multi-Step Task Agent - Reference Solution

This is a complete, working implementation of a research agent with:
- Explicit planning phase
- Tool-calling execution loop
- Working memory tracking
- Clear stopping condition
"""

from anthropic import Anthropic
import json

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

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

# Simulated search database
SEARCH_RESULTS = {
    "python vs javascript performance": "Python is 10-100x slower for compute-heavy tasks but better for data science. JavaScript is faster for web apps. Trade-off: Python wins for ML/AI.",
    "pytorch vs tensorflow comparison": "PyTorch: dynamic graphs, 59% market share, preferred for research. TensorFlow: static graphs, production-proven, 38% market share. PyTorch dominates in 2024.",
    "machine learning frameworks for beginners": "Start with scikit-learn (simpler). Then PyTorch or TensorFlow. JAX for advanced users. Most popular: PyTorch for learning, TensorFlow for production.",
    "why choose pytorch over tensorflow": "PyTorch is easier to debug (dynamic graphs), more popular in research, cleaner API. TensorFlow is better for production deployment and mobile.",
    "deep learning 2024 trends": "Transformers dominate. Multimodal models (GPT-4V, Claude). Open-source models improving (Llama 2, Mistral). Focus on efficiency and smaller models.",
    "how to learn deep learning": "1. Math: linear algebra, calculus. 2. Basics: neurons, layers, backprop. 3. Frameworks: PyTorch/TensorFlow. 4. Practice: Kaggle, projects. 5. Read papers.",
    "latest ai models 2024": "OpenAI GPT-4, Anthropic Claude 3, Google Gemini, Open-source: Llama 3, Mistral. All competitive on reasoning and code.",
}

def search_web(query: str) -> str:
    """Simulate a web search."""
    query_lower = query.lower()
    for key, value in SEARCH_RESULTS.items():
        if any(word in query_lower for word in key.split()):
            return value
    return f"No direct match for '{query}'. (Would return real results in production.)"

def process_tool_call(tool_name: str, tool_input: dict) -> str:
    """Process a tool call."""
    if tool_name == "search_web":
        return search_web(tool_input["query"])
    return f"Unknown tool: {tool_name}"

def run_research_agent(user_task: str, max_iterations: int = 10) -> dict:
    """
    Run a multi-step research agent.
    
    Args:
        user_task: The research task
        max_iterations: Max tool calls before stopping (safety limit)
    
    Returns:
        A dict with plan, findings, final_result, and status.
    """
    
    messages = []
    working_memory = {
        "task": user_task,
        "plan": None,
        "findings": [],
        "final_result": None,
        "status": "in_progress",
        "iterations": 0
    }
    
    # PHASE 1: Planning
    # Ask the agent to create a plan without executing yet.
    plan_prompt = f"""You are a research agent. The user has asked:

"{user_task}"

Please create a detailed plan of the specific searches and research steps you'll take to answer this question thoroughly.
Explain:
1. What information you need to find
2. Which searches you'll run (be specific about query terms)
3. How you'll know when you have enough information

Do NOT execute the searches yet. Just plan."""

    messages.append({"role": "user", "content": plan_prompt})
    
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=1024,
        tools=TOOLS,
        messages=messages
    )
    
    # Extract and store the plan
    plan_text = "".join([block.text for block in response.content if hasattr(block, "text")])
    working_memory["plan"] = plan_text
    print(f"[PLAN PHASE]\n{plan_text}\n")
    
    messages.append({"role": "assistant", "content": response.content})
    
    # PHASE 2: Execution
    # Tell the agent to execute the plan using tools.
    execution_prompt = """Now execute your plan step by step. Use the search_web tool to find information.
After each search, note what you learned. Stop when you have enough information to answer the original question completely."""

    messages.append({"role": "user", "content": execution_prompt})
    
    # PHASE 3: Agent loop
    print("[EXECUTION PHASE]")
    for iteration in range(max_iterations):
        working_memory["iterations"] = iteration + 1
        print(f"Iteration {iteration + 1}...")
        
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=2048,
            tools=TOOLS,
            messages=messages
        )
        
        # Extract tool calls and text
        tool_calls = [block for block in response.content if hasattr(block, "type") and block.type == "tool_use"]
        text_blocks = [block for block in response.content if hasattr(block, "text")]
        
        # STOPPING CONDITION: No tool calls = agent is done
        if not tool_calls:
            print("Agent stopping (no more tool calls).")
            final_result = " ".join([block.text for block in text_blocks])
            working_memory["final_result"] = final_result
            working_memory["status"] = "completed"
            return working_memory
        
        # Add assistant response to messages
        messages.append({"role": "assistant", "content": response.content})
        
        # Process each tool call
        tool_results = []
        for tool_call in tool_calls:
            query = tool_call.input.get("query", "")
            print(f"  → search_web: {query}")
            
            result = process_tool_call(tool_call.name, tool_call.input)
            
            # Store in working memory
            working_memory["findings"].append({
                "iteration": iteration + 1,
                "query": query,
                "result": result
            })
            
            print(f"    Result: {result[:60]}...")
            
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_call.id,
                "content": result
            })
        
        # Send tool results back to agent
        messages.append({"role": "user", "content": tool_results})
    
    # If we exhaust iterations
    working_memory["status"] = "max_iterations_reached"
    return working_memory

def print_results(result: dict) -> None:
    """Pretty-print the agent results."""
    print("\n" + "="*70)
    print("RESEARCH AGENT RESULTS")
    print("="*70)
    
    print(f"\nStatus: {result['status']}")
    print(f"Iterations used: {result['iterations']}")
    
    print(f"\nPlan:\n{result['plan']}")
    
    print(f"\nSearches performed ({len(result['findings'])}):")
    for i, finding in enumerate(result['findings'], 1):
        print(f"\n  {i}. [{finding['iteration']}] Query: {finding['query']}")
        print(f"     Result: {finding['result'][:100]}...")
    
    print(f"\nFinal Summary:")
    print(result['final_result'])
    print("="*70)

# Test tasks
if __name__ == "__main__":
    test_tasks = [
        "Research the top machine learning frameworks for Python. Compare PyTorch and TensorFlow. Which is better and why?",
        "I want to learn deep learning. What's the best path to get started? What should I learn first?",
    ]
    
    for task in test_tasks:
        print(f"\nTask: {task}\n")
        result = run_research_agent(task)
        print_results(result)
        print("\n\n")
