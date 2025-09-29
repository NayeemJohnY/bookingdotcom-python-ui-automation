"""Home Page Test"""

from pages.home_page import HomePage
from pages.hotels_page import HotelsPage
from pages.search_results_page import SearchResultsPage
from tests.base_test import BaseTest


class TestBookingHotels(BaseTest):
    """Booking Hotels Test Class"""

    homepage: HomePage
    hotels_page: HotelsPage
    search_results_page: SearchResultsPage

    def test_search_hotels_apply_multiple_filters_and_verify_result(self):
        """TC001: Search Hotels + Apply Multiple Filters And Result Verification"""
        self.homepage = HomePage(self.webdriver_ops)
        self.homepage.verify_home_page()
        self.hotels_page = self.homepage.navigate_to_menu_page("Hotels")
        search_request = {
            "destination": "Chennai",
            "adults": 4,
            "children": 1,
            "rooms": 1,
            "children_ages": [10],
            "currency": "INR",
        }
        self.search_results_page = self.hotels_page.search_hotels(search_request)
        self.search_results_page.verify_search_results(search_request)
        filter_data = {
            "Property rating": "3 stars",
            "Reservation policy": "Free cancellation",
            "Your budget (per night)": 5000,
        }
        self.search_results_page.apply_filters(filter_data)
        self.search_results_page.verify_properties_for_applied_filter(
            search_request, filter_data
        )
