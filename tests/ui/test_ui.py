import pytest
from playwright.sync_api import expect
import re
from pages.signin_page import SigninPage
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage
from utils.config import Config

def test_successful_login(page):
    signin_page = SigninPage(page)
    signin_page.login(Config.VALID_USER_EMAIL, Config.VALID_USER_PASSWORD)
    page.wait_for_url("**/account", timeout=5000)
    assert "account" in page.url

def test_unsuccessful_login(page):
    signin_page = SigninPage(page)
    signin_page.login("invalid@user.com", "wrongpassword")
    error_msg = page.locator(".alert-danger")
    expect(error_msg).to_be_visible()

def test_product_search_and_filtering(page):
    catalog = CatalogPage(page)
    catalog.search_product("Pliers")
    assert catalog.product_cards.count() > 0

def test_product_details_and_cart_addition(page):
    catalog = CatalogPage(page)
    catalog.search_product("Combination Pliers")
    
    # Click specifically on the product title link to ensure reliable navigation
    page.locator("a[data-test^='product-']").first.click()
    page.wait_for_url("**/product/**")
    
    # Add to cart
    add_to_cart_btn = page.locator("[data-test='add-to-cart']")
    expect(add_to_cart_btn).to_be_visible()
    add_to_cart_btn.click()
    
    # Verify success toast notification
    success_alert = page.locator(".toast-success")
    expect(success_alert).to_be_visible()

def test_cart_quantity_update_and_total(page):
    catalog = CatalogPage(page)
    catalog.search_product("Combination Pliers")
    
    page.locator("a[data-test^='product-']").first.click()
    page.wait_for_url("**/product/**")
    
    page.locator("[data-test='add-to-cart']").click()
    
    cart_page = CartPage(page)
    cart_page.open_cart()

    # Modify quantity field
    qty_input = page.locator("input[data-test='product-quantity']")
    expect(qty_input).to_be_visible()
    qty_input.fill("2")
    qty_input.press("Enter")

    # Validate updated total using text filter matching the expected price row
    total_cell = page.locator("td").filter(has_text="$28.30").first
    expect(total_cell).to_be_visible()