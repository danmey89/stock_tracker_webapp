import os
import requests
import json



def get_stocks(symbol, api_key= os.getenv('YHFINANCE_API_KEY')):
    url = "https://yfapi.net/v6/finance/quote"

    querystring = {"symbols":symbol}

    headers = {'x-api-key': api_key}

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    return data


with open('test1.json', 'w') as f:
    json.dump(get_stocks('NVDA,NFLX,META,AAPL,GOOGL'), f)

