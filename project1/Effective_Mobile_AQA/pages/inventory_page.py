from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_CONTAINER = (By.ID, "inventory_container")

    def is_opened(self):
        return self.is_visible(self.INVENTORY_CONTAINER)
