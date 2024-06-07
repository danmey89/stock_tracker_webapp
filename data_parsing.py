import json
import pandas as pd


with open('test1.json', 'r') as f:
    d = json.loads(f.read())
    
quote = d['quoteResponse']['result']

cols = ['symbol', 'shortName', 'currency', 'regularMarketPrice', 'postMarketPrice', 'postMarketChange',
        'regularMarketChange', 'regularMarketDayHigh', 'regularMarketDayRange', 'regularMarketDayLow',
        'regularMarketVolume', 'regularMarketPreviousClose',  'regularMarketOpen', 'bid', 'ask',
        'averageDailyVolume3Month', 'averageDailyVolume10Day', 'fiftyDayAverage', 'fiftyDayAverageChange',
        'fiftyDayAverageChangePercent', 'marketCap', 'averageAnalystRating', ]

data = []

for n in range(len(quote)):
    row = []
    for i in cols:
        row.append(quote[n][i])
    data.append(row)

print(data)

df = pd.DataFrame(data, columns=cols)

print(df)
print(df.info())
