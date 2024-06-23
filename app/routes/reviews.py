from flask import Blueprint, request, jsonify
from app.models import Review, User, Place
from app import db
from app.schemas import ReviewSchema

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

review_schema = ReviewSchema()

@reviews_bp.route('/places/<int:place_id>/reviews', methods=['POST'])
def create_review(place_id):
    data = request.json
    data['place_id'] = place_id

    # Validation
    errors = review_schema.validate(data)
    if errors:
        return jsonify({'message': 'Validation Error', 'errors': errors}), 400

    # Check if place_id exists
    place = Place.query.get(place_id)
    if not place:
        return jsonify({'message': 'Place not found', 'errors': {'place_id': 'Place does not exist'}}), 404

    # Check if user_id exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'message': 'User not found', 'errors': {'user_id': 'User does not exist'}}), 404

    # Create new review
    new_review = Review(
        user_id=data['user_id'],
        place_id=data['place_id'],
        rating=data['rating'],
        comment=data['comment']
    )

    db.session.add(new_review)
    db.session.commit()

    return jsonify({'message': 'Review created successfully', 'review': review_schema.dump(new_review)}), 201

@reviews_bp.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_user_reviews(user_id):
    user = User.query.get_or_404(user_id)
    reviews = Review.query.filter_by(user_id=user_id).all()
    return jsonify({'reviews': review_schema.dump(reviews, many=True)})

@reviews_bp.route('/places/<int:place_id>/reviews', methods=['GET'])
def get_place_reviews(place_id):
    place = Place.query.get_or_404(place_id)
    reviews = Review.query.filter_by(place_id=place_id).all()
    return jsonify({'reviews': review_schema.dump(reviews, many=True)})

@reviews_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get_or_404(review_id)
    return jsonify({'review': review_schema.dump(review)})

@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    data = request.json

    # Validation
    errors = review_schema.validate(data, partial=True)
    if errors:
        return jsonify({'message': 'Validation Error', 'errors': errors}), 400

    # Update review
    for field in review_schema.fields:
        if field in data:
            setattr(review, field, data[field])

    db.session.commit()
    return jsonify({'message': 'Review updated successfully', 'review': review_schema.dump(review)})

@reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'}), 204
