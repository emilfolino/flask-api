from flask import Flask
app = Flask(__name__)

from flask import jsonify
import requests

@app.route('/')
def root():
    data = {
        "data": {
            "routes": {
                "/unique": "Prints all unique products.",
                "/search/:query": "Searches the unique products and outputs matching products."
            },
            "author": "Emil Folino"
        }
    }
    return jsonify(data)



@app.route('/unique')
def unique():
    URL = 'https://lager.emilfolino.se/v2/products/everything'

    # Use requests module to get JSON data
    response = requests.get(URL)

    # Turns response json object into a Dictionary
    products_dict = response.json()

    return jsonify(products_dict)



@app.route('/search/<query>')
def show_user_profile(query):
    # show the user profile for that user
    data = { "data": query }

    return jsonify(data)