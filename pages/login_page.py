from playwright.sync_api import Page, Locator

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.email_input: Locator = page.locator('#email')
        self.password_input: Locator = page.locator('#password')
        self.submit_button: Locator = page.locator('#submit')
        self.sign_up_button: Locator = page.locator('#signup')
        self.error_msg: Locator = page.locator('#error')

    def navigate(self):
        self.page.goto('/')

    def login(self, email: str, password: str):
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def click_sign_up(self):
        self.sign_up_button.click()
