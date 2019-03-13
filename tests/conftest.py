import pytest
from app import ExchangeRateData, TrackRate, ExchangeRate
from datetime import datetime


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
