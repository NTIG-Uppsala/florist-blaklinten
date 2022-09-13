import unittest
import os
import sys
import time
from types import NoneType
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
    def test_check_openTime(self):
        self.browser.get(self.website_url)

        # Dict of open hours
        openTime = {
            "Monday": ["Måndagar","10-16"],
            "Tuesday": ["Tisdagar","10-16"],
            "Wedensday": ["Onsdagar","10-16"],
            "Thursday": ["Torsdagar", "10-16"],
            "Friday": ["Fredagar", "10-16"],
            "Saturday": ["Lördagar", "12-15"],
            "Sunday": ["Söndagar", "Stängt"],
        }

        openTimeTable = self.browser.find_element(By.CLASS_NAME, "openHours")
        openTimeElements = openTimeTable.find_elements(By.TAG_NAME, "tr")

        for open_hour in openTimeElements:
            current_day = open_hour.get_attribute("dayData")
            openTimeText = open_hour.text
            print(openTimeText)
            
            if current_day in openTimeText:
                self.assertIn(" ".join(openTime[current_day]), openTimeText)

    def test_check_products(self):
        self.browser.get(self.website_url)

        # Dict of open hours
        products = {
            "Sommarbuket": ["Sommarbuket","200 kr"],
            "Brollopsbruketter": ["Bröllopsbruketter","1200 kr"],
            "Begravningskrans": ["Begravningskrans","800 kr"],
            "Hostbukett": ["Höstbukett", "400 kr"],
            "Rosor": ["Rosor 10-pack", "150 kr"],
            "Tulpaner": ["Tulpaner 10-pack", "100 kr"],
            "Konsultation": ["Konsultation 30 min", "250 kr"],
        }

        productsTable = self.browser.find_element(By.CLASS_NAME, "products")
        productsElements = productsTable.find_elements(By.TAG_NAME, "tr")

        for products in productsElements:
            current_day = products.get_attribute("productData")
            productsText = products.text
            print(productsText)
            
            if current_day in productsText:
                self.assertIn(" ".join(products[current_day]), productsText)

    def test_check_contact(self):
        self.browser.get(self.website_url)
        contact = self.browser.find_element(By.TAG_NAME, "body").text

        controlText = [
            "Kontakta oss",
            "Fjällgatan 32H 981 39 Finspång",
            "0630-555-555",
            "info@blåklinten.se"
        ]

        for text in controlText:
            assert text in contact

    def test_check_background(self):
        pass

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
            icon_element =  self.browser.find_element(By.CLASS_NAME, f"fa-{social}")
            ActionChains(icon_element).move_to_element(icon_element).click()
            icon_href = icon_element.get_attribute("href")

            self.assertEqual(icon_href, f"https://{social}.com/ntiuppsala")
    
    def test_check_background(self):
        pass

if __name__ == "__main__":
    CheckWebsite.website_url = sys.argv.pop()
    unittest.main(verbosity=2)
