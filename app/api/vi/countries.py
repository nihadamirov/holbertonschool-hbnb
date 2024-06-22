from flask import Blueprint, jsonify, abort
import json

country_api = Blueprint('country_api', __name__)

with open('countries.json', 'r') as f:
    countries = json.load(f)

@country_api.route('/countries', methods=['GET'])
def get_countries():
    return jsonify(countries), 200

@country_api.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country = next((c for c in countries if c["code"] == country_code), None)
    if not country:
        abort(404, description="Country not found")
    return jsonify(country), 200

@country_api.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    cities = [city for city in data_manager.get_all('City') if city['country_code'] == country_code]
    return jsonify(cities), 200
