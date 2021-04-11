from datetime import datetime
from time import sleep, time
from pathlib import Path
from csv import writer
from bs4 import BeautifulSoup
import pandas as pd
import requests
import argparse
import re

# Change saved values below. Pass the base url and label for data maintenance.
quick_url = 'https://www.otodom.pl/wynajem/mieszkanie/powiat-wroclawski/?nrAdsPerPage=72'

csv_headers_rent = 'id,total,price,rent,area,room,year,loc,url,offer,seller,addons,market,floor,floor_count'
csv_headers_sell = 'id,price,price_m,area,room,year,loc,url,offer,seller,addons,market,floor,floor_count'

Path('out').mkdir(parents=True, exist_ok=True)
temp_path = Path('lib/temp.csv')
temp_path.parent.mkdir(parents=True, exist_ok=True)


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.content, 'html.parser')


soup = get_soup(quick_url)


class Soup:
    def __init__(self, soup):
        self.soup = soup
        self.full_url = self.soup.find('a', href=True)['href']
        self.id = re.findall('(ID.*)(?:.html)', self.full_url)[0]
        self.url = 'https://www.otodom.pl/pl/oferta/' + self.id
        self.detail_soup = self.get_detail_soup()

    def get_detail_soup(self):
        response = requests.get(self.url)
        return BeautifulSoup(response.content, 'html.parser')


class OfferModel(Soup):
    def __init__(self, soup):
        super().__init__(soup)
        self.price = self.get_price('li', 'offer-item-price')
        self.area = self.get_area()
        self.seller = self.get_seller()
        self.room = self.soup.find('li', 'offer-item-rooms hidden-xs').text.split(' ')[0]
        self.pic = self.soup.find('span', 'img-cover lazy')['data-src']
        self.offer = self.soup.find('span', 'offer-item-title').text
        self.loc = self.get_loc()
        self.year = self.get_year()
        self.market = self.get_market()
        self.floor = self.get_floor()
        self.floor_count = self.get_floor_count()
        self.addons = self.detail_soup.find_all('li', 'css-1r5xhnu e9d1vc81')
        self.addons = ':'.join([self.addons[i].text for i in range(len(self.addons))])

    def get_market(self):
        if 'pierwotny' in str(self.detail_soup.find_all('div', 'css-18h1kfv ecjfvbm3')):
            return 1
        else:
            return 0

    def get_floor_count(self):
        floor_count = self.detail_soup.find('div', {'aria-label': 'Liczba pięter'})
        if floor_count:
            return int(floor_count.find('div', 'css-1ytkscc ecjfvbm0')['title'])
        else:
            return 0

    def get_floor(self):
        floor = self.detail_soup.find('div', {'aria-label': 'Piętro'})
        if floor:
            return floor.find('div', 'css-1ytkscc ecjfvbm0')['title']
        else:
            return 0

    def get_loc(self):
        try:
            return self.detail_soup.find('a', 'css-1qz7z11 eom7om61').text
        except AttributeError:
            return 0

    def get_year(self):
        year = self.detail_soup.find('div', {'aria-label': 'Rok budowy'})
        if year:
            return int(year.find('div', 'css-1ytkscc ecjfvbm0')['title'])
        else:
            return 0

    def get_price(self, select_1, select_2):
        try:
            price = self.soup.find(select_1, select_2).text
            price = re.findall(r'(\d+\s*\d+\s*\d+\s*)', price)
            price = re.sub(r'\s', '', price[0])
            return int(price)
        except (AttributeError, IndexError):
            return 'ask for price'

    def get_seller(self):
        seller = self.soup.find('li', 'pull-right').text
        seller = re.findall(r'(\w+\s*\w+)', seller)
        return seller[0]

    def get_area(self):
        try:
            area = self.soup.find('strong', 'visible-xs-block').text
            area = re.findall(r'(.*)(?:\sm²)', area)
            area = re.sub(r',', '.', area[0])
            return float(area)
        except ValueError:
            print("value err")
            return 0


class Sell(OfferModel):
    def __init__(self, soup):
        super().__init__(soup)
        self.price_m = self.get_price('li', 'hidden-xs offer-item-price-per-m')

    def csv_object(self):
        columns = (self.id, self.price, self.price_m, self.area, self.room, self.year,
                   self.loc, self.url, self.offer, self.seller, self.addons, self.market,
                   self.floor, self.floor_count)
        return columns


class Rent(OfferModel):
    def __init__(self, soup):
        super().__init__(soup)
        self.rent = self.get_rent()
        self.total = self.price + self.rent

    def get_rent(self):
        rent = self.detail_soup.find('div', {'aria-label': 'Czynsz - dodatkowo'})
        if rent:
            rent = rent.find('div', 'css-1ytkscc ecjfvbm0')['title'].rstrip(' zł')
            rent = rent.replace(' ', '').replace(',', '')
            return float(rent)
        else:
            return 0

    def csv_object(self):
        columns = (self.id, self.total, self.price, self.rent, self.area, self.room,
                   self.year, self.loc, self.url, self.offer, self.seller, self.addons, self.market,
                   self.floor, self.floor_count)
        return columns


class Process:
    def __init__(self, url_site, query='test'):
        self.url_site = url_site
        self.query = query
        self.total = 0
        self.pagination()

    def pagination(self):
        url, page = self.validate_page()
        while True:
            try:
                url_page = url.strip(' ') + '&page=' + str(page)
                print(url_page, end=' ')

                if page > 1 and url_page != requests.get(url_page).url:
                    raise KeyError
                else:
                    self.scrape_page(url_page)
                    page += 1

            except KeyError:
                print('Checked ' + str(page - 1) + ' pages.')
                break

    def validate_page(self):
        if '?' in self.url_site:
            url = re.sub(r'&page=\d*', '', self.url_site)
            if '&page=' in self.url_site:
                page_number = re.findall(r'(?<=&page=)\d*', self.url_site)
                return url, int(page_number[0])
            else:
                return url, 1
        else:
            return self.url_site + '?search', 1

    def scrape_page(self, url_page):
        search_url = requests.get(url_page)
        main_soup = BeautifulSoup(search_url.content, 'html.parser')
        self.iterate_search_results(main_soup.select('article.offer-item'), url_page)

    def iterate_search_results(self, soup_select, url):
        page_total = len(soup_select)
        print(str(page_total), 'listings found')
        print('+')
        if page_total == 0:
            raise KeyError
        else:
            self.total += page_total
        i = count = 0
        while i < len(soup_select):
            duplicates = pd.read_csv(temp_path, encoding='utf-8', usecols=['id'])
            offer = soup_select[i]
            soup = BeautifulSoup(str(offer), 'html.parser')
            offer_id = Soup(soup).id

            # if offer.id in duplicates.index.values:
            if offer_id in duplicates['id'].values:
                print('> duplicate')
                count += 1
                i += 1
            else:
                sleep(0.8)
                if 'wynajem' in url:
                    offer = Rent(soup)
                elif 'sprzedaz' in url:
                    offer = Sell(soup)
                else:
                    offer = None

                row = offer.csv_object()
                print(row[0:9])

                with temp_path.open('a', newline='', encoding='utf-8') as temp:
                    csv_writer = writer(temp)
                    csv_writer.writerow(row)
                i += 1

        print('\n --> ' + str(count) + ' duplicates ' + str(page_total - count) + ' new offers ')


def create_db( df, location ):
    try:
        df.to_csv(location, index=False)
        print('File was successfully created -- {}'.format(location))
    except ValueError:
        pass


def write_and_clean(loc):
    df = pd.read_csv(temp_path, encoding="utf-8")
    create_db(df, loc)
    if Path(loc).exists():
        temp_path.unlink()


def main():
    try:
        t = time()
        timestamp = datetime.fromtimestamp(t).strftime('_%Y%m%d_%H_%M_%S')
        url, label = args_parser()
        search_type = ''

        csv_headers = ''
        if 'wynajem' in url:
            csv_headers = csv_headers_rent
            search_type = 'rent'
        elif 'sprzedaz' in url:
            search_type = 'sell'
            csv_headers = csv_headers_sell
        else:
            print('wrong_url')
            exit()

        if not temp_path.exists():
            temp_path.touch()
            temp_path.write_text(csv_headers + '\n')

        Process(url)

        loc = 'out/{}_{}_total{}.csv'.format(search_type, label, timestamp)
        write_and_clean(loc)

    except TypeError:
        print('\n')
        pass
    except KeyboardInterrupt:
        print(' [+] Keyboard Interrupt. Closing program.')
        exit()


def args_parser():
    description = "Scrape engine creating cvs files for further machine learning analysis"
    url_h = "Paste your url"

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-u', '--url', dest="url", type=str, help=url_h)
    parser.add_argument('-l', '--label', dest="label", type=str, help=url_h)

    args = parser.parse_args()
    url = str(args.url)
    label = str(args.label)

    if args.url is None:
        url = quick_url

    if args.label is None:
        label = 'label'

    return url, label


main()
