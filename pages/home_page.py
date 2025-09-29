"""Home Page Functions"""

from pages.hotels_page import HotelsPage
import time
import constants
from helpers.driver_manager import WebDriverOps
from locators.common_locators import *
from locators.home_page_locators import *


class HomePage:
    """Home Page class"""

    def __init__(self, webdriver_ops):
        self.webdriver_ops: WebDriverOps = webdriver_ops

    def verify_home_page(self):
        """Verify Home page"""
        time.sleep(20)
        self.webdriver_ops.click(login_popup_close_button, "Login Popup Close Button")
        self.webdriver_ops.wait_for_page_title_contains(constants.HOME_PAGE_TITLE)
        self.webdriver_ops.is_element_present(
            generic_text_locator, "Login Header", True, "Login or Create Account"
        )
        self.webdriver_ops.wait_for_element_to_be_visible(
            header_menu_active, "Header Active Menu", "Flights"
        )

    def navigate_to_menu_page(self, menu_name: str):
        """Navigate to menu page

        Args:
            menu_name (str): Menu Name to navigate
        """
        self.webdriver_ops.click(header_menu, "Header Menu", menu_name)
        return HotelsPage(self.webdriver_ops)
