"""
Core testing logic for the API Testing Automation Suite.

Provides:
- TestResult dataclass
- Validation helpers (status, JSON structure, response time)
- APITestSuite class to run GET/POST test scenarios

Author: Harsh Kumar
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

from .config import Config
from .http_client import HttpClient

logger = logging.getLogger(__name__)


@dataclass
class TestResult:
    """
    Represents the outcome of a single API test.
    """
    name: str
    success: bool
    status_code: Optional[int] = None
    response_time_ms: Optional[float] = None
    details: str = ""


class APITestSuite:
    """
    Encapsulates logic for executing and validating API requests.
    """

    def __init__(self, config: Config, client: HttpClient) -> None:
        self.config = config
        self.client = client
        self.results: List[TestResult] = []

    # ------------------------------------------------------------------ #
    # Public test methods
    # ------------------------------------------------------------------ #

    def run_get_test(
        self,
        name: str,
        path: str,
        expected_status: int,
        required_json_paths: Optional[List[str]] = None,
    ) -> TestResult:
        """
        Execute a GET request and validate:
        - status code
        - JSON structure (required paths)
        - response time
        """
        logger.info("Running GET test: %s", name)
        try:
            response = self.client.get(path)
            result = self._validate_response(
                name=name,
                response=response,
                expected_status=expected_status,
                required_json_paths=required_json_paths,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unhandled error in GET test '%s': %s", name, exc)
            result = TestResult(
                name=name,
                success=False,
                details=f"Exception while executing test: {exc}",
            )

        self.results.append(result)
        self._log_result(result)
        return result

    def run_post_test(
        self,
        name: str,
        path: str,
        payload: Dict[str, Any],
        expected_status: int,
        required_json_paths: Optional[List[str]] = None,
    ) -> TestResult:
        """
        Execute a POST request and validate:
        - status code
        - JSON structure (required paths)
        - response time
        """
        logger.info("Running POST test: %s", name)
        try:
            response = self.client.post(path, json=payload)
            result = self._validate_response(
                name=name,
                response=response,
                expected_status=expected_status,
                required_json_paths=required_json_paths,
            )
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unhandled error in POST test '%s': %s", name, exc)
            result = TestResult(
                name=name,
                success=False,
                details=f"Exception while executing test: {exc}",
            )

        self.results.append(result)
        self._log_result(result)
        return result

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _validate_response(
        self,
        name: str,
        response,
        expected_status: int,
        required_json_paths: Optional[List[str]] = None,
    ) -> TestResult:
        """
        Perform core validations on a response:
        - status code check
        - response time check
        - basic JSON schema/structure check via key paths
        """
        status_code = response.status_code
        elapsed_ms = response.elapsed.total_seconds() * 1000

        details_list: List[str] = []
        success = True

        # Status code check
        if status_code != expected_status:
            success = False
            details_list.append(
                f"Expected status {expected_status}, got {status_code}."
            )

        # Response time check
        if elapsed_ms > self.config.max_response_time_ms:
            success = False
            details_list.append(
                f"Response time {elapsed_ms:.2f} ms exceeded "
                f"limit {self.config.max_response_time_ms:.2f} ms."
            )

        # JSON structure validation
        if required_json_paths:
            try:
                payload = response.json()
            except json.JSONDecodeError:
                success = False
                details_list.append("Response is not valid JSON.")
            else:
                for path in required_json_paths:
                    if not self._has_json_path(payload, path):
                        success = False
                        details_list.append(f"Missing JSON path: {path}")

        if not details_list:
            details_list.append("All checks passed.")

        return TestResult(
            name=name,
            success=success,
            status_code=status_code,
            response_time_ms=elapsed_ms,
            details=" ".join(details_list),
        )

    @staticmethod
    def _has_json_path(payload: Any, path: str) -> bool:
        """
        Check whether a dotted JSON path exists in the response.

        Example:
            path="data.id" checks payload["data"]["id"]

        If any key is missing, returns False.
        """
        parts = path.split(".")
        current: Any = payload

        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return False
            current = current[part]
        return True

    def _log_result(self, result: TestResult) -> None:
        """
        Log a single result in a clean, human-friendly format.
        """
        status_str = "PASS" if result.success else "FAIL"
        logger.info(
            "[%s] %s (status=%s, time=%s ms) - %s",
            status_str,
            result.name,
            result.status_code,
            f"{result.response_time_ms:.2f}" if result.response_time_ms is not None else "N/A",
            result.details,
        )

    def write_report(self, path: Path) -> None:
        """
        Write a JSON-like text report with all test results.

        Kept simple for clarity; can be replaced later with JUnit/HTML output.
        """
        logger.info("Writing test report to %s", path)
        lines: List[str] = []
        for res in self.results:
            status_str = "PASS" if res.success else "FAIL"
            response_time_str = f"{res.response_time_ms:.2f}" if res.response_time_ms else "N/A"
            line = (
                f"{status_str} | {res.name} | "
                f"status={res.status_code} | "
                f"time={response_time_str} ms | "
                f"{res.details}"
            )
            lines.append(line)

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("\n".join(lines), encoding="utf-8")
