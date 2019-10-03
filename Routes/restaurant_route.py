import bson
import datetime
from flask import Blueprint, render_template, request, redirect
from Models import Restaurant, MongoDb
from Exceptions import exceptions

restaurant_page = Blueprint('simple_page', __name__,
                            template_folder='Templates')


@restaurant_page.route('/restaurant/<restaurant_id>')
def get_restaurant(restaurant_id):
    collection = MongoDb.mongo_collection('Test Restaurants ')
    item = collection.find_one({"_id": bson.objectid.ObjectId(restaurant_id)})
    restaurant = Restaurant.from_document(item)
    try:
        restaurant.wait_times = get_wait_times(restaurant_id)
    except exceptions.NoWaitFound:
        restaurant.wait_times = None
    return render_template('add_restuarant.html', restaurant=restaurant.__dict__,
                           wait_times=restaurant.__dict__['wait_times'])


@restaurant_page.route('/restuarant/submit-time', methods=['GET', 'POST'])
def submit_wait_time():
    dict = request.form
    for key in dict:
        print(
            'form key ' + dict[key] + ' means ' + key)

    id = dict['Id']
    time = dict['wait']
    Restaurant.submit_wait_time(id, time, datetime.datetime.now())
    return redirect('/restaurant/' + id)


def get_wait_times(restaurant_id):
    db = MongoDb.mongo_database('WaitTimes')
    collection_name = "Test Wait Times"
    collection = db[collection_name]
    items = collection.find({"RestaurantId": str(restaurant_id)})
    json_arr = []
    json_arr.extend(items)
    if not json_arr:
        raise exceptions.NoWaitFound()
    wait_time = json_arr[0]['WaitTime']
    return wait_time
