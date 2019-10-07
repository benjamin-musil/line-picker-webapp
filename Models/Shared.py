from flask import session, url_for


def generate_page_list():
    if session.get('logged_in'):
        pages = [
            {"name": "Home", "url": url_for(
                "ListAllRestaurant", _external=True)
             },
            {"name": "Search Restaurant", "url": url_for(
                "ListAllRestaurant", _external=True)
             },
            {"name": "Add a Restaurant", "url": url_for(
                "restaurant_page.add_restaurant", _external=True)
             },
            {"name": "My Submissions", "url": url_for('get_by_username', user_id=session.get('username'), _external=True)
             }
        ]
    else:
        pages = [{
            "name": "Login", "url": url_for('input', _external=True)
        }]
    return pages
