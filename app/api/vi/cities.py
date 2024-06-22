from flask import Blueprint, request, jsonify, abort
from app.models.city import City
from app.models.data_manager import DataManager

city_api = Blueprint('city_api', __name__)
data_manager = DataManager()

@city_api.route('/cities', methods=['POST'])
def create_city():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('country_code'):
        abort(400, description="Missing required fields")
    country = next((c for c in countries if c["code"] == data['country_code']), None)
    if not country:
        abort(400, description="Invalid country code")
    if data_manager.get(data['name'], 'City'):
        abort(409, description="City already exists in this country")
    city = City(name=data['name'], country_id=data['country_code'])
    data_manager.save(city)
    return jsonify(city.__dict__), 201

@city_api.route('/cities', methods=['GET'])
def get_cities():
    cities = data_manager.get_all('City')
    return jsonify(cities), 200

@city_api.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")
    return jsonify(city), 200

@city_api.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.get_json()
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")
    city.update(data)
    data_manager.save(city)
    return jsonify(city), 200

@city_api.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = data_manager.get(city_id, 'City')
    if not city:
        abort(404, description="City not found")
    data_manager.delete(city_id, 'City')
    return '', 204
