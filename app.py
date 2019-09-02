from flask import Flask, jsonify
from Models import  Restaurant
from Models import MongoDb

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
    restaurant_arr = []
    for i in tacos:
        restaurant = Restaurant.from_document(i)
        restaurant_arr.append(restaurant.__dict__)
    return jsonify(restaurant_arr)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
