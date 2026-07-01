# Answer Key — Session 7.4 Quiz

**1.** Because the cost of a rare miss (a real legal risk slipping through unnoticed) is far higher than the cost of the extra time human review takes on the many clauses that turn out to be fine — "usually accurate" isn't the bar for a domain where the rare failure is genuinely costly, so the design intentionally never allows full automation.

**2.** Something more subtle than a bug: the model under-weighted a legally significant word substitution because it looked lexically similar to the standard clause — a near-miss in phrasing, not in meaning. The system worked exactly as designed; the design itself had a blind spot around distinguishing surface-level similarity from substantive similarity.

**3.** False. As the case study shows, two clauses can be lexically very similar (small wording difference) while being substantively very different in legal meaning — text similarity metrics can miss exactly the kind of change that matters most.

**4.** The trade-off is more manual review time on clauses that will often turn out to be fine (a small, recurring cost). It's worth it because the alternative — a high-stakes clause slipping through with a falsely low severity label — is a much larger, rarer, but far more damaging risk; the firm chose to pay a small guaranteed cost to avoid a large possible one.

**5.** Whether you're actually measuring the specific success criteria stated in your Session 7.1 proposal, not just whether the system runs or looks impressive — it's easy to keep adding features while never checking if the original "how will you know it worked" question has an actual answer yet.

**6.** It practices reading and critiquing a GenAI system you didn't build under real stakes (your own grade/portfolio, or a peer's), which is the exact skill Session 7.2 introduced — and self-review with a checklist forces the same objectivity about your own project's risks that's naturally harder to apply to your own work than to someone else's.

**7.** "Usually right" isn't the relevant bar — the value of human-in-the-loop review is specifically in catching the cases where the model is confidently, subtly wrong (as happened in this case study), not in the majority of cases it already gets right. The rare miss is exactly where the stakes are highest.
