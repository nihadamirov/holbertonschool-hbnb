from app import db
from datetime import datetime

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    country = db.relationship('Country', backref=db.backref('cities', lazy=True))
    places = db.relationship('Place', backref='city', lazy=True)

    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id

    def add_place(self, place):
        if place not in self.places:
            self.places.append(place)

    def __repr__(self):
        return f"<City {self.id}: {self.name}, Country: {self.country.name}>"
