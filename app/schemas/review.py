from pydantic import BaseModel, validator
from app.models import User, Place

class ReviewSchema(BaseModel):
    user_id: int
    place_id: int
    rating: int
    comment: str

    @validator('rating')
    def check_rating_range(cls, v):
        if v < 1 or v > 5:
            raise ValueError('Rating must be between 1 and 5')
        return v
