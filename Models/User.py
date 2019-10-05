from Models import MongoDb
class User:
    def __init__(self, user_id, email, password, role, favorite_food):
        self.id = user_id
        self.email = email
        self.password = password
        self.role = role
        self.favorite_food = favorite_food


def from_document(document):
    """
    Take a cursor object (document) and convert it to a User object
    :param document: Document found from collection
    :return: Restaurant object
    """
    values = document.values()
    values = list(values)

    return User(str(values[0]), values[1], values[2], values[3], values[4])


def append_submit_wait(user_id, wait_time):
    """
    add to the user db that they submitted a time
    :param user_id:
    :param wait_time:
    :return:
    """
    # mainly for testing
    if user_id is None:
        user_id = 'admin'
    collection = MongoDb.mongo_collection('Users ')
    collection.find_one_and_update({'user_id': user_id}, {'$push': {'wait_time_submissions': wait_time}},
                                   {'_id': False})


def append_submit_image(user_id, image):
    """
    add to the user db that they submitted an image
    :param user_id:
    :param image:
    :return:
    """
    if user_id is None:
        user_id = 'admin'
    collection = MongoDb.mongo_collection('Users ')
    collection.find_one_and_update({'user_id': user_id}, {'$push': {'image_submissions': image}},
                                   {'_id': False})
