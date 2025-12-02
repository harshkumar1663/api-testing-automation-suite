# API Testing Automation Suite

**Author:** Harsh Kumar  
**Target Roles:** QA Automation Engineer / Backend Developer Intern


## 1. Purpose of the Project

This project is a small but realistic **API Testing Automation Suite** written in Python.

It is designed to demonstrate how a junior QA Automation Engineer or Backend Developer
would test REST APIs programmatically:

- Hitting real HTTP endpoints
- Validating status codes
- Checking JSON structure
- Measuring response times
- Logging pass/fail results
- Generating a simple report

The project uses a public mock API (**https://reqres.in**) so the tests can be run
without any private backend.


## 2. How It Works

The suite is intentionally structured like a lightweight internal testing tool:

1. **Configuration**  
   `api_tests/config.py` holds a `Config` object with:
   - `base_url` of the API under test
   - request timeout
   - maximum allowed response time
   - directories for logs and reports

2. **HTTP Client**  
   `api_tests/http_client.py` wraps the `requests` library:
   - Handles GET and POST
   - Applies timeouts
   - Centralizes logging and error handling

3. **Core Tester**  
   `api_tests/core_tester.py` implements:
   - `APITestSuite` with `run_get_test` and `run_post_test`
   - status code validation
   - response time validation
   - JSON structure validation via dotted key paths (`"data.id"`, `"data.email"`, etc.)
   - `TestResult` dataclass to track outcome, status, time, and details
   - simple text report writer (`write_report`)

4. **Test Cases**  
   `api_tests/test_cases.py` defines **concrete tests** against `https://reqres.in/api`, e.g.:
   - GET single user
   - GET users list
   - POST create user
   - POST login negative scenario (missing password)

5. **Test Runner**  
   `run_tests.py`:
   - sets up logging (console + `logs/api_tests.log`)
   - creates `Config`, `HttpClient`, `APITestSuite`
   - runs all tests from `test_cases.py`
   - prints a clean summary to the console
   - writes a detailed report to the `reports/` directory

## 3. Folder Structure

```text
api-testing-automation-suite/
├─ api_tests/
│  ├─ __init__.py           # Package metadata
│  ├─ config.py             # Config (base URL, timeouts, paths)
│  ├─ http_client.py        # Wrapper over `requests`
│  ├─ core_tester.py        # Test suite, validations, reporting
│  └─ test_cases.py         # Concrete API test definitions
├─ logs/                    # Log files (runtime)
│  └─ .gitkeep
├─ reports/                 # Test reports (runtime)
│  └─ .gitkeep
├─ run_tests.py             # Main test runner script
├─ requirements.txt         # Python dependencies
└─ README.md
