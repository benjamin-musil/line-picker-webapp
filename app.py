from flask import Flask
from pymongo import MongoClient
from datetime import datetime


app = Flask(__name__)


def mongodb_get():
    uri = "mongodb+srv://<username>:<password>@cluster0-wwuwc.mongodb.net/test?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client.test


@app.route('/example/endpoint', methods=['POST'])
def example_function():
    pass


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
