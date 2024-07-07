from app import db
from datetime import datetime

class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    cities = db.relationship('City', backref='country', lazy=True)

    def __init__(self, name):
        self.name = name

    def add_city(self, city):
        if city not in self.cities:
            self.cities.append(city)

    def __repr__(self):
        return f"<Country {self.id}: {self.name}>"
