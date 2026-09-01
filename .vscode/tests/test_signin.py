from pages.login_page import LoginPage
from utils.config import Config

def test_login_page_elements_and_interaction(page):
    login_page = LoginPage(page)
    
    # 1. Navigate directly to the login page route
    login_page.navigate("/auth/login")
    
    # 2. Verify visibility of input fields and submit control
    assert login_page.email_input.is_visible()
    assert login_page.password_input.is_visible()
    assert login_page.login_button.is_visible()
    
    # 3. Perform a test login execution using configuration credentials
    login_page.login(Config.VALID_USER_EMAIL, Config.VALID_USER_PASSWORD)
    
    # 4. Assert successful transition away from the login route to the user account page
    page.wait_for_url("**/account")
    assert "account" in page.url