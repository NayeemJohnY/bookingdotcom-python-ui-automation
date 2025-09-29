"""Common Locators"""

from selenium.webdriver.common.by import By

generic_text_locator = (By.XPATH, '//*[text()="{}"]')

generic_button_locator = (By.XPATH, '//button[text()="{}"]')

generic_attribute_locator = (By.XPATH, '//*[@{}="{}"]')

data_testid_locator = (By.XPATH, '//*[@data-testid="{}"]')

guest_count_dropdown = (By.XPATH, '//*[@data-testid="{}_count"]')

child_select_age_dropdown_by_index = (
    By.XPATH,
    '//*[contains(@class, "slctAge")]/descendant::*[@data-testid="child_count"][{}]',
)


def child_selected_age(age, index):
    """Child Selected Age Locator"""
    locator = f'//*[contains(@class, "slctAge")]/descendant::*[@data-testid="child_count"][{index}]'
    if age < 1:
        locator += '[text()= "<"]'
    locator += f'[text()="{age}"]'

    locator += '[text()= "yr"]' if age <= 1 else '[text()= "yrs"]'
    return (By.XPATH, locator)


guest_count_selected_value = (By.XPATH, guest_count_dropdown[1] + '[text()="{}"]')

guest_count_select_list = (
    By.XPATH,
    '//li[contains(@data-cy, "GuestSelect")][text()="{}"]',
)
