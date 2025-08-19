"""Search Results Page Locators"""

from selenium.webdriver.common.by import By

search_results_title = (
    By.XPATH,
    '//h1[contains(text(), "{}") and contains(text(),"properties found")]',
)

filter_group = (
    By.XPATH,
    '//*[@data-testid="filters-group"][descendant::*[text()="{}"]]/descendant::*[text()="{}"]',
)

price_slider_bar = (
    By.XPATH,
    '//*[@data-filters-group="price"]/descendant::div[@role="group"]/div[last()]',
)

price_slider_input_range = (
    By.XPATH,
    '//*[@data-filters-group="price"]/descendant::*[@type="range"][{}]',
)

filter_tag = (
    By.XPATH,
    '//*[contains(@data-testid,"filter")]/descendant::*[contains(text(),"{}")]',
)

PROPERTY_CARD_WITH_INDEX = '//*[@data-testid="property-card"][{}]'

property_card_review_score = (
    By.XPATH,
    PROPERTY_CARD_WITH_INDEX
    + '/descendant::*[@data-testid="review-score"]/descendant::*[text()>{}]',
)

property_card_recommended_units = (
    By.XPATH,
    PROPERTY_CARD_WITH_INDEX
    + '/descendant::*[@data-testid="recommended-units"]/descendant::*[contains(text(),"{}")]',
)

property_card_rating_stars = (
    By.XPATH,
    PROPERTY_CARD_WITH_INDEX
    + '/descendant::*[@data-testid="rating-stars" or @data-testid="rating-squares"][count(*)={}]',
)

property_card_price = (
    By.XPATH,
    PROPERTY_CARD_WITH_INDEX
    + '/descendant::*[@data-testid="price-and-discounted-price"]',
)

property_card_duration_member_info = (
    By.XPATH,
    PROPERTY_CARD_WITH_INDEX
    + '/descendant::*[@data-testid="price-for-x-nights"][normalize-space()="{}"]',
)
