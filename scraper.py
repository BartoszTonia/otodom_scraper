from selenium.common import WebDriverException
from selenium.webdriver.common.by import By
import re


class Scraper:
    def __init__(self, driver):
        self.driver = driver

    def extract(self, var_name, css_selector, return_type):
        print(f' >> extracting {var_name}:', end='')
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            print(f' >> type: {return_type}, text: {element.text}', end=' ')
            if element:
                if return_type == 'text':
                    print(f' >>{element.text} <<')
                    return element.text
                elif return_type == 'float':
                    # extract only the digits from the string and discard any other characters such as "m2"
                    value = float(re.findall(r'\d+\.\d+', element.text.replace(',', '.'))[0])
                    print(f' >> {value} <<')
                    return value
                elif return_type == 'int':
                    # remove any non-digit characters from the string, such as the currency symbol "zł".
                    value = int(re.sub(r'\D', '', element.text))
                    print(f' >> {value} <<')
                    return value

            else:
                return None
        except (AttributeError, IndexError, ValueError, WebDriverException) as e:
            return 0

    def get_title(self):
        return self.extract('title', "h1[data-cy='adPageAdTitle']", 'text')

    def get_location(self):
        return self.extract('location', "a[aria-label='Adres']", 'text')

    def get_room_count(self):
        return self.extract('room_count', "div[aria-label='Liczba pokoi'] > div:nth-child(3)", 'text')

    def get_addons(self):
        return self.extract('addons', "div[aria-label='Informacje dodatkowe'] > div:nth-child(2)", 'text')

    def get_area(self):
        return self.extract('area', "div[aria-label='Powierzchnia'] > div:nth-child(3)", 'float')

    def get_market(self):
        return self.extract('market', "div[aria-label='Rynek'] > div:nth-child(2)", 'text')

    def get_floor_count(self):
        try:
            floor_count = \
                self.extract('floor_count', "div[aria-label='Piętro'] > div:nth-child(3)", 'text').split('/')[1]
        except IndexError:
            floor_count = "no data"
        return floor_count

    def get_floor(self):
        try:
            floor = \
                self.extract('floor', "div[aria-label='Piętro'] > div:nth-child(3)", 'text').split('/')[0]
        except IndexError:
            floor = "no data"
        return floor

    def get_year(self):
        return self.extract('year', "div[aria-label='Rok budowy'] > div:nth-child(2)", 'int')

    def get_price(self):
        return self.extract('price', "strong[data-cy='adPageHeaderPrice']", 'int')

    # Sell model exclusive data information
    def get_price_per_meter(self):
        return self.extract('price_m', "div[aria-label='Cena za metr kwadratowy']", 'int')

    def get_rent(self):
        try:
            rent = self.extract('media_price', "div[aria-label='Czynsz dodatkowo']", 'int')
            if rent:
                rent = re.sub(r'\D', '', rent.text)
                rent = rent.replace(' ', '').replace(',', '')
                return float(rent)
            else:
                return 0
        except Exception:
            return 0