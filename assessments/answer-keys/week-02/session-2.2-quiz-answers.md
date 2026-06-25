# Answer Key — Session 2.2 Quiz

**1.** B — The defining difference is whether example input/output pairs are included in the prompt itself.

**2.** Because the model has no strong built-in sense of what those specific, company-internal categories actually mean in practice — naming a category isn't the same as demonstrating its boundaries. Without examples, the model has to guess at the implied rules and edge cases, which is exactly where zero-shot tends to fail on unusual or specific category schemes.

**3.** B — Role prompting shifts style, vocabulary, and focus by drawing on patterns associated with that expert framing in training data; it does not add new factual knowledge or guarantee accuracy.

**4.** Because "what doesn't belong in any of these categories" is often the hardest boundary to convey through instruction alone — without an explicit "Other" or "none of the above" example, the model may force genuinely unrelated inputs into one of the named categories simply because no other option was demonstrated.

**5.** Likely issue: the 8 similar examples are mostly redundant — they reinforce the same narrow pattern rather than broadening what the model has seen. Adding more near-duplicate examples doesn't help with an edge case unlike anything already shown. Better approach: replace some of the redundant examples with examples that specifically cover different kinds of edge cases, rather than adding more volume in the same direction.

**6.** The flaw: telling a model it's "a doctor" changes the STYLE and FRAMING of its answers — drawing on patterns associated with medical-expert language — but does not grant it verified medical knowledge or guarantee factual accuracy. A confident, doctor-sounding voice is not the same as verified expert accuracy, which connects back to Session 1.5's lesson that fluency and correctness are separate properties.
