from flask import Flask, request, jsonify
from Models import Restaurant, MongoDb


app = Flask(__name__)

# Can't do POST method until we have some kind of form that inputs data, since we're just testing db
# interaction, we'll use the default GET for now
# https://stackoverflow.com/questions/3477333/what-is-the-difference-between-post-and-get/3477374#3477374
@app.route('/post/test', methods=['GET'])
def example_post():
    collection = MongoDb.mongo_collection('Users ')
    test_user = {
        'username'      : 'Ben',
        'email'         : 'benjamin.musil@gmail.com',
        'password'      : 'hook3m',
        'role'          : 'admin',
        'favorite_food' : 'breakfast'
    }
    collection.insert_one(test_user)
    return{'message': 'Post successful'}


@app.route('/category/<category>', methods=['GET'])
def example_get(category):
    collection = MongoDb.mongo_collection('Test Restaurants ')
    results = collection.find({u'Category': u''+category+''})
    restaurant_arr = []
    for document in results:
        print(document)
        restaurant = Restaurant.from_document(document)
        restaurant_arr.append(restaurant.__dict__)
    return jsonify(restaurant_arr)


def mongo_get_wait_time_by_objectid(restaurant_id):
    db = MongoDb.mongo_database('WaitTimes')
    collection_name = "Test Wait Times"
    collection = db[collection_name]
    items = collection.find({"RestaurantId": str(restaurant_id)})
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
    collection = MongoDb.mongo_collection('Test Restaurants ')
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
