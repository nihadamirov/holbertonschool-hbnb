from flask import Blueprint, request, jsonify, abort
from app import db
from app.models.city import City
from app.models.country import Country

city_api = Blueprint('city_api', __name__)

@city_api.route('/cities', methods=['POST'])
def create_city():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('country_code'):
        abort(400, description="Missing required fields")
    
    country = Country.query.filter_by(code=data['country_code']).first()
    if not country:
        abort(400, description="Invalid country code")
    
    existing_city = City.query.filter_by(name=data['name'], country_id=data['country_code']).first()
    if existing_city:
        abort(409, description="City already exists in this country")
    
    new_city = City(name=data['name'], country_id=data['country_code'])
    db.session.add(new_city)
    db.session.commit()
    
    return jsonify(new_city.serialize()), 201

@city_api.route('/cities', methods=['GET'])
def get_cities():
    cities = City.query.all()
    return jsonify([city.serialize() for city in cities]), 200

@city_api.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = City.query.get(city_id)
    if not city:
        abort(404, description="City not found")
    return jsonify(city.serialize()), 200

@city_api.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.get_json()
    city = City.query.get(city_id)
    if not city:
        abort(404, description="City not found")
    
    city.name = data.get('name', city.name)
    country_code = data.get('country_code')
    if country_code:
        country = Country.query.filter_by(code=country_code).first()
        if not country:
            abort(400, description="Invalid country code")
        city.country_id = country_code
    
    db.session.commit()
    
    return jsonify(city.serialize()), 200

@city_api.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = City.query.get(city_id)
    if not city:
        abort(404, description="City not found")
    
    db.session.delete(city)
    db.session.commit()
    
    return '', 204
