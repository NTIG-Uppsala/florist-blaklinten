import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By

class CheckWebsite(unittest.TestCase):
    website_url = "https://ntig-uppsala.github.io/florist-blaklinten/florist-blaklint/" # Standard URL 

    def setUp(self):
        driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install() # Initializes the driver

        # Run the browser with no GUI
        chrome_options = Options()
        chrome_options.add_argument("--headless") 

        #Removes the "[0906/090604.968:INFO:CONSOLE(0)] "Error with Permissions-Policy header: Origin trial controlled feature not enabled: 'interest-cohort'.", source: (0)" warning
        chrome_options.add_argument("--log-level=1") 

        self.browser = webdriver.Chrome(driver_path, options=chrome_options) #Initializes the browser instance with the driver
        self.addCleanup(self.browser.quit) # Closes browser when the tests are finished

    #Check if "Florist Blåklinten" is in the <title> of the page
    def test_page_title(self):
        self.browser.get(self.website_url)
        self.assertIn("Florist Blåklinten", self.browser.title) 

        
    #checks the links and clicks on them and compares it with "current_url"
    def test_click_link_facebook(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.CSS_SELECTOR, ".fa-facebook").click()
        current_url = self.browser.find_element(By.CSS_SELECTOR, ".fa-facebook").get_attribute("href")
        assert current_url == "https://www.facebook.com/ntiuppsala"

    def test_check_link_twitter(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.CSS_SELECTOR, ".fa-twitter").click()
        current_url = self.browser.find_element(By.CSS_SELECTOR, ".fa-twitter").get_attribute("href")
        assert current_url == "https://twitter.com/ntiuppsala"

    def test_check_link_instagram(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.CSS_SELECTOR, ".fa-instagram").click()
        current_url = self.browser.find_element(By.CSS_SELECTOR, ".fa-instagram").get_attribute("href")
        assert current_url == "https://instagram.com/ntiuppsala"

if __name__ == "__main__":
    unittest.main(verbosity=2)
