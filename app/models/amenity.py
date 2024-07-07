from app import db
from datetime import datetime

class Amenity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Amenity {self.id}: {self.name}>"
