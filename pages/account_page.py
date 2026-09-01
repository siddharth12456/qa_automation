from pages.base_page import BasePage
from playwright.sync_api import expect

class AccountPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Locators specific to the user account dashboard
        self.page_title = page.locator("h1, h2, h3").filter(has_text="My Account")
        self.profile_menu_item = page.locator("[data-test='nav-profile']")
        self.my_orders_menu_item = page.locator("[data-test='nav-my-orders']")

    def verify_account_page_loaded(self):
        """Verify that the user has successfully landed on the account dashboard."""
        self.page.wait_for_url("**/account")
        expect(self.page_title).to_be_visible()