import requests
import os


def test_get_wait_by_restaurant():
    os.environ['NO_PROXY'] = '127.0.0.1'
    params = {
        "Restaurant Name": "Taco Bell",
        "Address": "212 Taco Street"
    }
    result = requests.get('http://127.0.0.1:5000/getwait/byrestaurant', params=params)
    expected_result = "Taco Bell has a wait time of 10 minutes reported at 2019-08-26 10:39:39.632863"
    assert (result.json() == expected_result)


test_get_wait_by_restaurant()