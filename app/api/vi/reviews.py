from flask import Blueprint, request, jsonify, abort
from app import db
from app.models.review import Review
from app.models.user import User
from app.models.place import Place

reviews_bp = Blueprint('reviews_api', __name__, url_prefix='/reviews')

@reviews_bp.route('/places/<int:place_id>/reviews', methods=['POST'])
def create_review(place_id):
    data = request.get_json()
    if not data or 'user_id' not in data or 'text' not in data or 'rating' not in data:
        abort(400, 'user_id, text, and rating are required')
    if not (1 <= data['rating'] <= 5):
        abort(400, 'Rating must be between 1 and 5')
    user = User.query.get(data['user_id'])
    place = Place.query.get(place_id)
    if not user:
        abort(404, 'User not found')
    if not place:
        abort(404, 'Place not found')
    if place.host_id == data['user_id']:
        abort(400, 'Hosts cannot review their own place')

    new_review = Review(place_id=place_id, user_id=data['user_id'], text=data['text'], rating=data['rating'])
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.serialize()), 201

@reviews_bp.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_reviews_by_user(user_id):
    reviews = Review.query.filter_by(user_id=user_id).all()
    if not reviews:
        abort(404, 'No reviews found')
    return jsonify([review.serialize() for review in reviews])

@reviews_bp.route('/places/<int:place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    reviews = Review.query.filter_by(place_id=place_id).all()
    if not reviews:
        abort(404, 'No reviews found')
    return jsonify([review.serialize() for review in reviews])

@reviews_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        abort(404, 'Review not found')
    return jsonify(review.serialize())

@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        abort(404, 'Review not found')

    data = request.get_json()
    if not data or 'text' not in data or 'rating' not in data:
        abort(400, 'text and rating are required')
    if not (1 <= data['rating'] <= 5):
        abort(400, 'Rating must be between 1 and 5')

    review.text = data['text']
    review.rating = data['rating']
    db.session.commit()
    return jsonify(review.serialize())

@reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if not review:
        abort(404, 'Review not found')
    db.session.delete(review)
    db.session.commit()
    return '', 204
