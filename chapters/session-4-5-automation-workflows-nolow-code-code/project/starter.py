"""
Session 4.5: Automation Workflows - Pro Path

Build a multi-step automation workflow:
1. Monitor inbox (simple rule)
2. Agent categorizes + extracts action items
3. Agent drafts response for urgent emails
4. Track completion and costs

This is less scaffolded. You design the structure.
"""

import json
from anthropic import Anthropic
from typing import Dict, List
from datetime import datetime

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

# Mock emails
MOCK_EMAILS = [
    {
        "id": "1",
        "from": "customer@company.com",
        "subject": "URGENT: Can't access my account",
        "body": "I've been locked out since this morning. This is blocking my work."
    },
    {
        "id": "2",
        "from": "partner@vendor.com",
        "subject": "Integration question",
        "body": "Hi, I have a quick question about the API..."
    },
    {
        "id": "3",
        "from": "alerts@monitoring.com",
        "subject": "ERROR: High CPU usage on server-03",
        "body": "Server-03 CPU is at 95%. This may impact performance."
    },
]

class EmailWorkflow:
    """Multi-step email automation workflow"""
    
    def __init__(self):
        self.results = []
        self.costs = {"simple_rule": 0, "agent_calls": 0}
        self.timestamps = {}
    
    def simple_monitor(self, email: Dict) -> bool:
        """
        Simple rule: Is this email worth processing?
        Returns True if it matches urgent patterns.
        """
        urgent_patterns = ["URGENT", "ERROR", "CRITICAL", "DOWN", "BLOCKED"]
        text = (email["subject"] + " " + email["body"]).upper()
        
        self.costs["simple_rule"] += 0  # No cost
        
        return any(pattern in text for pattern in urgent_patterns)
    
    def agent_analyze(self, email: Dict) -> Dict:
        """
        Agent: Analyze email, extract category and action items.
        """
        prompt = f"""Analyze this email and respond with JSON.

From: {email['from']}
Subject: {email['subject']}
Body: {email['body']}

Respond ONLY with valid JSON (no markdown):
{{
  "category": "urgent" | "important" | "normal",
  "action_items": ["item1", "item2"],
  "sentiment": "positive" | "neutral" | "negative",
  "priority_score": 0-10
}}"""
        
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=256,
            messages=[{"role": "user", "content": prompt}]
        )
        
        result = json.loads(response.content[0].text)
        self.costs["agent_calls"] += 0.01  # Approximate cost per call
        
        return result
    
    def agent_draft_response(self, email: Dict, analysis: Dict) -> str:
        """
        Agent: Draft a response for urgent/important emails.
        """
        if analysis["category"] == "normal":
            return None
        
        prompt = f"""Draft a professional response to this email.

From: {email['from']}
Subject: {email['subject']}
Priority: {analysis['category']}

Draft a brief, professional response (2-3 sentences):"""
        
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=150,
            messages=[{"role": "user", "content": prompt}]
        )
        
        self.costs["agent_calls"] += 0.01
        
        return response.content[0].text
    
    def process_email(self, email: Dict) -> Dict:
        """
        Main workflow for a single email.
        """
        start_time = datetime.now()
        
        result = {
            "email_id": email["id"],
            "from": email["from"],
            "subject": email["subject"],
            "passed_monitor": False,
            "analysis": None,
            "draft_response": None,
            "action_taken": None,
            "processing_time": None
        }
        
        # Step 1: Simple monitor (free)
        if not self.simple_monitor(email):
            result["action_taken"] = "skipped"
        else:
            result["passed_monitor"] = True
            
            # Step 2: Agent analysis
            analysis = self.agent_analyze(email)
            result["analysis"] = analysis
            
            # Step 3: Draft response if urgent/important
            if analysis["category"] in ["urgent", "important"]:
                draft = self.agent_draft_response(email, analysis)
                result["draft_response"] = draft
                result["action_taken"] = "draft_created"
            else:
                result["action_taken"] = "analyzed"
        
        result["processing_time"] = (datetime.now() - start_time).total_seconds()
        self.results.append(result)
        
        return result
    
    def process_batch(self, emails: List[Dict]) -> Dict:
        """
        Process a batch of emails and return summary.
        """
        print(f"Processing {len(emails)} emails...\n")
        
        for email in emails:
            result = self.process_email(email)
            self._print_result(result)
        
        return self.summary()
    
    def _print_result(self, result: Dict):
        """Pretty-print a result"""
        print(f"Email {result['email_id']}: {result['from']}")
        print(f"  Subject: {result['subject']}")
        print(f"  Passed monitor: {result['passed_monitor']}")
        if result['analysis']:
            print(f"  Category: {result['analysis']['category']}")
            print(f"  Priority: {result['analysis']['priority_score']}/10")
            print(f"  Action items: {result['analysis']['action_items']}")
        if result['draft_response']:
            print(f"  Draft: {result['draft_response'][:60]}...")
        print(f"  Action: {result['action_taken']}")
        print(f"  Time: {result['processing_time']:.2f}s\n")
    
    def summary(self) -> Dict:
        """Return workflow summary with costs and metrics"""
        total_processed = len(self.results)
        total_skipped = sum(1 for r in self.results if not r['passed_monitor'])
        total_analyzed = sum(1 for r in self.results if r['analysis'] is not None)
        total_drafted = sum(1 for r in self.results if r['draft_response'] is not None)
        total_time = sum(r['processing_time'] for r in self.results)
        
        return {
            "total_emails": total_processed,
            "skipped": total_skipped,
            "analyzed": total_analyzed,
            "drafts_created": total_drafted,
            "total_time": total_time,
            "avg_time_per_email": total_time / total_processed if total_processed > 0 else 0,
            "estimated_cost": self.costs,
            "total_cost": sum(self.costs.values())
        }

# Run the workflow
if __name__ == "__main__":
    workflow = EmailWorkflow()
    
    print("="*60)
    print("MULTI-STEP EMAIL WORKFLOW")
    print("="*60 + "\n")
    
    summary = workflow.process_batch(MOCK_EMAILS)
    
    print("="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total emails: {summary['total_emails']}")
    print(f"Skipped (simple rule): {summary['skipped']}")
    print(f"Analyzed by agent: {summary['analyzed']}")
    print(f"Drafts created: {summary['drafts_created']}")
    print(f"Total processing time: {summary['total_time']:.2f}s")
    print(f"Avg time per email: {summary['avg_time_per_email']:.2f}s")
    print(f"Estimated cost: ${summary['total_cost']:.2f}")
