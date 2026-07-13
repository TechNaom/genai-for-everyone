"""
Reference solution / worked example — Session 1.2: How LLMs Work, Without the Math Fear

NOTE ON THIS FILE: the reflection answers below describe the GENERAL PATTERN
you should observe (based on how cl100k_base-style tokenizers behave), since
exact token counts can vary slightly between tokenizer versions. Run
starter.py yourself to see your exact numbers, then compare the pattern of
what you see against the explanations below.

Uses tiktoken (OpenAI's free, open-source tokenizer) — no API key needed.
Install with: pip install tiktoken
"""

import sys
import tiktoken

# Make sure non-English text (Hindi) prints correctly on Windows terminals,
# which default to a non-UTF-8 encoding.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def run_solution():
    encoding = tiktoken.get_encoding("cl100k_base")

    examples = [
        "The cat sat on the mat.",
        "Antidisestablishmentarianism",
        "नमस्ते, आप कैसे हैं?",
        "Hello, how are you?",
        "supercalifragilisticexpialidocious",
    ]

    for text in examples:
        tokens = encoding.encode(text)
        pieces = [encoding.decode([t]) for t in tokens]
        print(f"\n'{text}'")
        print(f"  Token count: {len(tokens)}")
        print(f"  Split into: {pieces}")


# --- Reflection answers (expected pattern) ---
#
# 1. The biggest gap is usually on long, uncommon words like
#    "supercalifragilisticexpialidocious" or "Antidisestablishmentarianism" —
#    people often guess "1 token" because it's one word, but the tokenizer
#    splits rare words into several sub-word pieces since the whole word
#    never appeared often enough in training data to earn its own token.
#
# 2. The Hindi sentence typically uses noticeably MORE tokens than its
#    English equivalent for the same meaning. If you're billed per token
#    (which is how most LLM APIs charge), the same conversation costs more
#    in Hindi than in English purely because of tokenization efficiency —
#    not because the content is more complex. This is a real, documented
#    fairness concern in the field, and it's worth remembering once you get
#    to Week 6's cost engineering session.
#
# 3. The split on "supercalifragilisticexpialidocious" will look like
#    chunks that roughly resemble syllables or common sub-word fragments
#    (e.g. pieces resembling "super", "cali", "fragil", etc.) — not random
#    cuts, but also not necessarily clean linguistic syllables either. The
#    tokenizer is statistically driven, not linguistically aware.

if __name__ == "__main__":
    run_solution()
