

from datetime import datetime, timedelta

import constants
from helpers import utils
from helpers.driver_manager import WebDriverOps
from locators.common_locators import *
from locators.home_page_locators import *

OCCUPANCY_LIMITS = {
    'adults': {"min": 1, "max": 30},
    'children': {"min": 0, "max": 10},
    "rooms": {"min": 1, "max": 30}
}


class HomePage:

    def __init__(self, webdriver_ops):
        self.webdriver_ops: WebDriverOps = webdriver_ops

    def verify_home_page(self):
        """Verify Home page"""
        self.webdriver_ops.wait_for_page_title_contains(
            constants.HOME_PAGE_TITLE)
        self.webdriver_ops.is_element_present(
            generic_text_locator, "Register link", True, "Register")
        self.webdriver_ops.is_element_present(
            generic_text_locator, "Sign in link", True, "Sign in")
        if self.webdriver_ops.is_element_present(
                dismiss_sign_in_popup_button, "Dismiss Sign in Pop up close Icon", wait_time=10):
            self.webdriver_ops.click(
                dismiss_sign_in_popup_button, "Dismiss Sign in Pop up close Icon")

    def search_hotels(self, search_request: dict):
        """Search Hotels

        Args:
            search_request (dict): Search request dictionary
        """
        self.webdriver_ops.type_value(
            generic_attribute_locator, search_request['dest_search'], "Destination",
            ["placeholder", "Where are you going?"])
        if self.webdriver_ops.is_element_present(
                auto_complete_results, 'Auto Complete Results Trending', replace_value=1, wait_time=5):
            self.webdriver_ops.wait_for_element_to_be_visible(
                auto_complete_results, 'Auto Complete Results not Trending', 0)
        self.webdriver_ops.click(
            auto_complete_results_with_text, "Auto Complete Results", search_request['dest_search'])
        self.webdriver_ops.wait_for_element_to_be_visible(
            destination_selected_value, 'Selected Destination', search_request['destination'])
        self.select_check_in_out_date(search_request)
        self.fill_occupancy_detail(search_request)

    def select_check_in_out_date(self, search_request):
        """Select Check in Out date and verify selected date

        Args:
            search_request (dict):  Search request dictionary
        """
        if 'check_in_date' in search_request:
            check_in_date = utils.parse_datetime(
                search_request['check_in_date'], constants.YMD_DATE_FORMAT)
        else:
            check_in_date = datetime.today()

        if 'check_out_date' in search_request:
            check_out_date = utils.parse_datetime(
                search_request['check_out_date'], constants.YMD_DATE_FORMAT)
        else:
            check_out_date = datetime.today() + timedelta(weeks=2)

        self.webdriver_ops.click(
            check_in_out_date, 'Check In date', utils.format_datetime(check_in_date))
        self.webdriver_ops.click(
            check_in_out_date, 'Check out date', utils.format_datetime(check_out_date))

        check_in_str = (
            utils.format_datetime(check_in_date, constants.DAY_MONTH_FORMAT).strip() + " " +
            utils.format_datetime(
                check_in_date, constants.DATE_SINGLE_DIGIT_FORMAT).strip()
        )
        check_out_str = (
            utils.format_datetime(check_out_date, constants.DAY_MONTH_FORMAT).strip() + " " +
            utils.format_datetime(
                check_out_date, constants.DATE_SINGLE_DIGIT_FORMAT).strip()
        )
        self.webdriver_ops.wait_for_element_to_be_visible(
            date_display_field, 'Selected Check In date', ['start', check_in_str])
        self.webdriver_ops.wait_for_element_to_be_visible(
            date_display_field, 'Selected Check out date', ['end',  check_out_str])

    def fill_occupancy_detail(self, search_request):
        """Fill Occupancy detail

        Args:
            search_request (dict):  Search request dictionary
        """
        self.open_occpancy_config()
        self.update_occupant_detail("adults", search_request.get("adults", 1))
        self.update_occupant_detail("rooms", search_request.get("rooms", 1))
        self.webdriver_ops.click(generic_text_locator,
                                 "Search Button", "Search")

    def update_occupant_detail(self, occupant_entity, occupant_count):
        """Update Occupant details

        Args:
            occupant_entity (str): Occupant entity (adults, children, room)
            occupant_count (int): Occupant entity count

        Raises:
            ValueError: if occupant entity is less than min or greater than max
        """
        occupancy_limit = OCCUPANCY_LIMITS[occupant_entity]
        if occupant_count < occupancy_limit['min']:
            raise ValueError(
                f"{occupant_entity} count cannot be less than {occupancy_limit['min']}")
        if occupant_count > occupancy_limit['max']:
            raise ValueError(
                f"{occupant_entity} count cannot be greater than {occupancy_limit['min']}")

        while not self.webdriver_ops.is_element_present(
            occupany_group_detail_value, "occupant entity count",
                replace_value=[occupant_entity, occupant_count], wait_time=5):

            if occupant_count == 1:
                self.webdriver_ops.click(
                    occupany_group_detail_button, "Decrease count button", [occupant_entity, 1])
            elif occupant_count > 2:
                self.webdriver_ops.click(
                    occupany_group_detail_button, "Increase count button", [occupant_entity, 2])

        if occupant_count == occupancy_limit['min']:
            self.open_occpancy_config()
            self.webdriver_ops.wait_for_element_to_be_visible(
                occupany_group_detail_button_disabled, "Disabled Decrease count button", [occupant_entity, 1])
        elif occupant_count == occupancy_limit['max']:
            self.open_occpancy_config()
            self.webdriver_ops.wait_for_element_to_be_visible(
                occupany_group_detail_button_disabled, "Disabled Increase count button", [occupant_entity, 2])

    def open_occpancy_config(self):
        """Open Occupancy Config"""
        locator = generic_attribute_locator[0], generic_attribute_locator[1] + \
            '[@aria-expanded="false"]'
        if self.webdriver_ops.is_element_present(
                locator, "Number of travelers button", replace_value=["data-testid", "occupancy-config"], wait_time=1):
            self.webdriver_ops.click(
                generic_attribute_locator, "Number of travelers button", ["data-testid", "occupancy-config"])
