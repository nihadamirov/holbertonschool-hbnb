from BaseClass import BaseClass

class City(BaseClass):
    def __init__(self, name, country_id):
        super().__init__()
        self.name = name
        self.country_id = country_id
        self.places = []

    def add_place(self, place):
        self.places.append(place)
