"""
Exercise — Session 2.4: Structured Outputs

Resume Parser Prompt.

Setup:
  pip install anthropic python-dotenv
  Copy .env.example to .env and add your ANTHROPIC_API_KEY

Run: python resume_parser.py
"""

import json
import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

MODEL_NAME = "claude-haiku-4-5-20251001"

SAMPLE_RESUMES = [
    """Jane Martinez
    jane.martinez@email.com
    Software Engineer with 6 years of experience in Python, AWS, and
    distributed systems. Previously at TechCorp (2019-2024) and
    StartupXYZ (2018-2019).""",

    """Aiden Cole
    Backend developer. Worked at three companies over the past 4 years
    building APIs in Node.js and PostgreSQL. Strong in Docker and CI/CD.""",
    # Note: deliberately has NO email listed — tests null-handling

    """RAJ PATEL - DATA SCIENTIST
    Contact: raj.patel.ds@gmail.com | Skills: Python, R, SQL, TensorFlow,
    PyTorch | 8+ years building ML models for fintech applications.""",
]


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found. Copy .env.example to .env and add your key.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


# TODO: write the extraction prompt template. It should:
#   - Define an explicit JSON schema with types (name, email, years_experience, skills)
#   - Instruct null for missing fields, not guesses
#   - Instruct NO text before or after the JSON object
EXTRACTION_PROMPT_TEMPLATE = None  # TODO


def extract_resume_data(client, resume_text: str) -> str:
    if not EXTRACTION_PROMPT_TEMPLATE:
        raise NotImplementedError("Fill in EXTRACTION_PROMPT_TEMPLATE first.")
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(resume_text=resume_text)
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def parse_model_json(raw_text: str):
    """
    TODO: implement defensive parsing.
    - Try json.loads() directly first.
    - If that fails, try extracting the span between the first '{' and last '}'.
    - If everything fails, return None (don't let this crash the program).
    """
    raise NotImplementedError("Fill this in.")


def main():
    client = get_client()
    for i, resume in enumerate(SAMPLE_RESUMES, 1):
        print(f"\n--- Resume {i} ---")
        raw_output = extract_resume_data(client, resume)
        print(f"Raw model output:\n{raw_output}\n")

        parsed = parse_model_json(raw_output)
        if parsed is None:
            print("PARSING FAILED — this should be handled gracefully, not crash.")
        else:
            print(f"Parsed: {parsed}")


if __name__ == "__main__":
    main()
