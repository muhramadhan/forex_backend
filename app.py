from flask import Flask, request, jsonify, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'forex',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)

from models import TrackRate, ExchangeRate, ExchangeRateData


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/api/rate_data/add", methods=['POST'])
def add_rate_data():
    date = request.form.get('date')
    base = request.form.get('base')
    to = request.form.get('to')
    rate = request.form.get('rate')

    try:
        exchangerate = ExchangeRate.query.filter_by(base=base,  to=to).first()
        # If exchange rate doesn't exist
        if exchangerate is None:
            new_exchangeratedata = ExchangeRateData(date=datetime.date
                                                    (datetime.strptime(date,
                                                     '%Y-%m-%d')),
                                                    rate_value=rate)
            new_exchangerate = ExchangeRate(base=base, to=to)
            new_exchangerate.rate_data.append(new_exchangeratedata)
            db.session.add(new_exchangerate)
            db.session.add(new_exchangeratedata)
            exchangerate = new_exchangerate
        # If exchange rate already exist
        else:
            new_exchangeratedata = ExchangeRateData(date=datetime.
                                                    date(datetime.strptime
                                                         (date, '%Y-%m-%d')),
                                                    rate_value=rate)
            exchangerate.rate_data.append(new_exchangeratedata)
            db.session.add(new_exchangeratedata)
        db.session.commit()
        ret_json = exchangerate.serialize()
        ret_json['new_rate_data'] = new_exchangeratedata.serialize()
        return jsonify(ret_json)
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)})


@app.route("/api/rate_data", methods=['GET'])
def show_rate_data():
    base = request.args.get('base')
    to = request.args.get('to')
    try:
        exchangerate = ExchangeRate.query.filter_by(base=base,
                                                    to=to).first()
        if exchangerate is None:
            return jsonify({})
        else:
            exchangeratedatas = exchangerate.rate_data.limit(7)
            ret_json = exchangerate.serialize()
            # recent data so max allowerd year
            ret_json['statistic'] = exchangerate.statistic(datetime.
                                                           date(datetime.max))
            ret_json['rate_data'] = [e.serialize() for e in exchangeratedatas]
            return jsonify(ret_json)
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)})


@app.route("/api/track/<date_to_show>", methods=['GET'])
def show_track_rate(date_to_show):
    date = datetime.strptime(date_to_show, '%Y-%m-%d')
    try:
        tracked_rates = db.session.query(TrackRate)
        ret_json = dict()
        for tracked_rate in tracked_rates:
            rate_datas = [e for e in tracked_rate.rate.rate_data if e.date <= datetime.date(date)]
            json = tracked_rate.rate.serialize()
            if len(rate_datas) < 7:
                json['rate'] = 'insufficient data'
            else:
                json['rate'] = [e.serialize() for e in rate_datas[0:7]]
                json['statistic'] = tracked_rate.rate.statistic(datetime.date(date))
            ret_json['exchanges'] = [json]
            ret_json['success'] = True
        return jsonify(ret_json)
    except Exception as e:
        return jsonify({'success': False, 'message': e.orig.args})


@app.route("/api/track/add", methods=['POST'])
def add_track_rate():
    base = request.form.get('base')
    to = request.form.get('to')
    try:
        exchangerate = ExchangeRate.query.filter_by(base=base, to=to).first()
        if exchangerate is None:
            exchangerate = ExchangeRate(base=base, to=to)
            db.session.add(exchangerate)
        new_trackrate = TrackRate(rate=exchangerate)
        db.session.add(new_trackrate)
        db.session.commit()
        ret_json = new_trackrate.serialize()
        ret_json['success'] = True
        return jsonify(ret_json)
    except Exception as e:
        return jsonify({'success': False, 'message': e.orig.args})


@app.route("/api/track/delete", methods=['POST'])
def remove_track_rate():
    base = request.form.get('base')
    to = request.form.get('to')
    try:
        trackrate = db.session.query(TrackRate).join(TrackRate.rate).\
                    filter(ExchangeRate.base == base,
                           ExchangeRate.to == to).first()
        if trackrate is not None:
            db.session.delete(trackrate)
            ret_json = trackrate.serialize()
            ret_json['success'] = True
            db.session.commit()
            return jsonify(ret_json)
        else:
            raise ValueError('Data not found')
    except ValueError as e:
        print(e)
        return jsonify({'success': False, 'message': str(e)})
    except Exception as e:
        return jsonify({'success': False, 'message': e.orig.args})


if __name__ == '__main__':
    app.run()
