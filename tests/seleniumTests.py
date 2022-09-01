import unittest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By

class CheckSiteAvailability(unittest.TestCase):
    website_url = "http://127.0.0.1:5500/src/index.html" # Standard URL 

    def setUp(self):
        driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install() # Initializes the driver

        # Run the browser with no GUI
        chrome_options = Options()
        chrome_options.add_argument("--headless") 

        self.browser = webdriver.Chrome(driver_path, options=chrome_options) # Initializes the browser instance with the driver
        self.addCleanup(self.browser.quit) # Closes browser instance when the tests are done

    # Check if "Florist Blåklinten" is in the <title> of the page
    def test_page_title(self):
        self.browser.get(self.website_url)
        self.assertIn("Florist Blåklinten", self.browser.title) 

    # Tests if the class "fa-facebook" is on the page
    def test_check_facebook(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.CLASS_NAME, "fa-facebook")

    # Tests if the class "fa-twitter" is on the page
    def test_check_twitter(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.CLASS_NAME, "fa-twitter")

    # Tests if the class "fa-instagram" is on the page
    def test_check_instagram(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.CLASS_NAME, "fa-instagram")

if __name__ == "__main__":
    unittest.main()