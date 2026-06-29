# Session 5.5 Quiz: Guardrails & Mitigations

**6 questions. MC and short answer.**

---

## Q1: Guardrails vs. System Prompts

What's the key difference between a guardrail and a system prompt?

A) They're the same thing  
B) Guardrails enforce behavior with code; system prompts persuade the model  
C) System prompts are faster than guardrails  
D) Guardrails only work on output, system prompts only work on input  

**Answer:** B

---

## Q2: Defense Against Data Leakage

What's the MOST effective fix for a chatbot leaking secrets like passwords or API keys?

A) Add an output filter that redacts the word "password"  
B) Never put the secret in the model's context in the first place  
C) Ask the model nicely not to share secrets  
D) Encrypt the secret before adding it to context  

**Answer:** B

---

## Q3: Over-Blocking

Your input guardrail blocks any message containing the word "password," including "How do I reset my password?" This is an example of:

A) A false negative  
B) A false positive  
C) Correct behavior  
D) A jailbreak  

**Answer:** B

---

## Q4: Human Review Gates

Which scenario MOST clearly warrants a human review gate?

A) User asks "What are your business hours?"  
B) User asks the bot to approve a $2,000 refund  
C) User asks "What's your return policy?"  
D) User asks for the product catalog  

**Answer:** B

---

## Q5: Refusal Design

When a guardrail blocks a request, what should the response avoid doing?

A) Offering an alternative way to help  
B) Explaining exactly which detection pattern triggered the block  
C) Being polite  
D) Ending the conversation turn  

**Answer:** B

---

## Q6: Regression Testing Guardrails

After patching a chatbot's vulnerabilities, why is it important to re-run the exact same red-team prompts that originally found the bugs?

**Short answer:** (2-3 sentences)

---

*Session 5.5 Quiz | GenAI for Everyone | Week 5*
