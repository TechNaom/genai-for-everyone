# Session 1.2 Project: Token Cost Estimator

The takeaway build for Session 1.2 — a small, genuinely reusable tool that turns
the tokenizer intuition you just formed into something practical.

## What you'll build

Given any piece of text, the estimator reports how many tokens it is and roughly
what it would cost to send to an LLM (at a per-token rate). By running the same
sentence in English, Hindi, and Japanese, it makes the "non-English costs more
for the same meaning" effect impossible to miss — the exact real-world cost
lesson from this session.

Example run:

```
=== Token Cost Estimator ===
(rate: $0.5 per 1,000,000 input tokens)

Language   Tokens   Est. cost      Text
----------------------------------------------------------------------
English    7        $0.00000350    Hello, how are you today?
Hindi      24       $0.00001200    नमस्ते, आज आप कैसे हैं?
Japanese   10       $0.00000500    こんにちは、今日は元気ですか？

Takeaway: the Hindi version uses 24 tokens vs. 7 for English — about
3.4x more for the same meaning, and therefore ~3.4x the cost.
```

(Exact token counts can vary slightly between tokenizer versions.)

## How to run it

```bash
pip install tiktoken
python starter.py
```

`tiktoken` is free, runs entirely locally, and needs no API key. Fill in the
`# TODO` sections in `starter.py`. Want to see one finished version first? Run
`python solution.py`.

## Ideas to make it your own (optional stretch goals)

- Read text from a file or a command-line argument instead of the built-in list.
- Add a real per-token rate for a model you're curious about and compare.
- Show cost per 1,000 requests, so the difference between languages is dramatic.

## Why this project matters

Every time you compare LLM providers on price, you're comparing per-token rates —
so tokenization efficiency is literally a line item in a cloud bill. This tiny
tool is the shape of a real cost check you'll run before shipping an AI feature:
take some text, count its tokens, and translate that into money.
