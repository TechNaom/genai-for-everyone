"""
Session 2.1 Project: The Thoroughness Trap
See README.md in this folder for the full brief and an example run.

This is the Pro path build for Session 2.1: a prompt can be long,
well-formatted, and detailed-LOOKING while still being missing the one
critical piece of context that actually matters. Length and apparent
thoroughness don't guarantee correctness -- that's the whole lesson of
Part 4 ("When More Detail Stops Helping").

Each CASE below has a prompt that reads as thorough on first glance, plus a
short business situation paragraph that reveals the one detail the prompt
writer forgot. For each case, fill in:
  - missing_critical_detail: the ONE fact missing from the prompt
  - why_it_fails: one sentence on what goes wrong downstream without it
  - fixed_prompt: the thorough_prompt, rewritten to include the missing detail

No API calls needed -- this is a pure diagnostic-reasoning exercise, plain
Python, runs anywhere.
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
        "missing_critical_detail": None,   # TODO: the one fact missing from the prompt
        "why_it_fails": None,              # TODO
        "fixed_prompt": None,              # TODO
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
        "missing_critical_detail": None,
        "why_it_fails": None,
        "fixed_prompt": None,
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
        "missing_critical_detail": None,
        "why_it_fails": None,
        "fixed_prompt": None,
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
        "missing_critical_detail": None,
        "why_it_fails": None,
        "fixed_prompt": None,
    },
]


def run_diagnosis():
    incomplete = 0
    for i, case in enumerate(CASES, 1):
        print(f"\n{i}. {case['label']}")
        print(f"   Prompt (looks thorough): \"{case['thorough_prompt'][:70]}...\"")

        if (
            case["missing_critical_detail"] is None
            or case["why_it_fails"] is None
            or case["fixed_prompt"] is None
        ):
            incomplete += 1
            print("   (not yet diagnosed)")
            continue

        print(f"   Missing detail: {case['missing_critical_detail']}")
        print(f"   Why it fails:   {case['why_it_fails']}")
        print(f"   Fixed prompt:   \"{case['fixed_prompt'][:70]}...\"")

    if incomplete:
        print(f"\n{incomplete} of {len(CASES)} case(s) not yet diagnosed.")
    else:
        print(f"\nAll {len(CASES)} cases diagnosed. Compare against solution.py")


if __name__ == "__main__":
    run_diagnosis()
