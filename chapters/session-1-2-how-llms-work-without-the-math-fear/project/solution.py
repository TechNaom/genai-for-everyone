"""
Session 1.2 Project: Token Cost Estimator — reference solution.

Turns the tokenizer intuition from this session into a small, reusable tool:
given any text, report its token count and a rough API cost — and make the
"non-English costs more for the same meaning" effect impossible to miss.

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
    # TODO 1: encode `text` and return how many tokens it becomes.
    return len(encoding.encode(text))


def estimate_cost(token_count):
    # TODO 2: convert a token count into a dollar cost.
    return token_count / 1_000_000 * PRICE_PER_1M_TOKENS


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

    # TODO 3: print a row per sample, then a takeaway line.
    results = []
    for label, text in SAMPLE_TEXTS:
        tokens = count_tokens(encoding, text)
        cost = estimate_cost(tokens)
        results.append((label, tokens))
        print(f"{label:<10} {tokens:<8} ${cost:<13.8f} {text}")

    english_tokens = dict(results)["English"]
    priciest_label, priciest_tokens = max(results, key=lambda r: r[1])
    ratio = priciest_tokens / english_tokens
    print(
        f"\nTakeaway: the {priciest_label} version uses {priciest_tokens} tokens "
        f"vs. {english_tokens} for English — about {ratio:.1f}x more for the "
        f"same meaning, and therefore ~{ratio:.1f}x the cost."
    )


if __name__ == "__main__":
    run()
