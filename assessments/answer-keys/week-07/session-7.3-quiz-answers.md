# Answer Key — Session 7.3 Quiz

**1.** The biggest risk is running out of time with nothing that runs end to end. The countering practice is building the thinnest possible end-to-end pipeline first, before perfecting any individual piece.

**2.** (c) thinnest possible end-to-end pipeline with 3 hard-coded documents → (d) more documents added → (a) improved chunking strategy → (b) a UI. End-to-end first, then depth, then polish/presentation last.

**3.** False. Falling behind at Checkpoint 1 is exactly the signal to simplify immediately (cut a feature, hard-code something, shrink the dataset) — this is disciplined scope management, not giving up, and it's the entire point of treating checkpoints as go/no-go decisions.

**4.** Ask for help. Being stuck on the same specific error for 10-15+ minutes with no new information is the defined signal to get unblocked — this is time-management discipline, not failure. The actual failure mode this session warns against is silently struggling for 40 minutes instead.

**5.** Because "does it run" only confirms the pipeline executes without crashing — it says nothing about whether the outputs are actually correct or useful. A Week 5-style eval pass is what tells you whether the system is actually working, which is the whole distinction Session 5.1 draws between a demo and real evaluation.

**6.** An MVP-first, end-to-end approach — getting a crude full pipeline (including generation) working on day one would have surfaced the generation failure three days earlier, when there was still time to fix it, instead of discovering it only after investing heavily in one piece in isolation.

**7.** It forces an explicit, deliberate judgment call about scope and time trade-offs rather than an unexamined habit — practicing exactly the kind of reasoning a real engineering lead uses under a deadline, and making the decision visible/reviewable rather than just felt.
