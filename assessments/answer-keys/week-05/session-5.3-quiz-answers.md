# Session 5.3 Quiz Answers

---

## Q1: Prompt Injection
**Answer:** B) System executes attacker's instructions hidden in user input

- Explanation: Prompt injection happens when user input contains hidden commands the system treats as valid

---

## Q2: Jailbreak Defense
**Answer:** B) "I can't do that. I have values I won't compromise on."

- A: Complies with jailbreak (wrong)
- B: Correct—clear, firm refusal
- C: Generates harmful content (wrong)
- D: Suggests you might comply (wrong)

---

## Q3: Data Leakage Prevention
**Answer:** B) Explicitly refuse to share internal instructions

- Chatbot should detect "instructions" or "system prompt" queries and refuse
- Can't rely on cleverness or hiding—must explicitly refuse

---

## Q4: Output Filtering
**Answer:** B) Block/filter the response

- Even if "bomb" appears in educational context, filtering is safer
- Output filtering is defense in depth

---

## Q5: Red-Teaming
**Answer:** A) Attacking it to find vulnerabilities before hackers do

- Red-teaming = ethical hacking your own system
- Goal: Find bugs before malicious actors do

---

## Q6: Defense in Depth
**Expected answer:**
One defense can be bypassed. Multiple layers mean attacker must overcome all layers. Example: If input validation misses an attack, output filtering catches it. If output filtering fails, monitoring detects it.

---

*Session 5.3 Answer Key | GenAI for Everyone | Week 5*
