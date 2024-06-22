from BaseClass import BaseClass

class Review(BaseClass):
    def __init__(self, place_id, user_id, text, rating):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.text = text
        self.rating = rating
