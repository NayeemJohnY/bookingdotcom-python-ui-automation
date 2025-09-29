"""WebDriver Manager with Manage browser instance and manage actions on browser"""

import base64
from fake_useragent import UserAgent
import logging
import os
from datetime import datetime
from typing import List, Tuple, Union

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


logger = logging.getLogger(__name__)

SCREENSHOTS_DIR = os.path.join("test-results", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)


def add_chromium_options(options, width, height, headless):
    """Add Chromium Options"""
    if headless:
        options.add_argument(f"--window-size={width},{height}")
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    else:
        options.add_argument("--start-maximized")


def get_driver(browser="chrome", headless=None, grid_url=None):
    """To create and get webdriver"""
    driver = None
    # browser = browser.lower()
    # width, height = 1920, 1080
    # if browser == "chrome":
    #     options = webdriver.ChromeOptions()
    #     options.add_argument(
    #         'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"'
    #     )
    #     add_chromium_options(options, width, height, headless)

    # elif browser == "edge":
    #     options = webdriver.EdgeOptions()
    #     add_chromium_options(options, width, height, headless)

    # elif browser == "firefox":
    #     options = webdriver.FirefoxOptions()
    #     if headless:
    #         options.add_argument(f"--width={width}")
    #         options.add_argument(f"--height={height}")
    #         options.add_argument("--headless")
    #     else:
    #         options.add_argument("--start-maximized")

    # else:
    #     raise ValueError("Unsupported browser name " + browser)
    # if grid_url:
    #     driver = webdriver.Remote(command_executor=grid_url, options=options)
    # else:
    #     if browser == "chrome":
    #         driver = webdriver.Chrome(options=options)
    #     elif browser == "edge":
    #         driver = webdriver.Edge(options=options)
    #     elif browser == "firefox":
    #         driver = webdriver.Firefox(options=options)
    from common_test_foundation.lib.webdrivers import ChromeDriver, FirefoxDriver

    driver = FirefoxDriver(headless=headless)
    return driver


def capture_screenshot(driver: WebDriver, screenshot_name: str) -> str:
    """Allow to capture screenshot

    Args:
        driver (WebDriver): WebDriver instance
        screenshot_name (str): Screenshot name prefix

    Returns:
        str: Screenshot base64 string
    """
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_path = os.path.join(
        SCREENSHOTS_DIR, f"{screenshot_name}_{time_stamp}.png"
    )

    browser = driver.capabilities["browserName"].lower()
    if browser == "firefox":
        driver.save_full_page_screenshot(screenshot_path)
        screenshot_base64 = driver.get_full_page_screenshot_as_base64()
    else:
        metrics = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
        width = metrics["contentSize"]["width"]
        height = metrics["contentSize"]["height"]

        # Override viewport
        driver.execute_cdp_cmd(
            "Emulation.setDeviceMetricsOverride",
            {
                "mobile": False,
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
            },
        )

        # Take full-page screenshot
        screenshot = driver.execute_cdp_cmd(
            "Page.captureScreenshot",
            {
                "format": "png",
                "quality": 60,
                "clip": {
                    "x": 0,
                    "y": 0,
                    "width": width,
                    "height": height,
                    "scale": 1,
                },
            },
        )
        screenshot_base64 = screenshot["data"]
        # Save to file
        with open(screenshot_path, "wb") as f:
            f.write(base64.b64decode(screenshot_base64))
        driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})

    logger.info("Screenshot saved at Location : %s", screenshot_path)

    return screenshot_base64


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
        self.wait.until(EC.title_contains(title), "Page title not contains given value")

    def get_element_name_locator(
        self,
        locator: Tuple[By, str],
        elem_name: str,
        replace_value: Union[str, List, Tuple] = None,
    ) -> Tuple[Tuple[By, str], str]:
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

    def wait_for_element_condition(
        self,
        locator: Tuple[By, str],
        elem_name: str,
        condition: callable,
        wait_time: float = None,
    ) -> WebElement:
        """Wait for element condition

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.

        Returns:
            WebElement : WebElement once it is located and visible
        """
        ele_wait = WebDriverWait(self.driver, wait_time) if wait_time else self.wait
        elem = ele_wait.until(
            condition(locator), self.wait_msg.format(elem_name, locator)
        )
        return elem

    def wait_for_element_to_be_visible(
        self,
        locator: Tuple[By, str],
        elem_name,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ):
        """Wait for element to be visible

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value
        )
        logger.info("Waiting for element %s to be visible", elem_name)
        self.wait_for_element_condition(
            locator, elem_name, EC.visibility_of_element_located, wait_time
        )
        logger.info("Element %s is visible", elem_name)

    def is_element_present(
        self,
        locator: Tuple[By, str],
        elem_name: str,
        stop_on_fail=False,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ) -> bool:
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
            locator, elem_name, replace_value
        )
        try:
            self.wait_for_element_condition(
                locator, elem_name, EC.visibility_of_element_located, wait_time
            )
        except (NoSuchElementException, TimeoutException) as ex:
            logger.info("Element %s is not present", elem_name)
            if stop_on_fail:
                raise ex
            return False
        logger.info("Element %s is present", elem_name)
        return True

    def click(
        self,
        locator: Tuple[By, str],
        elem_name: str,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ):
        """To click on the Element

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value
        )
        element = self.wait_for_element_condition(
            locator, elem_name, EC.element_to_be_clickable, wait_time
        )
        element.click()
        logger.info("Clicked on the %s", elem_name)

    def enter_text(
        self,
        locator: Tuple[By, str],
        value: str,
        elem_name: str,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ):
        """Type value inside the element

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            value (str): value to type inside input
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value
        )
        element = self.wait_for_element_condition(
            locator, elem_name, EC.visibility_of_element_located, wait_time
        )
        element.clear()
        element.send_keys(value)
        logger.info("Entered text %s in the %s", value, elem_name)

    def select_value_from_dropdown(
        self,
        locator,
        value,
        elem_name: str,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ):
        """Select value from Dropdown

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            value (str): dropdown value to be selected
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value
        )
        select = Select(
            self.wait_for_element_condition(
                locator, elem_name, EC.visibility_of_element_located, wait_time
            )
        )
        select.select_by_value((str)(value))
        logger.info("Selected %s dropdown by value %s", elem_name, value)

    def execute_js_script_on_element(
        self,
        script,
        locator,
        elem_name: str,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ) -> str:
        """Move a element by offset

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        locator, elem_name = self.get_element_name_locator(
            locator, elem_name, replace_value
        )
        element = self.wait_for_element_condition(
            locator, elem_name, EC.presence_of_element_located, wait_time
        )
        value = self.driver.execute_script(script, element)
        logger.info(
            "Executed JS Script on Element %s on returned value %s", elem_name, value
        )
        return value

    def scroll_into_view_and_click(
        self,
        locator,
        elem_name: str,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ):
        """Scroll Into View to the element and click

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        self.execute_js_script_on_element(
            "arguments[0].scrollIntoViewIfNeeded()",
            locator,
            elem_name,
            replace_value,
            wait_time,
        )
        self.click(locator, elem_name, replace_value, wait_time)

    def scroll_into_view(
        self,
        locator,
        elem_name: str,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ):
        """Scroll Into View to the element

        Args:
            locator (Tuple): Tuple with locator type and locator string.
            elem_name (str): description of the element.
            replace_value (str | list, optional): values to replace in the locator. Defaults to None.
            wait_time (float, optional): custom wait time for the elements, Default driver default wait time.
        """
        self.execute_js_script_on_element(
            "arguments[0].scrollIntoViewIfNeeded()",
            locator,
            elem_name,
            replace_value,
            wait_time,
        )

    def click_on_element_by_offset(
        self,
        locator,
        elem_name: str,
        xoffset=0,
        yoffset=0,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ):
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
            locator, elem_name, replace_value
        )
        actions = ActionChains(self.driver)
        ele = self.wait_for_element_condition(
            locator, elem_name, EC.element_to_be_clickable, wait_time
        )
        actions.move_to_element_with_offset(ele, xoffset, yoffset).click().perform()
        logger.info(
            "Moved & Clicked on Element %s by offset %s", elem_name, [xoffset, yoffset]
        )

    def get_number_of_elements(
        self,
        locator: Tuple[By, str],
        elem_name: str,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ) -> int:
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
            locator, elem_name, replace_value
        )
        ele_wait = WebDriverWait(self.driver, wait_time) if wait_time else self.wait
        elements = ele_wait.until(
            EC.visibility_of_all_elements_located(locator),
            self.wait_msg.format(elem_name, locator),
        )
        return len(elements)

    def get_element_text(
        self,
        locator: Tuple[By, str],
        elem_name: str,
        replace_value: Union[str, List, Tuple] = None,
        wait_time: float = None,
    ) -> str:
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
            locator, elem_name, replace_value
        )
        ele = self.wait_for_element_condition(
            locator, elem_name, EC.presence_of_element_located, wait_time
        )
        return ele.text or ele.get_attribute("textContent")
