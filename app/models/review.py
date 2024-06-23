from app.models.BaseClass import BaseClass

class Review(BaseClass):
    def __init__(self, place_id, user_id, text, rating):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.text = text
        self.rating = rating

    @staticmethod
    def find_by_id(review_id):
        for review in Review._reviews:
            if review.id == review_id:
                return review
        return None

    @staticmethod
    def find_by_user_id(user_id):
        return [review for review in Review._reviews if review.user_id == user_id]

    @staticmethod
    def find_by_place_id(place_id):
        return [review for review in Review._reviews if review.place_id == place_id]

    @staticmethod
    def all():
        return Review._reviews

    def update(self, text, rating):
        self.text = text
        self.rating = rating
        self.updated_at = datetime.datetime.now()

    def delete(self):
        Review._reviews.remove(self)
