"""
Session 2.1 Project: The Thoroughness Trap — reference solution.

Note: the exact wording of each fixed_prompt isn't the point — what matters
is that your version actually surfaces the missing critical detail, the same
way these do.

Run it: python solution.py
"""

CASES = [
    {
        "label": "Outage apology email",
        "thorough_prompt": (
            "Write an email to all customers explaining that our service had a "
            "4-hour outage yesterday due to a database failover issue. Apologize "
            "sincerely, explain in plain language (no jargon) what happened and "
            "what we're doing to prevent it from recurring. Keep it under 200 "
            "words, warm and professional in tone, and format it as a complete "
            "email with a subject line."
        ),
        "business_situation": (
            "Enterprise-tier customers have a contractual SLA that entitles them "
            "to an automatic service credit whenever uptime drops below 99.9% in "
            "a month -- and yesterday's outage triggered that clause. The support "
            "team already confirmed the credits are being issued automatically."
        ),
        "missing_critical_detail": (
            "The prompt never mentions the SLA service credit that Enterprise "
            "customers are contractually owed and are already receiving."
        ),
        "why_it_fails": (
            "Without that detail, the generated email apologizes but says "
            "nothing about the credit -- Enterprise customers who know their "
            "contract will notice the omission and may escalate a support "
            "ticket asking where their credit is, creating exactly the "
            "confusion the email was supposed to prevent."
        ),
        "fixed_prompt": (
            "Write an email to all customers explaining that our service had a "
            "4-hour outage yesterday due to a database failover issue. Apologize "
            "sincerely, explain in plain language (no jargon) what happened and "
            "what we're doing to prevent it from recurring. For Enterprise-tier "
            "customers specifically, note that this outage triggered our SLA's "
            "99.9% uptime clause and that their service credit is already being "
            "issued automatically -- no action needed on their part. Keep it "
            "under 200 words, warm and professional in tone, and format it as a "
            "complete email with a subject line."
        ),
    },
    {
        "label": "Candidate rejection email",
        "thorough_prompt": (
            "Write a rejection email to a job candidate who interviewed for our "
            "Senior Backend Engineer role but wasn't selected. Be kind and "
            "encouraging, thank them for their time, and invite them to apply "
            "again in the future. Keep it under 120 words and format it as a "
            "complete email with a subject line."
        ),
        "business_situation": (
            "This candidate was referred by a current employee, Priya, on the "
            "engineering team. Company policy requires that Priya be personally "
            "notified before the rejection email goes out, so she isn't blindsided "
            "when the candidate mentions it to her."
        ),
        "missing_critical_detail": (
            "The prompt never mentions that the candidate was an employee "
            "referral, or the policy requirement to notify the referring "
            "employee first."
        ),
        "why_it_fails": (
            "The generated rejection email will be sent exactly like any other "
            "rejection, so the referring employee finds out secondhand from the "
            "candidate instead of from the company first -- an internal-policy "
            "and trust problem the prompt writer knew about but never told the "
            "model."
        ),
        "fixed_prompt": (
            "This candidate was referred by our engineer Priya. Before sending "
            "anything to the candidate, draft a short heads-up message to Priya "
            "letting her know the candidate wasn't selected, so she isn't "
            "surprised. Then write the rejection email to the candidate for our "
            "Senior Backend Engineer role: be kind and encouraging, thank them "
            "for their time, and invite them to apply again in the future. Keep "
            "the candidate email under 120 words and format it as a complete "
            "email with a subject line."
        ),
    },
    {
        "label": "Refund-processing function",
        "thorough_prompt": (
            "Write a Python function called process_refund that takes an "
            "order_id, the original charge_amount, and a requested_refund_amount. "
            "It should look up the order, log the refund request, and return a "
            "dictionary with the order_id, the approved amount, and a status "
            "string. Include a clear docstring and handle the case where the "
            "order_id doesn't exist by returning a status of 'not_found'."
        ),
        "business_situation": (
            "Finance flagged a real production bug last quarter: a support agent "
            "requested a refund amount larger than the original charge (a typo), "
            "and the system approved it -- because nothing in the code enforces "
            "that a refund can never exceed what the customer originally paid."
        ),
        "missing_critical_detail": (
            "The prompt never states the business rule that a refund must never "
            "exceed the original charge amount."
        ),
        "why_it_fails": (
            "Nothing in the specification tells the model to validate the "
            "requested amount against the charge amount, so the generated "
            "function has no bounds check -- reproducing the exact overpayment "
            "bug Finance already flagged."
        ),
        "fixed_prompt": (
            "Write a Python function called process_refund that takes an "
            "order_id, the original charge_amount, and a requested_refund_amount. "
            "It must first validate that requested_refund_amount does not exceed "
            "charge_amount and is not negative -- if it's invalid, return a "
            "status of 'invalid_amount' and do not process anything further. "
            "Otherwise, look up the order, log the refund request, and return a "
            "dictionary with the order_id, the approved amount, and a status "
            "string. Include a clear docstring and handle the case where the "
            "order_id doesn't exist by returning a status of 'not_found'."
        ),
    },
    {
        "label": "New product launch announcement",
        "thorough_prompt": (
            "Write a launch announcement for our new AI-powered journaling app, "
            "targeting a general consumer audience across all our markets. "
            "Highlight the smart prompts feature and the mood-tracking "
            "dashboard. Tone: upbeat and approachable. Keep it under 150 words, "
            "formatted as a single announcement paragraph."
        ),
        "business_situation": (
            "Legal has confirmed the app's EU data-processing agreement hasn't "
            "been finalized yet, so the product cannot legally be marketed or "
            "made available to users in the European Union until that's signed "
            "off -- the launch this prompt describes is for US and Canada only."
        ),
        "missing_critical_detail": (
            "The prompt says 'all our markets' but never mentions that the EU "
            "is legally excluded until the data-processing agreement is "
            "finalized."
        ),
        "why_it_fails": (
            "The generated announcement will read as a global launch and could "
            "be published or shared in EU-facing channels, creating a real "
            "compliance risk that legal specifically flagged as not yet cleared."
        ),
        "fixed_prompt": (
            "Write a launch announcement for our new AI-powered journaling app, "
            "targeting a general consumer audience in the US and Canada only "
            "(the EU is excluded from this launch pending a data-processing "
            "agreement, so do not imply a global or EU release). Highlight the "
            "smart prompts feature and the mood-tracking dashboard. Tone: "
            "upbeat and approachable. Keep it under 150 words, formatted as a "
            "single announcement paragraph."
        ),
    },
]


def run_diagnosis():
    for i, case in enumerate(CASES, 1):
        print(f"\n{i}. {case['label']}")
        print(f"   Missing detail: {case['missing_critical_detail']}")
        print(f"   Why it fails:   {case['why_it_fails']}")
        print(f"   Fixed prompt:   \"{case['fixed_prompt']}\"")


if __name__ == "__main__":
    run_diagnosis()
