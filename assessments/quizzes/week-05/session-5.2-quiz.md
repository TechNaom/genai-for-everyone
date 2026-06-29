# Session 5.2 Quiz: Evaluation Methods

**6 questions. Mix of MC, short answer, scenario.**

---

## Question 1: Rubric Grading

Which statement best describes rubric grading?

A) Fast, scalable, but often too generous  
B) Accurate, but slow and doesn't scale  
C) Cheap, but doesn't capture meaning  
D) Handles open-ended responses automatically  

**Answer:** B

---

## Question 2: LLM-as-Judge

You use Claude to score 1000 responses. It scores most highly (8/10+). What's the likely problem?

A) The responses are actually good  
B) LLM-as-judge tends to be too generous  
C) You need more examples  
D) The metric is misaligned  

**Answer:** B

---

## Question 3: Semantic Similarity

What does semantic similarity measure?

A) Exact word overlap (BLEU-like)  
B) Meaning and intent (embeddings)  
C) Grammar correctness  
D) Length of response  

**Answer:** B

---

## Question 4: Human-in-the-Loop

In human-in-the-loop evaluation, when should humans review?

A) Everything (100%)  
B) Nothing (0%, just use LLM)  
C) Uncertain or extreme cases (~20%)  
D) Random sample (10%)  

**Answer:** C

---

## Question 5: Scenario

You're evaluating 3 prompt variants on 500 examples. Which strategy is best?

A) Rubric grade all 500 manually  
B) LLM-as-judge all 500, no human review  
C) LLM-as-judge all 500, human review ~100 (uncertain cases)  
D) Semantic similarity on all 500 (no LLM)  

**Answer:** C

---

## Question 6: Method Disagreement

Your rubric grades a response 6/7 (good), but LLM-as-judge scores it 4/10 (poor). This disagreement is:

A) A problem we should ignore  
B) Informative—the methods measure different things  
C) A sign your dataset is wrong  
D) Proof LLM-as-judge is broken  

**Answer:** B

---

*Session 5.2 Quiz | GenAI for Everyone | Week 5*
