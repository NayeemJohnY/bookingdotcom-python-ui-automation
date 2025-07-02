"""WebDriver Manager with Manage browser instance and manage actions on browser"""
import logging

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


def get_driver(browser="chrome", headless=None):
    """To create and get webdriver"""
    driver = None
    if browser == "chrome":
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--incognito")
        if headless:
            chrome_options.add_argument("--headless")
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

    def goto_url(self, url):
        """Navigate to URL"""
        logger.info("Launching URL %s", url)
        self.driver.get(url)

    def wait_for_page_title_contains(self, title):
        """Wait for page title to contains given page title

        Args:
            title (str): Expected title to be contained by page title.

        Raises:
            TimeoutException : if page title is NOT contains the given title in a wait time.
        """
        self.wait.until(EC.title_contains(title),
                        "Page title not contains given value")

    def get_element_name_locator(self, locator, elem_name, replace_value=None):
        """Get element and locator name

        Args:
            locator (tuple): tuple with locator type and locator string.
            elem_name (str): description of the element.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.

        Returns:
            tuple: tuple of updated locator with replace value and updated 
        """
        if replace_value is not None:
            if not isinstance(replace_value, (list, tuple)):
                replace_value = [replace_value]
            locator = locator[0], locator[1].format(*replace_value)
            elem_name += f" with replace value {replace_value}"
        return locator, elem_name

    def _visibility_of_element(self, locator: tuple, elem_name,  wait_time=None):
        """Wait for element to be visible

        Args:
            locator (tuple): tuple with locator type and locator string.
            elem_name (str): description of the element.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.

        Returns:
            WebElement : WebElement once it is located and visible
        """
        ele_wait = WebDriverWait(
            self.driver, wait_time) if wait_time else self.wait
        elem = ele_wait.until(EC.visibility_of_element_located(
            locator), self.wait_msg.format(elem_name, locator))
        return elem

    def wait_for_element_to_be_visible(self, locator: tuple, elem_name, replace_value=None, wait_time=None):
        """Wait for element to be visible

        Args:
            locator (tuple): tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        logger.info("Waiting for element %s to be visible", elem_name)
        self._visibility_of_element(locator, elem_name, wait_time)
        logger.info("Element %s is visible", elem_name)

    def is_element_present(self, locator: tuple, elem_name: str, stop_on_fail=False, replace_value=None, wait_time=None):
        """To check if element is present

        Args:
            locator (tuple): tuple with locator type and locator string.
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
            self._visibility_of_element(locator, elem_name, wait_time)
        except (NoSuchElementException, TimeoutException) as ex:
            logger.info("Element %s is not present", elem_name)
            if stop_on_fail:
                raise ex
            return False
        logger.info("Element %s is present", elem_name)
        return True

    def click(self, locator: tuple, elem_name: str, replace_value=None, wait_time=None):
        """To click on the Element

        Args:
            locator (tuple): tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        element = self._visibility_of_element(locator, elem_name, wait_time)
        element.click()
        logger.info("Cicked on the %s", elem_name)

    def type_value(self, locator: tuple, value: str, elem_name: str, replace_value=None, wait_time=None):
        """Type value inside the element

        Args:
            locator (tuple): tuple with locator type and locator string.
            value (str): value to type inside input
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        element = self._visibility_of_element(locator, elem_name, wait_time)
        element.clear()
        element.send_keys(value)
        logger.info("Entered text %s in the %s", value, elem_name)

    def select_value_from_dropdown(self, locator, value, elem_name: str, replace_value=None, wait_time=None):
        """Select value from Dropdown

        Args:
            locator (tuple): tuple with locator type and locator string.
            value (str): dropdown value to be selected
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        select = Select(self._visibility_of_element(
            locator, elem_name, wait_time))
        select.select_by_value((str)(value))
        logger.info("Selected %s dropdown by value %s", elem_name, value)

    def execute_js_script_on_element(self, script, locator, elem_name: str, replace_value=None, wait_time=None):
        """Move a element by offset

        Args:
            locator (tuple): tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        ele_wait = WebDriverWait(
            self.driver, wait_time) if wait_time else self.wait
        ele = ele_wait.until(EC.presence_of_element_located(
            locator), self.wait_msg.format(elem_name, locator))
        value = self.driver.execute_script(script, ele)
        logger.info(
            "Executed JS Script on Element %s on returned value %s", elem_name, value)
        return value

    def click_on_element_by_offset(self, locator, elem_name: str, xoffset=0, yoffset=0, replace_value=None, wait_time=None):
        """Move to element by offset and then click

        Args:
            locator (tuple): tuple with locator type and locator string.
            elem_name (str): description of the element.
            xoffset: X offset to move to, as a positive or negative integer.
            yoffset: Y offset to move to, as a positive or negative integer.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        actions = ActionChains(self.driver)
        ele = self._visibility_of_element(locator, elem_name, wait_time)
        actions.move_to_element_with_offset(
            ele, xoffset, yoffset).click().perform()
        logger.info("Moved & Cliked on Element %s by offset %s",
                    elem_name, [xoffset, yoffset])

    def get_number_of_elements(self, locator: tuple, elem_name: str, replace_value=None, wait_time=None):
        """To get Number of webelements

        Args:
            locator (tuple): tuple with locator type and locator string.
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
    
    def get_element_text(self, locator: tuple, elem_name: str, replace_value=None, wait_time=None):
        """To get element text

        Args:
            locator (tuple): tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        
        Returns
            str : Element text string
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value)
        ele = self._visibility_of_element(locator, elem_name, wait_time)
        return ele.text or ele.get_attribute('textContent')