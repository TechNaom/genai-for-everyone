/*
  GenAI prompt box wiring for "GenAI for Everyone" (see CONTRIBUTING.md
  for the full spec of .genai-prompt-box).

  This does NOT grade or score a learner's prompt. An earlier version
  ran a client-side heuristic checklist and showed a score out of 5, but
  it was retired (2026-07-08) after testing showed it scored the
  course's own hand-written reference prompts below perfect (4/5, 3/5)
  — a tool that can't be satisfied by the course's best examples
  actively misleads learners about their own good prompts. This site is
  static (GitHub Pages, no backend, no API keys) and cannot send a
  prompt to a real model for grading either, so rather than fake
  precision with a heuristic score, the box simply reveals a strong
  reference prompt and tells the learner to test their own prompt
  against a real assistant. A genuine LLM-graded version is a possible
  future upgrade once this course has a backend; see CONTRIBUTING.md.

  Usage in HTML (see any chapter's lesson.html for a full example):
    <div class="genai-prompt-box">
      <p class="genai-thought"><strong>Thought process:</strong> ...</p>
      <div class="genai-try-first">
        <p class="genai-prompt-label">Write the prompt you'd give an AI assistant to build this:</p>
        <textarea class="genai-user-attempt" rows="3" placeholder="..."></textarea>
        <button type="button" class="genai-reveal-btn">Reveal a strong reference prompt</button>
        <div class="genai-compare-note" hidden>...</div>
      </div>
      <details class="genai-reveal">
        <summary>Show a strong version of this prompt</summary>
        <div class="genai-prompt-text"><pre>...</pre></div>
      </details>
    </div>

  No per-page JS is needed — this script finds every .genai-prompt-box
  on the page and wires up its own reveal button automatically, the
  same auto-wiring convention as quiz-engine.js and playground.js.
*/

(function () {
  "use strict";

  function wireUpBox(box) {
    const button = box.querySelector(".genai-reveal-btn");
    const note = box.querySelector(".genai-compare-note");
    const details = box.querySelector("details.genai-reveal");
    if (!button) return;

    button.addEventListener("click", function () {
      if (note) {
        note.hidden = false;
      }
      if (details) {
        details.open = true;
        details.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    });
  }

  function init() {
    document.querySelectorAll(".genai-prompt-box").forEach(wireUpBox);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
