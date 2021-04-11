import pandas as pd

pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 1600)

# This file is just prepared to take a look at shape of data
# while scraper is working

df = pd.read_csv('lib/temp.csv')
print(df)
print(df.describe().round(2))

# Run ready file with Jupyter Notebook
# https://github.com/BartoszTonia/otodom_notebook

