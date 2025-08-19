"""Base Test Module"""

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from helpers.driver_manager import WebDriverOps


class BaseTest:
    """Base Test Class"""

    driver: WebDriver
    webdriver_ops: WebDriverOps

    @pytest.fixture(scope="class", autouse=True)
    def init_driver(self, request, driver, env_config):
        """Initialize driver to test class"""
        request.node.driver = driver
        request.cls.driver = driver
        request.cls.webdriver_ops = WebDriverOps(driver, env_config["timeout"])
        request.cls.webdriver_ops.goto_url(env_config["url"])
