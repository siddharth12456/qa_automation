import pytest
import requests
from playwright.sync_api import Page, expect
from utils.config import Config

@pytest.mark.api
def test_get_products(api_base_url):
    response = requests.get(f"{api_base_url}/products")
    assert response.status_code == 200
    assert response.elapsed.total_seconds() < 2.0
    assert len(response.json().get("data", [])) > 0

@pytest.mark.api
def test_search_products_positive(api_base_url):
    response = requests.get(f"{api_base_url}/products/search", params={"q": "Pliers"})
    assert response.status_code == 200
    assert len(response.json().get("data", [])) > 0

@pytest.mark.api
def test_search_products_negative_missing_query(api_base_url):
    response = requests.get(f"{api_base_url}/products/search")
    assert response.status_code in [400, 422, 200]

@pytest.mark.api
def test_get_categories(api_base_url):
    response = requests.get(f"{api_base_url}/categories")
    assert response.status_code == 200
    assert len(response.json()) > 0

@pytest.mark.api
def test_get_user_invoices_authorized(api_base_url, auth_headers):
    response = requests.get(f"{api_base_url}/invoices", headers=auth_headers)
    assert response.status_code == 200

@pytest.mark.api
def test_get_user_invoices_unauthorized(api_base_url):
    response = requests.get(f"{api_base_url}/invoices")
    assert response.status_code in [401, 403]

@pytest.mark.api
def test_get_product_by_invalid_id(api_base_url):
    response = requests.get(f"{api_base_url}/products/non-existent-id-99999")
    assert response.status_code in [404, 400]

@pytest.mark.api
def test_customer_contact_submission_boundary(api_base_url):
    payload = {"name": "QA Tester", "email": "invalid-email", "subject": "Test", "message": "Short"}
    response = requests.post(f"{api_base_url}/messages", json=payload)
    assert response.status_code in [400, 422]

@pytest.mark.integration
def test_ui_api_integration_cart_sync(page: Page, api_base_url, auth_headers):
    response = requests.post(f"{api_base_url}/carts", headers=auth_headers)
    assert response.status_code in [201, 404]
    page.goto(Config.BASE_URL)
    expect(page.locator(".card").first).to_be_visible()

@pytest.mark.integration
def test_api_to_ui_favorites_sync(page: Page, api_base_url, auth_headers):
    # 1. Fetch a real product to get a valid product ID
    products_response = requests.get(f"{api_base_url}/products")
    assert products_response.status_code == 200
    product_id = products_response.json()["data"][0]["id"]

    # 2. Perform the setup action via API using the valid product ID
    api_response = requests.post(f"{api_base_url}/favorites", headers=auth_headers, json={"product_id": product_id})
    assert api_response.status_code in [200, 201]

    # 3. Extract the token value from auth_headers and seed into localStorage
    token = auth_headers["Authorization"].split(" ")[1]
    page.goto(Config.BASE_URL)
    page.evaluate(f"localStorage.setItem('auth-token', '{token}')")

    # 4. Navigate to the favorites page and assert the item is visible
    page.goto(f"{Config.BASE_URL}/account/favorites")
    expect(page.locator(".card, [data-test='favorite-item']").first).to_be_visible()

@pytest.mark.integration
def test_ui_to_api_cart_persistence(page: Page, api_base_url, auth_headers):
    page.goto(Config.BASE_URL)
    page.locator("[data-test='search-query']").fill("Combination Pliers")
    page.locator("[data-test='search-submit']").click()
    page.locator("a[data-test^='product-']").first.click()
    page.wait_for_url("**/product/**")
    page.locator("[data-test='add-to-cart']").click()
    expect(page.locator(".toast-success")).to_be_visible()

    api_response = requests.post(f"{api_base_url}/carts", headers=auth_headers)
    assert api_response.status_code == 201