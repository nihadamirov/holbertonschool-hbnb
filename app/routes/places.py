# app/routes/places.py
from flask import Blueprint, request, jsonify
from app.models import Place, City, Amenity
from app import db
from app.schemas import PlaceSchema

places_bp = Blueprint('places', __name__, url_prefix='/places')

place_schema = PlaceSchema()

@places_bp.route('/', methods=['POST'])
def create_place():
    data = request.json

    # Validation
    errors = place_schema.validate(data)
    if errors:
        return jsonify({'message': 'Validation Error', 'errors': errors}), 400

    # Check if city_id exists
    city = City.query.get(data['city_id'])
    if not city:
        return jsonify({'message': 'City not found', 'errors': {'city_id': 'City does not exist'}}), 404

    # Check if amenity_ids are valid
    amenities = Amenity.query.filter(Amenity.id.in_(data.get('amenity_ids', []))).all()
    if len(amenities) != len(data.get('amenity_ids', [])):
        return jsonify({'message': 'Invalid amenity IDs', 'errors': {'amenity_ids': 'One or more amenities do not exist'}}), 400

    # Create new place
    new_place = Place(
        name=data['name'],
        description=data['description'],
        address=data['address'],
        city_id=data['city_id'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        host_id=data['host_id'],
        number_of_rooms=data['number_of_rooms'],
        number_of_bathrooms=data['number_of_bathrooms'],
        price_per_night=data['price_per_night'],
        max_guests=data['max_guests'],
        amenities=amenities
    )

    db.session.add(new_place)
    db.session.commit()

    return jsonify({'message': 'Place created successfully', 'place': place_schema.dump(new_place)}), 201

@places_bp.route('/', methods=['GET'])
def get_all_places():
    places = Place.query.all()
    return jsonify({'places': place_schema.dump(places, many=True)})

@places_bp.route('/<int:place_id>', methods=['GET'])
def get_place(place_id):
    place = Place.query.get_or_404(place_id)
    return jsonify({'place': place_schema.dump(place)})

@places_bp.route('/<int:place_id>', methods=['PUT'])
def update_place(place_id):
    place = Place.query.get_or_404(place_id)
    data = request.json

    # Validation
    errors = place_schema.validate(data, partial=True)
    if errors:
        return jsonify({'message': 'Validation Error', 'errors': errors}), 400

    # Update place
    for field in place_schema.fields:
        if field in data:
            setattr(place, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Place updated successfully', 'place': place_schema.dump(place)})

@places_bp.route('/<int:place_id>', methods=['DELETE'])
def delete_place(place_id):
    place = Place.query.get_or_404(place_id)
    db.session.delete(place)
    db.session.commit()
    return jsonify({'message': 'Place deleted successfully'}), 204
