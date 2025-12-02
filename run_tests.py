"""
Test runner script for the API Testing Automation Suite.

- Sets up logging
- Instantiates Config + HttpClient + APITestSuite
- Runs all defined test cases
- Prints a clean console summary
- Writes a text report to the reports/ directory

Author: Harsh Kumar
"""

from __future__ import annotations

import logging
from datetime import datetime
from pathlib import Path

from api_tests.config import get_config
from api_tests.core_tester import APITestSuite, TestResult
from api_tests.http_client import HttpClient
from api_tests.test_cases import run_all_tests


def setup_logging(logs_dir: Path) -> None:
    """
    Configure logging to both console and file.
    """
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / "api_tests.log"

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def print_summary(results: list[TestResult]) -> None:
    """
    Print a compact test summary to the console.
    """
    total = len(results)
    passed = sum(1 for r in results if r.success)
    failed = total - passed

    print("\n" + "=" * 60)
    print("API TEST SUMMARY".center(60))
    print("=" * 60)
    for res in results:
        status = "PASS" if res.success else "FAIL"
        response_time_str = f"{res.response_time_ms:.2f}" if res.response_time_ms else "N/A"
        print(
            f"{status:<5} | {res.name:<40} "
            f"| status={res.status_code} "
            f"| time={response_time_str} ms"
        )
    print("-" * 60)
    print(f"Total: {total} | Passed: {passed} | Failed: {failed}")
    print("=" * 60 + "\n")


def main() -> None:
    """
    Main entry point. Wires everything together.
    """
    config = get_config()
    setup_logging(config.logs_dir)

    logger = logging.getLogger(__name__)
    logger.info("Starting API Testing Automation Suite")

    client = HttpClient(config)
    suite = APITestSuite(config, client)

    results = run_all_tests(suite)

    # Write report to file
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    report_path = config.reports_dir / f"api_test_report_{timestamp}.txt"
    suite.write_report(report_path)

    print_summary(results)
    logger.info("API Testing Automation Suite finished. Report: %s", report_path)


if __name__ == "__main__":
    main()
