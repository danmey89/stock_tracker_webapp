from flask import (
    Blueprint, render_template, request, jsonify
)
from newsapi import NewsApiClient
from .constants import NEWS_API_KEY as api_key
import json

bp = Blueprint('news', __name__)

@bp.route('/news')
def news():

    CATEGORIES = {'Business': 'business', 'Entertainment': 'entertainment', 'Health': 'health',
                   'Science': 'science', 'Sports': 'sports', 'Technology': 'technology'}
    COUNTRIES = {'Germany': 'de', 'United States': 'us', 'France': 'fr', 'Canada': 'ca', 'Italy': 'it',
                  'Poland': 'pl', 'Belgium': 'be', 'India': 'in', 'Switzerland': 'ch',
                  'Turkey': 'tr', 'Ukraine': 'ua', 'United Kingdom': 'gb', 'Austria': 'at'}

    return render_template('news.html', categories=CATEGORIES, countries=COUNTRIES)



@bp.route('/get_news/<id>', methods=['GET', 'POST'])
def update(id, testing=True):

    params = id.split('&')

    q = params[0] if params[0] != '' else None
    category = params[1] if params[1] != '' else None
    country = params[2] if params[2] != '' else None

    if not testing:

        if request.method == 'GET':
            newsapi = NewsApiClient(api_key)
            top_headlines = newsapi.get_top_headlines(
                                            q = q,
                                            category = category,
                                            country = country
        )
    else:
        with open('newsdump.json', 'r') as f:
            top_headlines = json.loads(f.read())  

    return jsonify(top_headlines)