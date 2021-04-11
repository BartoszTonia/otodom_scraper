## ..:: Otodom scraper ::..


### Features
- scrapes basic offer information from Otodom.pl search page, then retrieve more information from offer page.
- creates csv file prepared for further analysis with Jupyter notebooks 
(see https://github.com/BartoszTonia/otodom_notebook.git)
- scraper temporary writes in `lib/temp.csv`, updates line by line and converts into file only after the last page of search will be reached. This allows us to resume scraper from any page if something suddenly break the connection.
- created database contains set of columns depended from 'rent' or 'sell' type of offer:

```
- Exclusively for sell:
price - main offer price
price_m - price per meter

- Exclusively for rent: 
total - owner rent price + additional rent price
price - main offer price - owner share 
rent - additional rent price - advance for media 

- Common columns:
id - offer identification number
area - apartment/house area 
room - count of rooms
year - year of construction
loc - offer location
url - short url
offer - offer title 
seller - seller 
addons - additional information about real estate
market - follows one of two options (1) - aftermarket, (2) - primary market
floor - current floor
floor_counts - floors count in the building
```
### Prerequisites :coffee:

You will need the following things properly installed on your machine.

* python3
* pip3
```
apt-get install python3-pip
```

### Installation :books:
1. Install all dependencies using 
```
 pip3 install -r requirements.txt 
```


### Run
First, prepare link - open https://www.otodom.pl, filter for city, region, market and many other option, then click "Wyszukaj"

Copy full link of Otodom search page and pass as `--url` argument. Add search label with `--label`
```
python3 main.py --url "https://www.otodom.pl/wynajem/mieszkanie/jelenia-gora/?search%5Bregion_id%5D=1&search%5Bsubregion_id%5D=58&search%5Bcity_
id%5D=182&search%5Bdist%5D=5&nrAdsPerPage=72" --label jelenia-gora-25km
```
or put simpler form in case of bigger cities or areas
```
python3 main.py -u https://www.otodom.pl/sprzedaz/mieszkanie/jelenia-gora/?nrAdsPerPage=72 -l jelenia-gora
python3 main.py -u https://www.otodom.pl/wynajem/mieszkanie/powiat-wroclawski/?nrAdsPerPage=72&page=2 -l powiat_wroc
```
