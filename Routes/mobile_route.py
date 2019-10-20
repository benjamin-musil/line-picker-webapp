import json
import re
from flask import Flask, request, jsonify, session, Blueprint
from Models import Restaurant, User, MongoDb, Shared
from Exceptions import exceptions


mobile = Blueprint('mobile', __name__,  template_folder='templates')


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
        session['logged_in'], session['username'] = Shared.set_mobile_session(request.cookies.get("token"))
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
        session['logged_in'], session['username'] = Shared.set_mobile_session(request.cookies.get("token"))
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
    session['logged_in'], session['username'] = Shared.set_mobile_session(request.cookies.get("token"))
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


@mobile.route('/mobile/get-all-pages', methods=['GET'])
def get_pages():
    return jsonify(Shared.generate_page_list())


@mobile.route('/mobile/get-all-categories', methods=['GET'])
def get_categories():
    categories = MongoDb.mongo_collection('Test Restaurants ').distinct('Category')
    return jsonify(categories)
