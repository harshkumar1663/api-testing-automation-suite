"""
Definition of specific API test cases.

These use the public mock API at https://reqres.in to avoid needing
a private backend for demonstration.

Author: Harsh Kumar
"""

from __future__ import annotations

from typing import List

from .core_tester import APITestSuite, TestResult


def run_all_tests(suite: APITestSuite) -> List[TestResult]:
    """
    Register and run all test cases using the given APITestSuite.
    Returns a list of TestResult objects.
    """

    results: List[TestResult] = []

    # ------------------------------------------------------------------ #
    # GET tests
    # ------------------------------------------------------------------ #

    # Example: GET /users/2 -> expect a single user object
    results.append(
        suite.run_get_test(
            name="GET single user (id=2)",
            path="/users/2",
            expected_status=200,
            required_json_paths=[
                "data.id",
                "data.email",
                "data.first_name",
                "data.last_name",
            ],
        )
    )

    # Example: GET /users?page=2 -> expect list
    results.append(
        suite.run_get_test(
            name="GET users list (page=2)",
            path="/users?page=2",
            expected_status=200,
            required_json_paths=[
                "page",
                "data",  # ensure `data` list field exists
            ],
        )
    )

    # ------------------------------------------------------------------ #
    # POST tests
    # ------------------------------------------------------------------ #

    # Example: POST /users -> create user
    results.append(
        suite.run_post_test(
            name="POST create user",
            path="/users",
            payload={
                "name": "Harsh Bot",
                "job": "automation-tester",
            },
            expected_status=201,
            required_json_paths=[
                "name",
                "job",
                "id",
                "createdAt",
            ],
        )
    )

    # Example: POST /login with missing password (should fail with 400)
    results.append(
        suite.run_post_test(
            name="POST login without password (negative test)",
            path="/login",
            payload={
                "email": "peter@klaven",
            },
            expected_status=400,
            required_json_paths=[
                "error",
            ],
        )
    )

    return results
