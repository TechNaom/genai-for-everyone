# Session 2.6 Quiz — Week 2 Lab: Mini Build Day

*6 questions. Mixed multiple-choice and short-answer, testing whether you can combine Week 2's techniques into one working system rather than just naming them individually.*

---

**1.** A teammate writes a single prompt that tries to handle every support ticket tone by adding the sentence "respond in whatever tone seems appropriate" instead of giving the model explicit tone options and examples. What is the most likely failure mode of this approach?

A) The model will refuse to respond at all
B) The model will always default to a professional tone
C) Tone will be inconsistent across similar tickets, since "appropriate" is left for the model to interpret case by case
D) The output will no longer be valid JSON

---

**2.** In the support-reply generator design, the prompt asks the model to privately reason through several questions *before* writing the final reply, but instructs it not to include that reasoning in the output. Why design it this way instead of having the model show its reasoning to the user?

A) Showing reasoning would make the JSON output invalid
B) The reasoning step is unnecessary and could be removed without affecting output quality
C) The reasoning improves the quality of decisions like the escalate flag, but a customer-facing reply shouldn't expose internal deliberation
D) Models are not capable of multi-step reasoning, so this instruction has no real effect

---

**3.** True or False: If `parse_reply()` successfully parses a string into a JSON object, that's sufficient confirmation that the model's output is safe to use downstream.

---

**4. Short answer.** The reply generator's schema includes an `escalate` boolean and an `escalation_reason` field. Why is it important for a support-reply system to be able to say "I don't have enough information to resolve this" rather than always generating a confident-sounding reply?

---

**5.** Which of the following is the *strongest* reason to organize the support-reply prompt as a named, versioned template (e.g. `support_reply_v1`) rather than a one-off string hardcoded into the application?

A) Versioned templates run faster than hardcoded strings
B) It allows the prompt to be improved or fixed later without silently changing behavior for anyone already depending on the current version
C) JSON mode only works with named templates
D) It is required by the Anthropic API

---

**6. Short answer.** Suppose your defensive parser receives this raw model output:

```
{"reply_body": "Sure thing!", "tone_applied": "casual", "confidence": "high", "escalate": false, "escalation_reason": null}
```

Walk through what your validation logic should catch here, and what should happen as a result (don't just say "it should fail" — explain *which* check fails and why that matters).
