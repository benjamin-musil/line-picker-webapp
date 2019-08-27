from flask import Flask
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)


@app.route('/example/endpoint', methods=['POST'])
def example_function():
    pass


@app.route('/', methods=['GET'])
def example_get():
    # for the connection to work you need dnspython
    db = mongodb_get()
    print(db['Test Restaurants'])
    return{'message': 'hello world'}



def mongodb_get():
    uri = 'mongodb+srv://apt-6-admin:h00k3m@cluster0-wwuwc.mongodb.net/test?retryWrites=true&w=majority'
    client = MongoClient(uri)
    db = client['Restaurants']
    return db

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
