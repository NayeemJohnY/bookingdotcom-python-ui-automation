"""Home Page Test"""

from pages.home_page import HomePage
from tests.e2e.BaseTest import BaseTest


class TestHomePage(BaseTest):
    """Home Page Test Class"""
    homepage: HomePage

    def test_search_stays_apply_multiple_filters_and_verify_result(self):
        """TC001: Search Hotels + Apply Multiple Filters And Result Verification"""
        self.homepage = HomePage(self.webdriver_ops)
        self.homepage.verify_home_page()
        search_request = {'destination': "Chennai, Tamil Nadu, India", "dest_search": "Chennai",
                          "adults": 4, "children": 1, "rooms": 1}
        self.homepage.search_hotels(search_request)
