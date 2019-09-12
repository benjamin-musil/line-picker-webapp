import os
import requests



def test_get_wait_by_restaurant():
    os.environ['NO_PROXY'] = '127.0.0.1'
    params = {
        "Restaurant Name": "Taco Bell",
        "Address": "212 Taco Street"
    }
    result = requests.get('http://127.0.0.1:5000/getwait/byrestaurant', params=params)
    expected_result = "Taco Bell has a wait time of 10 minutes reported at 2019-08-26 10:39:39.632863"
    assert result.json() == expected_result


def test_get_restaurant_by_category():
    os.environ['NO_PROXY'] = '127.0.0.1'
    category = 'Tacos'
    result = requests.get(f'http://127.0.0.1:5000/category/{category}')
    one_restaurant = '{\'address\': \'212 Taco Street\', \'category\': \'Tacos\', \'id\': ' \
                     '\'5d63fbb41c9d440000acf1b4\', \'name\': \'Taco Bell\', \'wait_times\': \'Unknown\'}'
    assert one_restaurant in str(result.json())


if __name__ == '__main__':
    test_get_wait_by_restaurant()
    test_get_restaurant_by_category()
