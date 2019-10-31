import datetime
import json
import re
import bson
import requests
import ast
from flask import Flask, request, jsonify, session, Blueprint
from Models import Restaurant, User, MongoDb, Shared
from Exceptions import exceptions


mobile = Blueprint('mobile', __name__, template_folder='templates')


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


# Route here when using search bar on mobile
@mobile.route('/mobile/ListAllRestaurant/Search', methods=['GET', 'POST'])
def mobileSearchBar():
    try:
        if not request.headers.get("token"):
            return jsonify({'error': 'No token present'})
        session['logged_in'], session['username'] = Shared.set_mobile_session(request.headers.get("token"))
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
        for restaurant in data:
            if len(restaurant['images']) == 0:
                restaurant['images'].append('https://www.drupal.org/files/styles/grid-3-2x/public/project-images/drupal-addtoany-logo.png')
        # Pass a blank tab to load the template page
        UiContent = {'SelectedTab': '', 'RestaurantType': categories}
        # we now just return a json blob rather than a template
        return_dict = {
            "UiContent": UiContent,
            "restaurants": data,
            "user": session.get('username')
        }
        return jsonify(return_dict)
    except exceptions.TokenExpired:
        # returns an error message so mobile front end can render an error message
        return jsonify({"error": "token expired"})

# Mobile Route here for getting restaurants based on category
@mobile.route('/mobile/ListAllRestaurant', methods=['GET', 'POST'])
def mobileListAllRestaurant():
    try:
        # Get all restaurant categories
        if not request.headers.get("token"):
            return jsonify({'error': 'No token present'})
        session['logged_in'], session['username'] = Shared.set_mobile_session(request.headers.get("token"))
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
        return_dict = {
            "UiContent": UiContent,
            "restaurants": data,
            "user": session.get('username')
        }
        return jsonify(return_dict)
    except exceptions.TokenExpired:
        return jsonify({"error": "token expired"})


@mobile.route('/mobile/<user_id>/mysubmissions', methods=['GET'])
def mobile_get_by_username(user_id):
    if not request.headers.get("token"):
        return jsonify({'error': 'No token present'})
    session['logged_in'], session['username'] = Shared.set_mobile_session(request.headers.get("token"))
    user = User.get_submissions(user_id)
    return_dict = {
        "wait_submissions": user.__dict__['wait_time_submissions'],
        "image_submissions": user.__dict__['image_submissions'],
        "user": session.get('username')
    }
    return jsonify(return_dict)


@mobile.route('/mobile/user-settings', methods=['GET'])
def mobile_user_settings():
    try:
        if not request.headers.get('token'):
            return jsonify({'error': 'No token present'})
        session['logged_in'], session['username'] = Shared.set_mobile_session(request.headers.get('token'))
        return_dict = {
            "user": User.get_user_info(session.get('username'))
        }
        print(jsonify(return_dict))
        return jsonify(return_dict)
    except exceptions.TokenExpired:
        return jsonify({"error": "token expired"})


@mobile.route('/mobile/restaurant/<restaurant_id>')
def get_mobile_restaurant(restaurant_id):
    if not request.headers.get('token'):
        return jsonify({'error': 'No token present'})
    session['logged_in'], session['username'] = Shared.set_mobile_session(request.headers.get('token'))
    collection = MongoDb.mongo_collection('Test Restaurants ')
    item = collection.find_one({"_id": bson.objectid.ObjectId(restaurant_id)})
    restaurant = Restaurant.from_document(item)
    # if the restaurant has less than 3 images, force it to have 3
    # this is due to how my carousel component works
    while len(restaurant.images) < 3:
        restaurant.images.append(
            'https://www.drupal.org/files/styles/grid-3-2x/public/project-images/drupal-addtoany-logo.png')
    try:
        restaurant.wait_times = Restaurant.get_wait_times(restaurant_id)
    except exceptions.NoWaitFound:
        restaurant.wait_times = None
    return jsonify(restaurant.__dict__)


@mobile.route('/mobile/submit-time', methods=['POST'])
def submit_wait_time():
    if not request.headers.get('token'):
        return jsonify({'error': 'No token present'})
    session['logged_in'], session['username'] = Shared.set_mobile_session(request.headers.get('token'))
    args = request.get_json()
    restaurant_id = args.get('Id')
    wait_time = args.get('wait')
    geolocation = args.get('geolocation')

    # Post image to ImgBB and get url back
    image64 = args.get('image64')
    # apt-team-6 API key for ImgBB in POST request
    image_post = requests.post("https://api.imgbb.com/1/upload?key=3853892f353149fea471291dd38e9206",
                             data={"image": image64})
    image_url = json.loads(image_post.content).get('data').get('display_url')

    # Submit wait time and image url
    Restaurant.submit_wait_time(restaurant_id, wait_time, datetime.datetime.now(),
                                session.get('username'), geolocation)
    Restaurant.submit_image(restaurant_id, image_url, session.get('username'))

    return jsonify(args)

@mobile.route('/mobile/submit-restaurant', methods=['POST'])
def submit_mobile_restaurant():
    args = request.get_json()
    restaurant = Restaurant.Restaurant('', args.get('Name'), args.get('Address'),
                                       args.get('category'), '-')
    new_id = restaurant.add_to_db()
    new = {
        "id": str(new_id)
    }
    return jsonify(new)

@mobile.route('/mobile/verify-token', methods=['GET'])
def verify_mobile_token():
    if not request.headers.get('token'):
        return jsonify({'error': 'No token present'})
    try:
        session['logged_in'], session['username'] = Shared.set_mobile_session(request.headers.get('token'))
        return jsonify({"value": "good"})
    except exceptions.TokenExpired:
        return jsonify({"error": "token expired"})


@mobile.route('/mobile/verify-token', methods=['GET'])
def verify_mobile_token():
    if not request.headers.get('token'):
        return jsonify({'error': 'No token present'})
    try:
        session['logged_in'], session['username'] = Shared.set_mobile_session(request.headers.get('token'))
        return jsonify({"value": "good"})
    except exceptions.TokenExpired:
        return jsonify({"error": "token expired"})


@mobile.route('/mobile/get-all-pages', methods=['GET'])
def get_pages():
    return jsonify(Shared.generate_page_list())


@mobile.route('/mobile/get-all-categories', methods=['GET'])
def get_categories():
    categories = MongoDb.mongo_collection('Test Restaurants ').distinct('Category')
    return jsonify(categories)


@mobile.route('/mobile/update-user', methods=['GET', 'POST'])
def update_user():
    if not request.headers.get('token'):
        return jsonify({'error': 'No token present'})
    session['logged_in'], session['username'] = Shared.set_mobile_session(request.headers.get('token'))
    print(request.get_data())
    args = request.get_json()
    category = args.get('category')
    print(category)
    User.update_user(session.get('username'), category)
    return jsonify(args)
