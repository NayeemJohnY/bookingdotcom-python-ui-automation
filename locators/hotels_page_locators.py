"""Hotels Page Locators"""

from selenium.webdriver.common.by import By

hotels_city_location_popular = (
    By.XPATH,
    '//*[text()="{}"]/ancestor::li[@role="option"]',
)

hotels_city_location_suggestions = (
    By.XPATH,
    hotels_city_location_popular[1]
    + '[descendant::span[contains(@class, "recentLocationIcon")]]',
)

selected_city_location_value = (
    By.XPATH,
    '//*[@id="city" and @value="{}"]',
)
