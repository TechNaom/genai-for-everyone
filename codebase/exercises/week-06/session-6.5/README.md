# Exercise — Session 6.5: CI/CD & Versioning for Prompts

## Overview

Build a CI-style regression gate for prompt versions.

- **Core path:** Score a new prompt version against a golden dataset, compare to a stored baseline, return pass/fail
- **Pro path:** Add a version history with rollback and a changelog-style score trend report

## Setup

```bash
pip install -r requirements.txt
```

## Free/open path

Everything here uses a mocked scoring function against a small golden dataset — no API calls needed.

## Optional paid-API path

Swap `mock_score_prompt()` for a real call to your Week 3/4 project and a real rubric/LLM-as-judge scorer from Session 5.2.

## Starter code

See `starter.py` in this folder.

## Solution

See `codebase/solutions/week-06/session-6.5/` (don't peek before attempting!).
