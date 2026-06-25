# Quiz — Session 1.4: Your First GenAI Application

_6 questions, mixed format. Answer key in `assessments/answer-keys/`._

**1. (Multiple choice)** Which role represents instructions set once by the developer, applying to the whole conversation?
A) user
B) assistant
C) system
D) developer

**2. (Short answer)** True or false, with justification: "The LLM remembers everything said earlier in the conversation, the same way a human would." Explain your answer.

**3. (Multiple choice)** Why does a chat app like Claude.ai or ChatGPT feel like it has continuous memory across many messages?
A) The model has built-in long-term memory
B) The application re-sends the entire conversation history with every new message
C) Each message is stored permanently inside the model's weights
D) It doesn't actually have memory — the feeling is a bug

**4. (Short answer)** A chatbot you built responds to "make that shorter" with "shorter version of what?" What's the most likely bug, and how would you fix it?

**5. (Scenario)** You're debugging a teammate's chatbot code and notice they only ever send `[{"role": "user", "content": latest_message}]` with each request — nothing else. What problem will this cause, and why?

**6. (Scenario)** Describe, in your own words, the full request-response cycle that happens when your code sends a message to an LLM API, from constructing the request to being ready for the next turn.
