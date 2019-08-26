from flask import Flask


app = Flask(__name__)


@app.route('/example/endpoint', methods=['POST'])
def example_function():
    pass


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port='5000')
