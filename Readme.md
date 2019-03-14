# Forex Backend API

Backend API to be used in frontend

## Installation

Dillinger requires [Node.js](https://nodejs.org/) v4+ to run.

Change directory to the root of the project.
Then execute command below
```sh
$ sudo docker-compuse up --build
```

## Database Documentation
Relational Schema
![Relational Schema](https://i.imgur.com/Yv5WSsJ.png)

TrackRate -> ExchangeRate is one to one relation
ExchangeRateData -> ExchangeRate is many to one relation

* ExchangeRateData has responsibility to store daily rate data
* ExchangeRate has responsibility to store saved exchange rate like USD to IDR
* TrackRate has responsibility to store the tracked exchange rate.
  I was considering to just make a boolean table in exchangerate for knowing tracked rate. TrackRate table helps,
  if wanted to expand the feature using many users as association table between exchangerate table and user table.
## API Documentation
* ### Adding new rate data
    ```sh
    $(localhost):5000/api/rate_data/add
    ```
    Method: POST
    * date = *string | 'YYYY-MM-DD'*
    * base = *string | exchange rate from*
    * to = *string | exchange rate to*
    * rate = *number | exchange rate value*
        Example:
        date = 2019-01-01
        base = USD
        to = IDR
        rate = 14000

    Return:
    ```json
    {
    "base": "IDR",
    "id": 3,
    "new_rate_data": {
        "date": "2018-01-05",
        "id": 16,
        "rate_value": 50000
    },
    "to": "USD",
    "success": true
    }
    ```   
    Return error:
    ```json
    {
    "success": false,
    "message": "error message"
    }
    ```

* ### Display recent exchange rate
    ```sh
    $(localhost):5000/api/rate_data&{base}&{to}
    ```
    Method: GET
    * base = *string | exchange rate from*
    * to = *string | exchange rate to*
        Example:
        /api/rate_data?base=USD&to=IDR

    Return:
    ```json
    {
        "base": "USD",
        "id": 1,
        "rate_data": [
            {
                "date": "2018-01-05",
                "id": 1,
                "rate_value": 20000
            }
        ],
        "statistic": {
            "average": 20000,
            "variance": 0
        },
        "to": "IDR"
    }
    ```   
    Return error:
    ```json
    {
    "success": false,
    "message": "error message"
    }
    ```

* ### Adding new exchange rate to track
    ```sh
    $(localhost):5000/api/track/add
    ```
    Method: POST
    * base = *string | exchange rate from*
    * to = *string | exchange rate to*
        Example:
        base = USD
        to = IDR

    Return:
    ```json
    {
        "id": 6,
        "rate": {
            "base": "USD",
            "id": 1,
            "to": "IDR"
        },
        "success": true
    }
    ```   
    Return error:
    ```json
    {
    "success": false,
    "message": "error message"
    }
    ```

* ### Remove tracked exchange rate
    ```sh
    $(localhost):5000/api/track/add
    ```
    Method: POST
    * base = *string | exchange rate from*
    * to = *string | exchange rate to*
        Example:
        base = USD
        to = IDR

    Return:
    ```json
    {
        "id": 6,
        "rate": {
            "base": "USD",
            "id": 1,
            "to": "IDR"
        },
        "success": true
    }
    ```   
    Return error:
    ```json
    {
    "success": false,
    "message": "error message"
    }
    ```

* ### Display list of tracked exchange rate
    ```sh
    $(localhost):5000/api/track/<date>
    ```
    Method: GET
    * date = *string | exchange rate from*
        Example:
        /api/track/2019-01-10

    Return:
    ```json
    {
        "exchanges": [
            {
                "base": "USD",
                "id": 1,
                "rate": "insufficient data",
                "to": "IDR"
            },
            {
                "base": "IDR",
                "id": 3,
                "rate": [
                    {
                        "date": "2019-01-07",
                        "id": 24,
                        "rate_value": 50000
                    },
                    {
                        "date": "2019-01-07",
                        "id": 23,
                        "rate_value": 50000
                    },
                    {
                        "date": "2019-01-06",
                        "id": 22,
                        "rate_value": 50000
                    },
                    {
                        "date": "2019-01-05",
                        "id": 21,
                        "rate_value": 50000
                    },
                    {
                        "date": "2019-01-04",
                        "id": 20,
                        "rate_value": 50000
                    },
                    {
                        "date": "2019-01-03",
                        "id": 19,
                        "rate_value": 50000
                    },
                    {
                        "date": "2019-01-02",
                        "id": 18,
                        "rate_value": 50000
                    }
                ],
                "statistic": {
                    "average": 50000,
                    "variance": 0
                },
                "to": "USD"
            }
        ],
        "success": true
    }
    ```
    When the rate data doesn't reach 7 it will return insufficient data.

    Return error:
    ```json
    {
    "success": false,
    "message": "error message"
    }
    ```
