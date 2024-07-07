from flask import Blueprint, jsonify, abort
from app.models.city import City
from app.models.country import Country

country_api = Blueprint('country_api', __name__)

@country_api.route('/countries', methods=['GET'])
def get_countries():
    countries = Country.query.all()
    return jsonify([country.serialize() for country in countries]), 200

@country_api.route('/countries/<country_code>', methods=['GET'])
def get_country(country_code):
    country = Country.query.filter_by(code=country_code).first()
    if not country:
        abort(404, description="Country not found")
    return jsonify(country.serialize()), 200

@country_api.route('/countries/<country_code>/cities', methods=['GET'])
def get_cities_by_country(country_code):
    cities = City.query.filter_by(country_id=country_code).all()
    return jsonify([city.serialize() for city in cities]), 200
