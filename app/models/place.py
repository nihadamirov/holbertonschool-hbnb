from app.models.BaseClass import BaseClass

class Place(BaseClass):
    def __init__(self, name, description, address, city_id, latitude, longitude, host_id, number_of_rooms, number_of_bathrooms, price_per_night, max_guests):
        super().__init__()
        self.name = name
        self.description = description
        self.address = address
        self.city_id = city_id
        self.latitude = latitude
        self.longitude = longitude
        self.host_id = host_id
        self.number_of_rooms = number_of_rooms
        self.max_guests = max_guests
        self.number_of_bathrooms = number_of_bathrooms
        self.price_per_night = price_per_night
        self.amenities = []
        self.reviews = []

    def add_amenity(self, amenity):
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def add_review(self, review):
        self.reviews.append(review)
