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

    @classmethod
    def setUpClass(self):
        service = Service(executable_path=ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=service, options=options)

        self.page_names = [
        "index.html",
        "index-ua.html",
        "finspang.html",
        "finspang-ua.html",
        "norrkoping.html",
        "norrkoping-ua.html",
    ]
    
    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    # Check if "Florist Blåklinten" is in the <title> of the page
    def test_page_title(self):
        for p in self.page_names:
            self.driver.get(self.website_url + p)
            title = self.driver.title
            self.assertIn(title, "Florist Blåklinten")

    # Check if page has correct logo
    def test_check_logo(self):
        for p in self.page_names:
            self.driver.get(self.website_url + p)
            logoElement = self.driver.find_element(By.XPATH, "//link[@type='image/x-icon']")
            self.assertIn('favicon.ico', logoElement.get_attribute("href"))

    # checks for empty links
    def test_check_for_empty_links(self):
        for p in self.page_names:

            self.driver.get(self.website_url + p)
            links = self.driver.find_elements(By.TAG_NAME, "a")

            for link in links:
                self.assertNotEqual(link.get_attribute("href").split("/")[-1], "#")
                self.assertIsNotNone(link.get_attribute("href"))

    # Checks that all menu links work
    def test_menu_links(self):
        for p in self.page_names:
            if p == "index.html" or p == "index-ua.html":
                pass
            else:
                if "ua" in p:
                    localsPage = "index-ua.html"
                else:
                    localsPage = "index.html"
                self.driver.get(self.website_url + p)

                navigation = self.driver.find_element(By.TAG_NAME, "nav")
                links = navigation.find_elements(By.TAG_NAME, "a")
                required_links = [
                    "#header",
                    "#products",
                    "#services",
                    "#team",
                    "#find-us",
                    localsPage
                ]
                for link in required_links:
                    tag_list = []
                    crnt_tag = [link.get_attribute("href").split('/')[-1] for link in links]
                    for x in crnt_tag:
                        if "#" in x:
                            tag_list.append(x.split("html",1)[1])
                        else:
                            tag_list.append(x)

                    self.assertIn(link, tag_list)
    
    # Checks that language change button works
    def test_flag_links(self):
        for p in self.page_names:
            self.driver.get(self.website_url + p)

            if "ua" in p:
                crntIndex = self.page_names.index(p) - 1
            else:
                crntIndex = self.page_names.index(p) + 1

            navigation = self.driver.find_element(By.TAG_NAME, "nav")
            links = navigation.find_elements(By.TAG_NAME, "a")
            
            self.assertIn(self.page_names[crntIndex], [link.get_attribute("href").split('/')[-1] for link in links])

    # Checks all homepage links exists
    def test_click_links_homepage(self):
        self.driver.get(self.website_url + "index.html")	
        links = self.driver.find_elements(By.CSS_SELECTOR, "#page-content a")
        expectedLinks = [
            "finspang.html",
            "norrkoping.html",
        ]

        expectedLinksUa = [
            "finspang-ua.html",
            "norrkoping-ua.html",
        ]

        for link in links:
            self.assertIn(link.get_attribute("href").split("/")[-1], expectedLinks)
        
        self.driver.get(self.website_url + "index-ua.html")
        linksUa = self.driver.find_elements(By.CSS_SELECTOR, "#page-content a")

        for link in linksUa:
            self.assertIn(link.get_attribute("href").split("/")[-1], expectedLinksUa)

    # Checks all info on index page
    def test_check_info_homepage(self):
        self.driver.get(self.website_url + "index.html")
        pageText = self.driver.find_element(By.ID, "page-content").text.replace("\n", " ")
        copyrightText = self.driver.find_element(By.TAG_NAME, "footer").text.replace("\n", " ")

        pageText = [
            "VÅRA LOKALER",
            "Välj och tryck på en av bilderna nedan",
            "för att komma till en av våra två lokaler",
            "Finspång",
            "De Wijks väg 29",
            "612 30 Finspång",
            "Norrköping",
            "Färjledsvägen 38",
            "961 93 Norrköping",
            "Södra Sunderbyn"
        ]

        for text in pageText:
            self.assertIn(text, pageText)

        self.assertIn("© 2022 NTI-Gymnasiet", copyrightText)

    # Checks all info on ukrainian index page
    def test_check_info_ukrainian_homepage(self):
        self.driver.get(self.website_url + "index-ua.html")
        pageText = self.driver.find_element(By.ID, "page-content").text.replace("\n", " ")
        copyrightText = self.driver.find_element(By.TAG_NAME, "footer").text.replace("\n", " ")

        pageText = [
            "НАШІ ПРИМІЩЕННЯ",
            "Виберіть і торкніться одного із зображень нижче",
            "щоб прийти в одне з наших приміщень",
            "Finspång",
            "De Wijks väg 29",
            "612 30 Finspång",
            "Norrköping",
            "Färjledsvägen 38",
            "961 93 Norrköping",
            "Södra Sunderbyn"
        ]

        for text in pageText:
            self.assertIn(text, pageText)

        self.assertIn("© 2022 NTI-Gymnasiet", copyrightText)

    def test_check_info_ukrainian_finspang(self):
        self.driver.get(self.website_url + "finspang-ua.html")

        textDict = {
            "header": [
                "Florist Blåklinten",
                "Для бронювання та замовлення телефонуйте нам 0630-555-555",
            ],
            "products": [
                "Весільний букет", "1200 kr",
                "Вінок", "800 kr",
                "Осінній букет", "400 kr",
                "Літній букет", "200 kr",
                "Троянди 10 шт", "150 kr", 
                "Тюльпани 10 шт", "100 kr", 
            ],
            "services": [
                "Консультація 30 хв", "250 kr"
            ],
            "openHours": [
                "Пн-Пт", "10 - 16",
                "Субота", "12 - 15",
                "неділя", "Зачинено"
            ],
            "team": [
                "Наш персонал",
                "Вітаємо у Florist Blåklinten! Наша дружня команда з різними експертними навичками,які можуть допомогти вам найкращим чином.",
                "Örjan Johansson",
                "Флорист",
                "Якщо вам потрібен букет,чи то на весілля,день народження чи щось зовсім інше,я можу вам допомогти скласти букет за вашим бажанням.",
                "Anna Pettersson",
                "Експерт-садiвник",
                "Я кваліфікований садівник і можу допомогти вам або вашій компанії зробити найкращий вибір,фруктових дерев,декоративних рослин або овочевих культур,враховуючи ваші потреби,умови та вподобання.",
                "Fredrik Örtqvist",
                "Власник",
                "Моя любов до квітів заклала основу для існування Florist Blåklinten сьогодні, і я сподіваюся, що ви як клієнт можете надихнутися в нашому магазині."
            ],
            "holidays": [
                "Вихідні дні",
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
            ],
            "copyright": [
                "© 2022 NTI-Gymnasiet"
            ]
        } 

        for section, content in textDict.items():
            txt = self.driver.find_element(By.ID, section).text.replace("\n", " ")
            for text in content:
                self.assertIn(text, txt)
                

    def test_check_info_ukrainian_norrkoping(self):
        self.driver.get(self.website_url + "norrkoping-ua.html")

        textDict = {
            "header": [
                "Florist Blåklinten",
                "Для бронювання та замовлення телефонуйте нам 0640-555-333",
            ],
            "products": [
                "Весільний букет", "1200 kr",
                "Вінок", "800 kr",
                "Осінній букет", "400 kr",
                "Літній букет", "200 kr",
                "Троянди 10 шт", "150 kr", 
                "Тюльпани 10 шт", "100 kr", 
            ],
            "services": [
                "Консультація 30 хв", "250 kr"
            ],
            "openHours": [
                "Понеділок", "10 - 17",
                "Вівторок", "10 - 16",
                "Середа", "10 - 15",
                "четвер", "10 - 16",
                "П'ятниця", "10 - 16",
                "Субота", "12 - 15",
                "Неділя", "Зачинено"
            ],
            "team": [
                "Наш персонал",
                "Вітаємо у Florist Blåklinten! Наша дружня команда з різними експертними навичками,які можуть допомогти вам найкращим чином.",
                "Johan Olsson",
                "Флорист",
                "У своїх японських садах я знаходжу спокій і натхнення. Моя спеціалізація – спілкування з клієнтами, де ми разом створюємо індивідуальну квіткову концепцію!",
                "Anna Andersson",
                "Флорист",
                "Коли я складаю букет, то починаю з квітки. Я додаю по одній квітці в цю серцевину, поки букет не стане потрібного розміру.",
                "Elin Nygård",
                "Експерт-садiвник",
                "Мій сад – мій найкращий учитель. Дозвольте мені поділитися знаннями, які я отримав за десятки сезонів чергування пишних кольорів і уповільненого росту."
            ],
            "holidays": [
                "Вихідні дні",
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
            ],
            "copyright": [
                "© 2022 NTI-Gymnasiet"
            ]
        }

        for section, content in textDict.items():
            txt = self.driver.find_element(By.ID, section).text.replace("\n", " ")
            for text in content:
                self.assertIn(text, txt)


    # checks for important information on the website
    def test_check_info_on_finspang(self):
        self.driver.get(self.website_url + "finspang.html")

        textDict = {
            "header": [
                "Florist Blåklinten",
                "För bokning och beställning ring oss på 0630-555-555",
            ],
            "products": [
                "Bröllopsbukett", "1200 kr",
                "Begravningskrans", "800 kr",
                "Höstbukett", "400 kr",
                "Sommarbukett", "200 kr",
                "Rosor 10-pack", "150 kr", 
                "Tulpaner 10-pack", "100 kr", 
            ],
            "services": [
                "Konsultation 30 minuter", "250 kr"
            ],
            "openHours":[
                "Vardagar", "10 - 16",
                "Lördag", "12 - 15",
                "Söndag", "Stängt"
            ],
            "team": [
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
            ],
            "holidays": [
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
            ],
            "copyright": [
                "© 2022 NTI-Gymnasiet"
            ]
        }

        for section, content in textDict.items():
            txt = self.driver.find_element(By.ID, section).text.replace("\n", " ")
            for text in content:
                self.assertIn(text, txt)

    def test_check_info_on_norrkoping(self):
        self.driver.get(self.website_url + "norrkoping.html")

        textDict = {
            "header": [
                "Florist Blåklinten",
                "För bokning och beställning ring oss på 0640-555-333",
            ],
            "products": [
                "Bröllopsbukett", "1200 kr",
                "Begravningskrans", "800 kr",
                "Höstbukett", "400 kr",
                "Sommarbukett", "200 kr",
                "Rosor 10-pack", "150 kr", 
                "Tulpaner 10-pack", "100 kr", 
            ],
            "services": [
                "Konsultation 30 minuter", "250 kr"
            ],
            "openHours": [
                "Måndag", "10 - 17",
                "Tisdag", "10 - 16",
                "Onsdag", "10 - 15",
                "Torsdag", "10 - 16",
                "Fredag", "10 - 16",
                "Lördag", "12 - 15",
                "Söndag", "Stängt"
            ],
            "team": [
                "Vår personal",
                "Välkommen till oss på Florist Blåklinten! Vi är ett sammansvetsat gäng med olika expertkompetenser som därmed kan hjälpa dig på bästa sätt utifrån dina behov.",
                "Johan Olsson",
                "Florist",
                "Jag finner lugnet och inspirationen i mina japanska trädgårdar. Min specialitet är kundsamtalet där vi tillsammans drömmer fram just ert skräddarsydda blomsterkoncept!",
                "Anna Andersson",
                "Florist",
                "När jag gör en bukett utgår jag ifrån en enda blomma. Till denna kärna lägger jag sedan till en blomma i taget tills buketten är lagom stor.",
                "Elin Nygård",
                "Hortonom",
                "Min kolonilott är min bästa lärare. Låt mig få dela med mig av de kunskaper jag förvärvat genom dussintalet säsonger av ömsom färgprakt, ömsom missväxt."
            ],
            "holidays": [
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
            ],
            "copyright": [
                "© 2022 NTI-Gymnasiet"
            ]
        }

        for section, content in textDict.items():
            txt = self.driver.find_element(By.ID, section).text.replace("\n", " ")
            for text in content:
                self.assertIn(text, txt)

    def test_postnumber(self):
        finspang_postnumbers = [
            98139,
            98140,
            98142,
            98138,
        ]

        norrkoping_postnumbers = [
            96193,
            96194,
            96190,
            96191,
        ]

        for p in self.page_names:
            if p == "index-ua.html" or p == "index.html":
                pass
            else:
                self.driver.get(self.website_url + p)
                if p == "finspang.html" or p == "finspang-ua.html":
                    current_postnumber = finspang_postnumbers
                    if p == "finspang.html":
                        current_msgCheck = "Vi kör ut till ditt postnummer!"
                    else:
                        current_msgCheck = "Доставляємо на ваш поштовий індекс!"
                else:
                    current_postnumber = norrkoping_postnumbers
                    if p == "norrkoping.html":
                        current_msgCheck = "Vi kör ut till ditt postnummer!"
                    else:
                        current_msgCheck = "Доставляємо на ваш поштовий індекс!"

                for postnumber in current_postnumber:
                    inp = self.driver.find_element(By.ID, "submitText")
                    inp.clear()
                    inp.send_keys(postnumber)
                    self.driver.find_element(By.ID, "submitButton").click()
                    message = self.driver.find_element(By.ID, "submitMessage").text
                    self.assertIn(current_msgCheck, message)



    # checks background image
    def test_check_background(self):
        for p in self.page_names:
            if p == "index.html" or p == "index-ua.html":
                pass
            else:
                if p == "finspang.html" or p == "finspang-ua.html":
                    bg_image = "bg-b.jpg"
                    bg_class = "bgimg"
                elif p == "norrkoping.html" or p == "norrkoping-ua.html":
                    bg_image = "bg-r.jpg"
                    bg_class = "bgimg2"

                self.driver.get(self.website_url + p)
                my_property = self.driver.find_element(By.CLASS_NAME, bg_class).value_of_css_property("background-image")
                # my_property = WebDriverWait(self.driver, 60).until(EC.visibility_of_element_located((By.CSS_SELECTOR, bg_class))).value_of_css_property("background-image")
                self.assertIn(bg_image, my_property)

    # checks images on the page and if they exists
    def test_for_images_on_page(self):
        for p in self.page_names:
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
            # Assert if the file is greater than 500kb
            self.assertGreater(500_000, image_size)

    # checks the links and clicks on them and compares it with "current_url"
    def test_social_links(self):
        for p in self.page_names:
            if p == "index-ua.html" or p == "index.html":
                pass
            else:
                self.driver.get(self.website_url + p)

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
        self.driver.get(self.website_url + "finspang.html")
        map_url = "google.com/maps/embed?pb=!1m18!1m12!1m3!1d2072.472099087858!2d15.768257516460107!3d58.70529006794066!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46594feedcca3b1d%3A0x6c778af446b70e00!2sDe%20Wijks%20v%C3%A4g%2029%2C%20612%2030%20Finsp%C3%A5ng!5e0!3m2!1sen!2sse!4v1664435816938!5m2!1sen!2sse"
        map_element = self.driver.find_element(By.ID, "mapiframe")

        self.assertTrue(map_element.is_displayed())
        self.assertIn(map_url, map_element.get_attribute("src"))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        CheckWebsite.website_url = sys.argv.pop()

    unittest.main(verbosity=2)
    
