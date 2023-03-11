from process import Query, ProcessSearchPage, ProcessOffer, write_and_clean, check_duplicates
from offer_model import Rent, Sell
from pathlib import Path
from csv import writer
import argparse

# Change saved values below. Pass the base url and label for data maintenance.
quick_url = 'https://www.otodom.pl/pl/oferty/sprzedaz/mieszkanie/wroclaw?limit=72'

csv_headers_rent = 'id,price,total,rent,area,room,year,loc,url,offer,seller,addons,market,floor,floor_count,seller_type'
csv_headers_sell = 'id,price,price_m,area,room,year,loc,url,offer,seller,addons,market,floor,floor_count,seller_type'

Path('out').mkdir(parents=True, exist_ok=True)
temp_path = Path('lib/temp.csv')
temp_path.parent.mkdir(parents=True, exist_ok=True)


def main():
    try:
        url, label = args_parser()
        csv_headers = csv_headers_rent if 'wynajem' in url else csv_headers_sell if 'sprzedaz' in url else ''
        search_type = Rent if 'wynajem' in url else Sell if 'sprzedaz' in url else None
        if search_type is None:
            print('> wrong url')
            exit()

        if not temp_path.exists():
            temp_path.touch()
            temp_path.write_text(f"{csv_headers}\n")

        output_csv_path = f'out/{search_type}_{label}.csv'

        search_pages = Query(url).create_search_page_list()
        for page in search_pages:
            id_list = ProcessSearchPage(page).extract_ids()
            for id in id_list:
                url = f'https://www.otodom.pl/pl/oferta/{id}'
                if_not_scrapped = check_duplicates(id, temp_path)
                if if_not_scrapped:
                    row = ProcessOffer(url).scrape_offer(search_type)
                    if row:
                        row.insert(0, id)
                        with temp_path.open('a', newline='', encoding='utf-8') as temp:
                            csv_writer = writer(temp)
                            csv_writer.writerow(row)

        write_and_clean(temp_path, output_csv_path)

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


if __name__ == '__main__':
    main()
