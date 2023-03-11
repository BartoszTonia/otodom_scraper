from scraper import Scraper


class Offer:
    def __init__(self, url, driver):
        self.url = url
        self.price = Scraper(driver).get_price()
        if self.price != 0:
            self.area = Scraper(driver).get_area()
            self.room_count = Scraper(driver).get_room_count()
            self.title = Scraper(driver).get_title()
            self.location = Scraper(driver).get_location()
            self.year = Scraper(driver).get_year()
            self.market = Scraper(driver).get_market()
            self.floor = Scraper(driver).get_floor()
            self.floor_count = Scraper(driver).get_floor_count()
            self.addons = Scraper(driver).get_addons()
            self.seller = Scraper(driver).get_seller()
            self.seller_type = Scraper(driver).get_seller_type()

            print(f' ---> Title: {self.title} --- {self.market} ---> Price: {self.price} / {self.area} m2 '
                  f'/ {self.year} --{self.location} ')

        # self.addons = ':'.join([self.addons[i].text for i in range(len(self.addons))])
        # self.pic = self.soup.find('span', 'img-cover lazy')['data-src']

    def csv_object(self):
        columns = [self.price, self.area, self.room_count, self.year, self.location, self.url, self.title, self.seller,
                   self.addons, self.market, self.floor, self.floor_count, self.seller_type
                   ]
        return columns


class Sell(Offer):
    def __init__(self, url, driver):
        super().__init__(url, driver)
        self.price_m = Scraper(driver).get_price_per_meter()

    def csv_object(self):
        columns = super().csv_object()
        columns.insert(1, self.price_m)
        return columns


class Rent(Offer):
    def __init__(self, url, driver):
        super().__init__(url, driver)
        self.rent = Scraper(driver).get_rent()
        self.total = self.price + self.rent

    def csv_object(self):
        columns = super().csv_object()
        columns.insert(1, self.total)
        columns.insert(2, self.rent)
        return columns

