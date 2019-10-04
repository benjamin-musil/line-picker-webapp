from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from Models import Restaurant, User, MongoDb

USERID =''
app = Flask(__name__, template_folder='templates/')

@app.route('/Search', methods=['GET'])
def search_Restaurant():
    reqJason = request.json
    collection = MongoDb.mongo_collection('Test Restaurants ')
    results = collection.find(reqJason)
    restaurant_arr = []
    for document in results:
        restaurant = Restaurant.from_document(document)
        restaurant_arr.append(restaurant.__dict__)
    return jsonify(restaurant_arr)

@app.route('/post-user/<user>', methods=['GET','POST'])
def post_user(user):
    # get args from POST URL
    user_id = request.args.get('user_id')
    email = request.args.get('email')
    password = request.args.get('password')
    role = request.args.get('role')
    favorite_food = request.args.get('favorite_food')

    # pass args to json object to post
    user_post = {
        '_id': user_id,
        'email': email,
        'password': password,
        'role': role,
        'favorite_food': favorite_food
    }

    # connect to database and post
    collection = MongoDb.mongo_collection('Users ')
    collection.insert_one(user_post)
    return 'Post successful!'

# Future release should combine post-user and get-user functions, will need to add forms for POST
@app.route('/get-user/<user>', methods=['GET', 'POST'])
def get_user(user):
    # connect to database and search for user specified
    collection = MongoDb.mongo_collection('Users ')
    results = collection.find({'user_id': user})

    # display users found by that unique username
    # change this to be a singular return instead of a list
    user_arr = []
    for document in results:
        print(document)
        user_test = User.from_document(document)
        user_arr.append(user_test.__dict__)
    print(user_arr)
    return user_arr

@app.route('/delete-user/<user>', methods=['GET', 'POST'])
def delete_user(user):
    # connect to database and search for user specified
    collection = MongoDb.mongo_collection('Users ')
    results = collection.delete_one({u'_id': u'' + user + ''})
    return str(user + ' deleted!')

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


@app.route('/login', methods=['POST'])
def login():
    content = request.form
    user_id = content['userid']
    password = content['password']
    user_info = get_user(user_id)
    if user_info:
        if user_info[0].get("password") != password:
            return render_template('error.html')
        else:
            global USERID
            USERID = user_id
            return render_template('success_login.html')
    else:
        return render_template('error.html')


@app.route('/<userid>/mysubmissions', methods=['GET'])
def get_by_username(userid):
    print(USERID)
    if USERID != userid:
        return render_template('error.html')
    collection = MongoDb.mongo_collection('Test Restaurants ')
    results = collection.find({'ReportedBy': USERID})
    restaurant_arr = []
    for document in results:
        print(document)
        restaurant = Restaurant.from_document(document)
        restaurant_arr.append(restaurant.__dict__)
    return render_template('mysubmissions_result.html', restaurant_arr=restaurant_arr)


@app.route('/')
def input():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=False, host='localhost', port='5000')
