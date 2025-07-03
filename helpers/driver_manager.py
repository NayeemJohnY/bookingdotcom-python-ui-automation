"""WebDriver Manager with Manage browser instance and manage actions on browser"""
import logging
from typing import Tuple, List, Union

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from locators.home_page_locators import dismiss_sign_in_popup_button
import functools
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


def get_driver(browser="chrome", headless=None):
    """To create and get webdriver"""
    driver = None
    if browser == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--window-size=1920,1080") 
        if headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
    else:
        raise ValueError("Unsupported browser name " + browser)
    return driver


class WebDriverOps:
    """WebDriver Actions class with Browser Actions functions"""
    wait: WebDriverWait
    wait_msg = "Element {} with Locator {}"

    def __init__(self, driver: WebDriver, timeout=60):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def goto_url(self, url: str):
        """Navigate to URL"""
        logger.info("Launching URL %s", url)
        self.driver.get(url)

    def wait_for_page_title_contains(self, title: str):
        """Wait for page title to contains given page title

        Args:
            title (str): Expected title to be contained by page title.

        Raises:
            TimeoutException : if page title is NOT contains the given title in a wait time.
        """
        self.wait.until(EC.title_contains(title),
                        "Page title not contains given value")

    @staticmethod
    def handle_sign_in_popup(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            
            if not getattr(self, "_sign_in_popup_dismissed", False) and self.is_element_present(
                    dismiss_sign_in_popup_button, "Sign in Pop up dismiss Icon", wait_time=1):
                element = self._wait_for_element_condition(
                    dismiss_sign_in_popup_button, "Sign in Pop up dismiss Icon",
                    EC.element_to_be_clickable)
                element.click()
                logger.info("Closed Sign In Popup")
                self._sign_in_popup_dismissed = True  # Mark as dismissed
            return func(self, *args, **kwargs)
        return wrapper

    def get_element_name_locator(self, locator: Tuple[By, str], elem_name: str, replace_value: Union[str, List, Tuple] = None) -> Tuple[Tuple[By, str], str]:
        """Get element and locator name

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.

        Returns:
            Tuple: Tuple of updated locator with replace value and updated 
        """
        if replace_value is not None:
            if not isinstance(replace_value, (list, Tuple)):
                replace_value = [replace_value]
            locator = locator[0], locator[1].format(*replace_value)
            elem_name += f" with replace value {replace_value}"
        return locator, elem_name

    def _wait_for_element_condition(self, locator: Tuple[By, str], elem_name: str, condition: callable, wait_time: float = None) -> WebElement:
        """Wait for element condition

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.

        Returns:
            WebElement : WebElement once it is located and visible
        """
        ele_wait = WebDriverWait(
            self.driver, wait_time) if wait_time else self.wait
        elem = ele_wait.until(condition(locator),
                              self.wait_msg.format(elem_name, locator))
        return elem

    def wait_for_element_to_be_visible(self, locator: Tuple[By, str], elem_name, replace_value: Union[str, List, Tuple] = None, wait_time: float = None):
        """Wait for element to be visible

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        logger.info("Waiting for element %s to be visible", elem_name)
        self._wait_for_element_condition(
            locator, elem_name, EC.visibility_of_element_located, wait_time)
        logger.info("Element %s is visible", elem_name)

    def is_element_present(self, locator: Tuple[By, str], elem_name: str, stop_on_fail=False, replace_value: Union[str, List, Tuple] = None, wait_time: float = None) -> bool:
        """To check if element is present

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            stop_on_fail (bool, optional): Allow to raise the exception if element is not found. Defaults to False.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.

        Raises:
            NoSuchElementException | TimeoutException: Exception if stop_on_fail is equal to True.

        Returns:
            bool: `True` if element is found else `False`.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        try:
            self._wait_for_element_condition(
                locator, elem_name, EC.visibility_of_element_located, wait_time)
        except (NoSuchElementException, TimeoutException) as ex:
            logger.info("Element %s is not present", elem_name)
            if stop_on_fail:
                raise ex
            return False
        logger.info("Element %s is present", elem_name)
        return True

    @handle_sign_in_popup
    def click(self, locator: Tuple[By, str], elem_name: str, replace_value: Union[str, List, Tuple] = None, wait_time: float = None):
        """To click on the Element

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        element = self._wait_for_element_condition(
            locator, elem_name, EC.element_to_be_clickable, wait_time)
        element.click()
        logger.info("Clicked on the %s", elem_name)

    @handle_sign_in_popup
    def enter_text(self, locator: Tuple[By, str], value: str, elem_name: str, replace_value: Union[str, List, Tuple] = None, wait_time: float = None):
        """Type value inside the element

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            value (str): value to type inside input
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        element = self._wait_for_element_condition(
            locator, elem_name, EC.visibility_of_element_located, wait_time)
        element.clear()
        element.send_keys(value)
        logger.info("Entered text %s in the %s", value, elem_name)

    @handle_sign_in_popup
    def select_value_from_dropdown(self, locator, value, elem_name: str, replace_value: Union[str, List, Tuple] = None, wait_time: float = None):
        """Select value from Dropdown

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            value (str): dropdown value to be selected
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        select = Select(self._wait_for_element_condition(
            locator, elem_name, EC.visibility_of_element_located, wait_time))
        select.select_by_value((str)(value))
        logger.info("Selected %s dropdown by value %s", elem_name, value)

    def execute_js_script_on_element(self, script, locator, elem_name: str, replace_value: Union[str, List, Tuple] = None, wait_time: float = None) -> str:
        """Move a element by offset

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        element = self._wait_for_element_condition(
            locator, elem_name, EC.presence_of_element_located, wait_time)
        value = self.driver.execute_script(script, element)
        logger.info(
            "Executed JS Script on Element %s on returned value %s", elem_name, value)
        return value

    @handle_sign_in_popup
    def click_on_element_by_offset(self, locator, elem_name: str, xoffset=0, yoffset=0, replace_value: Union[str, List, Tuple] = None, wait_time: float = None):
        """Move to element by offset and then click

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            xoffset: X offset to move to, as a positive or negative integer.
            yoffset: Y offset to move to, as a positive or negative integer.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        actions = ActionChains(self.driver)
        ele = self._wait_for_element_condition(
            locator, elem_name, EC.element_to_be_clickable, wait_time)
        actions.move_to_element_with_offset(
            ele, xoffset, yoffset).click().perform()
        logger.info("Moved & Clicked on Element %s by offset %s",
                    elem_name, [xoffset, yoffset])

    def get_number_of_elements(self, locator: Tuple[By, str], elem_name: str, replace_value: Union[str, List, Tuple] = None, wait_time: float = None) -> int:
        """To get Number of webelements

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.

        Returns
            int : Number of webelements
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        ele_wait = WebDriverWait(
            self.driver, wait_time) if wait_time else self.wait
        elements = ele_wait.until(
            EC.visibility_of_all_elements_located(locator), self.wait_msg.format(elem_name, locator))
        return len(elements)

    def get_element_text(self, locator: Tuple[By, str], elem_name: str, replace_value: Union[str, List, Tuple] = None, wait_time: float = None) -> str:
        """To get element text

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.

        Returns
            str : Element text string
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        ele = self._wait_for_element_condition(
            locator, elem_name, EC.presence_of_element_located, wait_time)
        return ele.text or ele.get_attribute('textContent')
