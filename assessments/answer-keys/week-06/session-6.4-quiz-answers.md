# Answer Key — Session 6.4 Quiz

**1.** Any four of: the prompt/input (redacted if sensitive), the model's output, model/version used, token counts, latency, cost, and any downstream user signal (feedback, retry, abandonment).

**2.** Drift is quality degradation that happens without any code change: the questions users actually ask shift over time, a provider silently updates a model behind an alias, or (for RAG) the underlying documents change while retrieval logic stays the same. The system can "go stale" relative to a changing world even though nothing in the repository changed.

**3.** False. A golden dataset score is a snapshot — it reflects reality on the day it was measured. Input patterns, provider models, and underlying data can all drift afterward, so the score needs to be re-checked periodically, not assumed to hold indefinitely.

**4.** Retrieval drift. The symptom users would notice is the bot confidently giving outdated or wrong policy answers (grounded in stale documents) even though the underlying "policy" the company actually follows has changed — the code and retrieval logic work exactly as before, but the source of truth moved.

**5.** It's cheap to build (a single button plus logging the input/output pair with the vote) but produces a continuous stream of real, labeled examples of what's actually failing for real users — exactly the kind of high-signal data that's expensive to generate any other way, and it feeds directly back into growing your golden dataset.

**6.** The Week 5 concern is data leakage / sensitive information exposure (Session 5.3) — logs can contain personal data, secrets, or other sensitive content from user inputs or model outputs. Address it by redacting or hashing sensitive fields before logging, restricting log access, and not logging anything you wouldn't want exposed if the log storage were compromised.

**7.** Evaluating once before launch tells you the system was good at a single point in time, against examples you thought to include. Monitoring continuously after launch catches degradation caused by real-world drift (new user patterns, provider changes, stale data) that a one-time pre-launch eval can't see, because those changes hadn't happened yet when you ran it.
