import datetime
import bson
from flask import Blueprint, render_template, request, redirect, session, url_for
from Models import Restaurant, MongoDb, User
from Exceptions import exceptions

restaurant_page = Blueprint('restaurant_page', __name__,
                            template_folder='templates')


@restaurant_page.route('/restaurant/<restaurant_id>')
def get_restaurant(restaurant_id):
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
    return render_template('restaurant.html', restaurant=restaurant.__dict__,
                           wait_times=restaurant.__dict__['wait_times'], pages=generate_page_list(),
                           user=session.get('username'))


@restaurant_page.route('/restaurant/submit-time', methods=['GET', 'POST'])
def submit_wait_time():
    form_args = request.form
    restaurant_id = form_args['Id']
    wait_time = form_args['wait']
    Restaurant.submit_wait_time(restaurant_id, wait_time, datetime.datetime.now(), session.get('username'))
    return redirect('/restaurant/' + restaurant_id)


@restaurant_page.route('/add-restaurant/', methods=['GET'])
def add_restaurant():
    return render_template('add_restaurant.html')


@restaurant_page.route('/restaurant/submit-image', methods=['POST'])
def submit_image():
    form_args = request.form
    restaurant_id = form_args['Id']
    Restaurant.submit_image(restaurant_id, form_args['url'], session.get('username'))
    return redirect('/restaurant/' + restaurant_id)


@restaurant_page.route('/submit-restaurant/', methods=['POST'])
def submit_restaurant():
    form_args = request.form
    restaurant = Restaurant.Restaurant('', form_args['Name'], form_args['Address'], form_args['category'], '-')
    new_id = restaurant.add_to_db()
    return redirect('/restaurant/' + str(new_id))


def generate_page_list():
    if session.get('logged_in'):
        pages = [
            {"name": "Home", "url": url_for(
                "login")
             },
            {"name": "Search Restaurant", "url": url_for(
                "ListAllRestaurant")
             },
            {"name": "Add a Restaurant", "url": url_for(
                "restaurant_page.add_restaurant")
             },
            {"name": "My Submissions", "url": url_for('get_by_username', user_id=session.get('username'))
             }
        ]
    else:
        pages = [{
            "name": "Login", "url": url_for('input')
        }]
    return pages