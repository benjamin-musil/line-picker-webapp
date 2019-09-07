from flask import Flask, jsonify
from Models import Restaurant, MongoDb

app = Flask(__name__)

# Can't do POST method until we have some kind of form that inputs data, since we're just testing db
# interaction, we'll use the default GET for now
# https://stackoverflow.com/questions/3477333/what-is-the-difference-between-post-and-get/3477374#3477374
@app.route('/post/test',methods=['GET'])
def example_post():
    # for the connection to work you need dnspython
    db = MongoDb.mongo_client('Restaurants')
    collection = db['Users ']
    
    test_user = {
        'username'      : 'Ben',
        'email'         : 'benjamin.musil@gmail.com',
        'password'      : 'hook3m',
        'role'          : 'admin',
        'favorite_food' : 'breakfast'
    }
    
    post = collection.insert_one(test_restaurant)

    return{'message': 'Post successful'}

@app.route('/category/<category>', methods=['GET'])
def example_get(category):
    # for the connection to work you need dnspython
    db = MongoDb.mongo_client('Restaurants')
    # there is a space after the name, if you look on the website it doesn't look like there is though
    # so that's really annoying
    collection = db['Test Restaurants ']
    results = collection.find({u'Category': u''+category+''})
    restaurant_arr = []
    for document in results:
        restaurant = Restaurant.from_document(document)
        restaurant_arr.append(restaurant.__dict__)
    return jsonify(restaurant_arr)


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
