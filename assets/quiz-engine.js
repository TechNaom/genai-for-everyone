/*
  Quiz engine for "GenAI for Everyone" — supports two question types that
  can be freely mixed on the same page.

  1. Fill-in-the-blank:
    <input type="text" class="fib-blank" data-answers="print,Print" aria-label="Answer for question 1">
    <button class="check-btn" data-check-for="the input's id">Check</button>
    <span class="fib-feedback" aria-live="polite"></span>
  Wrap input + button + feedback span in one element with class "fib-row"
  and the engine wires it up automatically; no JS needed per page.
  Answer matching: comma-separated values in data-answers are all accepted.
  Comparison is trimmed and case-insensitive so small phrasing differences
  don't unfairly mark a correct answer wrong.

  2. Multiple choice (added Chapter 15 onward):
    <div class="quiz-question mcq-question">
      <label id="mcq1-label">Question text?</label>
      <div class="mcq-options" role="group" aria-labelledby="mcq1-label">
        <button type="button" class="mcq-option" data-correct="false">Option A</button>
        <button type="button" class="mcq-option" data-correct="true">Option B</button>
        <button type="button" class="mcq-option" data-correct="false">Option C</button>
      </div>
      <span class="mcq-feedback" aria-live="polite"></span>
    </div>
  Wrap the whole thing in an element with class "mcq-question" and the engine
  wires it up automatically. Exactly one `.mcq-option` per question should have
  `data-correct="true"`. Clicking any option answers the question once: the
  clicked option is marked correct (green) or incorrect (red); if wrong, the
  actually-correct option is also highlighted so the right answer is always
  visible after answering. All options in that question then lock (no
  re-answering), matching a single genuine attempt per question.
*/

(function () {
  function normalize(value) {
    return value.trim().toLowerCase();
  }

  function isCorrect(input) {
    const accepted = (input.dataset.answers || "")
      .split(",")
      .map(normalize)
      .filter(Boolean);
    return accepted.includes(normalize(input.value));
  }

  function checkOne(row) {
    const input = row.querySelector(".fib-blank");
    const feedback = row.querySelector(".fib-feedback");
    if (!input) return null;

    const correct = isCorrect(input);
    input.classList.remove("correct", "incorrect");
    input.classList.add(correct ? "correct" : "incorrect");
    input.setAttribute("aria-invalid", correct ? "false" : "true");

    if (feedback) {
      feedback.textContent = correct ? "✅ Correct" : "❌ Try again";
      feedback.classList.remove("correct", "incorrect");
      feedback.classList.add(correct ? "correct" : "incorrect");
    }
    return correct;
  }

  function answerMcq(question, chosenOption) {
    if (question.classList.contains("answered")) return; // one attempt only
    const options = question.querySelectorAll(".mcq-option");
    const feedback = question.querySelector(".mcq-feedback");
    const chosenCorrect = chosenOption.dataset.correct === "true";

    options.forEach((option) => {
      option.disabled = true;
      if (option === chosenOption) {
        option.classList.add(chosenCorrect ? "correct" : "incorrect");
      } else if (option.dataset.correct === "true") {
        // Reveal the actually-correct option whenever the learner got it wrong.
        if (!chosenCorrect) option.classList.add("reveal-correct");
      }
    });

    question.classList.add("answered", chosenCorrect ? "correct" : "incorrect");

    if (feedback) {
      feedback.textContent = chosenCorrect ? "✅ Correct" : "❌ Not quite — correct answer highlighted above";
      feedback.classList.add(chosenCorrect ? "correct" : "incorrect");
    }
  }

  function updateScore() {
    const scoreEl = document.getElementById("quiz-score");
    const fillEl = document.getElementById("quiz-progress-fill");
    const celebrationEl = document.getElementById("quiz-celebration");
    const fibRows = document.querySelectorAll(".fib-row");
    const mcqQuestions = document.querySelectorAll(".mcq-question");
    const total = fibRows.length + mcqQuestions.length;
    let correctCount = 0;

    fibRows.forEach((row) => {
      const input = row.querySelector(".fib-blank");
      if (!input) return;
      if (input.classList.contains("correct")) correctCount += 1;
    });

    mcqQuestions.forEach((question) => {
      if (question.classList.contains("correct")) correctCount += 1;
    });

    if (scoreEl) {
      scoreEl.textContent = `Score: ${correctCount} / ${total}`;
    }
    if (fillEl) {
      const pct = total ? Math.round((correctCount / total) * 100) : 0;
      fillEl.style.width = `${pct}%`;
    }
    const perfectScore = total > 0 && correctCount === total;
    if (celebrationEl) {
      celebrationEl.classList.toggle("show", perfectScore);
    }
    if (perfectScore && window.GFEProgress) {
      window.GFEProgress.markComplete(document.body.dataset.chapterId);
    }
  }

  function wireUp() {
    document.querySelectorAll(".fib-row").forEach((row) => {
      const input = row.querySelector(".fib-blank");
      const button = row.querySelector(".check-btn");
      if (!input || !button) return;

      button.addEventListener("click", () => {
        checkOne(row);
        updateScore();
      });

      input.addEventListener("keydown", (event) => {
        if (event.key === "Enter") {
          event.preventDefault();
          checkOne(row);
          updateScore();
        }
      });
    });

    document.querySelectorAll(".mcq-question").forEach((question) => {
      question.querySelectorAll(".mcq-option").forEach((option) => {
        option.addEventListener("click", () => {
          answerMcq(question, option);
          updateScore();
        });
      });
    });

    const checkAllBtn = document.getElementById("check-all-btn");
    if (checkAllBtn) {
      checkAllBtn.addEventListener("click", () => {
        document.querySelectorAll(".fib-row").forEach(checkOne);
        updateScore();
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", wireUp);
  } else {
    wireUp();
  }
})();
