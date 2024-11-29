import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="module")
def setup_playwright():
    with sync_playwright() as p:
        yield p

def test_enter_first_activity(setup_playwright):
    browser = setup_playwright.chromium.launch(headless=True)  
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://frontend-4713090974.us-east1.run.app/home")
    assert "Trippi" in page.title()

    page.wait_for_selector("div.overflow-hidden.hover\\:scale-105.transition.duration-200.rounded-2xl.cursor-pointer")
    first_activity = page.locator("div.overflow-hidden.hover\\:scale-105.transition.duration-200.rounded-2xl.cursor-pointer").first
    first_activity.click()
    page.wait_for_timeout(5000)
    assert "/activities/" in page.url, f"Failed to navigate to activity detail. Current URL: {page.url}"

    context.close()
    browser.close()
