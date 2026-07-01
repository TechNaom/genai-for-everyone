# Week 5 Interview Questions: Evaluation, Safety & Responsible AI

**Topic:** Eval Methods, Prompt Injection & Safety, Bias & Responsible AI, Guardrails
**Format:** Open-ended technical questions designed for real interviews
**Difficulty:** Intermediate-Advanced (assumes understanding of Sessions 5.1–5.6)

---

## Question 1: The Eval Mindset

**The Question:**
"Someone on your team says, 'I tried the new prompt on a few examples and it looked great.' Why isn't this sufficient, and what would you ask them to produce instead?"

**What a strong answer includes:**
- ✅ Identifies the core problem: anecdotal, cherry-picked, no systematic coverage
- ✅ Names the alternative: a golden dataset (happy path, edge case, boundary, adversarial examples) scored against an explicit rubric
- ✅ Mentions repeatability: a real eval produces a comparable, trackable result over time, not a one-off impression
- ✅ Doesn't dismiss the "it looked great" observation entirely — it's a starting signal, just not sufficient evidence

**Red flags in weak answers:**
- "That's fine, if it works it works" (misses the entire eval-mindset lesson)
- Can't name what a golden dataset actually contains
- No mention of coverage (edge cases, adversarial cases)

**Follow-up if they nail it:**
"How many examples is 'enough' for a golden dataset, and does that number change based on the stakes of the system?"

---

## Question 2: Rubric Grading vs. LLM-as-Judge

**The Question:**
"Compare rubric-based grading to using an LLM as a judge. When would you choose one over the other, and what's the biggest risk of relying on LLM-as-judge alone?"

**What a strong answer includes:**
- ✅ Rubric grading: explicit, human-defined criteria, consistent but doesn't scale without automation or manual effort
- ✅ LLM-as-judge: scales well, can apply nuanced judgment, but risk of sharing blind spots with the model being evaluated (fooled by fluent-but-wrong output)
- ✅ Choosing: rubric for high-stakes/well-defined criteria, LLM-as-judge for scale or fuzzier quality dimensions — often used together
- ✅ Biggest risk: a judge model can be "fooled" the same way a careless human skim-reader would be, especially on subtle omissions

**Red flags in weak answers:**
- "LLM-as-judge is basically the same as rubric grading" (misses the different failure modes)
- No mention of scale trade-offs
- Treats either method as infallible

**Follow-up if they nail it:**
"How would you validate that your LLM-judge's scores actually correlate with real human judgment?"

---

## Question 3: Prompt Injection via Retrieved Content

**The Question:**
"Explain prompt injection, and specifically why an injection hidden inside a retrieved document is a harder problem than one typed directly into a chat box."

**What a strong answer includes:**
- ✅ Defines prompt injection: text crafted to make the model ignore its original instructions and follow the attacker's instead
- ✅ Explains the retrieved-document case: attacker doesn't need direct chat access at all — any document the retrieval step might pull in becomes an attack surface
- ✅ Notes that retrieved content is often trusted/unfiltered by default, unlike user input which may get more scrutiny
- ✅ Mentions defenses: framing retrieved content as untrusted, output filtering, index-time scanning for injection signals

**Red flags in weak answers:**
- Treats all injection vectors as equivalent
- Doesn't recognize retrieved documents as a distinct, broader attack surface
- No mention of any defense

**Follow-up if they nail it:**
"If you can't fully sanitize every document in your retrieval index, what's your next line of defense?"

---

## Question 4: Bias Requires Comparison

**The Question:**
"A stakeholder says, 'I tested our hiring tool on a resume from a woman and it gave a fair result — so we're good on bias.' What's wrong with this claim?"

**What a strong answer includes:**
- ✅ Bias is a comparative property — a single output tells you nothing about whether treatment is *unequal*
- ✅ A real bias check requires matched variants (same underlying qualifications, varied only in a demographic/framing detail) and comparing outputs
- ✅ One fair-looking output doesn't rule out disparities that would appear across many comparisons or specific edge cases
- ✅ Bonus: mentions that bias checks should be an explicit, ongoing category of testing, not a one-time spot check

**Red flags in weak answers:**
- Accepts the stakeholder's claim as sufficient
- Doesn't mention the need for a controlled comparison
- Treats bias testing as a single pass/fail check rather than ongoing

**Follow-up if they nail it:**
"Design two matched test cases you'd use to check this hiring tool for bias."

---

## Question 5: Guardrails Are Layers, Not Solutions

**The Question:**
"You add a keyword-based output filter blocking any response containing the phrase 'system prompt.' A red-team attempt still extracts your instructions using different wording. Did the guardrail fail?"

**What a strong answer includes:**
- ✅ Not a total failure — it still blocks the literal case it was designed for
- ✅ But it's not a complete fix — keyword filters are inherently bypassable by rephrasing
- ✅ The correct response: document this as an open residual risk, don't treat the guardrail as "done"
- ✅ General principle: guardrails are layers of defense, not single solutions — expect to combine several and keep testing for bypasses

**Red flags in weak answers:**
- Calls it either a complete failure or a complete success with no nuance
- Doesn't mention documenting the residual risk
- No sense that keyword filters specifically are brittle

**Follow-up if they nail it:**
"What additional layer would you add on top of the keyword filter to catch semantically similar bypasses?"

---

## Question 6: Drift Without Code Changes

**The Question:**
"Explain how a GenAI system can get measurably worse in production over several months without a single line of code changing."

**What a strong answer includes:**
- ✅ Input drift: the real distribution of user queries shifts over time (new products, new slang, new use cases) in ways the original eval dataset didn't anticipate
- ✅ Silent upstream changes: a provider updates a model behind a version alias
- ✅ For RAG specifically: underlying documents change or go stale while retrieval logic and eval dataset stay fixed
- ✅ Mentions the fix: periodic re-scoring against the golden dataset (or real traffic) plus a feedback loop, not a one-time eval at launch

**Red flags in weak answers:**
- "If the code doesn't change, the system can't get worse" (misses drift entirely)
- Only names one drift source
- No mention of ongoing monitoring as the fix

**Follow-up if they nail it:**
"How would you design an alerting threshold for drift without generating constant false alarms?"

---

## Question 7: The Eval + Safety Report

**The Question:**
"Your team's eval + safety report shows: 88% golden-dataset pass rate, one patched MEDIUM-severity red-team finding, and two bias comparisons run with no gaps found. A PM asks if you can ship today. What do you say?"

**What a strong answer includes:**
- ✅ A grounded, qualified answer (not a flat yes or no) tied to the specific numbers
- ✅ Correctly interprets "two bias comparisons, no gaps found" as limited evidence, not proof of no bias — more comparisons are needed before treating this as settled
- ✅ Names a concrete next step: ongoing monitoring, more red-teaming, expanded bias testing
- ✅ Doesn't either block shipping unreasonably or wave away real gaps

**Red flags in weak answers:**
- Unqualified "yes, ship it" or "no, not safe at all" with no reasoning tied to the actual numbers
- Treats "no bias gaps found" as proof the system is unbiased
- No mention of what should happen after shipping (monitoring)

**Follow-up if they nail it:**
"What specific metric would you monitor post-launch to catch a problem the golden dataset didn't anticipate?"

---

## Question 8: Red-Teaming Your Own System

**The Question:**
"You red-team your own system with 5 attack attempts and all 5 fail to break it. What do you conclude, and what would you do next?"

**What a strong answer includes:**
- ✅ A near-perfect defense rate on the first pass is more likely to indicate weak attacks than a truly hardened system
- ✅ Recommends going back to a broader/more creative attack catalog (injection via multiple vectors, jailbreak framings, scope-escape attempts) before declaring the system safe
- ✅ Doesn't treat "5/5 blocked" as sufficient evidence of safety on its own

**Red flags in weak answers:**
- Concludes the system is safe and stops testing
- Doesn't question whether the attacks themselves were rigorous enough

**Follow-up if they nail it:**
"Give me one attack vector you'd try next that's meaningfully different from a typical direct jailbreak attempt."

---

## Question 9: Bonus — Fairness vs. Accuracy Trade-offs

**The Question:**
"A model achieves higher overall accuracy by performing very well on the majority group and noticeably worse on a minority group. Is this an acceptable trade-off? How would you think about it?"

**What a strong answer includes:**
- ✅ Recognizes this as a fairness/parity concern, not just an aggregate accuracy question
- ✅ Names the trade-off explicitly: optimizing for overall accuracy can mask harm concentrated in a subgroup
- ✅ Discusses context-dependence: acceptability depends on stakes (a hiring/lending/healthcare decision vs. a low-stakes recommendation)
- ✅ Mentions concrete responses: reporting per-group metrics separately, setting parity thresholds, adjusting decision thresholds per group, or accepting a small aggregate accuracy cost for better parity

**Red flags in weak answers:**
- "Higher overall accuracy is always better" (ignores the distributional harm)
- No mention of stakes/context mattering
- Doesn't propose any concrete mitigation

**Follow-up if they nail it:**
"How would you explain this trade-off to a stakeholder who only cares about the headline accuracy number?"

---

## Rapid-Fire Technical Q&A

Quick checks during interviews:

1. **"What's a golden dataset?"**
   → Answer: A curated set of examples with expected outputs, covering happy path, edge, boundary, and adversarial cases, scored against an explicit rubric.

2. **"What's the difference between a regression test and a one-time eval?"**
   → Answer: A regression test compares a new version's score against a known-good baseline to catch degradation; a one-time eval just measures current performance in isolation.

3. **"Name one RAG-specific prompt injection vector."**
   → Answer: Malicious instructions embedded inside a document the retrieval step pulls into context.

4. **"What's a 'residual risk' in a safety report?"**
   → Answer: A known, honestly documented risk that remains even after mitigations were added — guardrails reduce risk, they rarely eliminate it.

5. **"Why can't you detect bias from a single model output?"**
   → Answer: Bias is about unequal treatment, which requires comparing outputs across matched variants, not judging one output alone.

6. **"What's the difference between input filtering and output filtering as guardrails?"**
   → Answer: Input filtering screens what goes into the model (blocking known attack patterns); output filtering screens what the model produces before it reaches the user.

7. **"What causes drift in a deployed GenAI system?"**
   → Answer: Shifts in real user input patterns, silent provider-side model updates, or stale underlying data (e.g., outdated retrieved documents) — none require a code change.

---

## Interview Strategy Tips

1. **Listen for the eval-mindset instinct:** Do they reach for "how would we measure this" before claiming something works?
2. **Probe for nuance on guardrails:** Strong candidates know guardrails are layered defenses, not single fixes.
3. **Check bias-testing literacy:** Do they understand bias requires a controlled comparison, not a single spot check?
4. **Watch for honesty under pressure:** In shipping-decision questions, do they give a grounded, qualified answer or an overconfident yes/no?
5. **Real-world grounding:** Ask for a specific example from something they've actually red-teamed or evaluated, not just theory.

---

*Week 5 Interview Questions | GenAI for Everyone | Evaluation, Safety & Responsible AI*
