"""
Configuration module for the API Testing Automation Suite.

Author: Harsh Kumar
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


@dataclass
class Config:
    """
    Global configuration for API tests.
    """
    # Base URL of the API under test (using reqres.in as public mock API)
    base_url: str = "https://reqres.in/api"

    # Request timeout in seconds
    timeout: float = 10.0

    # Maximum allowed response time in milliseconds for performance checks
    max_response_time_ms: float = 800.0

    # Paths for logs and reports
    logs_dir: Path = BASE_DIR / "logs"
    reports_dir: Path = BASE_DIR / "reports"


def get_config() -> Config:
    """
    Factory function so it’s easy to extend later (e.g. env-based configs).
    """
    cfg = Config()
    cfg.logs_dir.mkdir(parents=True, exist_ok=True)
    cfg.reports_dir.mkdir(parents=True, exist_ok=True)
    return cfg
