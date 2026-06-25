# Quiz — Session 2.2: Prompting Techniques I

_6 questions, mixed format. Answer key in `assessments/answer-keys/`._

**1. (Multiple choice)** What distinguishes few-shot prompting from zero-shot prompting?
A) Few-shot uses a different model
B) Few-shot includes example input/output pairs in the prompt; zero-shot doesn't
C) Few-shot is always more expensive
D) Zero-shot can only be used for classification

**2. (Short answer)** Why might a zero-shot prompt struggle with a company-specific classification task (e.g., internal ticket categories), even if the instruction clearly names the categories?

**3. (Multiple choice)** What does role prompting actually change about a model's output?
A) It grants the model new factual knowledge it didn't have before
B) It shifts style, vocabulary, and focus, drawing on patterns associated with that expert voice
C) It makes the model's answers automatically more accurate
D) It has no real effect on output

**4. (Short answer)** Why is a "none of the above" example often one of the most valuable few-shot examples to include?

**5. (Scenario)** You add 10 few-shot examples to a prompt, but 8 of them are very similar cases. The classifier still struggles with an edge case unlike any of your 10 examples. What's the likely issue, and what would you do differently?

**6. (Scenario)** A teammate says: "I told the model it's a doctor, so now its medical answers must be accurate." What's the flaw in this reasoning?
