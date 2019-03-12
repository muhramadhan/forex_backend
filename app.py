from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

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
            new_exchangerate.rate_data.append([new_exchangeratedata])
            db.session.add(new_exchangerate)
            db.session.add(new_exchangeratedata)
            exchangerate = new_exchangerate
        # If exchange rate already exist
        else:
            new_exchangeratedata = ExchangeRateData(date=datetime.
                                                    date(datetime.strptime
                                                         (date, '%Y-%m-%d')),
                                                    rate_value=rate)
            exchangerate.append([new_exchangeratedata])
            db.session.add(new_exchangeratedata)
        db.session.commit()
        return jsonify(exchangerate.serialize())
    except Exception as e:
        return(str(e))


@app.route("/api/rate_data")
def show_rate_data():
    base = request.args.get('base')
    to = request.args.get('to')
    try:
        exchangerate = ExchangeRate.query.filter_by(base=base,
                                                    to=to).first()
        ret_json = jsonify(exchangerate.serialize())
        ret_json['statistic'] = exchangerate.statistic(datetime.
                                                       date(datetime.now()))
        return ret_json
    except Exception as e:
        return (str(e))


@app.route("/api/track/<date_to_show>")
def show_track_rate(date_to_show):
    date = datetime.strptime(date_to_show, '%Y-%m-%d')
    try:
        tracked_rates = db.session.query(TrackRate).\
                                join(TrackRate.rate).\
                                join(ExchangeRate.rate_data).\
                                filter(ExchangeRateData.date == datetime.
                                       date(date))
        ret_json = []
        for tracked_rate in tracked_rates:
            json = tracked_rate.rate.serialize()
            if tracked_rate.rate.rate_data.count() < 7:
                json['rate']['rate_data'] = 'insufficient data'
            ret_json.append(json)
        return jsonify(ret_json)
    except Exception as e:
        return (str(e))


# TODO ADD RATE TO LIST
@app.route("/api/track/add", methods=['POST'])
def add_track_rate():
    base = request.form.get('base')
    to = request.form.get('to')
    try:
        exchangerate = ExchangeRate.query.filter(base=base, to=to).first()
        if exchangerate is None:
            exchangerate = ExchangeRate(base=base, to=to)
            db.session.add(exchangerate)
        new_trackrate = TrackRate(rate=[exchangerate])
        db.session.add(new_trackrate)
        db.session.commit()
        return jsonify(new_trackrate.serialize())
    except Exception as e:
        return (str(e))


# TODO DELETE RATE FROM LIST
@app.route("/api/track/delete", methods=['POST'])
def remove_track_rate():
    base = request.form.get('base')
    to = request.form.get('to')
    try:
        trackrate = db.session.query(TrackRate).join(TrackRate.rate).\
                    filter_by(ExchangeRate.base == base,
                              ExchangeRate.to == to).first()
        db.session.delete(trackrate)
        db.session.commit()
        return jsonify(trackrate.serialize())
    except Exception as e:
        return (str(e))


if __name__ == '__main__':
    app.run()
