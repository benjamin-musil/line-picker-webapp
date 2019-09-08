from pymongo import MongoClient


def mongo_client(collection):
    """
    Connect to the collection given and return back that collection object
    :param collection: Name of the collection to connect to
    :return: MongoDB collection object
    """
    uri = 'mongodb+srv://apt-6-admin:h00k3m@cluster0-wwuwc.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(uri)
    db = client[collection]
    return db
