/*
  Live in-browser Python playground, powered by Pyodide (a real Python
  interpreter compiled to WebAssembly, loaded from a CDN — no backend,
  no install, works on any static page).

  Usage in HTML:
    <div class="playground">
      <div class="playground-bar">
        <span class="filename">try_it.py</span>
        <button class="playground-run-btn" data-playground-run>▶ Run Code</button>
      </div>
      <textarea class="playground-code" data-playground-code>
print("Hello, world!")
      </textarea>
      <div class="playground-output" data-playground-output>Click "Run Code" to see the output here.</div>
    </div>

  Pyodide is only downloaded the first time a learner clicks Run, so
  reading a lesson page never pays the (few-second, ~a few MB) load cost.
  input() is not supported in this sandbox — examples that use input()
  are intentionally left as download-and-run-locally code windows instead.

  Some chapters (from Chapter 23 onward) need third-party packages like
  numpy and pandas, which Pyodide does not include by default. getPyodide()
  loads numpy and pandas once, lazily, alongside the base interpreter — a
  no-op extra download for pages that never import them, and a one-time
  cost for pages that do, cached by the browser across every playground box
  on the page. pandas depends on numpy, so both are requested in one
  loadPackage() call and Pyodide resolves the load order correctly.
*/

(function () {
  let pyodideReadyPromise = null;

  function getPyodide() {
    if (!pyodideReadyPromise) {
      const script = document.createElement("script");
      script.src = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js";
      pyodideReadyPromise = new Promise((resolve, reject) => {
        script.onload = () => {
          window
            .loadPyodide()
            .then((pyodide) => pyodide.loadPackage(["numpy", "pandas"]).then(() => pyodide))
            .then(resolve)
            .catch(reject);
        };
        script.onerror = () => reject(new Error("Could not load the Python runtime. Check your internet connection and try again."));
      });
      document.head.appendChild(script);
    }
    return pyodideReadyPromise;
  }

  async function runOne(box) {
    const btn = box.querySelector("[data-playground-run]");
    const codeEl = box.querySelector("[data-playground-code]");
    const outputEl = box.querySelector("[data-playground-output]");
    if (!btn || !codeEl || !outputEl) return;

    const originalLabel = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Loading Python…";
    outputEl.textContent = "";

    try {
      const pyodide = await getPyodide();
      btn.textContent = "Running…";

      let output = "";
      pyodide.setStdout({ batched: (s) => { output += s + "\n"; } });
      pyodide.setStderr({ batched: (s) => { output += s + "\n"; } });

      await pyodide.runPythonAsync(codeEl.value);
      outputEl.textContent = output || "(no output)";
    } catch (err) {
      outputEl.textContent = "Error:\n" + (err && err.message ? err.message : String(err));
    } finally {
      btn.disabled = false;
      btn.textContent = originalLabel === "Loading Python…" || originalLabel === "Running…" ? "▶ Run Code" : originalLabel;
    }
  }

  function wireUp() {
    document.querySelectorAll(".playground").forEach((box) => {
      const btn = box.querySelector("[data-playground-run]");
      if (btn) {
        btn.addEventListener("click", () => runOne(box));
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wireUp);
  } else {
    wireUp();
  }
})();
