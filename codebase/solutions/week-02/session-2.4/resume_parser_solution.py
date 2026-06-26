"""
Reference solution — Session 2.4: Structured Outputs

Includes full defensive parsing AND type validation (successfully parsed
JSON can still have the wrong shape — this solution checks for that too).
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

    """RAJ PATEL - DATA SCIENTIST
    Contact: raj.patel.ds@gmail.com | Skills: Python, R, SQL, TensorFlow,
    PyTorch | 8+ years building ML models for fintech applications.""",
]

EXTRACTION_PROMPT_TEMPLATE = """Extract the following information from this resume text and return ONLY
a JSON object in exactly this format, with no other text before or after:

{{
  "name": "string",
  "email": "string or null if not found",
  "years_experience": "number, your best estimate based on listed roles",
  "skills": ["array", "of", "strings"]
}}

If a field cannot be determined from the text, use null for strings/numbers
or an empty array for skills. Do not guess at information not present.

Resume text:
{resume_text}"""

EXPECTED_SCHEMA = {
    "name": (str, type(None)),
    "email": (str, type(None)),
    "years_experience": (int, float, type(None)),
    "skills": (list,),
}


def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("No ANTHROPIC_API_KEY found. Copy .env.example to .env and add your key.")
        sys.exit(1)
    return Anthropic(api_key=api_key)


def extract_resume_data(client, resume_text: str) -> str:
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(resume_text=resume_text)
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def parse_model_json(raw_text: str):
    """Defensive parsing: try direct parse, then try extracting {...} span."""
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        start = raw_text.find('{')
        end = raw_text.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw_text[start:end + 1])
            except json.JSONDecodeError:
                pass
        return None


def validate_schema(parsed: dict) -> list:
    """Returns a list of validation problems (empty list = valid)."""
    if parsed is None:
        return ["parsed data is None"]
    problems = []
    for field, expected_types in EXPECTED_SCHEMA.items():
        if field not in parsed:
            problems.append(f"missing field: {field}")
            continue
        if not isinstance(parsed[field], expected_types):
            problems.append(
                f"field '{field}' has type {type(parsed[field]).__name__}, "
                f"expected one of {[t.__name__ for t in expected_types]}"
            )
    return problems


def main():
    client = get_client()
    for i, resume in enumerate(SAMPLE_RESUMES, 1):
        print(f"\n--- Resume {i} ---")
        raw_output = extract_resume_data(client, resume)
        print(f"Raw model output:\n{raw_output}\n")

        parsed = parse_model_json(raw_output)
        if parsed is None:
            print("PARSING FAILED — handled gracefully, program continues.")
            continue

        problems = validate_schema(parsed)
        if problems:
            print(f"Parsed but SCHEMA ISSUES found: {problems}")
        else:
            print(f"Parsed and schema-valid: {parsed}")

    print(
        "\nResume 2 has no email listed — check above that its 'email' field "
        "came back as null/None rather than a guessed address. That's the "
        "single most important thing to verify in this exercise."
    )


if __name__ == "__main__":
    main()
