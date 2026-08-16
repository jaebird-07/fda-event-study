import pandas as pd

df = pd.read_csv('data/event_prices.csv')
print(df['ticker'].value_counts())
