"""Home Page Locators"""

from selenium.webdriver.common.by import By

login_popup_close_button = (
    By.CSS_SELECTOR,
    'section[data-cy="CommonModal_2"] span[data-cy="closeModal"]',
)

header_menu = (By.XPATH, '//li[@data-cy="menu_{0}"][descendant::span[text()="{0}"]]')

header_menu_active = (
    By.XPATH,
    header_menu[1] + '[descendant::span[contains(@class, "active")]]',
)

check_in_out_date = (
    By.XPATH,
    '//*[contains(@class, "DayPicker-Day") and @aria-label="{}"]',
)

date_display_field = (
    By.XPATH,
    '//*[@data-cy="{}" and normalize-space()="{}"]',
)


currency_lang_switcher = (
    By.XPATH,
    '//*[contains(@class, "CurrencyText")]',
)

selected_currency_text = (
    By.XPATH,
    '//*[contains(@class, "CurrencyText")][text()="{}"]',
)

currency_dropdown = (
    By.CSS_SELECTOR,
    '[data-testid="currency-dropdown"]',
)

currency_dropdown_list_value = (
    By.XPATH,
    '//*[@data-testid="dropdown-list-currency"]/descendant::*[contains(@class, "CurrencyOption")]'
    '[descendant::text()="{}"]',
)
