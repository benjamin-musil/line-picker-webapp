from flask import Flask, jsonify
from Models import Restaurant, MongoDb

app = Flask(__name__)


@app.route('/example/endpoint', methods=['POST'])
def example_function():
    pass


@app.route('/category/<category>', methods=['GET'])
def example_get(category):
    # for the connection to work you need dnspython
    db = MongoDb.mongo_client('Restaurants')
    # there is a space after the name, if you look on the website it doesn't look like there is though
    # so that's really annoying
    collection = db['Test Restaurants ']
    results = collection.find({u'Category': u''+category+''})
    restaurant_arr = []
    for document in results:
        restaurant = Restaurant.from_document(document)
        restaurant_arr.append(restaurant.__dict__)
    return jsonify(restaurant_arr)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
