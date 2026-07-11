const weeks = [
  {
    id: "week-01",
    title: "Foundations of GenAI & LLMs",
    theme: "Mental models, LLM basics, first app, hallucination and bias",
    folder: "week-01-foundations",
    sessions: [
      ["1.1", "What GenAI Actually Is (and Isn't)", "Predictive vs. generative AI, where LLMs fit, and how to avoid project confusion.", "session-1.1-what-genai-actually-is-and-isnt.md"],
      ["1.2", "How LLMs Work, Without the Math Fear", "Tokens, next-token prediction, embeddings, and context windows explained without math anxiety.", "session-1.2-how-llms-work-without-the-math-fear.md"],
      ["1.3", "The GenAI Landscape", "Model families, open vs. closed choices, and how to compare models for real tasks.", "session-1.3-the-genai-landscape.md"],
      ["1.4", "Your First GenAI Application", "System, user, and assistant roles plus the first working Python chat loop.", "session-1.4-your-first-genai-application.md"],
      ["1.5", "Limitations, Hallucination & Bias", "Why fluent answers can be wrong and how to spot risky model behavior early.", "session-1.5-limitations-hallucination-bias.md"],
      ["1.6", "Week 1 Lab: Mini Build Day", "Build an audience-tuned explanation tool that ties the week together.", "session-1.6-week-1-lab-mini-build-day.md"]
    ]
  },
  {
    id: "week-02",
    title: "Prompt Engineering & Application Design",
    theme: "Prompt anatomy, reasoning patterns, structured outputs, reusable prompt systems",
    folder: "week-02-prompt-engineering",
    sessions: [
      ["2.1", "Anatomy of a Great Prompt", "Clarity, context, constraints, format, and the prompt rewrite muscle.", "session-2.1-anatomy-of-a-great-prompt.md"],
      ["2.2", "Prompting Techniques I", "Zero-shot, few-shot, and role prompting for practical classification and drafting.", "session-2.2-prompting-techniques-i.md"],
      ["2.3", "Prompting Techniques II", "Step-back prompting, self-consistency, and multi-step reasoning patterns.", "session-2.3-prompting-techniques-ii.md"],
      ["2.4", "Structured Outputs", "JSON, schema-constrained generation, parsing reliability, and output contracts.", "session-2.4-structured-outputs.md"],
      ["2.5", "Prompt Systems, Not Just Prompts", "Prompt templates, variables, chaining, libraries, and maintainable prompting.", "session-2.5-prompt-systems-not-just-prompts.md"],
      ["2.6", "Week 2 Lab: Mini Build Day", "Build a customer-support reply generator with tone control and reusable prompts.", "session-2.6-week-2-lab-mini-build-day.md"]
    ]
  },
  {
    id: "week-03",
    title: "Embeddings, Data & RAG",
    theme: "External knowledge, vector search, retrieval pipelines, RAG debugging",
    folder: "week-03-embeddings-rag",
    sessions: [
      ["3.1", "Why LLMs Need External Knowledge", "Knowledge cutoffs, trusted data, and deciding when RAG is the right answer.", "session-3.1-why-llms-need-external-knowledge.md"],
      ["3.2", "Embeddings Demystified", "Vector meaning, semantic similarity, and visualizing sentence relationships.", "session-3.2-embeddings-demystified.md"],
      ["3.3", "Vector Databases & Retrieval", "Chunking, top-k retrieval, vector stores, and local retrieval experiments.", "session-3.3-vector-databases-and-retrieval.md"],
      ["3.4", "Building a RAG Pipeline", "Retrieval, augmentation, generation, citations, and grounded answers.", "session-3.4-building-a-rag-pipeline.md"],
      ["3.5", "RAG Failure Modes & Fixes", "Chunking errors, retrieval misses, context stuffing, and debugging loops.", "session-3.5-rag-failure-modes-and-fixes.md"],
      ["3.6", "Week 3 Lab: Policy Q&A Bot", "Build a company policy Q&A bot over realistic documents.", "session-3.6-week-3-lab-policy-qa-bot.md"]
    ]
  },
  {
    id: "week-04",
    title: "Agents, Tool Use & Automation",
    theme: "Tool calling, agent loops, multi-step tasks, orchestration patterns",
    folder: "week-04-agents-automation",
    sessions: [
      ["4.1", "What AI Agents Actually Means", "Agent vs. workflow vs. chatbot, plus the plan-act-observe loop.", "session-4.1-what-ai-agents-actually-means.md"],
      ["4.2", "Function / Tool Calling", "Tool schemas, model tool selection, and safe tool invocation patterns.", "session-4.2-function-tool-calling.md"],
      ["4.3", "Multi-Step Task Agents", "Planning, subtasks, stopping conditions, and traceable multi-step work.", "session-4.3-multi-step-task-agents-v2.md"],
      ["4.4", "Multi-Agent Patterns", "Orchestrator-worker, reviewer, debate, and practical collaboration patterns.", "session-4.4-multi-agent-patterns-v2.md"],
      ["4.5", "Automation Workflows", "Where agents fit, where simple automation wins, and how to combine both.", "session-4.5-automation-workflows-nolow-code-code.md"],
      ["4.6", "Week 4 Lab: Mini Build Day", "Build an agent that researches a topic and drafts a report.", "session-4.6-week-4-lab-mini-build-day.md"]
    ]
  },
  {
    id: "week-05",
    title: "Evaluation, Safety & Responsible AI",
    theme: "Golden sets, eval harnesses, red teaming, guardrails, bias and safety",
    folder: "week-05-evaluation-safety",
    sessions: [
      ["5.1", "Why It Looks Good Isn't Evaluation", "Golden datasets, regression thinking, and the danger of vibe-based scoring.", "session-5.1-why-it-looks-good-isnt-evaluation.md"],
      ["5.2", "Evaluation Methods", "Rubrics, LLM-as-judge, human review, automatic metrics, and eval harnesses.", "session-5.2-evaluation-methods-v2.md"],
      ["5.3", "Safety Fundamentals", "Prompt injection, jailbreaks, leakage, content risks, and red-team habits.", "session-5.3-safety-fundamentals-v2.md"],
      ["5.4", "Responsible AI & Bias in Practice", "Fairness, representational harm, accessibility, and practical bias audits.", "session-5.4-responsible-ai-bias-in-practice.md"],
      ["5.5", "Guardrails & Mitigations", "Input/output filtering, prompt hardening, and human review gates.", "session-5.5-guardrails-and-mitigations.md"],
      ["5.6", "Week 5 Lab: Mini Build Day", "Build an eval and safety report for a prior GenAI project.", "session-5.6-week-5-lab-mini-build-day.md"]
    ]
  },
  {
    id: "week-06",
    title: "Deployment, Cost & Scaling",
    theme: "APIs, cost, latency, model selection, monitoring, prompt CI/CD",
    folder: "week-06-deployment-scaling",
    sessions: [
      ["6.1", "From Notebook to Application", "APIs, backend structure, environment config, and secrets management.", "session-6.1-from-notebook-to-application.md"],
      ["6.2", "Cost & Latency Engineering", "Token economics, caching, task-based model choice, and optimization loops.", "session-6.2-cost-latency-engineering.md"],
      ["6.3", "Choosing & Switching Models", "Open vs. closed trade-offs, fallback strategies, and comparison experiments.", "session-6.3-choosing-switching-models.md"],
      ["6.4", "Monitoring & Observability", "Prompt logs, output traces, drift signals, and feedback loops.", "session-6.4-monitoring-observability.md"],
      ["6.5", "CI/CD & Versioning for Prompts", "Prompt versioning, regression suites, pipeline checks, and rollback.", "session-6.5-cicd-versioning-for-prompts.md"],
      ["6.6", "Week 6 Lab: Hosted Demo", "Deploy a project as a simple hosted demo with operational thinking.", "session-6.6-week-6-lab-mini-build-day.md"]
    ]
  },
  {
    id: "week-07",
    title: "Capstone & Career Prep",
    theme: "Project scoping, case studies, demos, mock interviews, portfolio readiness",
    folder: "week-07-capstone-career-prep",
    sessions: [
      ["7.1", "Capstone Kickoff", "Scope a real-world GenAI project with success criteria and a build plan.", "session-7.1-capstone-kickoff.md"],
      ["7.2", "Real-World Case Study Day I", "Analyze an industry GenAI deployment and its trade-offs.", "session-7.2-real-world-case-study-day-i.md"],
      ["7.3", "Capstone Build Day I", "Build the first working version with instructor-style checkpoints.", "session-7.3-capstone-build-day-i.md"],
      ["7.4", "Case Study II + Build Day II", "Continue the capstone while comparing another real deployment pattern.", "session-7.4-real-world-case-study-day-ii-capstone-build-day-ii.md"],
      ["7.5", "Mock Technical Interviews", "Practice GenAI system design, live problem-solving, and explanation quality.", "session-7.5-mock-technical-interviews.md"],
      ["7.6", "Capstone Demo Day", "Present, package, and position the capstone for portfolio and career use.", "session-7.6-capstone-demo-day-program-wrap.md"]
    ]
  }
];

const tabs = document.querySelector("#week-tabs");
const grid = document.querySelector("#session-grid");
const spotlight = document.querySelector("#spotlight");
const search = document.querySelector("#session-search");

let activeWeek = "all";
let activeSessionKey = "1.1";

const resourceOverrides = {
  "4.3": { exerciseSlug: "4.3-v2", quizSlug: "4.3-quiz-v2", slideSlug: "4.3-v2", slideExt: "pptx" },
  "4.4": { exerciseSlug: "4.4-v2", quizSlug: "4.4-quiz-v2", slideSlug: "4.4-v2", slideExt: "pptx" },
  "5.2": { exerciseSlug: "5.2-v2", quizSlug: "5.2-quiz-v2", slideSlug: "5.2-v2", slideExt: "pptx" },
  "5.3": { exerciseSlug: "5.3-v2", quizSlug: "5.3-quiz-v2", slideSlug: "5.3-v2", slideExt: "pptx" },
  "5.6": { slideSlug: "5.6-NOTE", slideExt: "md" },
  "6.1": { slideSlug: "6.1-NOTE", slideExt: "md" },
  "6.2": { slideSlug: "6.2-NOTE", slideExt: "md" },
  "6.3": { slideSlug: "6.3-NOTE", slideExt: "md" },
  "6.4": { slideSlug: "6.4-NOTE", slideExt: "md" },
  "6.5": { slideSlug: "6.5-NOTE", slideExt: "md" },
  "6.6": { slideSlug: "6.6-NOTE", slideExt: "md" },
  "7.1": { slideSlug: "7.1-NOTE", slideExt: "md" },
  "7.2": { slideSlug: "7.2-NOTE", slideExt: "md" },
  "7.3": { slideSlug: "7.3-NOTE", slideExt: "md" },
  "7.4": { slideSlug: "7.4-NOTE", slideExt: "md" },
  "7.5": { slideSlug: "7.5-NOTE", slideExt: "md" },
  "7.6": { slideSlug: "7.6-NOTE", slideExt: "md" }
};

function sessionLinks(week, session) {
  const sessionSlug = session[0];
  const override = resourceOverrides[sessionSlug] || {};
  const exerciseSlug = override.exerciseSlug || sessionSlug;
  const quizSlug = override.quizSlug || `${sessionSlug}-quiz`;
  const slideSlug = override.slideSlug || sessionSlug;
  const slideExt = override.slideExt || "pptx";
  const lesson = `weeks/${week.folder}/${session[3]}`;
  const quiz = `assessments/quizzes/${week.id}/session-${quizSlug}.md`;
  const exercise = `codebase/exercises/${week.id}/session-${exerciseSlug}/`;
  const slides = `assets/slides/${week.id}/session-${slideSlug}.${slideExt}`;
  const exam = `assessments/written-exams/${week.id}-exam.md`;
  const interview = `assessments/interview-questions/${week.id}-interview-qs.md`;
  const slideLabel = slideExt === "md" ? "Open slide notes" : "Open slide deck";
  return { lesson, quiz, exercise, slides, exam, interview, slideLabel };
}

function allSessions() {
  return weeks.flatMap((week) => week.sessions.map((session) => ({ week, session })));
}

function renderTabs() {
  const items = [{ id: "all", label: "All" }, ...weeks.map((week) => ({ id: week.id, label: week.id.replace("week-", "W") }))];
  tabs.innerHTML = items.map((item) => `<button class="week-tab" type="button" role="tab" aria-selected="${item.id === activeWeek}" data-week="${item.id}">${item.label}</button>`).join("");
}

function renderCards() {
  const term = search.value.trim().toLowerCase();
  const visible = allSessions().filter(({ week, session }) => {
    const haystack = `${week.title} ${week.theme} ${session.join(" ")}`.toLowerCase();
    return (activeWeek === "all" || week.id === activeWeek) && (!term || haystack.includes(term));
  });

  grid.innerHTML = visible.map(({ week, session }) => {
    const links = sessionLinks(week, session);
    const isActive = session[0] === activeSessionKey;
    return `
      <article class="session-card ${isActive ? "is-active" : ""}" data-session="${session[0]}">
        <div class="session-meta">
          <span class="session-number">Session ${session[0]}</span>
          <span>${week.id.replace("week-", "Week ")}</span>
        </div>
        <h3>${session[1]}</h3>
        <p>${session[2]}</p>
        <div class="tag-row">
          <span class="tag">${week.title}</span>
          <span class="tag">Artifact-led</span>
        </div>
        <div class="resource-row">
          <a href="${links.lesson}">Lesson</a>
          <a href="${links.quiz}">Quiz</a>
          <a href="${links.exercise}">Exercise</a>
        </div>
      </article>
    `;
  }).join("");

  const active = visible.find(({ session }) => session[0] === activeSessionKey) || visible[0] || allSessions()[0];
  activeSessionKey = active.session[0];
  renderSpotlight(active.week, active.session);
}

function renderSpotlight(week, session) {
  const links = sessionLinks(week, session);
  spotlight.innerHTML = `
    <div class="spotlight-index">${session[0]}</div>
    <p class="eyebrow">${week.title}</p>
    <h3>${session[1]}</h3>
    <p>${session[2]}</p>
    <div class="spotlight-list">
      <a href="${links.lesson}">Open lesson doc</a>
      <a href="${links.slides}">${links.slideLabel}</a>
      <a href="${links.exercise}">Open hands-on exercise</a>
      <a href="${links.quiz}">Take session quiz</a>
      <a href="${links.exam}">Week written exam</a>
      <a href="${links.interview}">Week interview prep</a>
    </div>
    <p><strong>Learning rhythm:</strong> read, build, quiz, explain, then capture one portfolio note.</p>
  `;
}

tabs.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-week]");
  if (!button) return;
  activeWeek = button.dataset.week;
  renderTabs();
  renderCards();
});

grid.addEventListener("click", (event) => {
  const card = event.target.closest(".session-card");
  if (!card) return;
  if (event.target.closest("a")) return;
  activeSessionKey = card.dataset.session;
  renderCards();
});

search.addEventListener("input", renderCards);

renderTabs();
renderCards();
