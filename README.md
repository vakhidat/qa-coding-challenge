# QA Automation Coding Challenge - Python Pytest & Playwright

This repository contains an end-to-end (E2E) UI and API automation framework built with [Python](https://www.python.org/), [Pytest](https://docs.pytest.org/), and [Playwright](https://playwright.dev/python/). The tests cover the core functionalities of the [Thinking Tester Contact List](https://thinking-tester-contact-list.herokuapp.com/) application.

## 🏛 Architecture and Design
This solution adheres to Clean Code principles with a strong emphasis on reusability and maintainability:
- **Language**: Python for robust scripting and testing.
- **Framework**: Pytest test runner combined with Playwright for browser automation.
- **Reporting**: [Allure Report](https://allurereport.org/) for comprehensive test results.
- **API Testing**: Playwright's native `APIRequestContext` (`request`) is used to validate backend endpoints.

## 📂 Project Structure
```text
.
├── pages/
│   ├── contact_list_page.py     # POM for Contact List verification
│   ├── login_page.py            # POM for Login form
│   └── registration_page.py     # POM for Add User form
├───services
│   ├── api_service.py           # Service handling the API calls
│   └── auth_service.py          # Service hadling POMs
├── tests/
│   ├── api/
│   │   └── test_contacts.py     # CRUD tests for Contacts API
│   └── ui/
│       └── test_auth.py         # User Registration and Login E2E UI flows
├── conftest.py                  # Pytest fixtures and overall testing configuration
├── pytest.ini                   # Pytest configuration file
└── requirements.txt             # Python dependencies
```

## 🚀 Setup & Execution

### 1. Prerequisites
- **Python** (version 3.8+ recommended) installed.
- **Allure Report** (https://allurereport.org/docs/v3/install/) installed on your machine

### 2. Installation
Open a terminal inside the project directory and run:

```bash
# It is recommended to use a virtual environment
python -m venv .venv

# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
# source .venv/bin/activate

# Install the Python dependencies
pip install -r requirements.txt

# Install Playwright browsers and dependencies
playwright install chromium
```

### 3. Running the Tests

To run all tests (UI and API):
```bash
pytest
```

To run only the UI tests in headed mode (visible browser):
```bash
pytest tests/ui --headed
```

To run only the API tests:
```bash
pytest tests/api
```

### 4. Generating Allure Reports
The project uses `allure-pytest` to generate test reports.
To run tests and generate results in the `allure-results` directory:
```bash
pytest --alluredir=allure-results
```

To view the generated HTML report:
```bash
allure serve allure-results
```

## 🧪 Test Coverage
1. **Challenge 1 (UI Testing)**: 
   - Scenario 1: Registers a new user to validate the registration flow.
   - Scenario 2: Logs in with the newly registered user credential to validate the login flow.
2. **Challenge 2 (API Testing)**:
   - Contains Pytest fixtures to generate a transient user.
   - Tests the sequence: Login -> Add Contact -> Get Contact -> Update Contact (PUT) -> Update Contact (PATCH) -> Delete Contact -> Teardown (Delete User).
   - Validation assertions exist on correct HTTP Status codes and response JSON payloads.
