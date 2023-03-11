## Otodom Web Scraper 


This tool allows you to scrape from Otodom.pl offer pages. 

It creates a CSV file prepared for further analysis with Jupyter notebooks, 
which can be found at [BartoszTonia/otodom_notebook](https://github.com/BartoszTonia/otodom_notebook).

The scraper temporarily writes to lib/temp.csv, 
updating line by line and converting it into a file only after the last page of the search is reached. 
This allows you to resume the scraper from any page if the connection is lost.


### Features
The created database contains a set of columns dependent on the "rent" or "sell" type of offer:
```
For "sell" offers:
price - main offer price
price_m - price per meter

For "rent" offers: 
total - owner rent price + additional rent price
price - main offer price - owner share 
rent - additional rent price - advance for media 

Common columns:
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
### Prerequisites

You will need the following things properly installed on your machine.

* Python 3.x
* Selenium
* Pandas
```
apt-get install python3-pip
```

### Installation 
1. Install all dependencies using 
```
 pip3 install -r requirements.txt 
```
2. Install Chrome driver that corresponds to your Chrome version. The driver can be downloaded from [here](https://chromedriver.chromium.org/downloads).

### Run

First, prepare a link by opening https://www.otodom.pl, filtering for city, region, market and many other options, then click "Wyszukaj".

Copy the full link of the Otodom search page and pass it as the `--url` argument. Add a search label with `--label`.

For example, to scrape offers for renting apartments in Jelenia Gora:
```
$ python3 main.py --url "https://www.otodom.pl/wynajem/mieszkanie/jelenia-gora/?search%5Bregion_id%5D=1&search%5Bsubregion_id%5D=58&search%5Bcity_
id%5D=182&search%5Bdist%5D=5&nrAdsPerPage=72" --label jelenia-gora-25km

$ python3 main.py -u https://www.otodom.pl/sprzedaz/mieszkanie/jelenia-gora/?nrAdsPerPage=72 -l jelenia-gora

$ python3 main.py -u https://www.otodom.pl/wynajem/mieszkanie/powiat-wroclawski/?nrAdsPerPage=72&page=2 -l powiat_wroc
```
