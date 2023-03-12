from lib.run_driver import run_driver
from pathlib import Path
import pandas as pd
import re


class Query:
    def __init__(self, url):
        self.page_limit = 40
        self.url = url
        self.url, self.page = self.parse_url_page()

    def parse_url_page(self):
        if '?' in self.url:
            url = re.sub(r'&page=\d*', '', self.url)
            if '&page=' in self.url:
                page_number = re.findall(r'(?<=&page=)\d*', self.url)
                return url, int(page_number[0])
            else:
                return self.url, 1
        else:
            return f'{self.url}?limit=72', 1

    def create_search_page_list(self):
        url, page = self.url, self.page
        search_page_list = [url.strip(' ') + f'&page={i}' for i in range(page, self.page_limit + 1)]
        return search_page_list


class ProcessSearchPage:
    def __init__(self, url):
        self.driver = run_driver(url)
        self.page_source = self.driver.page_source
        self.driver.quit()

    def extract_ids(self):
        pattern = re.compile(r'"slug":"[^"]*-(?P<id>ID\w{5})",')
        # pattern = r'"slug":".*?(ID\w+)"'  # regex pattern to match the IDs
        matches = pattern.finditer(self.page_source)
        ids = []
        for match in matches:
            ids.append(match.group('id'))
        print(ids)
        unique_ids = list(set(ids))
        print(len(ids), len(unique_ids))
        return unique_ids


class ProcessOffer:
    MAX_ATTEMPTS = 5

    def __init__(self, url):
        self.url = url

    def scrape_offer(self, scraper):
        with run_driver(self.url) as driver:
            offer = scraper(self.url, driver)
            if offer.price == 0:
                print(' --- > no price')
                pass
            else:
                line = offer.csv_object()
                return line


def check_duplicates(id, temp_path):
    df = pd.read_csv(temp_path, encoding="utf-8")
    print(f'*** {id} ***', end='')
    if id in df['id'].values:
        print(f' duplicate')
        return False
    else:
        return True


def write_and_clean(temp_path, output_csv_path):
    df = pd.read_csv(temp_path, encoding="utf-8")
    try:
        df.to_csv(output_csv_path, index=False)
        print('File was successfully created -- {}'.format(output_csv_path))
    except ValueError:
        pass

    if Path(output_csv_path).exists():
        temp_path.unlink()
