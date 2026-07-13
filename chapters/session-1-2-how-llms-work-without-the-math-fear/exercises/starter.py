"""
Exercise — Session 1.2: How LLMs Work, Without the Math Fear

Tokenizer Playground.

For each sentence below:
  1. Fill in your_guess with how many tokens YOU think it will become
     (do this BEFORE running the script — that's the whole point)
  2. Run this file: python starter.py
  3. Compare your guess to the real count and look at how it actually split

Uses tiktoken (OpenAI's free, open-source tokenizer) — no API key needed.
Install with: pip install tiktoken
"""

import sys
import tiktoken

# Make sure non-English text (Hindi, Japanese, emoji) prints correctly on
# Windows terminals, which default to a non-UTF-8 encoding.
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

SENTENCES = [
    {"text": "The cat sat on the mat.", "your_guess": None},
    {"text": "Antidisestablishmentarianism", "your_guess": None},
    {"text": "GenAI is changing how we build software.", "your_guess": None},
    {"text": "नमस्ते, आप कैसे हैं?", "your_guess": None},  # Hindi: "Hello, how are you?"
    {"text": "Hello, how are you?", "your_guess": None},      # English equivalent, for comparison
    {"text": "def calculate_total(price, tax_rate):\n    return price * (1 + tax_rate)", "your_guess": None},
    {"text": "supercalifragilisticexpialidocious", "your_guess": None},
    {"text": "🎉🎊🥳", "your_guess": None},
]


def run_playground():
    # cl100k_base is the tokenizer used by GPT-4-era models — widely used as a
    # reference tokenizer for this kind of exploration.
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
    except Exception as e:
        print("Could not download the tokenizer's vocabulary file.")
        print("This usually means no internet access right now, or a firewall")
        print("blocking openaipublic.blob.core.windows.net.")
        print(f"\nOriginal error: {e}")
        return

    print(f"{'Text':<55} {'Your Guess':<12} {'Actual':<8} {'Tokens (visualized)'}")
    print("-" * 110)

    for item in SENTENCES:
        text = item["text"]
        tokens = encoding.encode(text)
        actual_count = len(tokens)
        decoded_pieces = [encoding.decode([t]) for t in tokens]
        visualized = " | ".join(repr(p) for p in decoded_pieces)

        guess_display = str(item["your_guess"]) if item["your_guess"] is not None else "(not guessed)"
        short_text = text.replace("\n", "\\n")[:50]

        print(f"{short_text:<55} {guess_display:<12} {actual_count:<8} {visualized}")

    print("\n--- Reflection questions (answer in a comment below) ---")
    print("1. Which sentence had the biggest gap between your guess and the actual count? Why do you think that happened?")
    print("2. Compare the Hindi sentence and its English equivalent. What does the token count difference imply about API cost if you were billed per token?")
    print("3. Look at how 'supercalifragilisticexpialidocious' got split. Does the split look like meaningful word-parts, or arbitrary chunks?")


# --- Your reflection answers ---
# 1.
# 2.
# 3.


if __name__ == "__main__":
    run_playground()
