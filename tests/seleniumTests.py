import unittest
import sys
import requests
from pathlib import Path
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

        self.driver = webdriver.Chrome(service=service, options=options)
        # Closes browser when the tests are finished
        self.addCleanup(self.driver.quit)

    # Check if "Florist Blåklinten" is in the <title> of the page
    def test_page_title(self):
        self.driver.get(self.website_url)
        title = self.driver.title
        self.assertIn(title, "Florist Blåklinten")

    def test_check_logo(self):
        self.driver.get(self.website_url)

        logoElement = self.driver.find_element(By.XPATH, "//link[@type='image/x-icon']")
        self.assertIn('favicon.ico', logoElement.get_attribute("href"))

    # checks for empty links
    def test_check_for_empty_links(self):
        self.driver.get(self.website_url)

        links = self.driver.find_elements(By.TAG_NAME, "a")

        for link in links:
            self.assertNotEqual(link.get_attribute("href").split("/")[-1], "#")
            self.assertIsNotNone(link.get_attribute("href"))

    def test_menu_links(self):
        self.driver.get(self.website_url)

        navigation = self.driver.find_element(By.TAG_NAME, "nav")
        links = navigation.find_elements(By.TAG_NAME, "a")
        required_links = [
            "#home",
            "#products",
            "#services",
            "#team"
        ]
        for link in required_links:
            self.assertIn(link, [link.get_attribute("href").split('/')[-1] for link in links])

    # checks for important information on the website
    def test_check_info_on_page(self):
        self.driver.get(self.website_url)

        headerText = self.driver.find_element(By.ID, "home").text.replace("\n", " ")
        openHourText = self.driver.find_element(By.CLASS_NAME, "openHours").text.replace("\n", " ")
        serviceText = self.driver.find_element(By.CLASS_NAME, "serviceCards").text.replace("\n", " ")
        productText = self.driver.find_element(By.CLASS_NAME, "cards").text.replace("\n", " ")

        header = [
            "Välkommen till Florist Blåklinten",
            "Ring oss på 0630-555-555 för frågor eller beställning",
        ]

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

        for text in header:
            self.assertIn(text, headerText)
        print("Header text found")
        
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
        self.driver.get(self.website_url)

        my_property = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".bgimg"))).value_of_css_property("background-image")
        self.assertIn("bg-b.jpg", my_property)

    # checks images on the page and if they exists
    def test_for_images_on_page(self):
        self.driver.get(self.website_url)
        # get all elements with img tag
        image_elements = self.driver.find_elements(By.TAG_NAME, 'img')

        for image in image_elements:
            image_source = image.get_attribute('src')

            # if the img has a src attribute with a image
            if image.get_attribute('src') is not None:
                # Assert that the image source is fetchable from the server ( < 400 )
                self.assertLess(requests.get(image_source).status_code, 400)
            else:  # assert False (Just a fail)
                self.assertTrue(False)
                continue

    def test_for_large_images(self):
        images = Path(__file__).resolve().parents[1] / Path('florist-blaklint/assets/images/')
        # Assert check for images larger than 1Mb
        for image in images.glob('**/*.*'):
            # Get the file size property
            image_size = Path(image).stat().st_size
            print("Image path: {} \t image size: {}".format(image, image_size))
            # Assert if the file is greater than 500kb
            self.assertGreater(500_000, image_size)

    # checks the links and clicks on them and compares it with "current_url"
    def test_social_links(self):
        self.driver.get(self.website_url)

        # List of social medias
        socials = ["facebook", "instagram", "twitter"]

        # Loop over list
        for social in socials:
            # Check if link and icon is on page
            socialElement =  self.driver.find_element(By.CLASS_NAME, f"fa-{social}")
            ActionChains(socialElement).move_to_element(socialElement).click()
            socialHref = socialElement.get_attribute("href")

            self.assertEqual(socialHref, f"https://{social}.com/ntiuppsala")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        CheckWebsite.website_url = sys.argv.pop()

    unittest.main(verbosity=2)
    
