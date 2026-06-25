# Answer Key — Session 1.5 Quiz

**1.** B — Hallucination specifically means fabricated content delivered with the same fluency and confidence as accurate content, not an error state or refusal.

**2.** Because fluency and accuracy are separate properties of the model's output — the model predicts the most statistically plausible continuation regardless of whether that continuation happens to be true, and it has no internal mechanism that flags uncertainty differently from confidence. Confident tone is a property of HOW the text is generated, not a signal of whether the underlying content was verified.

**3.** D — Server location isn't a documented bias entry point in this chapter's framework. Training data, prompt phrasing, and few-shot example selection all are.

**4.** Push back gently but clearly: hallucination is a structural consequence of how LLMs generate text (predicting plausible continuations, not retrieving verified facts), not a temporary bug. Newer models tend to reduce the FREQUENCY of hallucination on many tasks, but they don't eliminate the underlying possibility. Real mitigation comes from grounding answers in verified documentation (RAG, Week 3), evaluation (Week 5), and guardrails (Week 5) — not from waiting for a smarter model.

**5.** Most likely explanation: a fabricated citation. The signal: an oddly precise statistic (64.3%) attached to a specific named researcher and year, in a context where you can't independently verify the source — exactly the red-flag pattern from this session's exercise. This is a common, well-documented hallucination pattern, especially for citations.

**6.** A strong answer stays calm and mechanism-based, e.g.: "Our AI generates responses based on patterns it learned during training, not by looking up real-time facts about our specific product unless we've explicitly connected it to our documentation. In this case, it likely generated a plausible-sounding but incorrect answer because it wasn't grounded in our actual, current product information. We're working on connecting it to verified documentation so it can check facts before answering, which will reduce this kind of error significantly — though no AI system can guarantee this will never happen at all." (Full credit for any answer that avoids blaming the customer, avoids over-promising, and gives an honest, specific next step.)
