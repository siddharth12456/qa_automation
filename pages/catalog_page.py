from pages.base_page import BasePage
from playwright.sync_api import expect

class CatalogPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.search_input = page.locator("[data-test='search-query']")
        self.search_button = page.locator("[data-test='search-submit']")
        self.product_cards = page.locator(".card")

    def search_product(self, query: str):
        self.navigate("/")
        self.search_input.fill(query)
        self.search_button.click()
        expect(self.product_cards.first).to_be_visible()