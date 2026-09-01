from pages.base_page import BasePage
from playwright.sync_api import expect

class SigninPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.email_input = page.locator("[data-test='email']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-submit']")

    def login(self, email: str, password: str):
        self.navigate("/auth/login")
        self.email_input.fill(email)
        self.password_input.fill(password)
        # Explicitly ensure the button is visible and clickable before clicking
        expect(self.login_button).to_be_visible()
        self.login_button.click()