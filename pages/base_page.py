from playwright.sync_api import Page, expect

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = ""):
        self.page.goto(f"https://practicesoftwaretesting.com{path}")

    def wait_for_load(self):
        self.page.wait_for_load_state("networkidle")