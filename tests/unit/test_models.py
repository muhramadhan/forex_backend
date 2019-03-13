import datetime

def test_new_rate_data(new_rate_data):
    rate_data = new_rate_data[0]
    assert type(rate_data.date) is datetime.date
    assert rate_data.rate_value == 15000

def test_new_rate(new_exchangerate, new_rate_data):
    new_exchangerate.rate_data.extend(new_rate_data)
    assert new_exchangerate.base == 'USD'
    assert new_exchangerate.to == 'IDR'
    assert new_exchangerate.rate_data.count() > 0

def test_new_trackrate(new_exchangerate, new_trackrate,):
    new_trackrate.rate.append(new_exchangerate)
    assert len(new_trackrate.rate) == 1

# def test_statistic_method(new_exchangerate, new_rate_data):
#     new_exchangerate.rate_data.extend(new_rate_data)
#     statistic = new_exchangerate.statistic(datetime.datetime(2019, 1, 10)).date()
#     assert statistic['variance'] == 0
#     assert statistic['average'] == 15000
