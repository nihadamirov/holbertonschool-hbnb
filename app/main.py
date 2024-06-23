from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields, Namespace
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import blueprints and models from your application structure
from app.api.vi.users import user_api
from app.api.vi.countries import country_api
from app.api.vi.cities import city_api
from app.api.vi.reviews import reviews_bp
from app.api.vi.amenities import amenity_api

# Initialize Flask application
app = Flask(__name__)

# Register blueprints for different API endpoints
app.register_blueprint(user_api, url_prefix='/api/v1/users')
app.register_blueprint(country_api, url_prefix='/api/v1/countries')
app.register_blueprint(city_api, url_prefix='/api/v1/cities')
app.register_blueprint(reviews_bp, url_prefix='/api/v1/reviews')
app.register_blueprint(amenity_api, url_prefix='/api/v1/amenities')

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define models for SQLAlchemy
class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)

class Amenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    city = db.relationship('City', backref=db.backref('places', lazy=True))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    host_id = db.Column(db.Integer)
    number_of_rooms = db.Column(db.Integer)
    number_of_bathrooms = db.Column(db.Integer)
    price_per_night = db.Column(db.Float)
    max_guests = db.Column(db.Integer)
    amenities = db.relationship('Amenity', secondary='place_amenity', lazy='subquery',
                                backref=db.backref('places', lazy=True))

class PlaceAmenity(db.Model):
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), primary_key=True)
    amenity_id = db.Column(db.Integer, db.ForeignKey('amenity.id'), primary_key=True)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

# Define namespaces for Flask-Restx
places_ns = Namespace('places', description='Places endpoints')
reviews_ns = Namespace('reviews', description='Reviews endpoints')

# Serialization models
place_model = places_ns.model('Place', {
    'name': fields.String(required=True, description='Place name'),
    'description': fields.String(description='Place description'),
    'address': fields.String(description='Place address'),
    'city_id': fields.Integer(required=True, description='City ID'),
    'latitude': fields.Float(description='Latitude coordinate'),
    'longitude': fields.Float(description='Longitude coordinate'),
    'host_id': fields.Integer(description='Host ID'),
    'number_of_rooms': fields.Integer(description='Number of rooms'),
    'number_of_bathrooms': fields.Integer(description='Number of bathrooms'),
    'price_per_night': fields.Float(description='Price per night'),
    'max_guests': fields.Integer(description='Maximum number of guests'),
    'amenity_ids': fields.List(fields.Integer, description='List of amenity IDs')
})

review_model = reviews_ns.model('Review', {
    'user_id': fields.Integer(required=True, description='User ID'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'comment': fields.String(description='Review comment')
})

# Routes for Places Management Endpoints
@places_ns.route('/places')
class PlacesList(Resource):
    @places_ns.marshal_with(place_model, envelope='places')
    def get(self):
        """Retrieve all places"""
        places = Place.query.all()
        return places, 200

    @places_ns.expect(place_model)
    @places_ns.marshal_with(place_model, code=201)
    def post(self):
        """Create a new place"""
        data = request.json
        try:
            place = Place(
                name=data['name'],
                description=data.get('description'),
                address=data.get('address'),
                city_id=data['city_id'],
                latitude=data.get('latitude'),
                longitude=data.get('longitude'),
                host_id=data.get('host_id'),
                number_of_rooms=data.get('number_of_rooms'),
                number_of_bathrooms=data.get('number_of_bathrooms'),
                price_per_night=data.get('price_per_night'),
                max_guests=data.get('max_guests')
            )
            if 'amenity_ids' in data:
                amenities = Amenity.query.filter(Amenity.id.in_(data['amenity_ids'])).all()
                place.amenities.extend(amenities)
            
            db.session.add(place)
            db.session.commit()
            return place, 201
        except KeyError as e:
            return {'message': f'Missing required field: {str(e)}'}, 400
        except exc.IntegrityError:
            db.session.rollback()
            return {'message': 'Invalid city_id or amenity_ids provided.'}, 400

@places_ns.route('/places/<int:place_id>')
class PlaceDetail(Resource):
    @places_ns.marshal_with(place_model)
    def get(self, place_id):
        """Retrieve details of a specific place"""
        place = Place.query.get_or_404(place_id)
        return place, 200

    @places_ns.expect(place_model)
    @places_ns.marshal_with(place_model)
    def put(self, place_id):
        """Update a specific place"""
        data = request.json
        place = Place.query.get_or_404(place_id)
        try:
            place.name = data['name']
            place.description = data.get('description')
            place.address = data.get('address')
            place.city_id = data['city_id']
            place.latitude = data.get('latitude')
            place.longitude = data.get('longitude')
            place.host_id = data.get('host_id')
            place.number_of_rooms = data.get('number_of_rooms')
            place.number_of_bathrooms = data.get('number_of_bathrooms')
            place.price_per_night = data.get('price_per_night')
            place.max_guests = data.get('max_guests')

            if 'amenity_ids' in data:
                amenities = Amenity.query.filter(Amenity.id.in_(data['amenity_ids'])).all()
                place.amenities.clear()
                place.amenities.extend(amenities)
            
            db.session.commit()
            return place, 200
        except KeyError as e:
            return {'message': f'Missing required field: {str(e)}'}, 400
        except exc.IntegrityError:
            db.session.rollback()
            return {'message': 'Invalid city_id or amenity_ids provided.'}, 400

    @places_ns.response(204, 'Place deleted successfully')
    def delete(self, place_id):
        """Delete a specific place"""
        place = Place.query.get_or_404(place_id)
        db.session.delete(place)
        db.session.commit()
        return '', 204

# Routes for Review Management Endpoints
@reviews_ns.route('/places/<int:place_id>/reviews')
class PlaceReviews(Resource):
    @reviews_ns.marshal_with(review_model, envelope='reviews')
    def post(self, place_id):
        """Create a new review for a place"""
        data = request.json
        place = Place.query.get_or_404(place_id)
        try:
            review = Review(
                user_id=data['user_id'],
                place_id=place_id,
                rating=data['rating'],
                comment=data.get('comment')
            )
            db.session.add(review)
            db.session.commit()
            return review, 201
        except KeyError as e:
            return {'message': f'Missing required field: {str(e)}'}, 400
        except exc.IntegrityError:
            db.session.rollback()
            return {'message': 'Invalid user_id provided.'}, 400

@reviews_ns.route('/users/<int:user_id>/reviews')
class UserReviews(Resource):
    @reviews_ns.marshal_with(review_model, envelope='reviews')
    def get(self, user_id):
        """Retrieve all reviews written by a specific user"""
        reviews = Review.query.filter_by(user_id=user_id).all()
        return reviews, 200

@reviews_ns.route('/places/<int:place_id>/reviews')
class PlaceReviews(Resource):
    @reviews_ns.marshal_with(review_model, envelope='reviews')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        reviews = Review.query.filter_by(place_id=place_id).all()
        return reviews, 200

@reviews_ns.route('/reviews/<int:review_id>')
class ReviewDetail(Resource):
    @reviews_ns.marshal_with(review_model)
    def get(self, review_id):
        """Retrieve details of a specific review"""
        review = Review.query.get_or_404(review_id)
        return review, 200

    @reviews_ns.expect(review_model)
    @reviews_ns.marshal_with(review_model)
    def put(self, review_id):
        """Update a specific review"""
        data = request.json
        review = Review.query.get_or_404(review_id)
        try:
            review.user_id = data['user_id']
            review.rating = data['rating']
            review.comment = data.get('comment')
            db.session.commit()
            return review, 200
        except KeyError as e:
            return {'message': f'Missing required field: {str(e)}'}, 400
        except exc.IntegrityError:
            db.session.rollback()
            return {'message': 'Invalid user_id provided.'}, 400

if __name__ == "__main__":
    app.run(debug=True)

