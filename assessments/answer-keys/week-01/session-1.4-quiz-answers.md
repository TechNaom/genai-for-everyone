# Answer Key — Session 1.4 Quiz

**1.** C — The system role is set once by the developer and applies across the whole conversation; it's not something the end user writes.

**2.** False. The model itself is stateless — it has no built-in memory of earlier turns. Any sense of "remembering" comes entirely from the application re-sending the full conversation history (every prior user and assistant message) with each new request. If that history isn't sent, the model has no access to it at all.

**3.** B — The model is stateless; the persistent-memory feeling is created by the application layer silently re-sending the whole conversation every time.

**4.** Most likely bug: the code is only sending the latest user message, not the full conversation history, so the model never actually received the earlier exchange "that" was supposed to refer to. Fix: maintain a running list of all previous messages (both user and assistant turns) and include the entire list in every new request.

**5.** This means the model has no access to anything said earlier — every request looks like the start of a brand new conversation. The chatbot will appear to have no memory at all, since the model genuinely never receives previous turns; it has no way to "know" what was discussed before, because it was never given that information in the first place.

**6.** A strong answer includes: (1) the code constructs a request with role-tagged messages — system instructions, then the conversation history, ending with the new user message; (2) the request is sent to the provider's API as structured data (typically JSON); (3) the provider's servers run the model using everything in that request as context and generate a response; (4) the response comes back as structured data including the generated text plus metadata; (5) the code extracts the text and displays it; (6) for the conversation to continue correctly, the code appends both the user's message and the assistant's reply to its own running history, so the next request includes everything that came before.
