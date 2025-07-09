"""Conftest.py for driver manager and other fixtures"""
import pytest
from helpers.driver_manager import get_driver, capture_screenshot
import logging
import pytest_html.extras


logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def browser_config(request):
    """Get Browser Config: Browser Name and Headless Mode"""
    browser = request.config.getoption("--browser")
    if browser is None:
        browser = request.config.getini("browser")

    headless = request.config.getoption("--headless")
    if not headless:
        headless = request.config.getini("headless")

    grid_url = request.config.getoption("--grid-url")

    return {"browser": browser, "headless": headless, "grid_url": grid_url}


@pytest.fixture(scope="module", autouse=True)
def driver(browser_config: dict):  # pylint:disable=W0621
    """Provides a WebDriverManager instance and ensures the browser is quit after use."""
    driver_instance = get_driver(**browser_config)
    yield driver_instance
    driver_instance.quit()


@pytest.fixture(scope="module", autouse=True)
def app_url(request):
    """Get Application URL"""
    return request.config.getini("url")


@pytest.fixture(scope="module", autouse=True)
def timeout(request):
    """Default Timeout"""
    return request.config.getini("timeout")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # Only on failure
    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        test_name = item.name

        report.extras = getattr(report, 'extras', [])
        if driver:
            try:
                screenshot_base64 = capture_screenshot(driver, test_name)
                img_data = f"data:image/png;base64,{screenshot_base64}"
                report.extras.append(
                    pytest_html.extras.image(img_data, name=test_name))
            except Exception as e:
                logger.error("Error capturing screenshot for '%s' : %s",
                             test_name, e, exc_info=True)
        logger.error(
            "%s occurred at test: %s", call.excinfo.typename, test_name,
            exc_info=(call.excinfo.type, call.excinfo.value, call.excinfo.tb))


def pytest_addoption(parser: pytest.Parser):
    """pytest add options parser"""
    parser.addoption("--browser", type=str, choices=["chrome", "firefox", "edge"],
                     help="Specify the browser to run tests on: chrome, firefox, or edge.")
    parser.addoption("--headless", action="store_true",
                     help="Set Headless Mode")
    parser.addoption("--grid-url", type=str, help="Selenim Grid Hub URL")
    parser.addini(
        "browser", type='string', help="Specify the browser to run tests on", default="chrome")
    parser.addini(
        "headless", type='bool',  help="Specify Headless Mode", default="False")
    parser.addini(
        "url", type='string',  help="The base URL for the application under test")
    parser.addini(
        "timeout", type='float',  help="Default webdriver timeout")
