from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from pages.contact_list_page import ContactListPage

class AuthService:
    def __init__(self, page: Page):
        self.page = page
        self.login_page = LoginPage(page)
        self.reg_page = RegistrationPage(page)
        self.contact_list_page = ContactListPage(page)

    def register_user(self, user_data: dict):
        self.login_page.navigate()
        self.login_page.click_sign_up()
        self.reg_page.register_user(
            user_data['firstName'],
            user_data['lastName'],
            user_data['email'],
            user_data['password']
        )
        self.contact_list_page.wait_for_page_load()

    def login_user(self, email, password):
        self.login_page.navigate()
        self.login_page.login(email, password)

    def logout_user(self):
        self.contact_list_page.logout()

    def error_message(self):
        error_msg = self.page.locator('#error')
        error_msg.wait_for(state="visible", timeout=5000)
        return error_msg

    def get_session_token(self):
        self.contact_list_page.wait_for_page_load()

        token = self.page.evaluate("window.localStorage.getItem('token')")
        
        if not token:
            cookies = self.page.context.cookies()
            token_cookie = next((c for c in cookies if c['name'] == 'token'), None)
            if token_cookie:
                token = token_cookie['value']
                
        return token