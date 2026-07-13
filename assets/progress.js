/*
  Client-side progress tracker for GenAI for Everyone.
  No backend, no accounts — progress is stored in this browser's
  localStorage only, keyed by chapter id (e.g. "chapter-01").

  A chapter is marked complete when its quiz is answered 100% correct
  (quiz-engine.js calls GFEProgress.markComplete() on a perfect score).
  Pages that list chapters (index.html, docs/curriculum/index.html) call
  GFEProgress.renderBadges() to show a "Completed" badge on any chapter
  element with a matching data-chapter-link attribute.
*/

window.GFEProgress = (function () {
  const STORAGE_KEY = "gfe-progress-v1";

  function load() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (e) {
      return {};
    }
  }

  function save(data) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    } catch (e) {
      /* localStorage unavailable (private browsing, etc.) — fail silently */
    }
  }

  function markComplete(chapterId) {
    if (!chapterId) return;
    const data = load();
    data[chapterId] = true;
    save(data);
  }

  function isComplete(chapterId) {
    return !!load()[chapterId];
  }

  function completedCount() {
    return Object.keys(load()).length;
  }

  function renderBadges() {
    document.querySelectorAll("[data-chapter-link]").forEach((el) => {
      const id = el.getAttribute("data-chapter-link");
      if (isComplete(id) && !el.querySelector(".complete-badge")) {
        el.classList.add("chapter-complete");
        const badge = document.createElement("span");
        badge.className = "complete-badge";
        badge.textContent = "✓ Completed";
        el.appendChild(badge);
      }
    });
  }

  return { markComplete, isComplete, completedCount, renderBadges };
})();

document.addEventListener("DOMContentLoaded", function () {
  if (window.GFEProgress) window.GFEProgress.renderBadges();
});
