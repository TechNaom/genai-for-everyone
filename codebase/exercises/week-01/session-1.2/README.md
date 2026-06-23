# Exercise — Session 1.2: How LLMs Work, Without the Math Fear

## Tokenizer Playground

**Goal:** Build real intuition for how text gets split into tokens — and see, hands-on, why some languages and word choices cost more tokens than others.

### Instructions

1. Open `tokenizer_playground.py`
2. For each sentence in the `SENTENCES` list, **predict the token count before running the script** — write your guess in the `your_guess` field
3. Run the script. It will show the actual tokenization (each token visually separated) and the real count, next to your guess
4. Answer the reflection questions at the bottom of the script in a comment

### What you'll notice

- Common English words are often single tokens; rare or made-up words get split into pieces
- The same sentence in Hindi or Japanese often uses more tokens than the English equivalent
- Code and unusual punctuation tokenize differently than plain prose

## Free/open path

This exercise uses `tiktoken`, OpenAI's open-source tokenizer library. It's free, runs entirely locally, and needs no API key:

```bash
pip install tiktoken
python tokenizer_playground.py
```

## Optional paid-API path

Not needed for this exercise — tokenization is a local, free operation. (You'll use real API calls starting in Session 1.4.)

## Solution

See `codebase/solutions/week-01/session-1.2/` for a worked-through version with the reflection questions answered.
