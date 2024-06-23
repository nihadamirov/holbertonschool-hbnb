from flask import Flask
from app.api.v1.users import user_api
from app.api.v1.countries import country_api
from app.api.v1.cities import city_api
from app.api.v1.reviews import review_api
from app.api.v1.amenities import amenity_api

app = Flask(__name__)

app.register_blueprint(user_api, url_prefix='/api/v1')
app.register_blueprint(country_api, url_prefix='/api/v1')
app.register_blueprint(city_api, url_prefix='/api/v1')
app.register_blueprint(amenity_api, url_prefix='/api/v1')
app.register_blueprint(review_api, url_prefix='/api/v1')

if __name__ == "__main__":
    app.run(debug=True)
