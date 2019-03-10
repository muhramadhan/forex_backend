from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

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

if __name__ == '__main__':
    app.run()
