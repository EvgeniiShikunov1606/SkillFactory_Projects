import allure
from utils.driver_factory import get_driver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@allure.feature('Login')
class TestLogin:

    def setup_method(self):
        self.driver = get_driver()
        self.login_page = LoginPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    @allure.story('Successful login')
    def test_successful_login(self):
        self.login_page.open()
        self.login_page.login('standard_user', 'secret_sauce')

        inventory = InventoryPage(self.driver)
        assert 'inventory.html' in inventory.get_current_url()
        assert inventory.is_opened()

    @allure.story('Wrong password')
    def test_login_wrong_password(self):
        self.login_page.open()
        self.login_page.login('standard_user', 'wrong_password')

        assert self.login_page.get_error_text() == \
               'Epic sadface: Username and password do not match any user in this service'

    @allure.story('Locked user')
    def test_login_locked_user(self, driver):
        self.login_page.open()
        self.login_page.login('locked_out_user', 'secret_sauce')

        assert self.login_page.get_error_text() == \
               'Epic sadface: Sorry, this user has been locked out.'

    @allure.story('Empty fields')
    def test_login_empty_fields(self):
        self.login_page.open()
        self.login_page.login()

        assert self.login_page.get_error_text() == \
               'Epic sadface: Username is required'

    @allure.story('Performance glitch user')
    def test_login_performance_user(self):
        self.login_page.open()
        self.login_page.login('performance_glitch_user', 'secret_sauce')

        inventory = InventoryPage(self.driver)
        assert inventory.is_opened()
