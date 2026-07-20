"""
Reference solution.
Session 4.5: Automation Workflows - Core Path

Build an email categorization workflow:
1. Simple rule checks if email is urgent (keywords, sender)
2. If rule is unsure, call LLM agent to categorize
3. Based on category, take action (flag, send to Slack, etc.)

Complete the TODO sections to finish the workflow.
"""

from anthropic import Anthropic
from typing import Dict, Optional

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

# Mock data (in production, these come from Gmail API)
MOCK_EMAILS = [
    {
        "id": "1",
        "from": "boss@company.com",
        "subject": "URGENT: Q4 budget approval needed",
        "body": "We need your approval on the Q4 budget ASAP."
    },
    {
        "id": "2",
        "from": "newsletter@medium.com",
        "subject": "Weekly digest: AI trends",
        "body": "Here are this week's top AI articles..."
    },
    {
        "id": "3",
        "from": "support@vendor.com",
        "subject": "Server outage - Production down",
        "body": "Production server is currently unavailable. Investigating..."
    },
]

# Step 1: Simple rule-based categorization
def simple_categorize(email: Dict) -> Optional[str]:
    """
    Simple rules to catch obvious urgent emails.
    Returns "urgent" if urgent, None if unsure.
    """
    # TODO 1: Implement simple rules
    # Check for keywords like "URGENT", "ASAP", "ERROR", "DOWN"
    # Check if sender is in VIP_CLIENTS
    # Return "urgent" if matched, None if unsure
    # TODO 1 START
    
    VIP_CLIENTS = ["boss@company.com", "ceo@company.com"]
    
    urgent_keywords = ["URGENT", "ASAP", "ERROR", "DOWN", "CRITICAL"]
    subject_upper = email["subject"].upper()
    body_upper = email["body"].upper()
    
    # Check keywords
    for keyword in urgent_keywords:
        if keyword in subject_upper or keyword in body_upper:
            return "urgent"
    
    # Check VIP senders
    if email["from"] in VIP_CLIENTS:
        return "urgent"
    
    # Unsure
    return None
    
    # TODO 1 END

def agent_categorize(email: Dict) -> str:
    """
    Use LLM agent to intelligently categorize an email.
    Returns "urgent", "important", or "normal".
    """
    # TODO 2: Write the prompt for the agent
    # Ask the agent to categorize the email based on content
    # Return one of: urgent, important, normal
    # TODO 2 START
    
    prompt = f"""Categorize this email as one of: urgent, important, normal

From: {email['from']}
Subject: {email['subject']}
Body: {email['body']}

Return ONLY the category word: urgent, important, or normal"""
    
    # TODO 2 END
    
    messages = [{"role": "user", "content": prompt}]
    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=20,
        messages=messages
    )
    
    result = response.content[0].text.strip().lower()
    # Ensure valid category
    if result not in ["urgent", "important", "normal"]:
        result = "normal"
    return result

def take_action(email: Dict, category: str) -> str:
    """
    Simple action based on category.
    In production, these would flag in Gmail, send to Slack, etc.
    """
    # TODO 3: Implement actions for each category
    # urgent → flag in Gmail, send to Slack with "🚨"
    # important → add to to-do list
    # normal → skip
    # TODO 3 START
    
    if category == "urgent":
        action = f"[FLAG IN GMAIL] + [SLACK] 🚨 Email from {email['from']}: {email['subject']}"
    elif category == "important":
        action = f"[TO-DO] Review email from {email['from']}: {email['subject']}"
    else:
        action = f"[SKIP] Email from {email['from']}"
    
    # TODO 3 END
    
    return action

def workflow(email: Dict) -> Dict:
    """
    Main workflow: Simple rule → Agent if unsure → Action
    """
    # TODO 4: Implement the workflow
    # Step 1: Try simple rule
    # Step 2: If unsure, call agent
    # Step 3: Take action based on category
    # Step 4: Return result with all info
    # TODO 4 START
    
    result = {
        "email_id": email["id"],
        "from": email["from"],
        "subject": email["subject"],
        "simple_result": None,
        "agent_result": None,
        "final_category": None,
        "action": None
    }
    
    # Step 1: Simple rule
    simple_result = simple_categorize(email)
    result["simple_result"] = simple_result
    
    # Step 2: If unsure, use agent
    if simple_result is None:
        agent_result = agent_categorize(email)
        result["agent_result"] = agent_result
        final_category = agent_result
    else:
        final_category = simple_result
    
    # Step 3: Take action
    result["final_category"] = final_category
    result["action"] = take_action(email, final_category)
    
    # TODO 4 END
    
    return result

# Test the workflow
if __name__ == "__main__":
    print("="*60)
    print("EMAIL CATEGORIZATION WORKFLOW")
    print("="*60)
    
    for email in MOCK_EMAILS:
        print(f"\n--- Email {email['id']} ---")
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        
        result = workflow(email)
        
        print(f"Simple rule: {result['simple_result']}")
        if result['agent_result']:
            print(f"Agent categorization: {result['agent_result']}")
        print(f"Final category: {result['final_category']}")
        print(f"Action: {result['action']}")
