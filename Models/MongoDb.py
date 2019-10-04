from pymongo import MongoClient


def mongo_database(database):
    """
    Connect to the database given and return back the database object
    :param database: Name of the Database to connect to
    :return: MongoDB database object
    """
    uri = 'mongodb+srv://apt-6-admin:h00k3m@cluster0-wwuwc.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(uri)
    db = client[database]
    return db


def mongo_collection(collection_name, database_name="Restaurants"):
    """
    Connect to a specific collection (table)
    :param collection_name: name of the collection to connect to
    :param database_name: name of the database to connect to (optional) defaulted to Restaurants
    :return: MongoDB collection object
    """
    db = mongo_database(database_name)
    collection = db[collection_name]
    return collection
