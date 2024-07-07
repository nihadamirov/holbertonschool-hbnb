from datetime import datetime
from app import db 

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
    reviews = db.relationship('Review', backref='place', lazy=True)

    def __init__(self, name, description, address, city_id, latitude, longitude, host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests):
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.max_guests = max_guests

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        self.reviews.append(review)

    def __repr__(self):
        return f"<Place {self.id}: {self.name}>"
