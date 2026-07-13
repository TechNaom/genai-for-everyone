/*
  In-browser coding-challenge judge, powered by Pyodide (same WebAssembly
  Python runtime as assets/playground.js — no backend, nothing leaves the
  browser). Each challenge card defines a function signature the learner
  must implement, plus a set of test cases; clicking "Run Tests" actually
  executes the learner's code against every case and reports pass/fail
  per case, HackerRank-style.

  Usage in HTML:
    <div class="challenge-card" data-difficulty="Easy">
      <h3>1. Reverse a String</h3>
      <div class="challenge-statement">...problem prose, constraints, examples...</div>
      <div class="code-window">
        <textarea class="challenge-code" data-challenge-code>
def reverse_string(s):
    # TODO: return s reversed
    pass
        </textarea>
      </div>
      <button class="challenge-run-btn" data-challenge-run>&#9654; Run Tests</button>
      <div class="challenge-results" data-challenge-results></div>
      <script type="application/json" data-challenge-tests>
        { "function": "reverse_string",
          "cases": [ { "args": ["hello"], "expected": "olleh" } ] }
      </script>
      <details class="qa-item"><summary>Show Solution</summary>...</details>
    </div>

  A shared Pyodide instance is loaded once per page (lazily, on first
  "Run Tests" click) and reused across every challenge card on that page.
  input() is not supported in this sandbox, same constraint as the
  playground — challenge functions take arguments and return a value,
  they don't read from stdin.

  Some chapters (from Chapter 23 onward) grade challenges that import
  numpy and/or pandas, which Pyodide does not bundle by default.
  getPyodide() loads numpy and pandas once, lazily, alongside the base
  interpreter — a no-op extra download for chapters that never import
  them, and a one-time cost, cached across every challenge card on the
  page, for chapters that do. pandas depends on numpy, so both are
  requested together in one loadPackage() call and Pyodide resolves the
  load order correctly.
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

  function renderResults(resultsEl, result) {
    resultsEl.innerHTML = "";

    if (result.compile_error) {
      const err = document.createElement("div");
      err.className = "challenge-case fail";
      err.innerHTML = "<strong>Error:</strong> " + escapeHtml(result.compile_error);
      resultsEl.appendChild(err);
      return;
    }

    const cases = result.cases;
    const passCount = cases.filter((c) => c.pass).length;

    cases.forEach((c, i) => {
      const row = document.createElement("div");
      row.className = "challenge-case " + (c.pass ? "pass" : "fail");
      const argsStr = c.args.map((a) => JSON.stringify(a)).join(", ");
      let detail = "Input: (" + escapeHtml(argsStr) + ")  &rarr;  Expected: " + escapeHtml(JSON.stringify(c.expected));
      if (c.pass) {
        detail += "  &mdash;  Got: " + escapeHtml(JSON.stringify(c.actual)) + " &#10003;";
      } else if (c.error) {
        detail += "  &mdash;  Raised: " + escapeHtml(c.error);
      } else {
        detail += "  &mdash;  Got: " + escapeHtml(JSON.stringify(c.actual)) + " &#10007;";
      }
      row.innerHTML = "<span class=\"case-icon\">" + (c.pass ? "✅" : "❌") + "</span> <span class=\"case-num\">Test " + (i + 1) + "</span> " + detail;
      resultsEl.appendChild(row);
    });

    const summary = document.createElement("div");
    const allPass = passCount === cases.length;
    summary.className = "challenge-summary " + (allPass ? "all-pass" : "");
    summary.textContent = allPass
      ? "🎉 All " + cases.length + " tests passed!"
      : passCount + " / " + cases.length + " tests passed";
    resultsEl.appendChild(summary);
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  async function runChallenge(card) {
    const btn = card.querySelector("[data-challenge-run]");
    const codeEl = card.querySelector("[data-challenge-code]");
    const resultsEl = card.querySelector("[data-challenge-results]");
    const configEl = card.querySelector("[data-challenge-tests]");
    if (!btn || !codeEl || !resultsEl || !configEl) return;

    let config;
    try {
      config = JSON.parse(configEl.textContent);
    } catch (e) {
      resultsEl.textContent = "Internal error: could not read test cases for this challenge.";
      return;
    }

    const originalLabel = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Loading Python…";
    resultsEl.innerHTML = "";

    try {
      const pyodide = await getPyodide();
      btn.textContent = "Running tests…";

      pyodide.setStdout({ batched: () => {} });
      pyodide.setStderr({ batched: () => {} });

      pyodide.globals.set("_student_code", codeEl.value);
      pyodide.globals.set("_test_config_json", JSON.stringify(config));

      const harness = `
import json

_result = {"compile_error": None, "cases": []}
_ns = {}
try:
    exec(_student_code, _ns)
except Exception as _e:
    _result["compile_error"] = type(_e).__name__ + ": " + str(_e)

if _result["compile_error"] is None:
    _cfg = json.loads(_test_config_json)
    _fn = _ns.get(_cfg["function"])
    if _fn is None:
        _result["compile_error"] = "Function '" + _cfg["function"] + "' not found — did you rename it?"
    else:
        for _case in _cfg["cases"]:
            _entry = {"args": _case["args"], "expected": _case["expected"]}
            try:
                _actual = _fn(*_case["args"])
                _entry["actual"] = _actual
                _entry["pass"] = _actual == _case["expected"]
            except Exception as _e:
                _entry["actual"] = None
                _entry["error"] = type(_e).__name__ + ": " + str(_e)
                _entry["pass"] = False
            _result["cases"].append(_entry)

json.dumps(_result)
`;

      const resultJson = await pyodide.runPythonAsync(harness);
      const result = JSON.parse(resultJson);
      renderResults(resultsEl, result);
    } catch (err) {
      resultsEl.textContent = "Error running your code:\n" + (err && err.message ? err.message : String(err));
    } finally {
      btn.disabled = false;
      btn.textContent = originalLabel === "Loading Python…" || originalLabel === "Running tests…" ? "▶ Run Tests" : originalLabel;
    }
  }

  function wireUp() {
    document.querySelectorAll(".challenge-card").forEach((card) => {
      const btn = card.querySelector("[data-challenge-run]");
      if (btn) {
        btn.addEventListener("click", () => runChallenge(card));
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wireUp);
  } else {
    wireUp();
  }
})();
