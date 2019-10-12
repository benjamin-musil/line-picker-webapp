
import json
import os
import re
from flask import Flask, request, jsonify, render_template, session, redirect
from google.auth.transport import requests
import google.oauth2.id_token
from Models import Restaurant, User, MongoDb, Shared
from Exceptions import exceptions


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


# Route here for getting restaurants based on category or search
@app.route('/ListAllRestaurant', methods=['GET', 'POST'])
def ListAllRestaurant():
    try:
        # Get all restaurant categories
        if not request.cookies.get("token"):
            return redirect('/')
        session['logged_in'], session['username'] = Shared.set_session(request.cookies.get("token"))
        if session.get('RestaurantCategory') is None:
            categories = MongoDb.mongo_collection('Test Restaurants ').distinct('Category')
            session['RestaurantCategory'] = categories
        else:
            categories = session['RestaurantCategory']

        # Get selected restaurant category tab
        selected_category = request.args.get('select')
        # Get searched tag
        searched_tag = request.args.get('restaurant_tag')

        if selected_category is None:
            selected_tab = ''

            if searched_tag is None:
                # return all restaurants on empty search
                res = search_Restaurant({}).response[0]
            else:
                # return all restaurants matching a tag
                searched_tag_regex = re.compile(".*" + searched_tag + ".*", re.IGNORECASE)
                res = search_Restaurant({"$or": [{'Name': searched_tag_regex},
                                                 {'Category': searched_tag_regex}]}).response[0]

        else:
            selected_tab = selected_category
            json_input = {'Category': selected_tab}

            if searched_tag is None:
                # return all restaurants in a specific category
                res = search_Restaurant(json_input).response[0]
            else:
                # return all restaurants matching a tag with a specific category
                searched_tag_regex = re.compile(".*" + searched_tag + ".*", re.IGNORECASE)
                res = search_Restaurant({"$and": [{'Name': searched_tag_regex},
                                                  {'Category': selected_tab}]}).response[0]

        data = json.loads(res)
        UiContent = {'SelectedTab': selected_tab, 'RestaurantType': categories}
        return render_template("AllRestaurant.html", UiContent=UiContent, restaurants=data,
                               pages=Shared.generate_page_list(), user=session.get('username'))
    except exceptions.TokenExpired:
        return redirect('/')


firebase_request_adapter = requests.Request()


@app.route('/login', methods=['GET'])
def login():
    id_token = request.cookies.get("token")
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
        # This will be raised if the token is expired or any other
        # verification checks fail.
        error_message = str(exc)
        print(error_message)
    user_id = claims['name'].replace(' ', '_')
    user_email = claims['email']
    user_info = get_user(user_id)
    # get_user returns [] when not found
    if len(user_info) == 0:
        # add to the db yo
        User.add_user_to_db(user_id, user_email)
    session['username'] = claims['name'].replace(' ', '_')
    session['logged_in'] = True
    USERID = user_id
    return redirect('ListAllRestaurant')


@app.route('/<user_id>/mysubmissions', methods=['GET'])
def get_by_username(user_id):
    if not request.cookies.get("token"):
        return redirect('/')
    session['logged_in'], session['username'] = Shared.set_session(request.cookies.get("token"))
    user = User.get_submissions(user_id)
    return render_template('mysubmissions_result.html', wait_submissions=user.__dict__['wait_time_submissions'],
                           image_submissions=user.__dict__['image_submissions'], pages=Shared.generate_page_list(),
                           user=session.get('username'))


@app.route('/user-settings', methods=['GET'])
def user_settings():
    try:
        if not request.cookies.get("token"):
            return redirect('/')
        session['logged_in'], session['username'] = Shared.set_session(request.cookies.get("token"))
        categories = MongoDb.mongo_collection('Test Restaurants ').distinct('Category')
        return render_template('user_settings.html', user=session.get('username'),
                               categories=categories, pages=Shared.generate_page_list(),
                               dbuser=User.get_user_info(session.get('username')))
    except exceptions.TokenExpired:
        return redirect('/')


@app.route('/update-user', methods=['POST'])
def update_user():
    form_args = request.form
    User.update_user(session.get('username'), form_args['category'])
    return redirect('/user-settings')


@app.route('/')
def input():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=False, threaded="True")
