import json
import requests
import os
import sqlite3
import db
import pandas as pd
from datetime import datetime, timedelta

SYMBOLS = 'NVDA,NFLX,META,AAPL,GOOGL'

COLS = ('symbol', 'shortName', 'currency', 'regularMarketPrice', 'postMarketPrice', 'postMarketChange',
        'regularMarketChange', 'regularMarketDayHigh', 'regularMarketDayRange', 'regularMarketDayLow',
        'regularMarketVolume', 'regularMarketPreviousClose',  'regularMarketOpen', 'bid', 'ask',
        'averageDailyVolume3Month', 'averageDailyVolume10Day', 'fiftyDayAverage', 'fiftyDayAverageChange',
        'fiftyDayAverageChangePercent', 'marketCap', 'averageAnalystRating')


def get_quotes(symbol=SYMBOLS, api_key= os.getenv('YHFINANCE_API_KEY'), testing=True):
    if not testing:
        url = "https://yfapi.net/v6/finance/quote"

        querystring = {"symbols":symbol}
        headers = {'x-api-key': api_key}

        response = requests.request("GET", url, headers=headers, params=querystring)
        quotes = response.json()
        
    else:
        with open('test1.json', 'r') as f:
            quotes = json.loads(f.read())
            

    return quotes



def insert_quote(symbols=SYMBOLS, testing=True):
    if not testing:
        quote = get_quotes(symbols, testing=False)['quoteResponse']['result']
        db = db.get_db()
    else: 
        quote = get_quotes()['quoteResponse']['result']
        db = sqlite3.connect('../instance/stonks.sqlite')

    for n in range(len(quote)):
        row = []
        for i in COLS:
            row.append(quote[n][i])
        row = tuple(row)    
        db.execute(
            'INSERT INTO quote'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            row,
        )
        db.commit()



def get_history(symbol=SYMBOLS, api_key= os.getenv('YHFINANCE_API_KEY'), testing=True):
    if not testing:
        url='https://yfapi.net/v8/finance/spark?interval=1d&range=1y&'

        querystring = {"symbols":symbol}
        headers = {'x-api-key': api_key}

        response = requests.request("GET", url, headers=headers, params=querystring)
        hist = response.json()
        
    else:
        with open('test2.json', 'r') as f:
            hist = json.loads(f.read())
            

    return hist


def insert_history(symbols=SYMBOLS, testing=True):
    if not testing:
        history = get_history(symbols, testing=False)
        db = db.get_db()
    else:
        history = get_history()
        db = sqlite3.connect('instance/stonks.sqlite')

    try:
        newest = db.execute(
            'SELECT* FROM history ORDER BY idate DESC LIMIT 1;'
        ).fetchone()[0]
    except sqlite3.InterfaceError:
        newest = '2000-01-01'

    newest = datetime.strptime(newest, "%Y-%m-%d") + timedelta(hours=20)

    index = []
    for h in history['NFLX']['timestamp']:
        if pd.to_datetime(h, unit='s') > newest:
            index.append(h)
    

    columns = [k for k in history.keys()]
    columns.sort()
    columns.insert(0, 'date')

    df = pd.DataFrame(columns=columns, index=index)
    df['date'] = index
    df['date'] = pd.to_datetime(df['date'], unit='s')
    df['date'] = df['date'].dt.date
    
    for column in columns[1:]:    
        symbol = history[column]
        for i in range(len(symbol['timestamp'])):
            df_index = symbol['timestamp'][i]
            if df_index in index:
                df.loc[df_index, column] = symbol['close'][i]
    print(df)
    for i in range(len(df)):
        row = tuple(df.iloc[i])
        db.execute(
            'INSERT INTO history'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            row,
        )
        db.commit()

