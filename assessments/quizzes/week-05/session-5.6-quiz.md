# Session 5.6 Quiz: Week 5 Lab

**This is a lab-focused quiz. Scenario-based questions test your understanding of the eval + safety report capstone.**

---

## Question 1: Report vs. Demo

Your teammate says "I tried it 5 times and it worked, so it's evaluated." What's missing from this claim, and what would you ask them to produce instead?

**Short answer:** (3-4 sentences)

---

## Question 2: Golden Dataset Design

You're building the golden dataset for the policy Q&A bot. Which single example is most valuable to include, and why?

A) A tenth happy-path question phrased slightly differently
B) A question where the correct answer requires a specific number from the policy document
C) A question that's identical to one already in the dataset
D) A question completely unrelated to company policy

**Answer:** B

**Why:** Numeric, document-grounded answers are exactly where RAG systems hallucinate — this is the highest-signal example, not another easy happy-path case.

---

## Question 3: Red-Teaming Your Own System

You run 5 attack attempts and all 5 fail to break your system. What's the most likely explanation?

A) Your system is unusually well-built
B) Your attacks weren't aggressive or creative enough
C) LLMs can't be attacked
D) You should stop testing since it's clearly safe

**Answer:** B

**Why:** A near-perfect defense rate on your first 5 attempts is a red flag for weak red-teaming, not a strong system — go back to Session 5.3's attack catalog (injection via documents, jailbreak framings, scope-escape questions) before concluding it's safe.

---

## Question 4: Injection via Retrieved Content

Explain, in your own words, why a prompt injected inside a *retrieved document* is a different — and often harder — problem than a prompt injected directly by the user typing into the chat box.

**Short answer:** (3-5 sentences)

**Expected answer:** The system can filter or inspect user input directly, but retrieved documents are often treated as trusted context and inserted into the prompt without the same scrutiny. An attacker doesn't need access to the chat box at all — they just need to get malicious text into any document the retrieval step might pull in, making the attack surface much larger and harder to monitor.

---

## Question 5: Bias Check Design

To check whether your policy bot treats employee questions unequally, what's the *minimum* thing you need to do?

A) Ask it one question about a sensitive topic
B) Ask the same underlying question multiple ways, varying only the demographic/framing detail, and compare answers
C) Read the system prompt and check it doesn't mention any demographics
D) Assume it's unbiased since it's just retrieving facts from a document

**Answer:** B

**Why:** Bias is a *comparative* property — you can't detect unequal treatment from a single output. You need a controlled comparison where only one variable changes.

**Rubric (1 pt):**
| Points | Criteria |
|--------|----------|
| 1 pt | Answer is B |
| 0 pts | Any other answer |

---

## Question 6: Guardrails and Residual Risk

You add an output filter that blocks any response containing the phrase "system prompt." A red-team attempt still gets the bot to describe its own instructions in different words, without using that phrase. Is your guardrail a failure? What should the report say?

**Short answer:** (4-5 sentences)

**Rubric (2 pts):**
| Points | Criteria |
|--------|----------|
| 2 pts | Recognizes the guardrail reduced but didn't eliminate risk (keyword filters are brittle/bypassable), and that the report should document this specific bypass as an open, unresolved risk rather than omit it |
| 1 pt | Notes the guardrail didn't fully work, but doesn't connect it to "keyword filters are inherently bypassable" or doesn't mention documenting it honestly |
| 0 pts | Calls the guardrail a total failure with no nuance, or claims it's fully solved |

---

## Question 7: Choosing What to Ship

Your eval + safety report shows: 90% golden dataset pass rate, 2 of 5 red-team attempts partially succeeded (both MEDIUM severity), one bias gap found and not yet fixed. Would you ship this to production today? Justify your answer.

**Short answer:** (4-6 sentences)

**Rubric (2 pts):**
| Points | Criteria |
|--------|----------|
| 2 pts | Gives a clear yes/no/conditional answer AND justifies it using the specific numbers (severity of the red-team findings, whether the bias gap affects a protected/sensitive scenario, whether 90% is acceptable for the stakes of this specific system) |
| 1 pt | Gives an answer with generic justification not tied to the specific findings |
| 0 pts | No clear position, or ignores the findings entirely |

---

*Session 5.6 Quiz | GenAI for Everyone | Week 5 Lab*
