import sys
import json
import os
import re
from flask import Flask, request, jsonify, render_template, session, redirect
from Models import Restaurant, User, MongoDb, Shared


from Routes.restaurant_route import restaurant_page

USERID = ''
app = Flask(__name__, template_folder='templates/')
app.secret_key = os.urandom(24)
app.register_blueprint(restaurant_page)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('not_found.html'), 404


@app.route('/Search', methods=['GET'])
def search_Restaurant(reqJason):
    if reqJason is None:
        reqJason = request.json

    collection = MongoDb.mongo_collection('Test Restaurants ')
    results = collection.find(reqJason)
    restaurant_arr = []
    for document in results:
        restaurant = Restaurant.from_document(document)
        restaurant_arr.append(restaurant.__dict__)
    return jsonify(restaurant_arr)


@app.route('/post-user/<user>', methods=['GET', 'POST'])
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
    collection.delete_one({u'_id': u'' + user + ''})
    return str(user + ' deleted!')


@app.route('/category/<category>', methods=['GET'])
def get_category(category):
    collection = MongoDb.mongo_collection('Test Restaurants ')
    results = collection.find({u'Category': u'' + category + ''})
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


# Route here when using search bar
@app.route('/ListAllRestaurant/Search', methods=['GET', 'POST'])
def SearchBar():
    # Get all restaurant categories
    if session.get('RestaurantCategory') is None:
        categories = MongoDb.mongo_collection('Test Restaurants ').distinct('Category')
        session['RestaurantCategory'] = categories
    else:
        categories = session['RestaurantCategory']

    # Create regular expression of search query
    tag = request.args.get('restaurant_tag')
    tag_regex = re.compile(".*"+tag+".*", re.IGNORECASE)

    # Match search query to name or category of restaurant
    res = search_Restaurant({"$or": [{'Name': tag_regex}, {'Category': tag_regex}]}).response[0]
    data = json.loads(res)

    # Pass a blank tab to load the template page
    UiContent = {'SelectedTab': '', 'RestaurantType': categories}
    return render_template("AllRestaurant.html", UiContent=UiContent, restaurants=data,
                           pages=Shared.generate_page_list(), user=session.get('username'))


# Route here for getting restaurants based on category
@app.route('/ListAllRestaurant', methods=['GET', 'POST'])
def ListAllRestaurant():
    try:
        # Get all restaurant categories
        if session.get('RestaurantCategory') is None:
            categories = MongoDb.mongo_collection('Test Restaurants ').distinct('Category')
            session['RestaurantCategory'] = categories
        else:
            categories = session['RestaurantCategory']

        # Get selected restaurant category tab
        selected_category = request.args.get('select')

        if selected_category is None:
            # Empty table at startup
            SelectedTab = ''
        else:
            SelectedTab = selected_category

        jsonInput = {}
        jsonInput['Category'] = SelectedTab

        if selected_category == 'All':
            # Get all restaurants for All category
            res = search_Restaurant({}).response[0]
        else:
            # Get all restaurants for a specific category
            res = search_Restaurant(jsonInput).response[0]

        data = json.loads(res)
        UiContent = {'SelectedTab': SelectedTab, 'RestaurantType': categories}
        return render_template("AllRestaurant.html", UiContent=UiContent, restaurants=data,
                               pages=Shared.generate_page_list(), user=session.get('username'))
    except:
        strException = sys.exc_info()


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
            session['logged_in'] = True
            session['username'] = user_id
            return redirect('ListAllRestaurant')
    else:
        return render_template('error.html')


@app.route('/<user_id>/mysubmissions', methods=['GET'])
def get_by_username(user_id):
    if USERID != user_id:
        return render_template('error.html')
    user = User.get_submissions(user_id)
    return render_template('mysubmissions_result.html', wait_submissions=user.__dict__['wait_time_submissions'],
                           image_submissions=user.__dict__['image_submissions'], pages=Shared.generate_page_list(),
                           user=session.get('username'))


@app.route('/')
def input():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=False, threaded="True")
