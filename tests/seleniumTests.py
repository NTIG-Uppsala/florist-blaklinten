import unittest
import os
import sys
import time
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

    # checks that the opentimes are on the website
    def test_find_text(self):
        self.browser.get(self.website_url)
        pageText = self.browser.find_element(By.TAG_NAME, "body").text

        controlTexts = [
            "Florist Blåklinten",
            "Öppettider",
            "Måndag","10 - 16",
            "Tisdag","10 - 16",
            "Onsdag","10 - 16",
            "Torsdag","10 - 16",
            "Fredag","10 - 16",
            "Lördag","12 - 15",
            "Söndag","Stängt",
            "Kontakta oss",
            "Fjällgatan 32H 981 39 Finspång",
            "0630-555-555",
            "info@blåklinten.se",
            "Sommarbuket", "200 kr",
            "Bröllopsbruketter", "1200 kr",
            "Begravningskrans", "800 kr",
            "Höstbuket", "400 kr",
            "Rosor 10-pack", "150 kr", 
            "Tulpaner 10-pack", "100 kr", 
            "Konsultation 30 min", "250 kr"
        ]

        for text in controlTexts:
            self.assertIn(text, pageText)

    #checks images on the page and if they exists
    def test_check_images(self):
        self.browser.get(self.website_url)
        imageNames = ["bild1.jpg", "bild2.jpg", "bild3.jpg"]

        images = self.browser.find_elements(By.TAG_NAME, "img")

        for image in images:
            source = image.get_attribute("src")
            sourceImage = os.path.basename(os.path.normpath(source))
            print(sourceImage)
            assert sourceImage in imageNames

    # checks the links and clicks on them and compares it with "current_url"


    def test_click_links_on_page(self):
        self.browser.get(self.website_url)

        # List of social medias
        socials = ["facebook", "instagram", "twitter"]

        # Loop over list
        for social in socials:
            # Check if link and icon is on page
            iconElement =  self.browser.find_element(By.CLASS_NAME, f"fa-{social}")
            ActionChains(iconElement).move_to_element(iconElement).click()
            iconHref = iconElement.get_attribute("href")

            self.assertEqual(iconHref, f"https://{social}.com/ntiuppsala")
    
    def test_check_background(self):
        pass

if __name__ == "__main__":
    CheckWebsite.website_url = sys.argv.pop()
    unittest.main(verbosity=2)
