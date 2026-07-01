# Quiz — Session 6.4: Monitoring & Observability

_5-8 questions, mixed format. Answer key in `assessments/answer-keys/`._

1. Name four pieces of information that should be logged for every GenAI request, at minimum.
2. What is "drift," and why can a system get worse in production even if the code never changed?
3. True or False: If your golden dataset scored 95% at launch, you can assume that score still holds six months later without re-checking.
4. **Scenario:** A RAG-based support bot's underlying policy documents get updated, but the vector index is never rebuilt. What kind of drift is this, and what's the symptom users would notice?
5. Why is a simple thumbs-up/thumbs-down button disproportionately valuable compared to its implementation cost?
6. You want to log every request's prompt and response for debugging. What's the safety concern from Week 5 that applies directly here, and how would you address it?
7. What's the practical difference between evaluating a system once before launch (Week 5) and monitoring it continuously after launch (this session)?
