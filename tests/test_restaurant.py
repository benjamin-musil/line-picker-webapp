import unittest
from Models.Restaurant import from_document


class MyTestCase(unittest.TestCase):
    def test_from_document_works(self):
        expected = {'_id': ('5d63fbb41c9d440000acf1b4'), 'Name': 'Taco Bell', 'Address': '212 Taco Street',
                    'Category': 'Tacos', 'WaitTime': 'Unknown'}
        restaurant = from_document(expected)
        self.assertEqual(restaurant.name, 'Taco Bell')



if __name__ == '__main__':
    unittest.main()
