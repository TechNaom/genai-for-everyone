"""
Reference solution.
Session 4.6: Week 4 Lab — Research Agent (Core Path)

Build a research agent that:
1. Takes a topic
2. Plans research
3. Executes searches (mocked)
4. Analyzes findings
5. Drafts a report with citations

Complete the TODO sections.
"""

from anthropic import Anthropic
from typing import Dict, List

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

# Mock search results (replace with real API in production)
MOCK_SEARCH_DB = {
    "ai regulation united states": "The US approach to AI is sector-based. The NIST AI Risk Management Framework (2024) provides guidance. The FTC has issued warnings about AI risks. Congress is debating legislation but nothing passed yet.",
    "ai regulation european union": "The EU AI Act (2024) is the strictest framework globally. It categorizes AI by risk level (prohibited, high-risk, limited-risk, minimal-risk). Enforcement begins in phases starting 2025.",
    "ai regulation china": "China's approach emphasizes state oversight. AI algorithms must pass security review. Content moderation is strict. Government maintains control over AI development.",
    "ai regulation trends 2024": "Global trend: Moving from voluntary guidelines to legal frameworks. Key themes: transparency, accountability, data privacy, bias detection.",
}

def mock_search(query: str) -> str:
    """Simulate web search with mocked results"""
    query_lower = query.lower()
    for key, value in MOCK_SEARCH_DB.items():
        if any(word in query_lower for word in key.split()):
            return value
    return f"No results found for '{query}'. (In production, call real search API.)"

class ResearchAgent:
    """Research agent that plans, researches, analyzes, and reports"""
    
    def __init__(self, topic: str):
        self.topic = topic
        self.messages = []
        self.findings = []
        self.plan_text = None
        self.report = None
    
    def call_llm(self, prompt: str, max_tokens: int = 2048) -> str:
        """Call LLM and track conversation"""
        self.messages.append({"role": "user", "content": prompt})
        
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=max_tokens,
            messages=self.messages
        )
        
        result = response.content[0].text
        self.messages.append({"role": "assistant", "content": result})
        
        return result
    
    def phase_1_plan(self) -> str:
        """Phase 1: Create research plan"""
        # TODO 1: Write a prompt that asks the agent to plan research
        # Ask for:
        # - What searches to conduct
        # - What makes a source credible
        # - How to structure the report
        # TODO 1 START
        
        prompt = f"""You are a research expert. Topic: {self.topic}

Create a detailed research plan:
1. List 4-5 specific searches you will conduct
2. Describe what makes a source credible for this topic
3. Outline how you'll structure the final report

Be specific and actionable."""
        
        # TODO 1 END
        
        self.plan_text = self.call_llm(prompt, max_tokens=512)
        print("PLAN:\n", self.plan_text, "\n")
        return self.plan_text
    
    def phase_2_research(self) -> List[Dict]:
        """Phase 2: Execute searches based on plan"""
        # TODO 2: Extract search queries from the plan
        # Parse the plan text and identify key searches
        # For each search, call mock_search() and store results
        # TODO 2 START
        
        searches = [
            f"{self.topic} united states",
            f"{self.topic} european union",
            f"{self.topic} china",
            f"{self.topic} trends 2024"
        ]
        
        for search_query in searches:
            print(f"Searching: {search_query}")
            result = mock_search(search_query)
            self.findings.append({
                "query": search_query,
                "result": result
            })
            print(f"  Found: {result[:100]}...\n")
        
        # TODO 2 END
        
        return self.findings
    
    def phase_3_analyze(self) -> str:
        """Phase 3: Analyze findings"""
        # TODO 3: Ask agent to analyze what was found
        # Format findings as text and ask agent to:
        # - Identify key themes
        # - Note conflicts or gaps
        # - Rank sources by credibility
        # TODO 3 START
        
        findings_text = "\n".join([
            f"Search: {f['query']}\nResult: {f['result']}"
            for f in self.findings
        ])
        
        prompt = f"""Based on research on '{self.topic}':

{findings_text}

Analyze:
1. What are the key themes?
2. What contradicts?
3. What gaps remain?
4. Which sources are most credible?"""
        
        analysis = self.call_llm(prompt, max_tokens=512)
        print("ANALYSIS:\n", analysis, "\n")
        
        # TODO 3 END
        
        return analysis
    
    def phase_4_draft_report(self) -> str:
        """Phase 4: Draft final report"""
        # TODO 4: Ask agent to write the final report
        # Prompt should ask for:
        # - Executive summary
        # - Main body (organized sections)
        # - Key findings
        # - Citations (reference the searches)
        # - Length: 1000+ words
        # TODO 4 START
        
        findings_text = "\n".join([
            f"- {f['query']}: {f['result']}"
            for f in self.findings
        ])
        
        prompt = f"""Write a comprehensive research report on '{self.topic}'.

Base it on this research:
{findings_text}

Structure:
1. Executive Summary (2-3 paragraphs): Overview of findings
2. Main Analysis (3-4 sections): Detailed exploration
3. Key Findings: What stands out?
4. Implications: So what?
5. Citations: Reference sources you used

Write professional, well-organized report. 1000+ words."""
        
        report = self.call_llm(prompt, max_tokens=2048)
        self.report = report
        
        # TODO 4 END
        
        return report
    
    def run(self) -> str:
        """Execute full research workflow"""
        print("="*60)
        print(f"RESEARCH AGENT: {self.topic}")
        print("="*60 + "\n")
        
        print("PHASE 1: PLANNING")
        print("-"*60)
        self.phase_1_plan()
        
        print("PHASE 2: RESEARCHING")
        print("-"*60)
        self.phase_2_research()
        
        print("PHASE 3: ANALYZING")
        print("-"*60)
        self.phase_3_analyze()
        
        print("PHASE 4: DRAFTING REPORT")
        print("-"*60)
        report = self.phase_4_draft_report()
        
        return report

# Main
if __name__ == "__main__":
    topic = "AI regulation trends 2024-2025"
    
    agent = ResearchAgent(topic)
    report = agent.run()
    
    print("\n" + "="*60)
    print("FINAL REPORT")
    print("="*60)
    print(report)
