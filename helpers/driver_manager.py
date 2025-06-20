"""WebDriver Manager with Manage browser instance and manage actions on browser"""
import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

logger = logging.getLogger(__name__)


class WebDriverManager:
    """WebDriver Manager to create and manger WebDriver"""

    def __init__(self, url=None, browser="chrome", headless=None):
        if browser == "chrome":
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--incognito")
            if headless:
                chrome_options.add_argument("--headless")
            self._driver = webdriver.Chrome(options=chrome_options)
        else:
            raise ValueError("Unsupported browser name " + browser)

        self._webdriver_actions = WebDriverActions(self._driver)
        self._webdriver_actions.goto_url(url)

    @property
    def driver(self):
        """WebDriver instance"""
        return self._driver

    @property
    def webdriver_actions(self):
        """WebDriverActions"""
        return self._webdriver_actions

    def quit(self):
        """Close and Quit driver instance"""
        if getattr(self, '_driver') is not None:
            self._driver.quit()


class WebDriverActions:
    """WebDriver Actions class with Browser Actions functions"""

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def goto_url(self, url):
        """Navigate to URL"""
        logger.info("Launching URL %s", url)
        self.driver.get(url)
