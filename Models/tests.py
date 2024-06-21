import unittest
from user import User
from place import Place
from review import Review
from city import City
from country import Country
from amenity import Amenity

class TestModels(unittest.TestCase):

    def test_user_creation(self):
        user = User(email="test@example.com", password="pass", first_name="Ali", last_name="Aliyev")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.first_name, "Ali")
        self.assertEqual(user.last_name, "Aliyev")
        self.assertIsNotNone(user.id)
        self.assertIsNotNone(user.created_at)
        self.assertIsNotNone(user.updated_at)

    def test_user_unique_email(self):
        user1 = User(email="unique@example.com", password="pass", first_name="Ali", last_name="Aliyev")
        with self.assertRaises(ValueError):
            user2 = User(email="unique@example.com", password="pass", first_name="Nara", last_name="Zamanova")

    def test_place_creation(self):
        host = User(email="host@example.com", password="pass", first_name="Host", last_name="User")
        place = Place(
            name="Nice Place",
            description="A very nice place",
            address="123 Main St",
            city_id=1,
            latitude=50.0,
            longitude=8.0,
            host=host,
            number_of_rooms=3,
            number_of_bathrooms=2,
            price_per_night=100.0,
            max_guests=4
        )
        self.assertEqual(place.name, "Nice Place")
        self.assertEqual(place.description, "A very nice place")
        self.assertEqual(place.address, "123 Main St")
        self.assertEqual(place.latitude, 50.0)
        self.assertEqual(place.longitude, 8.0)
        self.assertEqual(place.host, host)

    def test_amenity_addition(self):
        place = Place(
            name="Nice Place",
            description="A very nice place",
            address="123 Main St",
            city_id=1,
            latitude=50.0,
            longitude=8.0,
            host=User(email="host2@example.com", password="pass", first_name="Host", last_name="User"),
            number_of_rooms=3,
            number_of_bathrooms=2,
            price_per_night=100.0,
            max_guests=4
        )
        amenity = Amenity(name="Wi-Fi")
        place.add_amenity(amenity)
        self.assertIn(amenity, place.amenities)

    def test_review_creation(self):
        place = Place(
            name="Nice Place",
            description="A very nice place",
            address="123 Main St",
            city_id=1,
            latitude=50.0,
            longitude=8.0,
            host=User(email="host3@example.com", password="pass", first_name="Host", last_name="User"),
            number_of_rooms=3,
            number_of_bathrooms=2,
            price_per_night=100.0,
            max_guests=4
        )
        user = User(email="reviewer@example.com", password="pass", first_name="Reviewer", last_name="User")
        review = Review(place_id=place.id, user_id=user.id, text="Great place!", rating=5)
        place.add_review(review)
        self.assertIn(review, place.reviews)

    def test_city_and_country(self):
        country = Country(name="Wonderland")
        city = City(name="DreamCity", country_id=country.id)
        country.add_city(city)
        self.assertIn(city, country.cities)

if __name__ == "__main__":
    unittest.main()
