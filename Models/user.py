from .BaseClass import BaseClass

class User(BaseClass):
    def __init__(self, email, password, first_name, last_name):
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.reviews = []
        self.places = []

    def add_place(self, place):
        self.places.append(place)

    def add_review(self, review):
        self.reviews.append(review)
