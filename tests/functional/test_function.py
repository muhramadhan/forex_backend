import json

# Test adding new daily rate when data is empty
def test_add_daily_rate_empty(test_client, init_database_empty):
    postdata=dict(
        date='2018-01-06',
        base='USD',
        to='IDR',
        rate=20000
    )
    response = test_client.post('/api/rate_data/add', data=postdata)
    res_data = json.loads(response.data)
    assert response.status_code == 200
    assert res_data['base'] == postdata['base']
    assert res_data['to'] == postdata['to']
    assert res_data['new_rate_data']['date'] == postdata['date']
    assert res_data['new_rate_data']['rate_value'] == postdata['rate']

# Test adding new daily rate when rate already exist
def test_add_daily_rate_exist(test_client, init_database_added_rate):
    postdata=dict(
        date='2018-01-06',
        base='USD',
        to='IDR',
        rate=20000
    )
    response = test_client.post('/api/rate_data/add', data=postdata)
    res_data = json.loads(response.data)
    assert response.status_code == 200
    assert res_data['base'] == postdata['base']
    assert res_data['to'] == postdata['to']
    assert res_data['new_rate_data']['date'] == postdata['date']
    assert res_data['new_rate_data']['rate_value'] == postdata['rate']

# Test get recent data but no data yet
def test_get_recent_rate_data_empty(test_client, init_database_empty):
    params=dict(
        base='USD',
        to='IDR'
    )
    response = test_client.get('/api/rate_data?base={}&to={}'.format(params['base'], params['to']))
    res_data = json.loads(response.data)
    assert response.status_code == 200
    assert res_data == {}

# Test get recent data of a rate
def test_get_recent_rate_data(test_client, init_database_added_rate_ratedata):

    params=dict(
        base='USD',
        to='IDR'
    )
    response = test_client.get('/api/rate_data?base={}&to={}'.format(params['base'], params['to']))
    res_data = json.loads(response.data)

    assert response.status_code == 200
    assert res_data['base'] == params['base']
    assert res_data['to'] == params['to']
    assert len(res_data['rate_data']) == 7
    assert res_data['rate_data'][0]['date'] == '2019-01-10'
    assert res_data['statistic']['average'] == 15000
    assert res_data['statistic']['variance'] == 0

# Add rate to track but data empty
def test_add_rate_to_track_empty(test_client, init_database_empty):
    postdata=dict(
        base='USD',
        to='IDR',
    )
    response = test_client.post('/api/track/add', data=postdata)
    res_data = json.loads(response.data)

    assert response.status_code == 200
    assert res_data['success'] == True

# Add rate to track rate already exist
def test_add_rate_to_track(test_client, init_database_added_rate):
    postdata=dict(
        base='USD',
        to='IDR',
    )
    response = test_client.post('/api/track/add', data=postdata)
    res_data = json.loads(response.data)
    assert response.status_code == 200
    assert res_data['success'] == True

# Re-add same rate to track should fail
def test_add_rate_to_track_already_tracked(test_client, init_database_added_track_rate_insufficient_data):
    postdata=dict(
        base='USD',
        to='IDR',
    )
    response = test_client.post('/api/track/add', data=postdata)
    res_data = json.loads(response.data)
    assert response.status_code == 200
    assert res_data['success'] == False

# Test tracked rate to have insufficient data
def test_track_rate_insufficient_data(test_client, init_database_added_track_rate_insufficient_data):
    params = dict(
        date='2019-01-10'
    )
    response = test_client.get('/api/track/{}'.format(params['date']))
    res_data = json.loads(response.data)
    print(res_data)
    assert response.status_code == 200
    assert res_data['success'] == True
    assert res_data['exchanges'][0]['rate'] == 'insufficient data'

# Test tracked rate to have sufficient data
def test_track_rate_sufficient_data(test_client, init_database_added_track_rate_sufficient_data):
    params = dict(
        date='2019-01-10'
    )
    response = test_client.get('/api/track/{}'.format(params['date']))
    res_data = json.loads(response.data)
    assert response.status_code == 200
    assert res_data['success'] == True
    assert len(res_data['exchanges'][0]['rate']) == 7
    assert res_data['exchanges'][0]['rate'][0]['rate_value'] == 15000
    assert res_data['exchanges'][0]['statistic']['average'] == 15000

# Test remove tracked rate fail cause empty
def test_delete_track_rate_empty(test_client, init_database_empty):
    postdata=dict(
        base='USD',
        to='IDR',
    )
    response = test_client.post('/api/track/delete', data=postdata)
    res_data = json.loads(response.data)

    assert response.status_code == 200
    assert res_data['success'] == False

# Test remove tracked rate success
def test_delete_track_rate_exist(test_client, init_database_added_track_rate_sufficient_data):
    postdata=dict(
        base='USD',
        to='IDR',
    )
    response = test_client.post('/api/track/delete', data=postdata)
    res_data = json.loads(response.data)

    assert response.status_code == 200
    assert res_data['success'] == True
