import pandas as pd

pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 1600)

df = pd.read_csv('lib/temp.csv')
print(df)
print(df.describe().round(2))