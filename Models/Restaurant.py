import bson
from Models import MongoDb, User
from Exceptions import exceptions


class Restaurant:
    def __init__(self, restaurant_id, name, address, category, wait_times, reported_by=None, images=[]):
        self.id = restaurant_id
        self.name = name
        self.address = address
        self.category = category
        self.wait_times = wait_times
        self.reported_by = reported_by
        self.images = images

    def add_to_db(self):
        collection = MongoDb.mongo_collection('Test Restaurants ')
        obj = {
            'Name': self.name,
            'Address': self.address,
            'Category': self.category,
            'WaitTimes': 'unknown'
        }
        return collection.insert_one(obj).inserted_id


def from_document(document):
    """
    Take a cursor object (document) and convert it to a Restaurant object
    :param document: Document found from collection
    :return: Restaurant object
    """
    values = list(document.values())
    images = document.get('Images')
    # Image needs to be an array to be used later
    if images is None:
        images = []
    return Restaurant(str(values[0]), document.get('Name'), document.get('Address'), document.get('Category'),
                      document.get('WaitTimes'), document.get('ReportedBy'), images)


def submit_wait_time(restaurant_id, wait_time, time, submitter):
    """
    Submit the wait time to the DB
    :param restaurant_id: Restaurant ID
    :param wait_time: wait time
    :param time: time submitted
    :param submitter: who submitted the wait time
    :return:
    """
    # mostly for testing
    if submitter is None:
        submitter = 'admin'
    collection = MongoDb.mongo_collection('Test Wait Times', database_name='WaitTimes')
    if collection.find_one_and_update({"RestaurantId": str(restaurant_id)},
                                      {'$push': {'WaitTime': [wait_time, str(time), submitter]}}, {'_id': False}) \
            is None:
        # submit the wait for the first time
        wait_post = {
            'RestaurantId': str(restaurant_id),
            'WaitTime': [[wait_time, str(time), submitter]]
        }
        collection.insert_one(wait_post)
    User.append_submit_wait(submitter, [wait_time, str(time), str(restaurant_id)])


def submit_image(restaurant_id, url, submitter):
    """
    submit the image url to the db
    :param restaurant_id: ID of restaurant to add the image to
    :param url: url to the image
    :param submitter: who submitted the image
    :return: None
    """
    collection = MongoDb.mongo_collection('Test Restaurants ')
    collection.find_one_and_update({"_id": bson.objectid.ObjectId(restaurant_id)}, {'$push': {'Images': url}})
    User.append_submit_image(submitter, [url, str(restaurant_id)])


def get_wait_times(restaurant_id):
    """
    Get the wait times of a restaurant
    :param restaurant_id:
    :return: An array of wait times
    :raises: No Wait Time found
    """
    db = MongoDb.mongo_database('WaitTimes')
    collection_name = "Test Wait Times"
    collection = db[collection_name]
    items = collection.find_one({"RestaurantId": str(restaurant_id)}, {'_id': False})
    wait_times = items['WaitTime']
    if items is None:
        raise exceptions.NoWaitFound()
    # if something was submitted before the users were tracked, it was an admin that did it
    for wait_time in wait_times:
        if len(wait_time) < 3:
            wait_time.append('admin')
    return wait_times
