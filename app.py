from flask import Flask, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from Models import User
from Models import MongoDb
from datetime import datetime

app = Flask(__name__)


@app.route('/example/endpoint', methods=['POST'])
def example_function():
    pass


@app.route('/', methods=['GET'])
def example_get():
    # for the connection to work you need dnspython
    db = MongoDb.mongo_client('Restaurants')
    # there is a space after the name, if you look on the website it doesn't look like there is though
    # so that's really annoying
    collection = db['Test Restaurants ']
    tacos = collection.find({u'Category': u'Tacos'})
    json_arr = []
    for i in tacos:
        print(i)
        json_arr.append(dumps(i))
    print(json_arr)
    return(jsonify(json_arr))


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
