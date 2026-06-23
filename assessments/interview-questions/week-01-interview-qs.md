# Week 1 Interview Questions — Foundations of GenAI & LLMs

_These mirror how real entry-level and early-career GenAI interviews actually open in 2026: fundamentals first, but probing for genuine understanding rather than memorized definitions. Interviewers consistently say they're listening for trade-off reasoning and concrete examples, not textbook recall. Use these for self-testing, peer mock interviews, or instructor-led mock rounds in Week 7._

---

## Section A — Core Concepts (Sessions 1.1–1.2)

**1. "Explain the difference between predictive and generative AI, using an example from everyday life."**
*What a strong answer includes:* a clear definition of each ("predictive selects from existing options, generative creates new content"), one concrete example of each, and ideally a note that real products sometimes combine both.

**2. "What is a token, and why does the same sentence sometimes cost more in one language than another?"**
*What a strong answer includes:* tokens as sub-word units (not letters or always whole words), the idea that common English words are often single tokens while rare words or less-common languages get split into more pieces, and the direct link to per-token API pricing.

**3. "Explain embeddings to a non-technical stakeholder, without using any math."**
*What a strong answer includes:* an analogy (a "map of meaning" works well), the key idea that similar-meaning words land close together, and ideally the king/queen example to show the relationship is learned, not programmed.

**4. "What is a context window, and what's a practical problem that can arise from a very long conversation?"**
*What a strong answer includes:* the "working memory" framing, the fact that information outside the window is invisible to the model, and a real consequence (early conversation details get "forgotten," or the "lost in the middle" effect with long documents).

**5. "Why can a large language model produce a confident, fluent, completely incorrect answer to a factual question?"**
*What a strong answer includes:* the core mechanism (predicting plausible next tokens, not retrieving verified facts), and the practical takeaway that fluency and accuracy are separate properties — this is the seed explanation for hallucination.

---

## Section B — The GenAI Landscape & First Application (Sessions 1.3–1.4)

**6. "How would you choose between an open-weight model and a closed/proprietary API for a new project?"**
*What a strong answer includes:* a structured trade-off — closed models (e.g., Claude, GPT) typically offer stronger out-of-the-box capability and zero infrastructure burden; open-weight models (e.g., Llama, Mistral) offer cost control, data privacy, and self-hosting flexibility but require GPU infrastructure and more operational work. The "right" answer depends on the constraint (cost, privacy, capability) the interviewer hints at.

**7. "Walk me through what happens, end to end, when your code sends a message to an LLM API and gets a response back."**
*What a strong answer includes:* the request/response shape (system/user/assistant roles), that the model statelessly processes the full conversation history sent with each call (it doesn't "remember" between calls on its own), and that the response comes back as structured data your code then parses and displays.

**8. "What's the difference between the system prompt, the user prompt, and the assistant's previous responses in a chat application?"**
*What a strong answer includes:* system = instructions/persona/rules set by the developer, user = the live human input, assistant = the model's own prior turns — and that all of this together is what's sent on each new request, since the model has no memory between API calls otherwise.

---

## Section C — Limitations, Hallucination & Bias (Session 1.5)

**9. "How would you explain 'hallucination' to a product manager who is panicking after seeing a wrong answer from your company's new AI feature?"**
*What a strong answer includes:* calm, non-jargon framing of why it happens, an honest statement that no current LLM eliminates this risk entirely, and a forward-looking note about mitigations (grounding in retrieved documents, evaluation, guardrails — which are covered in later weeks).

**10. "Where can bias enter a GenAI system, and is it only a 'training data' problem?"**
*What a strong answer includes:* bias can enter via training data, via how a prompt is written, via which examples are chosen for few-shot prompting, and via how outputs get evaluated — it's not a single point of failure, and addressing it requires attention across the whole pipeline.

---

## Section D — Scenario-Based (Synthesizing the whole week)

**11. "Your manager says: 'Let's add AI to our checkout flow to stop fraud.' Walk me through how you'd scope this."**
*What a strong answer includes:* recognizing this is likely a predictive AI problem (classification/scoring), not generative, and the discipline of asking clarifying questions before writing any code — what does "stop fraud" mean operationally, what data is available, what's the cost of a false positive vs. a false negative.

**12. "Give an example of a business request that sounds like it needs generative AI but is actually better solved with a simpler, non-AI approach."**
*What a strong answer includes:* a concrete example (e.g., a templated, rules-based auto-reply that doesn't actually need an LLM at all) and the reasoning for why added complexity isn't justified when a simpler tool does the job just as well.

---

### How to use this set

- **Self-testing:** cover the "what a strong answer includes" line, answer out loud, then check yourself against it.
- **Peer mock interviews:** one person asks, the other answers without notes, then swap — discuss what was missing.
- **Instructor-led mock rounds (Week 7):** these can be mixed with later-week questions to simulate a real, multi-topic interview rather than testing one week in isolation.
