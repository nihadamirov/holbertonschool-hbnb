import json

countries = [
    {"code": "US", "name": "United States"},
    {"code": "CA", "name": "Canada"},
    {"code": "GB", "name": "United Kingdom"},
    # Add more countries as needed
]

with open('countries.json', 'w') as f:
    json.dump(countries, f)
