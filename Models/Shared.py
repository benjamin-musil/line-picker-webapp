from flask import session, url_for
import google.oauth2.id_token
from google.auth.transport import requests
from Models import Shared, User
from flask import request
from Exceptions import exceptions


def generate_page_list():
    session['logged_in'], session['username'] = Shared.set_session(request.cookies.get("token"))
    favorite_food = User.get_user_info(session.get('username'))['favorite_food']
    if not favorite_food:
        favorite_food = ""
    if session.get('logged_in'):
        pages = [
            {"name": "Home", "url": url_for(
                "SearchBar", restaurant_tag=favorite_food,
                _external=True)
             },
            {"name": "Search Restaurant", "url": url_for(
                "ListAllRestaurant", _external=True)
             },
            {"name": "Add a Restaurant", "url": url_for(
                "restaurant_page.add_restaurant", _external=True)
             },
            {"name": "My Submissions", "url": url_for('get_by_username', user_id=session.get('username'), _external=True)
             },
            {"name": "Settings", "url": url_for('user_settings', _external=True)
             }

        ]
    else:
        pages = [{
            "name": "Login", "url": url_for('input', _external=True)
        }]
    return pages


firebase_request_adapter = requests.Request()

def set_session(id_token):
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
        if claims:
            return True, claims['name'].replace(' ', '_')
    except ValueError:
        raise exceptions.TokenExpired()


def set_mobile_session(id_token):
    """
    set the mobile session based on mobile info
    :param id_token: id_token from the mobile app
    :return: True, and user_name
    """
    try:
        user = google.oauth2.id_token.verify_oauth2_token(id_token, requests.Request())
        return True, user['name'].replace(' ', '_')
    except ValueError:
        raise exceptions.TokenExpired()