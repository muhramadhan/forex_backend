import pytest
from app import ExchangeRateData, TrackRate, ExchangeRate, app, db
from datetime import datetime


def conf_db(app):
    POSTGRES = {
        'user': 'postgres',
        'pw': 'postgres',
        'db': 'forex_test',
        'host': 'localhost',
        'port': '5432',
    }
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES


@pytest.fixture(scope='module')
def new_rate_data():
    test_date = [
        '2019-01-01', '2019-01-02', '2019-01-03', '2019-01-04', '2019-01-05',
        '2019-01-06', '2019-01-07', '2019-01-08', '2019-01-09', '2019-01-10'
    ]
    exchangeratedatas = []
    for date in test_date:
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        exchangeratedatas.append(ExchangeRateData(date=datetime.date(parsed_date), rate_value=15000))
    return exchangeratedatas

@pytest.fixture(scope='module')
def new_exchangerate():
    exchangerate = ExchangeRate(base='USD', to='IDR')
    return exchangerate

@pytest.fixture(scope='module')
def new_trackrate():
    trackrate = TrackRate(rate=[])
    return trackrate

@pytest.fixture(scope='function')
def test_client():
    flask_app = app
    flask_app.config['TESTING'] = True
    conf_db(flask_app)
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture(scope='function')
def init_database_empty(test_client):
    db.app = test_client
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function')
def init_database_added_rate(test_client):
    db.app = test_client
    db.create_all()

    exchangerate = ExchangeRate(base='USD', to='IDR')
    db.session.add(exchangerate)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function')
def init_database_added_rate_ratedata(test_client):
    db.app = test_client
    db.create_all()

    exchangerate = ExchangeRate(base='USD', to='IDR')
    test_date = [
        '2019-01-01', '2019-01-02', '2019-01-03', '2019-01-04', '2019-01-05',
        '2019-01-06', '2019-01-07', '2019-01-08', '2019-01-09', '2019-01-10'
    ]
    exchangeratedatas = []
    for date in test_date:
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        exchangeratedatas.append(ExchangeRateData(date=datetime.date(parsed_date), rate_value=15000))
    exchangerate.rate_data.extend(exchangeratedatas)
    db.session.add(exchangerate)
    db.session.bulk_save_objects(exchangeratedatas)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function')
def init_database_added_track_rate_insufficient_data(test_client):
    db.app = test_client
    db.create_all()

    exchangerate = ExchangeRate(base='USD', to='IDR')
    trackrate = TrackRate(rate=exchangerate)
    test_date = [
        '2019-01-06', '2019-01-07', '2019-01-08', '2019-01-09', '2019-01-10'
    ]
    exchangeratedatas = []
    for date in test_date:
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        exchangeratedatas.append(ExchangeRateData(date=datetime.date(parsed_date), rate_value=15000))
    exchangerate.rate_data.extend(exchangeratedatas)

    db.session.add(exchangerate)
    db.session.add(trackrate)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()

@pytest.fixture(scope='function')
def init_database_added_track_rate_sufficient_data(test_client):
    db.app = test_client
    db.create_all()

    exchangerate = ExchangeRate(base='USD', to='IDR')
    trackrate = TrackRate(rate=exchangerate)
    test_date = [
        '2019-01-01', '2019-01-02', '2019-01-03', '2019-01-04', '2019-01-05',
        '2019-01-06', '2019-01-07', '2019-01-08', '2019-01-09', '2019-01-10'
    ]
    exchangeratedatas = []
    for date in test_date:
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        exchangeratedatas.append(ExchangeRateData(date=datetime.date(parsed_date), rate_value=15000))
    exchangerate.rate_data.extend(exchangeratedatas)

    db.session.add(exchangerate)
    db.session.add(trackrate)
    db.session.commit()

    yield db

    db.session.remove()
    db.drop_all()
