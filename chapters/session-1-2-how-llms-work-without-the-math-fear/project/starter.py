"""
Session 1.2 Project: Token Cost Estimator
See README.md in this folder for the full brief and an example run.

This is the takeaway build for Session 1.2: a small, genuinely reusable tool
that turns the tokenizer intuition into something practical — given any piece
of text, it tells you how many tokens it is and roughly what it would cost to
send to an LLM. It also makes the "non-English costs more" effect impossible
to miss.

Uses tiktoken (OpenAI's free, open-source tokenizer) — no API key needed.
Install with: pip install tiktoken
"""

import sys
import tiktoken

# Make sure non-English text (Hindi, Japanese) prints correctly on Windows
# terminals, which default to a non-UTF-8 encoding.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

# A realistic example input rate: US dollars per 1,000,000 input tokens.
# (Made-up-but-plausible number — real rates vary by model and change often.)
PRICE_PER_1M_TOKENS = 0.50

# Same meaning, three languages — so the cost gap is easy to see.
SAMPLE_TEXTS = [
    ("English", "Hello, how are you today?"),
    ("Hindi", "नमस्ते, आज आप कैसे हैं?"),
    ("Japanese", "こんにちは、今日は元気ですか？"),
]


def count_tokens(encoding, text):
    # TODO 1: encode `text` with the given `encoding` and return the number
    # of tokens (the length of the encoded list).
    return 0


def estimate_cost(token_count):
    # TODO 2: convert a token count into a dollar cost using
    # PRICE_PER_1M_TOKENS. Formula: token_count / 1_000_000 * PRICE_PER_1M_TOKENS
    return 0.0


def run():
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
    except Exception as e:
        print("Could not download the tokenizer's vocabulary file.")
        print("This usually means no internet access, or a firewall blocking")
        print("openaipublic.blob.core.windows.net.")
        print(f"\nOriginal error: {e}")
        return

    print("=== Token Cost Estimator ===")
    print(f"(rate: ${PRICE_PER_1M_TOKENS} per 1,000,000 input tokens)\n")
    print(f"{'Language':<10} {'Tokens':<8} {'Est. cost':<14} Text")
    print("-" * 70)

    # TODO 3: loop over SAMPLE_TEXTS. For each (label, text), get the token
    # count with count_tokens(), the cost with estimate_cost(), and print a
    # row. Then print a one-line takeaway comparing the most expensive
    # language to English.


if __name__ == "__main__":
    run()
