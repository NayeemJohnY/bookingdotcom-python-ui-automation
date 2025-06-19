"""Conftest.py for driver and other fixtures"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="module", autouse=True)
def driver():
    """Get Driver Fixture"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    d = webdriver.Chrome(chrome_options)
    yield d
    d.quit()


@pytest.fixture(scope="module", autouse=True)
def load_url(driver):
    "Load URL"
    driver.get("https://www.booking.com/")
