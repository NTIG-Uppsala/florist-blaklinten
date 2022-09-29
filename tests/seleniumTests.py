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
    
    def test_flag_links(self):
        self.driver.get(self.website_url)

        navigation = self.driver.find_element(By.TAG_NAME, "nav")
        links = navigation.find_elements(By.TAG_NAME, "a")
        
        self.assertIn("index-ua.html", [link.get_attribute("href").split('/')[-1] for link in links])

        self.driver.get(self.website_url + "index-ua.html")
        
        navigation = self.driver.find_element(By.TAG_NAME, "nav")
        links = navigation.find_elements(By.TAG_NAME, "a")

        self.assertIn("index.html", [link.get_attribute("href").split('/')[-1] for link in links])

    def test_check_info_ukranian(self):
        self.driver.get(self.website_url + "index-ua.html")

        headerText = self.driver.find_element(By.ID, "home").text.replace("\n", " ")
        openHourText = self.driver.find_element(By.CLASS_NAME, "openHours").text.replace("\n", " ")
        serviceText = self.driver.find_element(By.CLASS_NAME, "serviceCards").text.replace("\n", " ")
        productText = self.driver.find_element(By.CLASS_NAME, "cards").text.replace("\n", " ")
        teamText = self.driver.find_element(By.ID, "team").text.replace("\n", " ")
        closedDaysText = self.driver.find_element(By.ID, "closingDays").text.replace("\n", " ")

        header = [
            "Florist Blåklinten",
            "Телефонуйте нам 0630-555-555",
        ]

        products = [
            "Весільний букет", "1200 kr",
            "Похоронний вінок", "800 kr",
            "Осінній букет", "400 kr",
            "Літній букет", "200 kr",
            "Троянди 10 шт", "150 kr", 
            "Тюльпани 10 шт", "100 kr", 
        ]

        services = [
            "Консультація 30 хв", "250 kr"
        ]

        openHours = [
            "Робочі дні", "10 - 16",
            "Субота", "12 - 15",
            "неділя", "Зачинено"
        ]

        team = [
            "Наш персонал",
            "Вітаю до нас у Florist Blåklinten! Ми є згуртованою групою з різними експертними навичками, які можуть допомогти вам найкращим чином відповідно до ваших потреб.",
            "Örjan Johansson",
            "Флорист",
            "Якщо вам потрібен букет, будь то на весілля, день народження чи щось зовсім інше, я можу допомогти вам скласти букет на основі ваших побажань.",
            "Anna Pettersson",
            "Хортолог",
            "Я кваліфікований садівник і можу допомогти вам або вашій компанії зробити найкращий вибір, виходячи з ваших потреб та умов щодо фруктових дерев, овочівництва та декоративних рослин.",
            "Fredrik Örtqvist",
            "Власник",
            "Моя любов до квітів заклала основу для існування Florist Blåklinten сьогодні, і я сподіваюся, що ви як клієнт можете надихнутися в нашому магазині."
        ]

        closedDays = [
            "Неробочі дні",
            "Новий рік",
            "1 січня",
            "Тринадцятий день Різдва",
            "6 січня",
            "1 травня",
            "1 травня",
            "Національний день Швеції",
            "6 червня",
            "Святвечір",
            "24 грудня",
            "Різдво",
            "25 грудня",
            "День подарунків Різдва",
            "26 грудня",
            "Переддень Нового року",
            "31 грудня",
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

        for text in team:
            self.assertIn(text, teamText)
        print("Team text found")

        for text in closedDays:
            self.assertIn(text, closedDaysText)
        print("Closed days text found")


    # checks for important information on the website
    def test_check_info_on_page(self):
        self.driver.get(self.website_url)

        headerText = self.driver.find_element(By.ID, "home").text.replace("\n", " ")
        openHourText = self.driver.find_element(By.CLASS_NAME, "openHours").text.replace("\n", " ")
        serviceText = self.driver.find_element(By.CLASS_NAME, "serviceCards").text.replace("\n", " ")
        productText = self.driver.find_element(By.CLASS_NAME, "cards").text.replace("\n", " ")
        teamText = self.driver.find_element(By.ID, "team").text.replace("\n", " ")
        closedDaysText = self.driver.find_element(By.ID, "closingDays").text.replace("\n", " ")

        header = [
            "Florist Blåklinten",
            "Ring oss på 0630-555-555 ",
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

        team = [
            "Vår personal",
            "Välkommen till oss på Florist Blåklinten! Vi är ett sammansvetsat gäng med olika expertkompetenser som därmed kan hjälpa dig på bästa sätt utifrån dina behov.",
            "Örjan Johansson",
            "Florist",
            "Om du behöver en bukett, oavsett om det är till bröllop, födelsedagsfirande eller något helt annat kan jag hjälpa dig att komponera buketten utifrån dina önskemål.",
            "Anna Pettersson",
            "Hortonom",
            "Jag är utbildad hortonom och kan hjälpa dig eller ditt företag att göra det bästa valet utifrån dina behov och förutsättningar vad det gäller fruktträd, grönsaksodling och prydnadsväxter.",
            "Fredrik Örtqvist",
            "Ägare",
            "Min kärlek till blommor lade grunden till att Florist Blåklinten finns idag och jag hoppas att du som kund kan inspireras i vår butik."
        ]

        closedDays = [
            "Nyårsdagen",
            "1 Januari",
            "Trettondedag jul",
            "6 Januari",
            "Första maj",
            "1 Maj",
            "Sveriges nationaldag",
            "6 Juni",
            "Julafton",
            "24 December",
            "Juldagen",
            "25 December",
            "Annandag jul",
            "26 December",
            "Nyårsafton",
            "31 December",
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

        for text in team:
            self.assertIn(text, teamText)
        print("Team text found")

        for text in closedDays:
            self.assertIn(text, closedDaysText)
        print("Closed days text found")

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
                print("Checking {}".format(image_source))
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
    # Check for map
    def test_check_map(self):
        self.driver.get(self.website_url)
        map_url = "google.com/maps/embed?pb=!1m18!1m12!1m3!1d2072.472099087858!2d15.768257516460107!3d58.70529006794066!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46594feedcca3b1d%3A0x6c778af446b70e00!2sDe%20Wijks%20v%C3%A4g%2029%2C%20612%2030%20Finsp%C3%A5ng!5e0!3m2!1sen!2sse!4v1664435816938!5m2!1sen!2sse"
        map_element = self.driver.find_element(By.ID, "mapiframe")

        self.assertTrue(map_element.is_displayed())
        self.assertIn(map_url, map_element.get_attribute("src"))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        CheckWebsite.website_url = sys.argv.pop()

    unittest.main(verbosity=2)
    
