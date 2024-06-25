from flask import (
    Blueprint, render_template, jsonify
)
from .constants import NEWS_API_KEY as api_key
import json
import requests

bp = Blueprint('news', __name__)

@bp.route('/news/')
def news():

    CATEGORIES = {'Business': 'business', 'Entertainment': 'entertainment', 'Health': 'health',
                   'Science': 'science', 'Sports': 'sports', 'Technology': 'technology'}
    COUNTRIES = {'Germany': 'de', 'United States': 'us', 'France': 'fr', 'Canada': 'ca', 'Italy': 'it',
                  'Poland': 'pl', 'Belgium': 'be', 'India': 'in', 'Switzerland': 'ch',
                  'Turkey': 'tr', 'Ukraine': 'ua', 'United Kingdom': 'gb', 'Austria': 'at'}

    return render_template('news.html', categories=CATEGORIES, countries=dict(sorted(COUNTRIES.items())))



@bp.route('/get_news/<id>', methods=['GET', 'POST'])
def update(id, testing=False):

    params = id.split('&')

    if not testing:

        key = api_key

        keywords = params[0]
        country = params[1]
        category = params[2]

        if keywords != '':
            param_0 = 'q=' + keywords + '&'
        else:
            param_0 = keywords

        if country != "":
            param_1 = 'country=' + country + '&'
        else:
            param_1 = country

        if category != "":
            param_2 = 'category=' + category + '&'
        else:
            param_2 = category

        url = f'https://newsapi.org/v2/top-headlines?{param_0}{param_1}{param_2}apiKey={key}'

        news = requests.get(url)
        news = news.json()


    else:
        with open('newsdump.json', 'r') as f:
            news = json.loads(f.read())  

    return jsonify(news)

#TODO link from stocks details to news of company 