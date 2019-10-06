from Models import MongoDb


class User:
    def __init__(self, user_id, user_name, email, password, role, favorite_food, wait_time_submissions=[],
                 image_submissions=[]):
        self.id = user_id
        self.user_name = user_name
        self.email = email
        self.password = password
        self.role = role
        self.favorite_food = favorite_food
        self.wait_time_submissions = wait_time_submissions
        self.image_submissions = image_submissions


def from_document(document):
    """
    Take a cursor object (document) and convert it to a User object
    :param document: Document found from collection
    :return: Restaurant object
    """
    values = document.values()
    values = list(values)
    image_submissions = document.get('image_submissions')
    wait_submissions = document.get('wait_time_submissions')
    if image_submissions is None:
        image_submissions = []
    if wait_submissions is None:
        wait_submissions = []

    return User(str(values[0]), document.get('user_id'), document.get('email'), document.get('password'),
                document.get('role'), document.get('favorite_food'), wait_submissions, image_submissions)


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


def get_submissions(user_id):
    """
    get all the submissions
    :param user_id:
    :return:
    """
    if user_id is None:
        user_id = 'admin'
    collection = MongoDb.mongo_collection('Users ')
    item = collection.find_one({'user_id': user_id}, {'_id': False})
    return from_document(item)
