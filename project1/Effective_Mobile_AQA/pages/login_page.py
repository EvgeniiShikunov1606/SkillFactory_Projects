from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    def open(self):
        self.open_url(self.URL)

    def login(self, username="", password=""):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def is_error_displayed(self):
        return self.is_visible(self.ERROR_MESSAGE)

    def get_error_text(self):
        return self.get_text(self.ERROR_MESSAGE)
