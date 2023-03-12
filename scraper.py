from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
import re


class Scraper:
    def __init__(self, driver):
        self.driver = driver

    def extract(self, css_selector, return_type):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            if element:
                if return_type == 'text':
                    return element.text
                elif return_type == 'float':
                    # extract only the digits from the string and discard any other characters such as "m2"
                    value = float(re.findall(r'\d+(?:\.\d+)?', element.text.replace(',', '.'))[0])
                    return value
                elif return_type == 'int':
                    # remove any non-digit characters from the string, such as the currency symbol "zł".
                    value = element.text.split(',')[0]
                    value = re.sub(r'\D', '', value)
                    return int(value)

            else:
                return None
        except (AttributeError, IndexError, ValueError, WebDriverException) as e:
            return 0

    def get_title(self):
        return self.extract("h1[data-cy='adPageAdTitle']", 'text')

    def get_location(self):
        return self.extract("a[aria-label='Adres']", 'text')

    def get_seller_type(self):
        seller_type = self.extract("span[aria-label='Typ przedstawiciela agencji']", 'text')
        if seller_type != 0:
            return seller_type
        else:
            return 'Oferta Prywatna'

    def get_seller(self):
        seller = self.extract("strong[aria-label='Nazwa agencji']", 'text')
        if seller != 0:
            return seller
        else:
            return 'Oferta Prywatna'

    def get_room_count(self):
        return self.extract("div[aria-label='Liczba pokoi'] > div:nth-child(3)", 'text')

    def get_addons(self):
        return self.extract("div[aria-label='Informacje dodatkowe'] > div:nth-child(2)", 'text')

    def get_area(self):
        return self.extract("div[aria-label='Powierzchnia'] > div:nth-child(3)", 'float')

    def get_market(self):
        return self.extract("div[aria-label='Rynek'] > div:nth-child(2)", 'text')

    def get_floor_count(self):
        try:
            floor_count = \
                self.extract("div[aria-label='Piętro'] > div:nth-child(3)", 'text').split('/')[1]
        except IndexError:
            floor_count = "no data"
        return floor_count

    def get_floor(self):
        try:
            floor = \
                self.extract("div[aria-label='Piętro'] > div:nth-child(3)", 'text').split('/')[0]
        except IndexError:
            floor = "no data"
        return floor

    def get_year(self):
        return self.extract("div[aria-label='Rok budowy'] > div:nth-child(2)", 'int')

    def get_price(self):
        return self.extract("strong[data-cy='adPageHeaderPrice']", 'int')

    # Sell model exclusive data information
    def get_price_per_meter(self):
        return self.extract("div[aria-label='Cena za metr kwadratowy']", 'int')

    def get_rent(self):
        try:
            rent = self.extract("div[aria-label='Czynsz dodatkowo']", 'text')
            if rent:
                rent = re.sub(r'\D', '', rent)
                rent = rent.replace(' ', '').replace(',', '')
                return float(rent)
            else:
                return 0
        except Exception:
            return 0
