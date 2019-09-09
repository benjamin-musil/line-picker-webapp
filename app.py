from flask import Flask, request, jsonify
from pymongo import MongoClient


app = Flask(__name__)


def mongodb_get_restaurants():
    uri = 'mongodb+srv://apt-6-admin:h00k3m@cluster0-wwuwc.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(uri)
    db = client['Restaurants']
    collection_name = "Test Restaurants "
    collection = db[collection_name]
    return collection


def mongo_get_wait_time_by_objectid(id):
    uri = 'mongodb+srv://apt-6-admin:h00k3m@cluster0-wwuwc.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(uri)
    db = client['WaitTimes']
    collection_name = "Test Wait Times"
    collection = db[collection_name]
    items = collection.find({"RestaurantId": str(id)})
    json_arr = []
    for item in items:
        json_arr.append(item)
    print(json_arr)
    wait_time = json_arr[0]['WaitTime'][0][0]
    print(wait_time)
    timestamp = json_arr[0]['WaitTime'][0][1]
    return wait_time, timestamp


@app.route('/getwait/byrestaurant', methods=['GET'])
def get_wait():
    content = request.args
    name = content.get('Restaurant Name')
    address = content.get('Address')
    collection = mongodb_get_restaurants()
    items = collection.find({"Address": address})
    json_arr = []
    for item in items:
        json_arr.append(item)
    object_id = json_arr[0]['_id']
    print(object_id)
    wait_time, timestamp = mongo_get_wait_time_by_objectid(object_id)
    return jsonify(str(name) + ' has a wait time of ' + str(wait_time) + ' reported at ' + str(timestamp)), 200


@app.route('/', methods=['GET'])
def example_get():
    # for the connection to work you need dnspython
    db = mongodb_get()
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
    # return{'message': 'hello world'}



def mongodb_get():
    uri = 'mongodb+srv://apt-6-admin:h00k3m@cluster0-wwuwc.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(uri)
    db = client['Restaurants']
    return db

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
