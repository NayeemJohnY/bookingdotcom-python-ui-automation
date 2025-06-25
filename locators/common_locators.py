"""Common Locators"""
from selenium.webdriver.common.by import By

generic_text_locator = (By.XPATH, '//*[text()="{}"]')

generic_attribute_locator = (By.XPATH, '//*[@{}="{}"]')



