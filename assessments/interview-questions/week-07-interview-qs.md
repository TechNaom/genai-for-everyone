# Week 7 Interview Questions: Capstone, Real-World Case Studies & Career Prep

**Topic:** Project Scoping, Case Study Analysis, Build Discipline, Interview Performance, Portfolio Presentation
**Format:** Open-ended technical and behavioral questions designed for real interviews
**Difficulty:** Intermediate-Advanced (assumes understanding of Sessions 7.1–7.6, and draws on the full program)

---

## Question 1: Walk Me Through Your Project

**The Question:**
"Walk me through a GenAI project you built."

**What a strong answer includes:**
- ✅ Leads with the problem and specific user, not a list of technologies
- ✅ Explains the approach and *why* that approach was chosen over alternatives
- ✅ Names one specific hard trade-off or decision made during building
- ✅ States actual success criteria and whether they were met, with real numbers

**Red flags in weak answers:**
- "I used LangChain, a vector database, and Claude" with no problem statement or reasoning
- No mention of how they know it worked
- Can't name a single hard decision or trade-off — suggests limited hands-on ownership

**Follow-up if they nail it:**
"What would you do differently if you rebuilt this from scratch today?"

---

## Question 2: Scoping an Ambiguous Request

**The Question:**
"Your manager says, 'Build us an AI feature for the customer portal,' with no further detail. What's your first move?"

**What a strong answer includes:**
- ✅ Doesn't start building — scopes the request first
- ✅ Asks clarifying questions targeting: specific user/problem, end-to-end description, why AI (and which kind) is actually needed, and how success will be measured
- ✅ Mentions writing this down (a short proposal) before committing engineering time

**Red flags in weak answers:**
- Jumps straight to proposing an architecture or technology stack
- Doesn't ask any clarifying questions
- Treats "AI feature" as self-evidently well-defined

**Follow-up if they nail it:**
"The manager pushes back: 'Just build something, we don't have time for a proposal.' How do you respond?"

---

## Question 3: System Design — Support Documentation Assistant

**The Question:**
"Design a GenAI feature that helps new employees find answers in company documentation. Walk me through your approach."

**What a strong answer includes:**
- ✅ Starts with clarifying questions (who exactly, what documentation, how is this failing today) before describing architecture
- ✅ Correctly identifies this as a RAG use case and explains why (need for grounding in real, current documents, not general knowledge)
- ✅ Addresses an eval plan: how would you know if answers are actually correct and helpful
- ✅ Mentions at least one operational concern: cost, latency, or what happens when the docs change (drift)

**Red flags in weak answers:**
- Jumps directly into describing a specific tech stack with no scoping questions
- No eval plan mentioned at all
- Doesn't consider what happens as underlying documents change over time

**Follow-up if they nail it:**
"How would you know if this system is getting worse over time, without anyone filing a complaint?"

---

## Question 4: Live Debugging — The Silent Accuracy Drop

**The Question:**
"An eval report shows accuracy dropped from 90% to 60% over the past month, with no code changes. Walk me through how you'd diagnose this."

**What a strong answer includes:**
- ✅ Doesn't guess at a fix immediately — investigates the specific failing examples first to find the pattern
- ✅ Considers drift explicitly: has the input distribution changed, has an underlying model or document set changed
- ✅ Checks whether the golden dataset itself is still representative, or whether it needs updating
- ✅ Proposes a systematic diagnostic process, not a single guess

**Red flags in weak answers:**
- Proposes a fix (e.g., "just retrain it" or "switch models") before investigating the actual failure pattern
- Doesn't mention drift as a possible cause
- Treats this as necessarily a code bug

**Follow-up if they nail it:**
"You find the drop is concentrated entirely in one specific question category. What does that tell you, and what would you check next?"

---

## Question 5: Reading Someone Else's System

**The Question:**
"I'm going to describe a system to you that you've never seen before: it's a support-ticket triage tool that classifies tickets and drafts suggested responses, gated by a confidence score. What would you want to know before you trusted this system?"

**What a strong answer includes:**
- ✅ Asks where evaluation happens and against what dataset
- ✅ Asks what the fallback/review path is for low-confidence or uncertain cases
- ✅ Asks how drift would be detected — is the confidence calibration re-validated over time
- ✅ Asks whether guardrails/review requirements are applied consistently across all risk levels, or unevenly

**Red flags in weak answers:**
- "Looks good to me" with no probing questions
- Only asks about the model/technology, not about evaluation or failure handling
- Doesn't ask about what happens when the system is wrong

**Follow-up if they nail it:**
"Given what you now know about this exact system, what's the single most likely place for a hidden failure to be hiding?"

---

## Question 6: The Human-in-the-Loop Trade-off

**The Question:**
"A stakeholder asks: 'Why do we need a human to review every flagged output if the model is usually right?' How do you answer?"

**What a strong answer includes:**
- ✅ Reframes "usually right" as not the relevant bar — the value of human review is specifically in catching the rare, confidently wrong cases
- ✅ Explains that in high-stakes domains, the cost of a rare miss can vastly outweigh the cost of routine review time
- ✅ Can point to a category of failure (e.g., a model treating a small wording difference as insignificant when it's actually legally/factually significant) where confidence alone would have been misleading

**Red flags in weak answers:**
- "If it's usually right, we probably don't need review" (misses the entire point of human-in-the-loop design)
- No concrete example of what a confident-but-wrong failure looks like
- Doesn't distinguish stakes/domain as a factor in the decision

**Follow-up if they nail it:**
"Under what conditions would you feel comfortable removing the human review step for a subset of cases?"

---

## Question 7: MVP-First Build Discipline

**The Question:**
"You have a week to build a working demo of a GenAI feature. Walk me through how you'd allocate your time."

**What a strong answer includes:**
- ✅ Builds the thinnest possible end-to-end pipeline first, however crude, before polishing any individual piece
- ✅ Treats early milestones as go/no-go checkpoints — if behind schedule, simplifies immediately rather than pushing forward on the original plan
- ✅ Reserves real time for an actual evaluation pass, not just "does it run"
- ✅ Mentions getting unblocked quickly (asking for help) rather than silently struggling on a single issue

**Red flags in weak answers:**
- Plans to perfect one component (e.g., retrieval quality) fully before ever testing the pipeline end to end
- No mention of evaluation time in the schedule
- No contingency plan if behind schedule partway through

**Follow-up if they nail it:**
"Day 4 of 5, you're behind schedule and only have a rough end-to-end pipeline with no eval done yet. What do you cut?"

---

## Question 8: Portfolio Presentation

**The Question:**
"Two candidates have technically similar projects. One's GitHub README is a single line: 'RAG chatbot, run python app.py.' The other has a paragraph on the problem, a screenshot, eval numbers, and run instructions. Does this matter, and why?"

**What a strong answer includes:**
- ✅ Yes, it matters — a recruiter/hiring manager skimming for under 2 minutes needs the value made instantly visible
- ✅ The fuller README demonstrates the same judgment/communication skill being assessed in "walk me through your project," just in written form
- ✅ Notes the README's real audience: a stranger with zero shared context, not someone who already knows the project

**Red flags in weak answers:**
- "The code is what matters, not the README" (misses that unreviewed code has zero signal to a time-constrained reviewer)
- No mention of the README's actual audience

**Follow-up if they nail it:**
"What's the one thing you'd cut from a README if you only had room for 4 of the 5 recommended sections?"

---

## Question 9: Bonus — Diagnosing a Vague AI Request

**The Question:**
"A VP says: 'Let's put AI on customer support, it's a mess right now.' List at least three meaningfully different projects this could mean, and the one question you'd ask first."

**What a strong answer includes:**
- ✅ Names at least 3 distinct possible projects (e.g., drafting reply suggestions, auto-routing tickets, predicting escalation risk, summarizing long threads) with different data/eval requirements
- ✅ Correctly classifies at least one as predictive vs. generative
- ✅ The clarifying question surfaces which specific pain point (speed, accuracy, agent workload) the VP actually means

**Red flags in weak answers:**
- Only identifies one possible project, or treats "AI for support" as a single well-defined task
- Clarifying question is generic ("what do you want?") rather than targeted at surfacing the ambiguity

**Follow-up if they nail it:**
"The VP says 'all of the above, whatever's fastest.' How do you push back on scoping this into one project first?"

---

## Rapid-Fire Technical Q&A

Quick checks during interviews:

1. **"What are the four things a capstone/project proposal needs to define?"**
   → Answer: Specific problem and user, end-to-end description, techniques used and why, and concrete success criteria.

2. **"Why build the thinnest end-to-end pipeline first?"**
   → Answer: It guarantees something runs completely, however crude, rather than risking several unfinished, individually-polished pieces when time runs out.

3. **"What should you do if you've been stuck on the same error for 15+ minutes with no new information?"**
   → Answer: Ask for help — that's a time-management signal, not a failure.

4. **"What's the difference between a demo and evidence a system works?"**
   → Answer: A demo shows it working on chosen examples; evidence is a scored evaluation against a golden dataset covering edge and adversarial cases.

5. **"Who is a portfolio README's real audience?"**
   → Answer: A stranger with no shared context — a recruiter or hiring manager who will spend under two minutes deciding whether to look closer.

6. **"Why might 'usually right' not be a sufficient bar for removing human review?"**
   → Answer: Because the value of review is in catching the rare, confidently wrong cases, which is exactly what a high average accuracy rate can mask.

7. **"What's the highest-leverage first move when given an ambiguous 'add AI' request?"**
   → Answer: Scope it — ask which specific problem, for which user, is actually meant, rather than starting to build.

---

## Interview Strategy Tips

1. **Listen for judgment over jargon:** A strong candidate explains *why* they made a choice, not just what tools they used.
2. **Probe scoping instincts:** Do they ask clarifying questions before proposing a solution to an ambiguous request?
3. **Check for eval-mindset carryover:** Does "how do you know it worked" come up naturally when they describe their own project?
4. **Watch for case-study-style critical thinking:** Can they read an unfamiliar system description and immediately identify what they'd want to know?
5. **Assess communication, not just correctness:** A candidate who can explain a trade-off clearly to a non-technical stakeholder is demonstrating a distinct, valuable skill.

---

*Week 7 Interview Questions | GenAI for Everyone | Capstone, Real-World Case Studies & Career Prep*
