from Models import MongoDb


class Restaurant:
    def __init__(self, restaurant_id, name, address, category, wait_times):
        self.id = restaurant_id
        self.name = name
        self.address = address
        self.category = category
        self.wait_times = wait_times

    def add_to_db(self):
        collection = MongoDb.mongo_collection('Test Restaurants ')
        obj = {
            'Name': self.name,
            'Address': self.address,
            'Category': self.category,
            'WaitTimes': 'unknown'
        }
        collection.insert_one(obj)


def from_document(document):
    """
    Take a cursor object (document) and convert it to a Restaurant object
    :param document: Document found from collection
    :return: Restaurant object
    """
    values = document.values()
    values = list(values)
    return Restaurant(str(values[0]), values[1], values[2], values[3], values[4])


def submit_wait_time(restuarant_id, wait_time, time):
    """
    Submit the wait time to the DB
    :param restuarant_id: Restuarant ID
    :param wait_time: wait time
    :param time: time submitted
    :return:
    """
    collection = MongoDb.mongo_collection('Test Wait Times', database_name='WaitTimes')
    if collection.find_one_and_update({"RestaurantId": str(restuarant_id)},
                                      {'$push': {'WaitTime': [wait_time, str(time)]}}, {'_id': False}) \
            is None:
        # submit the wait for the first time
        wait_post = {
            'RestaurantId': str(restuarant_id),
            'WaitTime': [[wait_time, str(time)]]
        }
        collection.insert_one(wait_post)

