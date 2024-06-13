import json
import requests
import os
import sqlite3
from .db import get_db
import pandas as pd
from datetime import datetime, timedelta

SYMBOLS = 'NVDA,NFLX,META,AAPL,GOOGL'

COLS = ('symbol', 'shortName', 'currency', 'regularMarketPrice',
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
        db = get_db()
    else: 
        quote = get_quotes()['quoteResponse']['result']
        db = sqlite3.connect('../instance/stonks.sqlite')

    db.execute('DELETE FROM quote')
    db.commit()

    for n in range(len(quote)):
        row = []
        for i in COLS:
            row.append(quote[n][i])
        row = tuple(row)    
        db.execute(
            'INSERT INTO quote'
            ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            row,
        )
        db.commit()



def get_history(symbol=SYMBOLS, api_key= os.getenv('YHFINANCE_API_KEY'), testing=True):
    if not testing:
        url='https://yfapi.net/v8/finance/spark?interval=1d&range=1mo&'

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
        db = get_db()
    else:
        history = get_history()
        db = sqlite3.connect('instance/stonks.sqlite')

    
    newest = db.execute(
        'SELECT* FROM history ORDER BY idate DESC LIMIT 1;'
    ).fetchone()[0]
    
    newest = newest.strftime('%s')
    
    for sym in history:
        [int(str(k)[:-4]+'0000') for k in history[sym]['timestamp']]
    
    
    index = history['NFLX']['timestamp']

    columns = [k for k in history.keys()]
    columns.sort()
    columns.insert(0, 'date')

    df = pd.DataFrame(columns=columns, index=index)
    df['date'] = [datetime.fromtimestamp(k) for k in history['NFLX']['timestamp']]
    df['date'] = df['date'].dt.date
    
    for column in columns[1:]:    
        symbol = history[column]
        for i in range(len(symbol['timestamp'])):
            df_index = symbol['timestamp'][i]
            if df_index in index:
                df.loc[df_index, column] = symbol['close'][i]
    
    for i in range(len(df)):
        row = tuple(df.iloc[i])
        db.execute(
            'INSERT OR REPLACE INTO history'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            row,
        )
        db.commit()
