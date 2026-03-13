import pytest
import time
import re
from playwright.sync_api import expect, APIRequestContext

from typing import Dict, Optional

class TestRegistration:
    test_user: Optional[Dict[str, str]] = None

    @pytest.fixture(scope="class", autouse=True)
    def setup_user(self):
        timestamp = int(time.time() * 1000)
        TestRegistration.test_user = {
            'firstName': 'Brand',
            'lastName': 'NewUser',
            'email': f'reguser_{timestamp}@test.com',
            'password': 'myPassword123!',
        }

    def test_registration_success(self, auth_service: AuthService):
        """Successful user registration"""
        auth_service.register_user(self.test_user)
        
        expect(auth_service.contact_list_page.logout_button).to_be_visible()
        
        auth_service.logout_user()
        expect(auth_service.page).to_have_url(re.compile(r".*/$"))

    def test_duplicate_user_prevention(self, auth_service: AuthService):
        """Attempting to register with an existing email triggers an error"""
        auth_service.login_page.navigate()
        auth_service.login_page.click_sign_up()
        auth_service.reg_page.register_user(**self.test_user) 

        error_msg = auth_service.error_message()
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text("Email address is already in use", timeout=10000)

    def test_empty_form_submission(self, auth_service: AuthService):
        """Submitting an empty form triggers an error message"""
        auth_service.login_page.navigate()
        auth_service.login_page.click_sign_up()

        auth_service.reg_page.submit_button.click()

        error_msg = auth_service.error_message()
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text("User validation failed")

class TestLogin:
    test_user: Optional[Dict[str, str]] = None
    token: Optional[str] = None

    @pytest.fixture(scope="class", autouse=True)
    def setup_existing_user(self, api_context: APIRequestContext):
        """Creates a user via the API for login tests"""
        timestamp = int(time.time() * 1000)
        TestLogin.test_user = {
            'firstName': 'Login',
            'lastName': 'User',
            'email': f'loginuser_{timestamp}@test.com',
            'password': 'myPassword123!',
        }
        res = api_context.post('/users', data=TestLogin.test_user)
        assert res.ok, "Registration failed"
        
        TestLogin.token = res.json()['token']

        yield
        if TestLogin.token:
            api_context.delete('/users/me', headers={'Authorization': f'Bearer {TestLogin.token}'})

    def test_standard_login(self, auth_service: AuthService):
        """Successful authentication with valid credentials and redirect to Dashboard"""
        auth_service.login_user(self.test_user['email'], self.test_user['password'])
        auth_service.contact_list_page.wait_for_page_load()

        expect(auth_service.contact_list_page.logout_button).to_be_visible()
        
        auth_service.logout_user()

    def test_invalid_credentials(self, auth_service: AuthService):
        """Verify an error message appears for incorrect password"""
        auth_service.login_user(self.test_user['email'], "WrongPassword123!")

        error_msg = auth_service.error_message()
 
        expect(error_msg).to_be_visible()
        expect(error_msg).to_contain_text("Incorrect username or password")

    def test_auth_session_token(self, auth_service: AuthService):
        """Verify that a valid token is stored upon login"""
        auth_service.login_user(self.test_user['email'], self.test_user['password'])

        token = auth_service.get_session_token()
        assert token is not None, "Token was not found in localStorage or Cookies after login"
        assert len(token) > 20, f"Token seems too short to be a valid one: {token}"
        
        auth_service.logout_user()

        def test_logout_success(self, auth_service: AuthService):
            """User is redirected back"""
            auth_service.login_user(self.test_user['email'], self.test_user['password'])
            auth_service.contact_list_page.wait_for_page_load()
            
            with auth_service.page.expect_response("**/users/logout"):
                auth_service.logout_user()
                    
            expect(auth_service.page).to_have_url(re.compile(r".*login|/$"))
            