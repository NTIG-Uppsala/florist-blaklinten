import unittest
import os
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


class CheckWebsite(unittest.TestCase):
    website_url = "http://localhost:8000/"  # Standard URL

    def setUp(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        self.browser = webdriver.Chrome(service=service, options=options)
        # Closes browser when the tests are finished
        self.addCleanup(self.browser.quit)

    # Check if "Florist Blåklinten" is in the <title> of the page
    def test_page_title(self):
        self.browser.get(self.website_url)
        title = self.browser.title
        assert title == "Florist Blåklinten"

    def test_check_logo(self):
        self.browser.get(self.website_url)

        logoElement = self.browser.find_element(By.XPATH, "//link[@type='image/x-icon']")
        self.assertIn('favicon-32x32.ico', logoElement.get_attribute("href"))

    # checks for important information on the website
    def test_check_info_on_page(self):
        self.browser.get(self.website_url)

        openHourText = self.browser.find_element(By.CLASS_NAME, "openHours").text
        serviceText = self.browser.find_element(By.CLASS_NAME, "serviceCards").text
        productText = self.browser.find_element(By.CLASS_NAME, "cards").text

        products = [
            "Bröllopsbukett", "1200 kr",
            "Begravningskrans", "800 kr",
            "Höstbukett", "400 kr",
            "Sommarbukett", "200 kr",
            "Rosor 10-pack", "150 kr", 
            "Tulpaner 10-pack", "100 kr", 
        ]

        services = [
            "Konsultation 30 minuter", "250 kr"
        ]

        openHours = [
            "Vardagar", "10 - 16",
            "Lördag", "12 - 15",
            "Söndag", "Stängt"
        ]
        
        for hours in openHours:
            self.assertIn(hours, openHourText)
        print("Open hours found")

        for service in services:
            self.assertIn(service, serviceText)
        print("Services found")

        for product in products:
            self.assertIn(product, productText)
        print("Products found")

    # checks background image
    def test_check_background(self):
        self.browser.get(self.website_url)

        my_property = WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bgimg"))).value_of_css_property("background-image")
        self.assertIn("bg-b.jpg", my_property)

    # checks images on the page and if they exists
    def test_check_images(self):
        self.browser.get(self.website_url)
        imageNames = ["brollopsblommor.jpg", "hostbukett.jpg", "krans.jpg", "rosor.jpg", "sommarbukett.jpg", "tjanster.jpg", "tulpaner.jpg", "orjan_johansson.png", "fredrik_ortqvist.png", "anna_pettersson.png"]

        images = self.browser.find_elements(By.TAG_NAME, "img")

        for image in images:
            source = image.get_attribute("src")
            sourceImage = os.path.basename(os.path.normpath(source))
            print(sourceImage)
            self.assertIn(sourceImage, imageNames)

    # checks the links and clicks on them and compares it with "current_url"
    def test_click_links_on_page(self):
        self.browser.get(self.website_url)

        # List of social medias
        socials = ["facebook", "instagram", "twitter"]

        # Loop over list
        for social in socials:
            # Check if link and icon is on page
            socialElement =  self.browser.find_element(By.CLASS_NAME, f"fa-{social}")
            ActionChains(socialElement).move_to_element(socialElement).click()
            socialHref = socialElement.get_attribute("href")

            self.assertEqual(socialHref, f"https://{social}.com/ntiuppsala")

if __name__ == "__main__":
    CheckWebsite.website_url = sys.argv.pop()
    unittest.main(verbosity=2)
