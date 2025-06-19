"""Conftest.py for driver and other fixtures"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="module", autouse=True)
def driver():
    """Get Driver Fixture"""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    driver_instance = webdriver.Chrome(options=chrome_options)
    driver_instance.get("https://www.booking.com/")
    yield driver_instance
    driver_instance.quit()
