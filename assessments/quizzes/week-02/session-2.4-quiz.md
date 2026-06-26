# Quiz — Session 2.4: Structured Outputs

_6 questions, mixed format. Answer key in `assessments/answer-keys/`._

**1. (Multiple choice)** Why might a model's JSON output fail to parse even when the model "understood" the task correctly?
A) JSON is a programming language the model can't use
B) The model may wrap the JSON in conversational text like "Sure, here's the JSON:"
C) JSON output is always truncated
D) Models cannot produce JSON under any circumstances

**2. (Short answer)** What's the difference between a prompt that "successfully produces parseable JSON" and one that's "production-reliable"?

**3. (Multiple choice)** Why should a model be instructed to return `null` for missing fields rather than guessing?
A) null is faster to generate
B) Guessing risks a confidently hallucinated value being mistaken for real data
C) JSON doesn't support guessed values
D) It makes the output shorter

**4. (Short answer)** What's wrong with code that does `json.loads(model_response)` with no error handling at all?

**5. (Scenario)** Your resume parser returns `{"years_experience": "8 years"}` instead of `{"years_experience": 8}`. The JSON parsed successfully. What additional check would have caught this, and why does it matter?

**6. (Scenario)** You've tested your extraction prompt on 10 examples and it works perfectly every time. Should you consider it production-ready? Why or why not?
