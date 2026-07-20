"""
Session 6.3 Project: The Fallback Rate Monitor
See README.md in this folder for the full brief and an example run.

This is the Pro path build for Session 6.3: on top of the adapter layer from
the exercises, implement a fallback wrapper -- call_model_with_fallback --
that calls a primary provider, catches a simulated outage, automatically
retries against a fallback provider, and logs which provider actually served
each request. That log is what turns "we have a fallback" into a measurable
fallback rate.

No API key, no internet access, no external libraries needed -- the outage
is simulated in-process with `random`, so this runs the same way anywhere.

Run: python starter.py
"""

import random
import time
from typing import Dict, List


def _call_primary(prompt: str) -> Dict:
    """Mock primary provider: strong, but simulates a 25% outage rate."""
    if random.random() < 0.25:
        raise ConnectionError("primary: simulated outage")
    time.sleep(0.03)
    return {"text": f"[primary] answer to: {prompt}", "cost": 0.03, "latency_ms": 30}


def _call_secondary(prompt: str) -> Dict:
    """Mock secondary provider: always available, a bit weaker/cheaper."""
    time.sleep(0.015)
    return {"text": f"[secondary] answer to: {prompt}", "cost": 0.008, "latency_ms": 15}


PROVIDERS = {"primary": _call_primary, "secondary": _call_secondary}

# TODO 1: fill this in -- a running log of every call_model_with_fallback
# invocation, so measure_fallback_rate() can summarize it afterward.
# Each entry should be a dict, e.g. {"prompt": ..., "used_provider": ...}.
CALL_LOG: List[Dict] = []


def call_model(prompt: str, provider: str = "primary") -> Dict:
    """
    TODO 2: look up the provider function in PROVIDERS and call it.
    Raise a clear ValueError if the provider name isn't recognized.
    """
    raise NotImplementedError


def call_model_with_fallback(prompt: str, primary: str, fallback: str) -> Dict:
    """
    TODO 3 (the core of this project): call `primary` via call_model(). If it
    raises a ConnectionError, catch it and call `fallback` instead. Either
    way:
      - add an "used_provider" key to the result: the plain provider name if
        the primary succeeded, or "<fallback> (fallback from <primary>)" if
        the fallback had to be used
      - append a record to CALL_LOG (at minimum: prompt and used_provider)
        so measure_fallback_rate() has something to summarize
    Return the result dict.
    """
    raise NotImplementedError


def measure_fallback_rate(n_calls: int = 50) -> None:
    """
    TODO 4: call call_model_with_fallback() n_calls times with any prompt,
    primary="primary", fallback="secondary". Then use CALL_LOG to compute and
    print how many of those calls actually used the fallback, as a count and
    a percentage (compare it to the ~25% simulated outage rate above).
    """
    raise NotImplementedError


if __name__ == "__main__":
    print("=== Single call with fallback ===")
    result = call_model_with_fallback("What is a circuit breaker?", primary="primary", fallback="secondary")
    print(result)

    print("\n=== Measuring the fallback rate over many calls ===")
    measure_fallback_rate(50)
