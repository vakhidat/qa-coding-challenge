import pytest
from playwright.sync_api import APIRequestContext, Playwright
from typing import Generator
from services.auth_service import AuthService
from services.api_service import ApiService

@pytest.fixture(scope="session")
def api_context(playwright: Playwright, target_url: str) -> Generator[APIRequestContext, None, None]:
    # We create an isolated APIRequestContext for API operations
    request_context = playwright.request.new_context(base_url=target_url)
    yield request_context
    request_context.dispose()

@pytest.fixture(scope="session")
def target_url():
    return "https://thinking-tester-contact-list.herokuapp.com"

@pytest.fixture
def auth_service(page):
    return AuthService(page)

@pytest.fixture(scope="class")
def api_service(api_context: APIRequestContext):
    return ApiService(api_context)

@pytest.fixture(scope="function")
def clean_page(browser: Browser):
    """
    Creates a brand new browser context and page for every test.
    This ensures no cookies or local storage leak between tests.
    """
    context = browser.new_context()
    page = context.new_page()
    yield page
    page.close()
    context.close()
