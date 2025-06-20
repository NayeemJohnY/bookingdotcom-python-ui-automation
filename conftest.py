"""Conftest.py for driver manager and other fixtures"""
import pytest

from helpers.driver_manager import WebDriverManager


@pytest.fixture(scope="module", autouse=True)
def test_config(request):
    """Get Test Config: URL, Browser Name and Headless Mode"""
    url = request.config.getini("url")
    browser = request.config.getoption("--browser")
    if browser is None:
        browser = request.config.getini("browser")

    headless = request.config.getoption("--headless")
    if not headless:
        headless = request.config.getini("headless")

    return {"browser": browser, "headless": headless, "url": url}


@pytest.fixture(scope="module", autouse=True)
def driver_manager(test_config: dict):  # pylint:disable=W0621
    """Provides a WebDriverManager instance and ensures the browser is quit after use."""
    manager = WebDriverManager(**test_config)
    yield manager
    manager.quit()


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
