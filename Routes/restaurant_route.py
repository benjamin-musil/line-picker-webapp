from flask import Blueprint, render_template, abort, jsonify
from Models import Restaurant, User, MongoDb
import bson

restaurant_page = Blueprint('simple_page', __name__,
                        template_folder='Templates')


@restaurant_page.route('/restaurant/<restaurant_id>')
def get_restaurant(restaurant_id):
    collection = MongoDb.mongo_collection('Test Restaurants ')
    item = collection.find_one({"_id": bson.objectid.ObjectId(restaurant_id)})
    restaurant = Restaurant.from_document(item)
    try:
        restaurant.wait_times = get_wait_times(restaurant_id)
    except:
        restaurant.wait_times = None
    return render_template('add_restuarant.html', restaurant=restaurant.__dict__,
                           wait_times=restaurant.__dict__['wait_times'])


def get_wait_times(restaurant_id):
    db = MongoDb.mongo_database('WaitTimes')
    collection_name = "Test Wait Times"
    collection = db[collection_name]
    items = collection.find({"RestaurantId": str(restaurant_id)})
    json_arr = []
    json_arr.extend(items)
    if len(json_arr) < 1:
        raise Exception("not found")
    wait_time = json_arr[0]['WaitTime']
    return wait_time

