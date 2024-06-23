import sys
import os
from flask import Flask

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.vi.users import user_api
from app.api.vi.countries import country_api
from app.api.vi.cities import city_api
from app.api.vi.reviews import reviews_bp 
from app.api.vi.amenities import amenity_api

app = Flask(__name__)

app.register_blueprint(user_api, url_prefix='/api/v1/users')
app.register_blueprint(country_api, url_prefix='/api/v1/countries')
app.register_blueprint(city_api, url_prefix='/api/v1/cities')
app.register_blueprint(reviews_bp, url_prefix='/api/v1/reviews') 
app.register_blueprint(amenity_api, url_prefix='/api/v1/amenities')

if __name__ == "__main__":
    app.run(debug=True)
