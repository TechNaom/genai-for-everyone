/*
  Renders the persistent left-hand "digital textbook" chapter sidebar on
  every page, from the single chapter roster in assets/chapters-data.js.

  Expects a placeholder element already in the page:
    <aside id="chapter-sidebar" class="sidebar" data-root="../../"></aside>
  `data-root` is the relative path back to the repo root from that page's
  location (e.g. "" for index.html, "../../" for a chapter's lesson.html).

  The current page's chapter can be highlighted by setting
  `data-active-chapter="chapter-02"` on <body>. Completion checkmarks are
  read from assets/progress.js's localStorage-backed tracker, if loaded.
*/

(function () {
  function escapeHtml(str) {
    return str.replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }

  function isComplete(chapterId) {
    return !!(window.GFEProgress && window.GFEProgress.isComplete(chapterId));
  }

  function buildSidebarHtml(root, activeChapter) {
    const modules = window.GFE_MODULES || [];
    let html = `<a href="${root}index.html" class="sidebar-brand">🤖 GenAI for Everyone</a>`;
    html += `<span class="sidebar-subtitle">Free &amp; interactive, session by session</span>`;

    modules.forEach((mod, index) => {
      const containsActive = mod.chapters.some((c) => c.id === activeChapter);
      const isOpen = containsActive || index === 0 ? "open" : "";
      html += `<details class="sidebar-module" ${isOpen}><summary>${escapeHtml(mod.title)}</summary>`;
      html += `<ul class="sidebar-chapter-list">`;
      mod.chapters.forEach((ch) => {
        const activeClass = ch.id === activeChapter ? "active" : "";
        if (ch.path) {
          const check = isComplete(ch.id) ? `<span class="sidebar-check">✓</span>` : `<span>${ch.num}.</span>`;
          html += `<li class="${activeClass}"><a href="${root}${ch.path}">${check} ${escapeHtml(ch.title)}</a>`;
          if (ch.subtopics && ch.subtopics.length) {
            html += `<ul class="sidebar-subtopic-list">`;
            ch.subtopics.forEach((sub) => {
              html += `<li><a href="${root}${ch.path}#${sub.id}">${escapeHtml(sub.title)}</a></li>`;
            });
            html += `</ul>`;
          }
          html += `</li>`;
        } else {
          html += `<li><span class="soon">${ch.num}. ${escapeHtml(ch.title)} <em>(soon)</em></span></li>`;
        }
      });
      html += `</ul>`;
      if (mod.examPath) {
        html += `<a class="sidebar-exam-link" href="https://github.com/TechNaom/genai-for-everyone/blob/main/${mod.examPath}">📝 Week Written Exam</a>`;
      }
      html += `</details>`;
    });

    return html;
  }

  function wireMobileToggle() {
    const sidebar = document.getElementById("chapter-sidebar");
    const toggle = document.getElementById("sidebar-toggle");
    const scrim = document.getElementById("sidebar-scrim");
    if (!sidebar || !toggle || !scrim) return;

    function open() {
      sidebar.classList.add("open");
      scrim.classList.add("show");
      toggle.setAttribute("aria-expanded", "true");
    }
    function close() {
      sidebar.classList.remove("open");
      scrim.classList.remove("show");
      toggle.setAttribute("aria-expanded", "false");
    }
    toggle.addEventListener("click", () => {
      sidebar.classList.contains("open") ? close() : open();
    });
    scrim.addEventListener("click", close);
  }

  function init() {
    const sidebar = document.getElementById("chapter-sidebar");
    if (!sidebar) return;
    const root = sidebar.getAttribute("data-root") || "";
    const activeChapter = document.body.getAttribute("data-active-chapter") || "";
    sidebar.innerHTML = buildSidebarHtml(root, activeChapter);
    wireMobileToggle();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
