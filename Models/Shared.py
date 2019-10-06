from flask import session, url_for


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
