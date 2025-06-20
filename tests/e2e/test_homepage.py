"""Home Page Test"""


def test_home_page_landing(driver_manager):
    """Verify Home page lannding title"""
    driver = driver_manager.driver
    assert "Booking.com | Official site | The best hotels, flights, car rentals & accommodations" in driver.title
