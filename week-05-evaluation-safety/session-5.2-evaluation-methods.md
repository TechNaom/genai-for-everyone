# Session 5.2: Evaluation Methods

**Week 5: Evaluation, Safety & Responsible AI**  
**Live session format:** 60–90 minutes  
**Outcome:** Build an eval harness that scores 3 prompt variants using multiple methods

---

## Why this chapter exists

Session 5.1 taught you the **eval mindset**: golden datasets, rubrics, regression testing.

This chapter teaches you the **tools and techniques** to actually do evaluation at scale:

- **Rubric grading:** Manual scoring with explicit criteria
- **LLM-as-judge:** Use an LLM to score responses automatically
- **Automatic metrics:** BLEU, ROUGE, semantic similarity
- **Human-in-the-loop:** Combine automation with human review

You'll learn when to use each, how to combine them, and how to build an evaluation harness.

---

## Part 1: Rubric Grading (Manual)

**What it is:** You score each response manually using explicit criteria.

**Pros:**
- ✅ Most accurate (humans catch nuance)
- ✅ Can score subjective qualities (tone, empathy)
- ✅ Transparent (you explain why)

**Cons:**
- ❌ Slow (1-2 minutes per response)
- ❌ Biased (your mood affects scoring)
- ❌ Doesn't scale (can't grade 10,000 responses)

**When to use:**
- Small golden dataset (10-100 examples)
- Need subjective evaluation (tone, creativity, safety)
- One-time evaluation before shipping

**Example rubric:**

```python
def grade_response(user_input, actual_output, expected_output):
    """Manual rubric grading"""
    
    # Relevance (0-2)
    relevance = 2 if expected_output in actual_output else 1
    
    # Accuracy (0-2)
    accuracy = 2  # Manual check: is it factually correct?
    
    # Tone (0-1)
    tone = 1  # Manual check: professional?
    
    # Safety (0-2)
    safety = 2  # Manual check: no hallucinations?
    
    return relevance + accuracy + tone + safety  # Out of 7
```

---

## Part 2: LLM-as-Judge (Automated)

**What it is:** Use an LLM to score responses automatically.

**Pros:**
- ✅ Fast (scores 1000s in seconds)
- ✅ Consistent (same prompt = same scores)
- ✅ Scales to large datasets
- ✅ Can score subjective qualities

**Cons:**
- ❌ Less accurate than humans (often too generous)
- ❌ Can be gamed (model favors certain styles)
- ❌ Costs money (LLM API calls)

**When to use:**
- Large dataset (1000+ examples)
- Need rapid evaluation
- Cost is acceptable ($0.01-0.10 per 100 responses)
- Combining with human review (hybrid)

**Example LLM-as-judge:**

```python
from anthropic import Anthropic

def llm_score_response(user_input, actual_output, expected_output):
    """Use LLM to score a response"""
    
    prompt = f"""Score this customer support response on a scale of 0-10.

User question: {user_input}
Expected response: {expected_output}
Actual response: {actual_output}

Criteria:
- Relevance: Does it address the question?
- Accuracy: Is information correct?
- Helpfulness: Can user act on this?
- Tone: Is it professional?

Score (0-10): """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # Parse score
    score_text = response.content[0].text.strip()
    score = int(score_text.split()[0])  # Extract first number
    
    return score
```

**Warning:** LLM-as-judge can be biased. It may:
- Favor verbose responses
- Be too generous (always score 8+)
- Hallucinate reasoning

**Mitigation:** Use reference-based scoring (compare against gold standard) and validate with humans.

---

## Part 3: Automatic Metrics

**What they are:** Computational metrics that compare actual output to expected output.

### BLEU Score
Measures n-gram overlap. Higher = more similar to expected.

```python
from nltk.translate.bleu_score import sentence_bleu

actual = "I can help you reset your password".split()
expected = "I can help you reset your password or email support".split()

# Score 0-1
score = sentence_bleu([expected], actual)  # ~0.8
```

**Pros:** Fast, simple, no LLM calls  
**Cons:** Doesn't understand meaning, harsh on paraphrasing  
**Use when:** Exact wording matters (formal docs, code)

### ROUGE Score
Measures recall of n-grams. Higher = captures expected content.

```python
from rouge import Rouge

rouge = Rouge()
scores = rouge.get_scores(actual, expected)
# Returns: precision, recall, f1-score
```

**Pros:** Better for summary evaluation  
**Cons:** Still surface-level  
**Use when:** Evaluating summaries or abstracts

### Semantic Similarity
Uses embeddings to compare meaning (not exact wording).

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

embeddings1 = model.encode(actual_output)
embeddings2 = model.encode(expected_output)

# Similarity 0-1
similarity = util.pytorch_cos_sim(embeddings1, embeddings2)  # ~0.95
```

**Pros:** Captures meaning, forgiving of paraphrasing  
**Cons:** Requires embedding model, slower  
**Use when:** Evaluating open-ended responses (explanations, summaries)

---

## Part 4: Human-in-the-Loop

**What it is:** Combine automation (fast) with humans (accurate).

**Workflow:**

```
Step 1: LLM-as-judge scores all 1000 responses (fast)
Step 2: Filter responses: flagged = score < 5 or > 8
Step 3: Human review flagged responses (small set)
Step 4: Combine LLM scores + human corrections
```

**Example:**

```python
def human_in_the_loop_eval(responses):
    # Step 1: LLM scores all
    llm_scores = [llm_score(r) for r in responses]
    
    # Step 2: Filter uncertain/extreme
    flagged = [
        (i, r, s) for i, (r, s) in enumerate(zip(responses, llm_scores))
        if s < 5 or s > 8 or s == 5  # Low, high, or uncertain
    ]
    
    # Step 3: Human reviews ~20% of data
    human_scores = {}
    for idx, response, llm_score in flagged[:len(flagged)//5]:
        human_score = input(f"Score this (0-10): {response}")
        human_scores[idx] = int(human_score)
    
    # Step 4: Combine
    final_scores = llm_scores.copy()
    for idx, human_score in human_scores.items():
        # Weight: 70% human, 30% LLM
        final_scores[idx] = 0.7 * human_score + 0.3 * llm_scores[idx]
    
    return final_scores
```

**Benefits:**
- ✅ Fast (only humans review ~20% of data)
- ✅ Accurate (human judgment on uncertain cases)
- ✅ Scalable (combine automation + humans)

---

## Part 5: Building an Evaluation Harness

An **eval harness** is code that:
1. Takes prompt variants
2. Runs them on golden dataset
3. Scores each response (using multiple methods)
4. Compares results
5. Reports which variant is best

**Example harness:**

```python
class EvalHarness:
    def __init__(self, golden_dataset):
        self.dataset = golden_dataset
        self.results = {}
    
    def eval_prompt(self, prompt_func, name):
        """Evaluate a single prompt"""
        scores = {
            "rubric": [],
            "llm_judge": [],
            "semantic": []
        }
        
        for example in self.dataset:
            response = prompt_func(example["input"])
            
            # Score using multiple methods
            scores["rubric"].append(
                grade_response(example["input"], response, example["expected"])
            )
            scores["llm_judge"].append(
                llm_score_response(example["input"], response, example["expected"])
            )
            scores["semantic"].append(
                semantic_similarity(response, example["expected"])
            )
        
        # Average scores
        self.results[name] = {
            "rubric": sum(scores["rubric"]) / len(scores["rubric"]),
            "llm_judge": sum(scores["llm_judge"]) / len(scores["llm_judge"]),
            "semantic": sum(scores["semantic"]) / len(scores["semantic"]),
        }
        
        return self.results[name]
    
    def compare(self, variant_names):
        """Compare prompt variants"""
        print("\nEvaluation Results:")
        print("-" * 60)
        
        for name in variant_names:
            scores = self.results[name]
            avg = sum(scores.values()) / len(scores)
            print(f"\n{name}:")
            print(f"  Rubric: {scores['rubric']:.1f}/7")
            print(f"  LLM Judge: {scores['llm_judge']:.1f}/10")
            print(f"  Semantic: {scores['semantic']:.2f}")
            print(f"  Average: {avg:.2f}")
```

---

## Part 6: Combining Methods

Each method has strengths and weaknesses. **Combine them:**

| Method | Accuracy | Speed | Scale | Cost |
|--------|----------|-------|-------|------|
| Rubric | ⭐⭐⭐⭐⭐ | ⭐ | ⭐ | 💰 (human time) |
| LLM-as-judge | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰 |
| BLEU | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰 |
| Semantic | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰 |
| Human-in-loop | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 💰💰💰 |

**Strategy:**

For **small dataset (< 100 examples):**
- Use manual rubric grading + semantic similarity
- Human judgment catches nuance
- Semantic similarity validates consistency

For **medium dataset (100-1000):**
- LLM-as-judge on all
- Human review of uncertain cases (20%)
- Combine for final scores

For **large dataset (1000+):**
- BLEU + semantic on all (cheap)
- LLM-as-judge on sample (expensive)
- Extrapolate results

---

## Part 7: Common Pitfalls

### ❌ Pitfall 1: Trusting one metric
"BLEU score improved, so the system is better."  
**Fix:** Use multiple metrics. They measure different things.

### ❌ Pitfall 2: LLM-as-judge hallucination
LLM scores highly but skips objective criteria.  
**Fix:** Validate LLM scores with human review on subset.

### ❌ Pitfall 3: Metric misalignment
"Semantic similarity improved" but users say responses are less helpful.  
**Fix:** Metrics should match your actual goals.

### ❌ Pitfall 4: Not documenting trade-offs
"This variant is better" but you didn't explore speed/accuracy/cost.  
**Fix:** Document trade-offs explicitly.

---

## Points to Remember

1. **No single perfect metric.** Combine rubric, LLM, and automatic methods.
2. **Rubric grading is most accurate** but slow. Use for small golden datasets.
3. **LLM-as-judge scales** but can hallucinate. Validate with humans.
4. **Automatic metrics are fast** but surface-level. Use as sanity check.
5. **Human-in-the-loop** gets best of both: automation + accuracy.
6. **Align metrics to goals.** Speed, accuracy, safety—pick your priority.

---

## Quick Check: Fill in the Blanks

1. **Rubric grading** is accurate but slow because it requires \_\_\_\_\_\_\_\_\_\_\_\_ review.
   - Answer: *manual* or *human*

2. **LLM-as-judge** can score 1000s of responses but risks \_\_\_\_\_\_\_\_\_\_\_\_ (favoring certain styles).
   - Answer: *bias* or *hallucination*

3. **BLEU score** measures n-gram overlap but misses \_\_\_\_\_\_\_\_\_\_\_\_.
   - Answer: *meaning* or *paraphrasing*

4. **Semantic similarity** captures \_\_\_\_\_\_\_\_\_\_\_\__ better than BLEU but is slower.
   - Answer: *meaning* or *intent*

5. **Human-in-the-loop** evaluates only \_\_\_\_\_\_\_\_\_\_\_\__ examples manually (maybe 20%) and uses automation for the rest.
   - Answer: *uncertain* or *flagged* or *a subset*

---

## Quiz and Interview Questions

**Full quiz:** [assessments/quizzes/week-05/session-5.2-quiz.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/quizzes/week-05/session-5.2-quiz.md)  
**Answer key:** [assessments/answer-keys/week-05/session-5.2-quiz-answers.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/answer-keys/week-05/session-5.2-quiz-answers.md)  
**Interview questions:** [assessments/interview-questions/week-05-interview-qs.md](https://github.com/TechNaom/genai-for-everyone/blob/main/assessments/interview-questions/week-05-interview-qs.md)

---

## Core path and Pro path exercises

### Core path
Build an **evaluation harness** that:
1. Takes 3 prompt variants (v1, v2, v3)
2. Runs each on 5-10 examples from golden dataset
3. Scores using:
   - Manual rubric (you score manually)
   - Semantic similarity (automatic)
4. Compares results: which variant wins?
5. Documents trade-offs

Scaffolded code. Focus on understanding the workflow.

### Pro path
Build a **multi-method eval harness**:
1. Implement rubric grading
2. Implement LLM-as-judge
3. Implement semantic similarity
4. Implement human-in-the-loop (flag uncertain scores)
5. Compare all 4 methods on same dataset
6. Analyze: which method is best for YOUR use case?

More challenging: requires understanding all methods + designing a hybrid.

---

## What's next

**Session 5.3** covers **Safety Fundamentals** — prompt injection, jailbreaks, data leakage, content risks.

For now, master evaluation methods. Combining rubric + LLM + automatic metrics gives you a production-grade evaluation system.

---

*Session 5.2 | GenAI for Everyone | Week 5: Evaluation, Safety & Responsible AI*
