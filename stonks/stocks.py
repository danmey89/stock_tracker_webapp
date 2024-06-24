from flask import (
    Blueprint, render_template, request, jsonify
)
from .db import get_db
import json
from datetime import date, timedelta
from .data_parsing import insert_quote, insert_history
import os

bp = Blueprint('stocks', __name__)

@bp.route('/')
def index():
    db = get_db()

    last_update = os.path.join('stonks', 'last_download.txt')
    today = str(date.today())
    
    with open(last_update, 'r') as f:
        last_download = f.readline()
    
    if last_download != today:
        with open(last_update, 'w') as f:
            f.write(today)
        print('loading Data')
        
        insert_quote(testing=False)
        insert_history(testing=False)


    quotes = db.execute(
        'SELECT * FROM quote;'
    ).fetchall()

    columns = db.execute(
        "SELECT c.name FROM pragma_table_info('quote') c;"
    ).fetchall()
    columns = [k[0] for k in columns]
    

    return render_template('/stocks.html', quotes=quotes, columns=columns)



@bp.route('/get_data/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        db = get_db()
        
        comp = id.split('&')[0]
        time = id.split('&')[1]

        date_off =date.today() - timedelta(days= float(time))
        

        data = db.execute(
        f'SELECT idate, {comp}  FROM history'
        f" WHERE idate > '{date_off}';"
        ).fetchall()

        detail = db.execute(
            'SELECT * FROM quote'
            f" WHERE symbol = '{comp}';"
        ).fetchone()

        columns = db.execute(
        "SELECT c.name FROM pragma_table_info('quote') c;"
        ).fetchall()
        columns = [k[0] for k in columns]

        detail = [k for k in detail]
        columns = [k for k in columns]
        data = [k for k in data]

        detail_data = {}

        for i in range(len(detail)):
            detail_data.update( {columns[i]: detail[i]})

        history = []

        for i in data:
            if i[1] != None:
                object = {'date': i[0].strftime('%Y-%m-%d'), 'close': i[1]}
                history.append(object)
        
        detail_data.update( {'history': history} )

        return jsonify(detail_data)
