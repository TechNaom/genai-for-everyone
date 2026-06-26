# Quiz — Session 2.5: Prompt Systems, Not Just Prompts

_6 questions, mixed format. Answer key in `assessments/answer-keys/`._

**1. (Multiple choice)** What distinguishes a prompt system from a single good prompt?
A) A prompt system always uses a bigger model
B) Reusable templates with variables, versioning, consistent testing, and often chaining
C) A prompt system never needs testing
D) There is no real difference

**2. (Short answer)** Why is storing prompts as hardcoded strings inside application logic a problem six months into a project, even if the prompts themselves are well-written?

**3. (Multiple choice)** What's a reasonable lightweight test for a prompt template, given that LLM output varies each time?
A) An exact string match against one example output
B) No testing is possible for LLM output
C) Checking for specific characteristics the output should have, like containing a required name or staying under a length
D) Only checking that the API call doesn't error

**4. (Short answer)** When is chaining multiple prompts together the right choice, versus using one larger prompt?

**5. (Scenario)** A team has 15 different prompts scattered across different files in their codebase, with no naming convention and no documentation of what variables each expects. What specific problems will this likely cause as the team grows?

**6. (Scenario)** You're deciding whether to chain a task into 3 separate prompts or use 1 combined prompt. What trade-off should you explicitly consider before deciding?
