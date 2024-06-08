import json
import requests
import os
import sqlite3
import db

SYMBOLS = 'NVDA,NFLX,META,AAPL,GOOGL'

COLS = ('symbol', 'shortName', 'currency', 'regularMarketPrice', 'postMarketPrice', 'postMarketChange',
        'regularMarketChange', 'regularMarketDayHigh', 'regularMarketDayRange', 'regularMarketDayLow',
        'regularMarketVolume', 'regularMarketPreviousClose',  'regularMarketOpen', 'bid', 'ask',
        'averageDailyVolume3Month', 'averageDailyVolume10Day', 'fiftyDayAverage', 'fiftyDayAverageChange',
        'fiftyDayAverageChangePercent', 'marketCap', 'averageAnalystRating')


def get_quotes(symbol, api_key= os.getenv('YHFINANCE_API_KEY'), testing=True):
    if not testing:
        url = "https://yfapi.net/v6/finance/quote"

        querystring = {"symbols":symbol}
        headers = {'x-api-key': api_key}

        response = requests.request("GET", url, headers=headers, params=querystring)
        quotes = response.json()
        
    else:
        with open('../test1.json', 'r') as f:
            quotes = json.loads(f.read())
            

    return quotes



def insert_quote(symbols=SYMBOLS, testing=True):
    if not testing:
        quote = get_quotes(symbols, testing=False)['quoteResponse']['result']
        db = db.get_db()
    else: 
        quote = get_quotes(symbols)['quoteResponse']['result']
        db = sqlite3.connect('../instance/stonks.sqlite')

    for n in range(len(quote)):
        row = []
        for i in COLS:
            row.append(quote[n][i])
        row = tuple(row)
        print(row)    
        db.execute(
            'INSERT INTO quote'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            row,
        )
        db.commit()


