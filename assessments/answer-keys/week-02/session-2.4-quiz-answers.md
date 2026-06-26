# Answer Key — Session 2.4 Quiz

**1.** B — Conversational wrapper text around the JSON (a common, well-documented pattern) is the most frequent cause of parsing failures, not a fundamental inability to produce JSON.

**2.** "Successfully produces parseable JSON" means it worked in your testing. "Production-reliable" means it has defensive parsing for when the model's output isn't perfect, type validation beyond just JSON syntax, explicit handling for missing data, and has been tested against a range of inputs including messy or unusual ones — not just the convenient examples used during development.

**3.** B — Letting a model guess at missing information risks a fabricated, confident-looking value being mistaken for verified data, directly connecting to Session 1.5's hallucination warning. null is an honest signal that the information wasn't found; a guess is not.

**4.** It will crash the program (raise an uncaught exception) the moment the model's output isn't perfectly valid JSON — which happens regularly in practice (wrapper text, malformed syntax). Production code should always wrap this in error handling and have a defined fallback behavior rather than letting a parsing failure take down the whole application.

**5.** A type validation check (confirming `years_experience` is actually a number, not just confirming the JSON parsed successfully) would have caught this. It matters because successfully parsed JSON can still have the wrong shape or types — JSON syntax validity and schema correctness are two different things, and only checking the former leaves real bugs undetected.

**6.** Not necessarily — 10 examples, especially if they're the "convenient" ones used during initial development, may not represent the full range of real-world inputs the prompt will eventually face. Genuine production-readiness requires testing against a broader, more representative, and intentionally messier set of inputs — this is exactly why Week 5's evaluation practices exist as a formal discipline rather than informal spot-checking.
