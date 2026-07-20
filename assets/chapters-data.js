/*
  Single source of truth for the course's session roster, used by
  assets/sidebar.js to render the persistent left-hand navigation, and by
  docs/curriculum/index.html conceptually (kept in sync by hand there).

  `path` is the file path from the repo root to that session's lesson.html.
  Leave `path: null` for sessions that haven't been built yet in the new
  template — the sidebar renders those as plain, non-clickable
  "coming soon" text.

  `subtopics`, when present, is the list of that session's lesson.html
  sub-sections — `{ id, title }`, where `id` matches the anchor id on that
  section's <h2> (or its wrapping <div class="subtopic">) in lesson.html.
  The sidebar renders these nested under the session link as `#id` anchors.
  Leave it off (or empty) for sessions without a `path` yet.
*/

window.GFE_MODULES = [
  {
    title: "Week 1 — Foundations of GenAI & LLMs",
    examPath: "assessments/written-exams/week-01-exam.md",
    chapters: [
      { id: "session-1-1", num: "1.1", title: "What GenAI Actually Is (and Isn't)", path: "chapters/session-1-1-what-genai-actually-is-and-isnt/lesson.html", subtopics: [
        { id: "the-big-split", title: "The Big Split: Predictive AI vs. Generative AI" },
        { id: "how-llms-work", title: "How Generative AI (Specifically LLMs) Actually Works" },
        { id: "three-myths", title: "Three Myths That Cause Real Problems" },
        { id: "worked-scenario", title: "A Real-World Scenario, Worked Through" }
      ] },
      { id: "session-1-2", num: "1.2", title: "How LLMs Work, Without the Math Fear", path: "chapters/session-1-2-how-llms-work-without-the-math-fear/lesson.html", subtopics: [
        { id: "tokens", title: "Tokens — the actual unit an LLM \"reads\"" },
        { id: "embeddings", title: "Embeddings — turning words into math, intuitively" },
        { id: "context-window", title: "Context windows — the model's working memory" },
        { id: "putting-together", title: "Putting the three pieces together" }
      ] },
      { id: "session-1-3", num: "1.3", title: "The GenAI Landscape", path: "chapters/session-1-3-the-genai-landscape/lesson.html", subtopics: [
        { id: "players", title: "The major players — a map, not a leaderboard" },
        { id: "dimensions", title: "The dimensions that actually matter for choosing" },
        { id: "framework", title: "A practical decision framework" },
        { id: "worked", title: "A worked comparison" }
      ] },
      { id: "session-1-4", num: "1.4", title: "Your First GenAI Application", path: "chapters/session-1-4-your-first-genai-application/lesson.html", subtopics: [
        { id: "roles", title: "The three roles — system, user, assistant" },
        { id: "statelessness", title: "The most important mechanical fact — statelessness" },
        { id: "cycle", title: "The request-response cycle, end to end" },
        { id: "mistake", title: "A realistic mistake, worked through" }
      ] },
      { id: "session-1-5", num: "1.5", title: "Limitations, Hallucination & Bias", path: "chapters/session-1-5-limitations-hallucination-bias/lesson.html", subtopics: [
        { id: "hallucination", title: "Hallucination — confident, fluent, and wrong" },
        { id: "bias", title: "Where bias enters the pipeline" },
        { id: "limitations", title: "Other real limitations to know cold" },
        { id: "scenario", title: "A realistic scenario, worked through" }
      ] },
      { id: "session-1-6", num: "1.6", title: "Week 1 Lab — Mini Build Day", path: "chapters/session-1-6-week-1-lab-mini-build-day/lesson.html", subtopics: [
        { id: "the-build", title: "The build: \"Explain It To Me Simply\"" },
        { id: "why-this-tool", title: "Why this tool touches all of Week 1" },
        { id: "steps", title: "The build, step by step" },
        { id: "done-well", title: "\"Done well\" vs. \"done technically\"" },
        { id: "reflection", title: "Reflection: what clicked, what's fuzzy" }
      ] }
    ]
  },
  {
    title: "Week 2 — Prompt Engineering & Application Design",
    examPath: "assessments/written-exams/week-02-exam.md",
    chapters: [
      { id: "session-2-1", num: "2.1", title: "Anatomy of a Great Prompt", path: "chapters/session-2-1-anatomy-of-a-great-prompt/lesson.html", subtopics: [
        { id: "just-ask-nicely", title: "Why \"Just Ask Nicely\" Isn't a Strategy" },
        { id: "four-pillars", title: "The Four Pillars of a Great Prompt" },
        { id: "worked-rewrite", title: "A Worked Rewrite, Pillar by Pillar" },
        { id: "when-to-stop", title: "When More Detail Stops Helping" }
      ] },
      { id: "session-2-2", num: "2.2", title: "Prompting Techniques I — Few-Shot, Zero-Shot, Role", path: "chapters/session-2-2-prompting-techniques-i/lesson.html", subtopics: [
        { id: "zero-shot", title: "Zero-Shot Prompting — Just the Instruction" },
        { id: "few-shot", title: "Few-Shot Prompting — Show, Don't Just Tell" },
        { id: "role-prompting", title: "Role Prompting — Assigning a Persona or Expertise Frame" },
        { id: "combining", title: "Combining the Techniques" }
      ] },
      { id: "session-2-3", num: "2.3", title: "Prompting Techniques II — Chain-of-Thought, Step-Back, Self-Consistency", path: "chapters/session-2-3-prompting-techniques-ii/lesson.html", subtopics: [
        { id: "chain-of-thought", title: "Chain-of-Thought Prompting" },
        { id: "step-back", title: "Step-Back Prompting" },
        { id: "self-consistency", title: "Self-Consistency" },
        { id: "choosing-the-right-tool", title: "Choosing the Right Tool for the Job" }
      ] },
      { id: "session-2-4", num: "2.4", title: "Structured Outputs", path: "chapters/session-2-4-structured-outputs/lesson.html", subtopics: [
        { id: "harder-than-it-sounds", title: "Why Reliable JSON Is Harder Than It Sounds" },
        { id: "techniques", title: "Four Techniques That Actually Improve Reliability" },
        { id: "worked-example", title: "A Worked Example: The Resume Parser" },
        { id: "still-goes-wrong", title: "When Structured Output Still Goes Wrong" }
      ] },
      { id: "session-2-5", num: "2.5", title: "Prompt Systems, Not Just Prompts", path: "chapters/session-2-5-prompt-systems-not-just-prompts/lesson.html", subtopics: [
        { id: "prompt-vs-system", title: "A Prompt vs. A Prompt System" },
        { id: "templates-and-variables", title: "Prompt Templates and Variables" },
        { id: "organizing-a-library", title: "Organizing a Prompt Library" },
        { id: "chaining-prompts", title: "Chaining Prompts Together" }
      ] },
      { id: "session-2-6", num: "2.6", title: "Week 2 Lab — Mini Build Day", path: "chapters/session-2-6-week-2-lab-mini-build-day/lesson.html", subtopics: [
        { id: "the-build", title: "The build: a support reply generator with tone control" },
        { id: "why-this-tool", title: "Why this build needs every technique from the week" },
        { id: "steps", title: "The build, step by step" },
        { id: "done-well", title: "\"Done well\" vs. \"done technically\"" },
        { id: "reflection", title: "Reflection: what clicked, what's fuzzy" }
      ] }
    ]
  },
  {
    title: "Week 3 — Working with Data: Embeddings & RAG",
    examPath: "assessments/written-exams/week-03-exam.md",
    chapters: [
      { id: "session-3-1", num: "3.1", title: "Why LLMs Need External Knowledge", path: null, subtopics: [] },
      { id: "session-3-2", num: "3.2", title: "Embeddings Demystified", path: null, subtopics: [] },
      { id: "session-3-3", num: "3.3", title: "Vector Databases & Retrieval", path: null, subtopics: [] },
      { id: "session-3-4", num: "3.4", title: "Building a RAG Pipeline", path: null, subtopics: [] },
      { id: "session-3-5", num: "3.5", title: "RAG Failure Modes & Fixes", path: null, subtopics: [] },
      { id: "session-3-6", num: "3.6", title: "Week 3 Lab — Mini Build Day (Policy Q&A Bot)", path: null, subtopics: [] }
    ]
  },
  {
    title: "Week 4 — Tool Use, Agents & Automation",
    examPath: "assessments/written-exams/week-04-exam.md",
    chapters: [
      { id: "session-4-1", num: "4.1", title: "What \"AI Agents\" Actually Means", path: null, subtopics: [] },
      { id: "session-4-2", num: "4.2", title: "Function / Tool Calling", path: null, subtopics: [] },
      { id: "session-4-3", num: "4.3", title: "Multi-Step Task Agents", path: null, subtopics: [] },
      { id: "session-4-4", num: "4.4", title: "Multi-Agent Patterns", path: null, subtopics: [] },
      { id: "session-4-5", num: "4.5", title: "Automation Workflows — No/Low-Code + Code", path: null, subtopics: [] },
      { id: "session-4-6", num: "4.6", title: "Week 4 Lab — Mini Build Day", path: null, subtopics: [] }
    ]
  },
  {
    title: "Week 5 — Evaluation, Safety & Responsible AI",
    examPath: "assessments/written-exams/week-05-exam.md",
    chapters: [
      { id: "session-5-1", num: "5.1", title: "Why \"It Looks Good\" Isn't Evaluation", path: null, subtopics: [] },
      { id: "session-5-2", num: "5.2", title: "Evaluation Methods", path: null, subtopics: [] },
      { id: "session-5-3", num: "5.3", title: "Safety Fundamentals", path: null, subtopics: [] },
      { id: "session-5-4", num: "5.4", title: "Responsible AI & Bias in Practice", path: null, subtopics: [] },
      { id: "session-5-5", num: "5.5", title: "Guardrails & Mitigations", path: null, subtopics: [] },
      { id: "session-5-6", num: "5.6", title: "Week 5 Lab — Mini Build Day", path: null, subtopics: [] }
    ]
  },
  {
    title: "Week 6 — Deployment, Cost, Scaling & MLOps-for-GenAI",
    examPath: "assessments/written-exams/week-06-exam.md",
    chapters: [
      { id: "session-6-1", num: "6.1", title: "From Notebook to Application", path: null, subtopics: [] },
      { id: "session-6-2", num: "6.2", title: "Cost & Latency Engineering", path: null, subtopics: [] },
      { id: "session-6-3", num: "6.3", title: "Choosing & Switching Models", path: null, subtopics: [] },
      { id: "session-6-4", num: "6.4", title: "Monitoring & Observability", path: null, subtopics: [] },
      { id: "session-6-5", num: "6.5", title: "CI/CD & Versioning for Prompts", path: null, subtopics: [] },
      { id: "session-6-6", num: "6.6", title: "Week 6 Lab — Mini Build Day", path: null, subtopics: [] }
    ]
  },
  {
    title: "Week 7 — Capstone, Real-World Case Studies & Career Prep",
    examPath: null,
    chapters: [
      { id: "session-7-1", num: "7.1", title: "Capstone Kickoff", path: null, subtopics: [] },
      { id: "session-7-2", num: "7.2", title: "Real-World Case Study Day I", path: null, subtopics: [] },
      { id: "session-7-3", num: "7.3", title: "Capstone Build Day I", path: null, subtopics: [] },
      { id: "session-7-4", num: "7.4", title: "Real-World Case Study Day II + Capstone Build Day II", path: null, subtopics: [] },
      { id: "session-7-5", num: "7.5", title: "Mock Technical Interviews", path: null, subtopics: [] },
      { id: "session-7-6", num: "7.6", title: "Capstone Demo Day & Program Wrap", path: null, subtopics: [] }
    ]
  }
];
