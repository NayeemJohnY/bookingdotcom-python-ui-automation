"""Conftest.py for driver manager and other fixtures"""

import logging

import pytest
import pytest_html.extras
import yaml

from helpers.driver_manager import capture_screenshot, get_driver

logger = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def env_config(request):
    """Environment Config"""
    env = request.config.getoption("--env")
    with open("config.yaml", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config[env]


@pytest.fixture(scope="module")
def browser_config(request, env_config):  # pylint:disable=W0621
    """Get Browser Config: Browser Name and Headless Mode"""
    # Support both command-line options and config.yaml, prioritize command-line
    browser = request.config.getoption("--browser")
    if not browser:
        browser = env_config.get("browser", "chrome")

    headless = request.config.getoption("--headless")
    if headless is None or headless is False:
        headless = env_config.get("headless", False)

    grid_url = request.config.getoption("--grid-url")
    if not grid_url:
        grid_url = env_config.get("grid_url", None)

    return {"browser": browser, "headless": headless, "grid_url": grid_url}


@pytest.fixture(scope="module", autouse=True)
def driver(browser_config: dict):  # pylint:disable=W0621
    """Provides a WebDriverManager instance and ensures the browser is quit after use."""
    driver_instance = get_driver(**browser_config)
    yield driver_instance
    driver_instance.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Pytest Hook to update report with screenshot and log errors"""
    outcome = yield
    report = outcome.get_result()
    # Only on failure
    if report.when == "call" and report.failed:
        report_driver = item.funcargs.get("driver")
        test_name = item.name

        report.extras = getattr(report, "extras", [])
        if report_driver:
            try:
                screenshot_base64 = capture_screenshot(report_driver, test_name)
                img_data = f"data:image/png;base64,{screenshot_base64}"
                report.extras.append(pytest_html.extras.image(img_data, name=test_name))
            except Exception as e:  # pylint:disable=W0718
                logger.error(
                    "Error capturing screenshot for '%s' : %s",
                    test_name,
                    e,
                    exc_info=True,
                )
        logger.error(
            "%s occurred at test: %s",
            call.excinfo.typename,
            test_name,
            exc_info=(call.excinfo.type, call.excinfo.value, call.excinfo.tb),
        )


def pytest_addoption(parser: pytest.Parser):
    """pytest add options parser"""
    parser.addoption(
        "--browser",
        type=str,
        choices=["chrome", "firefox", "edge"],
        help="Specify the browser to run tests on: chrome, firefox, or edge.",
    )
    parser.addoption("--headless", action="store_true", help="Set Headless Mode")
    parser.addoption("--grid-url", type=str, help="Selenium Grid Hub URL")
    parser.addoption(
        "--env",
        type=str,
        choices=["dev", "stage", "prod"],
        help="Test Environment",
        default="stage",
    )
