"""Hotels Page Functions"""

from datetime import datetime, timedelta
import time
import constants
from helpers import utils
from helpers.driver_manager import WebDriverOps
from locators.common_locators import *
from locators.home_page_locators import *
from locators.hotels_page_locators import *
from pages.search_results_page import SearchResultsPage


class HotelsPage:
    """Hotels Page class"""

    def __init__(self, webdriver_ops):
        self.webdriver_ops: WebDriverOps = webdriver_ops

    def select_currency(self, currency: str):
        """Select Currency

        Args:
            currency (str): Currency to be selected (INR /USD)
        """
        if not self.webdriver_ops.is_element_present(
            selected_currency_text,
            "Selected Currency",
            replace_value=currency,
            wait_time=1,
        ):
            self.webdriver_ops.click(currency_lang_switcher, "Currency Picker Trigger")
            self.webdriver_ops.click(currency_dropdown, "Currency Dropdown")
            self.webdriver_ops.scroll_into_view_and_click(
                currency_dropdown_list_value, "Currency Dropdown list value", currency
            )
            self.webdriver_ops.click(generic_button_locator, "Apply Button", "Apply")
            self.webdriver_ops.wait_for_element_to_be_visible(
                selected_currency_text, "Selected Currency", currency
            )

    def search_hotels(self, search_request: dict):
        """Search Hotels

        Args:
            search_request (dict): Search request dictionary
        """
        self.select_currency(search_request["currency"])
        self.webdriver_ops.click(
            generic_attribute_locator,
            "Destination",
            ["id", "city"],
        )

        if self.webdriver_ops.is_element_present(
            hotels_city_location_popular,
            "Popular Locations",
            replace_value=search_request["destination"],
            wait_time=2,
        ):
            self.webdriver_ops.click(
                hotels_city_location_popular,
                "Popular Locations",
                search_request["destination"],
            )
        else:
            self.webdriver_ops.enter_text(
                generic_attribute_locator,
                search_request["destination"],
                "Destination",
                ["id", "city"],
            )
            self.webdriver_ops.scroll_into_view_and_click(
                hotels_city_location_suggestions,
                "Hotel City Location Suggestions",
                search_request["destination"],
            )

        self.webdriver_ops.wait_for_element_to_be_visible(
            selected_city_location_value,
            "Selected Destination",
            search_request["destination"],
        )

        self.select_check_in_out_date(search_request)
        self.fill_occupancy_detail(search_request)
        self.webdriver_ops.click(generic_text_locator, "Search Button", "Search")
        return SearchResultsPage(self.webdriver_ops)

    def select_check_in_out_date(self, search_request):
        """Select Check in Out date and verify selected date

        Args:
            search_request (dict):  Search request dictionary
        """
        if "check_in_date" in search_request:
            check_in_date = utils.parse_datetime(
                search_request["check_in_date"], constants.YMD_DATE_FORMAT
            )
        else:
            check_in_date = datetime.today()

        if "check_out_date" in search_request:
            check_out_date = utils.parse_datetime(
                search_request["check_out_date"], constants.YMD_DATE_FORMAT
            )
        else:
            check_out_date = datetime.today() + timedelta(weeks=2)

        self.webdriver_ops.click(
            check_in_out_date,
            "Check In date",
            utils.format_datetime(check_in_date, constants.DAY_MONTH_DATE_YEAR_FORMAT),
        )
        self.webdriver_ops.click(
            check_in_out_date,
            "Check out date",
            utils.format_datetime(check_out_date, constants.DAY_MONTH_DATE_YEAR_FORMAT),
        )

        check_in_str = utils.format_datetime(
            check_in_date, constants.SELECTED_DATE_FORMAT
        ).lstrip("0")
        check_out_str = utils.format_datetime(
            check_out_date, constants.SELECTED_DATE_FORMAT
        ).lstrip("0")

        self.webdriver_ops.wait_for_element_to_be_visible(
            date_display_field, "Selected Check In date", ["checkInDate", check_in_str]
        )
        self.webdriver_ops.wait_for_element_to_be_visible(
            date_display_field,
            "Selected Check out date",
            ["checkOutDate", check_out_str],
        )

        days = (check_out_date - check_in_date).days
        search_request["x_nights"] = days

    def fill_occupancy_detail(self, search_request):
        """Fill Occupancy detail

        Args:
            search_request (dict):  Search request dictionary
        """
        self.update_occupant_detail("room", search_request.get("rooms", 1))
        adults = search_request.get("adults", 1)
        children = search_request.get("children", 0)
        self.update_occupant_detail("adult", adults)
        self.update_occupant_detail("children", children)
        self.update_children_age(search_request.get("children_ages", None))

        # region build duration member info
        parts = []
        x_nights = search_request["x_nights"]
        if x_nights % 7 == 0:
            weeks = x_nights // 7
            parts.append(f"{weeks} week" if weeks == 1 else f"{weeks} weeks")

        parts.append(f"{adults} adult" if adults == 1 else f"{adults} adults")

        if children:
            parts.append(
                f"{children} child" if children == 1 else f"{children} children"
            )

        search_request["duration_and_members"] = ", ".join(parts)
        # endregion
        self.webdriver_ops.click(generic_button_locator, "Apply Button", "APPLY")

    def update_occupant_detail(self, occupant_entity, occupant_count):
        """Update Occupant details

        Args:
            occupant_entity (str): Occupant entity (adults, children, room)
            occupant_count (int): Occupant entity count

        Raises:
            ValueError: if occupant entity is less than min or greater than max
        """

        if not self.webdriver_ops.is_element_present(
            guest_count_selected_value,
            "Selected Occupant Count",
            replace_value=[occupant_entity, occupant_count],
            wait_time=2,
        ):
            self.webdriver_ops.click(
                guest_count_dropdown,
                "Occupant Entity Dropdown",
                replace_value=[occupant_entity],
            )
            self.webdriver_ops.click(
                guest_count_select_list,
                "Occupant Count Dropdown list",
                replace_value=[occupant_count],
            )
        self.webdriver_ops.wait_for_element_to_be_visible(
            guest_count_selected_value,
            "Selected Occupant Count",
            replace_value=[occupant_entity, occupant_count],
        )

    def update_children_age(self, children_ages: list):
        """Update children age for selected children

        Args:
            children_ages (list): List of children ages

        Raises:
            ValueError: Raises value Error if children age is greater than 17
        """
        if children_ages:
            for i, age in enumerate(children_ages):
                self.webdriver_ops.click(
                    child_select_age_dropdown_by_index,
                    "Child Select Age Dropdown",
                    replace_value=i + 1,
                )
                self.webdriver_ops.click(
                    guest_count_select_list,
                    "Child Select Age Dropdown list",
                    replace_value=age,
                )
                self.webdriver_ops.wait_for_element_to_be_visible(
                    child_selected_age(age, i + 1),
                    f"Selected Child Age for index {i+1}",
                )
