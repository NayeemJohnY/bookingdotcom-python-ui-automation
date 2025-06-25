"""Home Page Locators"""
from selenium.webdriver.common.by import By

dismiss_sign_in_popup_button = (
    By.XPATH, '//*[@role="dialog"][descendant::*[text()="Sign in, save money"]]'
    '/descendant::button[@aria-label="Dismiss sign-in info."]')

auto_complete_results = (
    By.XPATH, '//*[@id="autocomplete-results"][count(descendant::*[text()= "Trending destinations"])={}]')

auto_complete_results_with_text = (
    By.XPATH, '//*[@id="autocomplete-results"]/descendant::*[text()="{}"]')

destination_selected_value = (
    By.XPATH, '//*[@placeholder="Where are you going?" and @value="{}"]')

check_in_out_date = (By.XPATH, '//*[@data-date="{}"]')

date_display_field = (
    By.XPATH, '//*[@data-testid="date-display-field-{}" and text()="{}"]')

occupany_group_detail_button = (
    By.XPATH, '//*[contains(@id, "{}")]/preceding-sibling::*/button[{}]')

occupany_group_detail_value = (
    By.XPATH, '//*[contains(@id, "{}")]/preceding-sibling::*/span[text()="{}"]')

occupany_group_detail_button_disabled = (
    By.XPATH, occupany_group_detail_button[1] + '[@disabled]')