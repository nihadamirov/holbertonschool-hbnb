from flask import Blueprint, request, jsonify, abort
from app import db
from app.models import Amenity

amenity_api = Blueprint('amenity_api', __name__)

@amenity_api.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Missing required field: name")
    
    existing_amenity = Amenity.query.filter_by(name=data['name']).first()
    if existing_amenity:
        abort(409, description="Amenity name must be unique")
    
    new_amenity = Amenity(name=data['name'])
    db.session.add(new_amenity)
    db.session.commit()
    
    return jsonify(new_amenity.serialize()), 201

@amenity_api.route('/amenities', methods=['GET'])
def get_amenities():
    amenities = Amenity.query.all()
    return jsonify([amenity.serialize() for amenity in amenities]), 200

@amenity_api.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")
    return jsonify(amenity.serialize()), 200

@amenity_api.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Missing required field: name")
    
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")
    
    existing_amenity = Amenity.query.filter(Amenity.name == data['name'], Amenity.id != amenity_id).first()
    if existing_amenity:
        abort(409, description="Amenity name must be unique")
    
    amenity.name = data['name']
    db.session.commit()
    
    return jsonify(amenity.serialize()), 200

@amenity_api.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = Amenity.query.get(amenity_id)
    if not amenity:
        abort(404, description="Amenity not found")
    
    db.session.delete(amenity)
    db.session.commit()
    
    return '', 204
