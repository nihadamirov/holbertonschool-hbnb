from .BaseClass import BaseClass

class Country(BaseClass):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.cities = []

    def add_city(self, city):
        self.cities.append(city)
