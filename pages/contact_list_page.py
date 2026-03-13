from playwright.sync_api import Page, Locator

class ContactListPage:
    def __init__(self, page: Page):
        self.page = page
        self.logout_button: Locator = page.locator('#logout')
        self.add_contact_button: Locator = page.locator('#add-contact')

    def wait_for_page_load(self):
        self.page.wait_for_url('**/contactList')

    def logout(self):
        self.logout_button.click()
