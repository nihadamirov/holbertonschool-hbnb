from flask import Blueprint, request, jsonify, abort
from uuid import uuid4
import json
import os

amenity_api = Blueprint('amenity_api', __name__)

if os.path.exists('amenities.json'):
    with open('amenities.json', 'r') as f:
        amenities = json.load(f)
else:
    amenities = []

def save_amenities():
    with open('amenities.json', 'w') as f:
        json.dump(amenities, f)

@amenity_api.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Missing required field: name")
    if any(amenity['name'] == data['name'] for amenity in amenities):
        abort(409, description="Amenity name must be unique")
    amenity = {
        'id': str(uuid4()),
        'name': data['name'],
        'created_at': "current_timestamp",
        'updated_at': "current_timestamp"
    }
    amenities.append(amenity)
    save_amenities()
    return jsonify(amenity), 201

@amenity_api.route('/amenities', methods=['GET'])
def get_amenities():
    return jsonify(amenities), 200

@amenity_api.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = next((a for a in amenities if a['id'] == amenity_id), None)
    if not amenity:
        abort(404, description="Amenity not found")
    return jsonify(amenity), 200

@amenity_api.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400, description="Missing required field: name")
    amenity = next((a for a in amenities if a['id'] == amenity_id), None)
    if not amenity:
        abort(404, description="Amenity not found")
    if any(a['name'] == data['name'] and a['id'] != amenity_id for a in amenities):
        abort(409, description="Amenity name must be unique")
    amenity['name'] = data['name']
    amenity['updated_at'] = "current_timestamp"
    save_amenities()
    return jsonify(amenity), 200

@amenity_api.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    global amenities
    amenities = [a for a in amenities if a['id'] != amenity_id]
    save_amenities()
    return '', 204
