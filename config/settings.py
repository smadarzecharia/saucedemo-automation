"""Environment-facing configuration.

Values come from the project's `.env` file (gitignored — see `.env.example`),
and real environment variables override the file. No credentials or usernames
in code: missing values fail fast with a clear message instead of a confusing
test failure later.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Real env vars win over the file (override=False is the default).
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required setting {name!r} — define it in .env "
            "(see .env.example) or as an environment variable."
        )
    return value


# The base URL is not a secret, so a default is fine.
BASE_URL = os.getenv("SAUCEDEMO_BASE_URL", "https://www.saucedemo.com")

PASSWORD = _require("SAUCEDEMO_PASSWORD")
STANDARD_USER = _require("SAUCEDEMO_STANDARD_USER")
LOCKED_OUT_USER = _require("SAUCEDEMO_LOCKED_OUT_USER")
PROBLEM_USER = _require("SAUCEDEMO_PROBLEM_USER")
