from flask import session, url_for
import google.oauth2.id_token
from google.auth.transport import requests
from Models import Shared, User
from flask import request


def generate_page_list():
    session['logged_in'], session['username'] = Shared.set_session(request.cookies.get("token"))
    if session.get('logged_in'):
        pages = [
            {"name": "Home", "url": url_for(
                "SearchBar",restaurant_tag=User.get_user_info(session.get('username'))['favorite_food'], _external=True)
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
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, firebase_request_adapter)
    if claims:
        return True, claims['name'].replace(' ', '_')
