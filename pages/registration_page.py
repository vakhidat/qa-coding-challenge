from playwright.sync_api import Page, Locator

class RegistrationPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input: Locator = page.locator('#firstName')
        self.last_name_input: Locator = page.locator('#lastName')
        self.email_input: Locator = page.locator('#email')
        self.password_input: Locator = page.locator('#password')
        self.submit_button: Locator = page.locator('#submit')
        self.cancel_button: Locator = page.locator('#cancel')

    def navigate(self):
        self.page.goto('/addUser')

    def register_user(self, firstName: str, lastName: str, email: str, password: str):
        self.first_name_input.fill(firstName)
        self.last_name_input.fill(lastName)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
