# GenAI for Everyone — Master Curriculum Map

**Program length:** 7 weeks, 6 live sessions/week (Mon–Sat) = 40 sessions
**Audience:** Mixed — complete beginners through working professionals, in one cohort
**Format:** Daily live session (60–90 min) + self-paced exercise + end-of-session quiz
**Outcome:** Job-ready, portfolio-backed GenAI practitioner — able to design, build, evaluate, and deploy real GenAI applications

---

## Design principles

1. **One topic, two depths.** Every session has a shared concept block for all learners, then forks into:
   - **Core path** — guided hands-on, scaffolded code, lower ambiguity
   - **Pro path** — same topic, harder real-world scenario, less scaffolding, expected to extend/break/fix things
2. **Spiral, not linear.** Concepts (prompting, evaluation, safety, cost) are introduced early and revisited at increasing depth in later weeks rather than taught once and dropped.
3. **Always end in something real.** Every session produces a working artifact (a prompt library entry, a script, a mini-app, an eval report) — not just notes.
4. **Capstone-driven.** Week 7 is a applied capstone build + presentation + mock interview, assessed like a real hiring loop.

---

## Program at a glance

| Week | Theme | Job-relevance anchor |
|---|---|---|
| 1 | Foundations of GenAI & LLMs | Understand what you're actually building on |
| 2 | Prompt Engineering & Application Design | The most in-demand immediately-usable skill |
| 3 | Working with Data: Embeddings, RAG | The #1 real-world GenAI use case in industry |
| 4 | Tool Use, Agents & Automation | What "AI agents" actually means, built from scratch |
| 5 | Evaluation, Safety & Responsible AI | What separates a toy from a production system |
| 6 | Deployment, Cost, Scaling & MLOps-for-GenAI | Shipping it — the part most courses skip |
| 7 | Capstone, Real-World Case Studies & Career Prep | Job-readiness: portfolio, interviews, case studies |

---

## Week 1 — Foundations of GenAI & LLMs

**Goal:** Build accurate mental models. Kill misconceptions early. Get hands dirty with a model on day one.

| Session | Title | Core concept | Hands-on artifact |
|---|---|---|---|
| 1.1 | What GenAI Actually Is (and Isn't) | Generative vs. predictive AI, where LLMs fit in AI history | Personal "AI capability map" worksheet |
| 1.2 | How LLMs Work, Without the Math Fear | Tokens, embeddings, next-token prediction, context windows | Tokenizer playground exercise |
| 1.3 | The GenAI Landscape | Model families (GPT, Claude, Gemini, Llama, etc.), open vs. closed, when to use what | Comparison matrix of 4 models on the same task |
| 1.4 | Your First GenAI Application | Calling an LLM API, system/user/assistant roles, basic chat loop | Working CLI chatbot in Python |
| 1.5 | Limitations, Hallucination & Bias | Why models confidently make things up; bias sources | Hallucination detection exercise (spot the fake fact) |
| 1.6 | Week 1 Lab — Mini Build Day | Integration of week's concepts | Build: "Explain it to me simply" tool (topic → audience-tuned explanation) |

---

## Week 2 — Prompt Engineering & Application Design

**Goal:** Move from "talking to a chatbot" to systematically designing prompts and small applications.

| Session | Title | Core concept | Hands-on artifact |
|---|---|---|---|
| 2.1 | Anatomy of a Great Prompt | Clarity, context, constraints, format specification | Prompt rewrite exercise (bad → great) |
| 2.2 | Prompting Techniques I | Few-shot, zero-shot, role prompting | Few-shot classifier prompt |
| 2.3 | Prompting Techniques II | Chain-of-thought, step-back prompting, self-consistency | Multi-step reasoning prompt for a real business problem |
| 2.4 | Structured Outputs | JSON mode, schema-constrained generation, parsing reliability | Resume-parser prompt returning structured JSON |
| 2.5 | Prompt Systems, Not Just Prompts | Prompt templates, variables, chaining, prompt libraries | Reusable prompt template library (5+ templates) |
| 2.6 | Week 2 Lab — Mini Build Day | Integration | Build: customer-support reply generator with tone control |

---

## Week 3 — Working with Data: Embeddings & RAG

**Goal:** Understand and build Retrieval-Augmented Generation — the most common real-world GenAI architecture.

| Session | Title | Core concept | Hands-on artifact |
|---|---|---|---|
| 3.1 | Why LLMs Need External Knowledge | Knowledge cutoffs, hallucination on facts, when RAG is the answer (and when it isn't) | "RAG or not?" decision worksheet across 6 scenarios |
| 3.2 | Embeddings Demystified | Vector representations, semantic similarity, cosine distance | Visualize embeddings of 20 sentences in 2D |
| 3.3 | Vector Databases & Retrieval | Chunking strategies, vector stores, top-k retrieval | Build a local vector store over a PDF |
| 3.4 | Building a RAG Pipeline | Retrieval → augmentation → generation, citation grounding | End-to-end RAG app over a document set |
| 3.5 | RAG Failure Modes & Fixes | Chunking errors, retrieval misses, context stuffing, re-ranking | Debug a broken RAG pipeline (given) |
| 3.6 | Week 3 Lab — Mini Build Day | Integration | Build: a "company policy Q&A bot" over real-world-style docs |

---

## Week 4 — Tool Use, Agents & Automation

**Goal:** Go beyond single-turn generation — build systems that take actions, call tools, and reason in steps.

| Session | Title | Core concept | Hands-on artifact |
|---|---|---|---|
| 4.1 | What "AI Agents" Actually Means | Agent vs. workflow vs. chatbot; the agent loop (plan-act-observe) | Agent loop diagram + trace walkthrough |
| 4.2 | Function/Tool Calling | Defining tools, schema design, when models call tools | LLM that calls a real weather/calculator tool |
| 4.3 | Multi-Step Task Agents | Planning, sub-tasks, stopping conditions | Agent that completes a 3-step research task |
| 4.4 | Multi-Agent Patterns | Orchestrator-worker, debate, reviewer patterns | Two-agent system: writer + critic |
| 4.5 | Automation Workflows (No/Low-code + Code) | Where agents fit vs. simple automation; combining both | Automate a real repetitive task end-to-end |
| 4.6 | Week 4 Lab — Mini Build Day | Integration | Build: an agent that researches a topic and drafts a report |

---

## Week 5 — Evaluation, Safety & Responsible AI

**Goal:** Learn what makes GenAI systems trustworthy and production-grade, not just demo-grade.

| Session | Title | Core concept | Hands-on artifact |
|---|---|---|---|
| 5.1 | Why "It Looks Good" Isn't Evaluation | Eval mindset, golden datasets, regression testing for prompts | Build a 10-example golden test set |
| 5.2 | Evaluation Methods | Rubric grading, LLM-as-judge, human-in-the-loop, automatic metrics | Eval harness scoring 3 prompt variants |
| 5.3 | Safety Fundamentals | Prompt injection, jailbreaks, data leakage, content risks | Red-team your own app (attack exercise) |
| 5.4 | Responsible AI & Bias in Practice | Fairness, representational harm, accessibility, real incidents | Bias audit on a sample model output set |
| 5.5 | Guardrails & Mitigations | Input/output filtering, system prompt hardening, human review gates | Add guardrails to a vulnerable app from 5.3 |
| 5.6 | Week 5 Lab — Mini Build Day | Integration | Build: an eval + safety report for a Week 3/4 project |

---

## Week 6 — Deployment, Cost, Scaling & MLOps-for-GenAI

**Goal:** Ship it. Understand the operational realities most courses skip entirely.

| Session | Title | Core concept | Hands-on artifact |
|---|---|---|---|
| 6.1 | From Notebook to Application | APIs, basic backend structure, environment config, secrets management | Wrap a prior project as a proper API service |
| 6.2 | Cost & Latency Engineering | Token economics, caching, model selection by task, batching | Cost calculator + optimization exercise on a real workload |
| 6.3 | Choosing & Switching Models | Open vs. closed trade-offs, self-hosting basics, fallback strategies | Run the same task across 3 models, compare cost/quality |
| 6.4 | Monitoring & Observability | Logging prompts/outputs, drift detection, user feedback loops | Add logging + a feedback button to an app |
| 6.5 | CI/CD & Versioning for Prompts | Prompt versioning, regression suites in pipelines, rollback strategy | Set up a basic prompt-eval CI check |
| 6.6 | Week 6 Lab — Mini Build Day | Integration | Build: deploy a project as a simple hosted demo |

---

## Week 7 — Capstone, Real-World Case Studies & Career Prep

**Goal:** Synthesize everything into a portfolio piece; prepare for the actual job search.

| Session | Title | Core concept | Hands-on artifact |
|---|---|---|---|
| 7.1 | Capstone Kickoff | Scoping a real-world GenAI project, problem selection, success criteria | Capstone project proposal (1-pager) |
| 7.2 | Real-World Case Study Day I | Walkthrough of an industry GenAI deployment (support, legal, healthcare, etc.) | Case study analysis worksheet |
| 7.3 | Capstone Build Day I | Applied build time with instructor support | Working capstone v1 |
| 7.4 | Real-World Case Study Day II + Capstone Build Day II | Second industry case + continued build | Case study analysis + capstone v2 |
| 7.5 | Mock Technical Interviews | GenAI interview formats, live problem-solving, system design Qs | Mock interview (peer or instructor) + feedback |
| 7.6 | Capstone Demo Day & Program Wrap | Present capstone, peer feedback, career next-steps | Final capstone + portfolio README |

---

## Assessment map

- **Per session (40 total):** Short quiz (5–8 questions, mixed MCQ/short-answer) — `assessments/quizzes/`
- **Per week (7 total):** Written exam (deeper, scenario-based) — `assessments/written-exams/`
- **Per week (7 total):** Interview-question set tied to that week's topics — `assessments/interview-questions/`
- **Final:** Capstone rubric + mock interview scorecard — `assessments/written-exams/` and `assessments/interview-questions/`

## File naming convention

```
weeks/week-01-foundations/session-1.1-what-genai-actually-is.md
assets/slides/week-01/session-1.1.pptx
codebase/exercises/week-01/session-1.1/
assessments/quizzes/week-01/session-1.1-quiz.md
assessments/written-exams/week-01-exam.md
assessments/interview-questions/week-01-interview-qs.md
```

## Build status tracker

| Week | Lesson docs | Slides | Exercises | Quizzes | Exam | Interview Qs |
|---|---|---|---|---|---|---|
| 1 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| 2 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| 3 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| 4 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| 5 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| 6 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |
| 7 | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ | ⏳ |

*(Updated as each week is built. ⏳ pending, 🚧 in progress, ✅ done)*
