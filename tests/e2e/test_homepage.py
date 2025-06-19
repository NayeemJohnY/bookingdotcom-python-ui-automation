"""Home Page Test"""


def test_home_page_landing(driver):
    """Verify Home page lannding title"""
    assert "Booking.com | Official site | The best hotels, flights, car rentals & accommodations" in driver.title
