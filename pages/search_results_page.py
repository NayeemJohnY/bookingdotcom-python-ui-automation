"""Search Results Page Functions"""

from helpers import utils
from helpers.driver_manager import WebDriverOps
from locators.common_locators import *
from locators.search_results_page_locators import *


class SearchResultsPage:
    """Search Results Page class"""

    def __init__(self, webdriver_ops):
        self.webdriver_ops: WebDriverOps = webdriver_ops

    def verify_search_results(self, search_request: dict):
        """Verify Search Results

        Args:
            search_request (dict): Search request dictionary
        """
        self.webdriver_ops.wait_for_element_to_be_visible(
            generic_text_locator, "Results Breadcrumb", "Search results"
        )
        self.webdriver_ops.wait_for_element_to_be_visible(
            search_results_title, "Location Title", search_request["dest_search"]
        )
        # At least 1 property is available in results
        self.webdriver_ops.wait_for_element_to_be_visible(
            data_testid_locator, "Property card", "property-card"
        )

    def apply_filters(self, filter_data: dict):
        """Apply Filter with Filter Data

        Args:
            filter_data (dict): Filter Data dictionary

        """
        for group, value in filter_data.items():
            if group == "Your budget (per night)":
                slider_width = int(
                    self.webdriver_ops.execute_js_script_on_element(
                        "return arguments[0].scrollWidth",
                        price_slider_bar,
                        "Slider bar",
                    )
                )
                slider_min_value = int(
                    self.webdriver_ops.execute_js_script_on_element(
                        "return arguments[0].value",
                        price_slider_input_range,
                        "Min Sider Input Range",
                        1,
                    )
                )
                slider_max_value = int(
                    self.webdriver_ops.execute_js_script_on_element(
                        "return arguments[0].value",
                        price_slider_input_range,
                        "Max Sider Input Range",
                        2,
                    )
                )
                if value < slider_max_value:
                    offset = round(
                        slider_width
                        * (value - slider_min_value)
                        / (slider_max_value - slider_min_value)
                    )
                    offset_from_center = offset - slider_width // 2
                    self.webdriver_ops.click_on_element_by_offset(
                        price_slider_bar, "Max price Slider", offset_from_center
                    )
                    value = f"{value:,} (per night)"
                    self.webdriver_ops.wait_for_element_to_be_visible(
                        filter_tag, "Filter Tag", value
                    )
            else:
                self.webdriver_ops.click(filter_group, "Select Filter", [group, value])
                self.webdriver_ops.wait_for_element_to_be_visible(
                    filter_tag, "Filter Tag", value
                )
            self.webdriver_ops.wait_for_element_to_be_visible(
                data_testid_locator, "Property card", "property-card"
            )

    def get_locator_for_property_dtl(self, key, value):
        """Build and return Locator For Property Detail

        Args:
            key (str): Property key
            value (_type_): Property value

        Returns:
            tuple: Tuple of locator and value
        """
        locator = None
        if key == "Review score":
            locator = property_card_review_score
            value = utils.get_number_from_text(value)
        elif key == "Property rating":
            locator = property_card_rating_stars
            value = utils.get_number_from_text(value)
        elif key == "Reservation policy":
            locator = property_card_recommended_units
        elif key == "Your budget (per night)":
            locator = property_card_price
        return locator, value

    def verify_properties_for_applied_filter(self, request_data, filter_data: dict):
        """Verify properties for applied Filter

        Args:
            request_data (dict): Request Data dictionary
            filter_data (dict): Filter Data dictionary
        """
        for i in range(
            1,
            self.webdriver_ops.get_number_of_elements(
                data_testid_locator, "Property card", "property-card"
            )
            + 1,
        ):
            for group, value in filter_data.items():
                locator, value = self.get_locator_for_property_dtl(group, value)
                if group == "Your budget (per night)":
                    self.webdriver_ops.is_element_present(
                        property_card_duration_member_info,
                        "Duration Memeber Info",
                        stop_on_fail=True,
                        replace_value=[i, request_data["duration_and_members"]],
                    )
                    price = self.webdriver_ops.get_element_text(
                        locator, "Property card", i
                    )
                    price = utils.get_number_from_text(price)
                    assert price / request_data["x_nights"] <= value

                else:
                    self.webdriver_ops.is_element_present(
                        locator,
                        f"Property card with {group}",
                        stop_on_fail=True,
                        replace_value=[i, value],
                    )
