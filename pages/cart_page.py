from pages.base_page import BasePage
from playwright.sync_api import expect

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.cart_menu_link = page.locator("[data-test='nav-cart']")
        self.quantity_input = page.locator("input[type='number']")

    def open_cart(self):
        self.cart_menu_link.click()
        self.page.wait_for_url("**/checkout")

    def update_quantity(self, quantity_value: str):
        expect(self.quantity_input).to_be_visible()
        self.quantity_input.fill(quantity_value)
        self.quantity_input.press("Enter")