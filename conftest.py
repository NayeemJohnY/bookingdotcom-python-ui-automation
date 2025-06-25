"""Conftest.py for driver manager and other fixtures"""
import pytest

from helpers.driver_manager import get_driver


@pytest.fixture(scope="module")
def browser_config(request):
    """Get Browser Config: Browser Name and Headless Mode"""
    browser = request.config.getoption("--browser")
    if browser is None:
        browser = request.config.getini("browser")

    headless = request.config.getoption("--headless")
    if not headless:
        headless = request.config.getini("headless")
    return {"browser": browser, "headless": headless}


@pytest.fixture(scope="module", autouse=True)
def driver(browser_config: dict):  # pylint:disable=W0621
    """Provides a WebDriverManager instance and ensures the browser is quit after use."""
    driver_instance = get_driver(**browser_config)
    yield driver_instance
    # driver_instance.quit()


@pytest.fixture(scope="module", autouse=True)
def app_url(request):
    """Get Application URL"""
    return request.config.getini("url")


@pytest.fixture(scope="module", autouse=True)
def timeout(request):
    """Default Timeout"""
    return request.config.getini("timeout")


def pytest_addoption(parser: pytest.Parser):
    """pytest add options parser"""
    parser.addoption("--browser", type=str, choices=["chrome", "firefox", "edge"],
                     help="Specify the browser to run tests on: chrome, firefox, or edge.")
    parser.addoption("--headless", action="store_true",
                     help="Set Headless Mode")
    parser.addini(
        "browser", type='string', help="Specify the browser to run tests on", default="chrome")
    parser.addini(
        "headless", type='bool',  help="Specify Headless Mode", default="False")
    parser.addini(
        "url", type='string',  help="The base URL for the application under test")
    parser.addini(
        "timeout", type='float',  help="Default webdriver timeout")
