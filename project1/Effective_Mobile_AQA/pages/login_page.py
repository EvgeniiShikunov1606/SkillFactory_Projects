from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    def open(self):
        self.driver.get(self.URL)

    def login(self, username="", password=""):
        self.driver.find_element(*self.USERNAME).clear()
        self.driver.find_element(*self.USERNAME).send_keys(username)
        self.driver.find_element(*self.PASSWORD).clear()
        self.driver.find_element(*self.PASSWORD).send_keys(password)
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def is_error_displayed(self):
        return WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(self.ERROR_MESSAGE)
        ).is_displayed()

    def get_error_text(self):
        return self.driver.find_element(*self.ERROR_MESSAGE).text
