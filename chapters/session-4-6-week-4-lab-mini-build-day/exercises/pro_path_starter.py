"""
Session 4.6: Week 4 Lab — Research Agent with Fact-Checking (Pro Path)

Advanced version:
1. Research agent gathers information
2. Fact-checker agent verifies claims
3. Final report includes uncertainty notes

This is less scaffolded. You design the architecture.
"""

from anthropic import Anthropic
from typing import Dict, List
import json

client = Anthropic()
MODEL_ID = "claude-3-5-sonnet-20241022"

# Mock search and fact-checking data
MOCK_SEARCH_DB = {
    "ai regulation united states": "The US approach to AI is sector-based. The NIST AI Risk Management Framework (2024) provides guidance. The FTC has issued warnings about AI risks. Congress is debating legislation.",
    "ai regulation european union": "The EU AI Act (2024) is the strictest framework globally. It categorizes AI by risk level. Enforcement begins in phases starting 2025.",
    "ai regulation china": "China's approach emphasizes state oversight. AI algorithms must pass security review. Content moderation is strict.",
    "ai regulation trends 2024": "Global trend: Moving from voluntary guidelines to legal frameworks. Key themes: transparency, accountability, data privacy.",
}

FACT_CHECK_DB = {
    "NIST AI Risk Management Framework 2024": "VERIFIED - Released in Sept 2023, updated 2024",
    "EU AI Act 2024": "PARTIALLY VERIFIED - Passed 2024, enforcement timeline varies",
    "FTC warnings about AI": "VERIFIED - Multiple warnings issued 2023-2024",
    "Congress debating AI legislation": "VERIFIED - Multiple bills proposed, none passed as of June 2024",
}

class ResearchAgentWithFactChecking:
    """Research + fact-checking workflow"""

    def __init__(self, topic: str):
        self.topic = topic
        self.findings = []
        self.draft_report = None
        self.fact_checks = []
        self.final_report = None

    def call_llm(self, prompt: str, max_tokens: int = 2048) -> str:
        """Call LLM"""
        response = client.messages.create(
            model=MODEL_ID,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    def research_phase(self) -> str:
        """Step 1: Research"""
        print("STEP 1: RESEARCH")
        print("-" * 60)

        searches = [
            f"{self.topic} united states",
            f"{self.topic} european union",
            f"{self.topic} china",
            f"{self.topic} trends 2024"
        ]

        for query in searches:
            result = MOCK_SEARCH_DB.get(query.lower(), "No results")
            self.findings.append({"query": query, "result": result})
            print(f"✓ {query}: {result[:80]}...")

        print()
        return "Research complete"

    def draft_phase(self) -> str:
        """Step 2: Draft report from research"""
        print("STEP 2: DRAFT REPORT")
        print("-" * 60)

        findings_text = "\n".join([
            f"- {f['query']}: {f['result']}"
            for f in self.findings
        ])

        prompt = f"""Write a research report on '{self.topic}'.

Research findings:
{findings_text}

Structure:
1. Executive Summary
2. Key Findings (3-4 sections)
3. Implications
4. Citations

Make it comprehensive but clear. Include specific claims that can be fact-checked."""

        self.draft_report = self.call_llm(prompt, max_tokens=1500)
        print("✓ Draft report generated")
        print(f"✓ Length: {len(self.draft_report.split())} words\n")

        return self.draft_report

    def fact_check_phase(self) -> List[Dict]:
        """Step 3: Fact-check the draft"""
        print("STEP 3: FACT-CHECKING")
        print("-" * 60)

        # Extract claims from draft (simplified)
        prompt = f"""Review this draft and list key factual claims that should be verified:

{self.draft_report}

List ONLY the claims (one per line). Focus on:
- Named laws/frameworks
- Specific dates
- Attributions ("X said", "X did")

Respond with just a numbered list."""

        claims = self.call_llm(prompt, max_tokens=512)
        print(f"Found claims to verify:\n{claims}\n")

        # Mock fact-checking
        for claim, verdict in FACT_CHECK_DB.items():
            if any(word in self.draft_report.lower() for word in claim.lower().split()):
                self.fact_checks.append({
                    "claim": claim,
                    "verdict": verdict,
                    "verified": "VERIFIED" in verdict
                })
                status = "✓" if "VERIFIED" in verdict else "⚠"
                print(f"{status} {claim}: {verdict}")

        print()
        return self.fact_checks

    def incorporate_feedback(self) -> str:
        """Step 4: Incorporate fact-check feedback"""
        print("STEP 4: REVISE BASED ON FACT-CHECKS")
        print("-" * 60)

        feedback_text = "\n".join([
            f"- {fc['claim']}: {fc['verdict']}"
            for fc in self.fact_checks
        ])

        prompt = f"""Revise this draft based on fact-checking feedback:

DRAFT:
{self.draft_report}

FACT-CHECK RESULTS:
{feedback_text}

Instructions:
1. Keep verified claims as-is
2. Flag unverified claims with "[⚠️ UNVERIFIED]"
3. Add a "Verification Notes" section at the end
4. Keep the report professional

Return the revised report:"""

        self.final_report = self.call_llm(prompt, max_tokens=1500)
        print("✓ Report revised based on fact-checks\n")

        return self.final_report

    def run(self) -> str:
        """Execute full workflow"""
        print("="*60)
        print(f"RESEARCH AGENT WITH FACT-CHECKING: {self.topic}")
        print("="*60 + "\n")

        self.research_phase()
        self.draft_phase()
        self.fact_check_phase()
        self.incorporate_feedback()

        print("="*60)
        print("FINAL REPORT (WITH FACT-CHECK ANNOTATIONS)")
        print("="*60)
        print(self.final_report)

        # Metrics
        verified_count = sum(1 for fc in self.fact_checks if fc['verified'])
        print(f"\nFact-Check Summary: {verified_count}/{len(self.fact_checks)} claims verified")

        return self.final_report

# Main
if __name__ == "__main__":
    topic = "AI regulation trends 2024-2025"

    agent = ResearchAgentWithFactChecking(topic)
    report = agent.run()
