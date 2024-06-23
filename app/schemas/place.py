from pydantic import BaseModel, validator
from typing import List

class PlaceSchema(BaseModel):
    name: str
    description: str
    address: str
    city_id: int
    latitude: float
    longitude: float
    host_id: int
    number_of_rooms: int
    number_of_bathrooms: int
    price_per_night: float
    max_guests: int
    amenity_ids: List[int] = []

    @validator('latitude', 'longitude')
    def coordinates_within_limits(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError('Coordinates must be within the range of -90 to 90')
        return v

    @validator('number_of_rooms', 'number_of_bathrooms', 'max_guests')
    def non_negative_integer(cls, v):
        if not isinstance(v, int) or v < 0:
            raise ValueError('Must be a non-negative integer')
        return v
