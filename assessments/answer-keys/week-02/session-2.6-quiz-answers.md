# Session 2.6 Quiz — Answer Key

---

**1. Answer: C**

Leaving tone interpretation to the model case-by-case is exactly the gap few-shot examples and explicit tone definitions exist to close. Without anchoring, "appropriate" will drift depending on subtle differences in ticket phrasing — sometimes warm, sometimes flat, sometimes overly casual — even though nothing about the actual instruction changed. This is the tone-consistency problem the session's worked example specifically addresses by pairing role framing with concrete example replies.

---

**2. Answer: C**

Chain-of-thought reasoning improves the quality of a decision (here, whether to escalate, and how confident to be) without that reasoning needing to be customer-visible. This is a different pattern from "show your work" chain-of-thought used in math/reasoning exercises earlier in the week — sometimes the value of structured thinking is a better final answer, not a transparent one. The schema only surfaces the *conclusions* of that reasoning (`escalate`, `confidence`), not the deliberation itself.

---

**3. Answer: False**

Successfully parsing valid JSON only confirms the *syntax* is correct — it says nothing about whether the *content* is correct. The parsed object could be missing required fields, have a `tone_applied` value outside the three allowed tones, have `confidence` as the wrong type, or otherwise violate the schema's actual constraints. This is exactly why `parse_reply()` needs a separate validation step after `json.loads()` succeeds, not just a try/except around the parse itself.

---

**4. Sample answer:**

A system that always generates a confident-sounding reply, even when it doesn't actually have enough information, will eventually generate replies that are wrong, made-up, or unhelpful — and because they're confidently worded, the customer (and possibly the support team) may trust them more than they should. Being able to flag "I don't have enough information" and route to a human is what makes the system trustworthy enough to actually deploy. A system that knows the boundary of what it can safely answer is safer than one that never admits uncertainty — this is the same principle Week 5 covers in depth under evaluation and guardrails, but it shows up here already as a basic design requirement, not an advanced add-on.

---

**5. Answer: B**

Speed and JSON-mode compatibility aren't affected by whether a prompt is named/versioned — those are non-reasons. The real reason, covered in session 2.5 and reinforced here, is that a versioned template lets you improve a prompt over time without silently breaking whatever already depends on the current behavior. If the support team's ticketing integration is built against `support_reply_v1`'s exact schema and tone behavior, you want to be able to ship `v2` deliberately, not have an in-place edit change behavior under everyone's feet.

---

**6. Sample answer:**

The JSON parses successfully — it's syntactically valid — so a parser that only checks `json.loads()` would let this through. But `"tone_applied": "casual"` is not one of the three valid tones (`empathetic`, `professional`, `concise`). The validation step should specifically check that `tone_applied` is a member of the allowed tone set, and since `"casual"` isn't, it should raise a `ValueError` describing exactly that ("tone_applied must be one of (...), got 'casual'"). The practical consequence: `generate_reply()` should catch that `ValueError` and fall back to a safe escalation response, rather than passing a reply with an unrecognized tone value downstream into a ticketing system that doesn't know what to do with it.
