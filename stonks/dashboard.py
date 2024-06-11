from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from .db import get_db
import json
from datetime import date, timedelta

bp = Blueprint('dashboard', __name__)

@bp.route('/')
def index():
    db = get_db()

    quotes = db.execute(
        'SELECT * FROM quote;'
    ).fetchall()

    columns = db.execute(
        "SELECT c.name FROM pragma_table_info('quote') c;"
    ).fetchall()
    columns = [k[0] for k in columns]
    

    return render_template('/dashboard.html', quotes=quotes, columns=columns)



@bp.route('/get_data/<id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'GET':
        db = get_db()
        
        comp = id.split('&')[0]
        time = id.split('&')[1]

        date_off =date.today() - timedelta(days= float(time))
        

        data = db.execute(
        f'SELECT idate, {comp}  FROM history'
        f" WHERE idate > '{date_off}'"
        ).fetchall()

        history = []
        for i in data:
            object = {'date': i[0], 'close': i[1]}
            history.append(object)

        return jsonify(history)
    