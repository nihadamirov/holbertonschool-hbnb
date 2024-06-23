from flask import Blueprint, request, jsonify, abort
from models.review import Review
from models.user import User
from models.place import Place

reviews_bp = Blueprint('reviews_api', __name__, url_prefix='/reviews')

@reviews_bp.route('/places/<int:place_id>/reviews', methods=['POST'])
def create_review(place_id):
    data = request.get_json()
    if 'user_id' not in data or 'text' not in data or 'rating' not in data:
        abort(400, 'user_id, text, and rating are required')
    if not (1 <= data['rating'] <= 5):
        abort(400, 'Rating must be between 1 and 5')
    if not User.find_by_id(data['user_id']):
        abort(404, 'User not found')
    if not Place.find_by_id(place_id):
        abort(404, 'Place not found')
    if Place.find_by_id(place_id).host_id == data['user_id']:
        abort(400, 'Hosts cannot review their own place')

    new_review = Review(place_id, data['user_id'], data['text'], data['rating'])
    return jsonify(id=new_review.id, place_id=new_review.place_id, user_id=new_review.user_id, text=new_review.text, rating=new_review.rating, created_at=new_review.created_at, updated_at=new_review.updated_at), 201

@reviews_bp.route('/users/<int:user_id>/reviews', methods=['GET'])
def get_reviews_by_user(user_id):
    reviews = Review.find_by_user_id(user_id)
    if not reviews:
        abort(404, 'No reviews found')
    return jsonify([{'id': review.id, 'place_id': review.place_id, 'user_id': review.user_id, 'text': review.text, 'rating': review.rating, 'created_at': review.created_at, 'updated_at': review.updated_at} for review in reviews])

@reviews_bp.route('/places/<int:place_id>/reviews', methods=['GET'])
def get_reviews_by_place(place_id):
    reviews = Review.find_by_place_id(place_id)
    if not reviews:
        abort(404, 'No reviews found')
    return jsonify([{'id': review.id, 'place_id': review.place_id, 'user_id': review.user_id, 'text': review.text, 'rating': review.rating, 'created_at': review.created_at, 'updated_at': review.updated_at} for review in reviews])

@reviews_bp.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.find_by_id(review_id)
    if not review:
        abort(404, 'Review not found')
    return jsonify({'id': review.id, 'place_id': review.place_id, 'user_id': review.user_id, 'text': review.text, 'rating': review.rating, 'created_at': review.created_at, 'updated_at': review.updated_at})

@reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = Review.find_by_id(review_id)
    if not review:
        abort(404, 'Review not found')

    data = request.get_json()
    if 'text' not in data or 'rating' not in data:
        abort(400, 'text and rating are required')
    if not (1 <= data['rating'] <= 5):
        abort(400, 'Rating must be between 1 and 5')

    review.update(data['text'], data['rating'])
    return jsonify({'id': review.id, 'place_id': review.place_id, 'user_id': review.user_id, 'text': review.text, 'rating': review.rating, 'created_at': review.created_at, 'updated_at': review.updated_at})

@reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.find_by_id(review_id)
    if not review:
        abort(404, 'Review not found')
    review.delete()
    return '', 204
