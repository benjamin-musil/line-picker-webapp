from flask import Flask, jsonify
from pymongo import MongoClient
import pprint
import logging
from datetime import datetime


app = Flask(__name__)


def mongodb_get():
    uri = "mongodb+srv://rofranklin:Froggy01@cluster0-wwuwc.mongodb.net/test?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client.get_database('Restaurants')
    collection_name = "Test Restaurants"
    collection = db[collection_name]
    items = collection.find({"Name": "Taco Bell"})
    for item in items:
        logging.error(pprint.pprint(item))

    return(pprint.pprint(items))




@app.route('/example/endpoint', methods=['GET'])
def example_function():
    db_instance = mongodb_get()
    return jsonify(db_instance), 200


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
