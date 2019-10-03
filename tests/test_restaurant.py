import unittest
import datetime
from Models.Restaurant import from_document, submit_wait_time


class MyTestCase(unittest.TestCase):
    def test_from_document_works(self):
        expected = {'_id': ('5d63fbb41c9d440000acf1b4'), 'Name': 'Taco Bell', 'Address': '212 Taco Street',
                    'Category': 'Tacos', 'WaitTime': 'Unknown'}
        restaurant = from_document(expected)
        self.assertEqual(restaurant.name, 'Taco Bell')

    def test_submit_wait(self):
        submit_wait_time("5d64a2af1c9d440000f35b69", 10, datetime.datetime.now())



if __name__ == '__main__':
    unittest.main()
