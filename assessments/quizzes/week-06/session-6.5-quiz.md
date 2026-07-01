# Quiz — Session 6.5: CI/CD & Versioning for Prompts

_5-8 questions, mixed format. Answer key in `assessments/answer-keys/`._

1. Why does a "small wording change" to a prompt deserve the same review/testing rigor as a code change?
2. What does a CI regression gate for prompts compare a new version's score against, in order to decide pass/fail?
3. True or False: Because LLM outputs aren't deterministic, it's not meaningful to build an automated pass/fail check for prompt changes.
4. **Scenario:** A prompt change makes the golden dataset score drop from 92% to 78%. The CI gate's threshold is "no more than 5 points below baseline." What should happen, and why?
5. Why should prompts live as their own versioned files rather than as inline strings duplicated across several source files?
6. Should the golden dataset itself be version-controlled alongside the prompts it evaluates? Why or why not?
7. A regression is caught in production, not in CI. What's the fastest safe first response, and why is investigating the root cause not the first step?
