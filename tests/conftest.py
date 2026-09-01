import pytest
from playwright.sync_api import Browser, Playwright

@pytest.fixture(scope="session")
def shared_page(playwright: Playwright):
    # Launch browser once for the entire test session
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    yield page
    
    # Teardown after all tests complete
    context.close()
    browser.close()