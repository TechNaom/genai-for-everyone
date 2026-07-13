# Session 1.2 Exercise: Tokenizer Playground

Build real intuition for how text gets split into tokens — and see, hands-on,
why some languages and word choices cost more tokens than others.

## How to run

```bash
pip install tiktoken
python starter.py
```

`tiktoken` is OpenAI's open-source tokenizer library. It's free, runs entirely
locally, and needs no API key. (You won't make a real API call until Session 1.4.)

## Task 1 — Predict before you run

Open `starter.py`. For each sentence in the `SENTENCES` list, fill in
`your_guess` with how many tokens you think it will become — **before** running
the script. Predicting first is the whole point; it's what turns the output
into a genuine "huh, that's weird" moment.

## Task 2 — Run and compare

Run `python starter.py`. It prints each sentence next to your guess, the actual
token count, and a visualization of exactly where each token split.

## Task 3 — Answer the reflection questions

The script prints three reflection questions. Answer them in the comment block
at the bottom of `starter.py`:

1. Which sentence had the biggest gap between your guess and the actual count?
2. Compare the Hindi sentence to its English equivalent — what does the token
   difference imply about per-token API cost?
3. Does the split on `supercalifragilisticexpialidocious` look like meaningful
   word-parts, or arbitrary chunks?

## What you'll notice

- Common English words are often single tokens; rare or made-up words get split.
- The same sentence in Hindi or Japanese often uses more tokens than English.
- Code and unusual punctuation tokenize differently than plain prose.

## Checking your work

Compare against `solution.py`, which runs a worked subset and answers the
reflection questions with the general pattern to expect. Exact token counts can
vary slightly between tokenizer versions — the goal is that the *pattern* you
observe matches the explanations.
