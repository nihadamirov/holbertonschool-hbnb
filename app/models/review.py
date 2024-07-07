from datetime import datetime
from app import db  

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, place_id, user_id, text, rating):
        self.place_id = place_id
        self.user_id = user_id
        self.text = text
        self.rating = rating

    @classmethod
    def find_by_id(cls, review_id):
        return cls.query.get(review_id)

    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_place_id(cls, place_id):
        return cls.query.filter_by(place_id=place_id).all()

    @classmethod
    def all(cls):
        return cls.query.all()

    def update(self, text, rating):
        self.text = text
        self.rating = rating
        self.updated_at = datetime.utcnow()
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f"<Review {self.id}>"
