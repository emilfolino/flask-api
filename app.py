from flask import Flask, render_template, request
app = Flask(__name__)

import json

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


def filter_unique(products):
    unique_dict = {}
    for key in products["data"]:
        if not isinstance(key["stock"], int):
            key["stock"] = 0

        if key["name"] in unique_dict:
            unique_dict[key["name"]] += key["stock"]
        else:
            unique_dict[key["name"]] = key["stock"]

    return unique_dict

def create_list(unique_dict):
    unique_list = []
    for name in unique_dict:
        element = {
            "name": name,
            "stock": unique_dict[name]
        }
        unique_list.append(element)

    return unique_list


def fetch_data():
    URL = 'https://lager.emilfolino.se/v2/products/everything'

    # Use requests module to get JSON data
    response = requests.get(URL)

    # Turns response json object into a Dictionary
    return response.json()


@app.route('/unique')
def unique():
    products_dict = fetch_data()

    unique_dict = filter_unique(products_dict)

    json_output = { "data" : create_list(unique_dict) }

    return jsonify(json_output)



@app.route('/search/<query>')
def search(query):
    products_dict = fetch_data()

    unique_dict = filter_unique(products_dict)

    search_results = {}
    for name in unique_dict:
        if query in name:
            search_results[name] = unique_dict[name]

    json_output = { "data" : create_list(search_results) }

    return jsonify(json_output)



@app.route('/image_search')
def image_search():
    image_url = request.args.get("image-url", "")

    if image_url:
        # do lots of stuff
        print(image_url)

    return render_template("index.html", image_url=image_url)
