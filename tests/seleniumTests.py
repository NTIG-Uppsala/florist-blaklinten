import unittest
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By

class CheckWebsite(unittest.TestCase):
    website_url = "https://localhost:8000/" # Standard URL 

    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        self.browser = webdriver.Chrome(service=service, options=options)
        self.addCleanup(self.browser.quit) # Closes browser when the tests are finished

    #Check if "Florist Blåklinten" is in the <title> of the page
    def test_page_title(self):
        self.browser.get(self.website_url)
        title = self.browser.title
        assert title == "Florist Blåklinten"
        
    #checks the links and clicks on them and compares it with "current_url"
    def test_click_link_facebook(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.CLASS_NAME, "fa-facebook").click()
        current_url = self.browser.find_element(By.CLASS_NAME, "fa-facebook").get_attribute("href")
        assert current_url == "https://www.facebook.com/ntiuppsala"

    def test_check_link_twitter(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.CLASS_NAME, "fa-twitter").click()
        current_url = self.browser.find_element(By.CLASS_NAME, "fa-twitter").get_attribute("href")
        assert current_url == "https://twitter.com/ntiuppsala"

    def test_check_link_instagram(self):
        self.browser.get(self.website_url)
        self.browser.find_element(By.CLASS_NAME, "fa-instagram").click()
        current_url = self.browser.find_element(By.CLASS_NAME, "fa-instagram").get_attribute("href")
        assert current_url == "https://instagram.com/ntiuppsala"

if __name__ == "__main__":
    CheckWebsite.website_url = sys.argv.pop()
    unittest.main(verbosity=2)
