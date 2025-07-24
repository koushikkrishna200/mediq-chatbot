import os
import googlemaps
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Google Maps API with your API key
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_API_KEY'))

# Sample hospital data (you can replace this with actual data or connect to a database/API)
hospital_data = pd.DataFrame([
    {"hospital_name": "City Medical Center", "location": "New York", "specialty": "Cardiology", "rating": 4.5},
    {"hospital_name": "Sunrise Health", "location": "California", "specialty": "Orthopedics", "rating": 4.0},
    {"hospital_name": "Green Valley Hospital", "location": "Texas", "specialty": "Neurology", "rating": 4.7},
    {"hospital_name": "HealthPlus", "location": "Florida", "specialty": "Pediatrics", "rating": 4.3},
    {"hospital_name": "St. Joseph's Medical", "location": "Chicago", "specialty": "Cardiology", "rating": 4.6},
    # Add more hospitals here...
])

# Function to search hospitals by specialty or location
def search_hospitals(specialty=None, location=None):
    result = hospital_data
    if specialty:
        result = result[result["specialty"].str.contains(specialty, case=False, na=False)]
    if location:
        result = result[result["location"].str.contains(location, case=False, na=False)]
    return result

# Function to get nearby hospitals from Google Maps API
def get_nearby_hospitals(location, radius=5000, type='hospital'):
    # Geocode the location to get latitude and longitude
    geocode_result = gmaps.geocode(location)
    if geocode_result:
        lat, lng = geocode_result[0]['geometry']['location'].values()
    else:
        return pd.DataFrame()  # Return empty DataFrame if location not found
    
    # Search for hospitals within the specified radius
    places_result = gmaps.places_nearby((lat, lng), radius=radius, type=type)
    
    hospitals = []
    for place in places_result['results']:
        hospital_info = {
            "hospital_name": place["name"],
            "location": place["vicinity"],
            "rating": place.get("rating", "N/A"),
            "specialty": "General"  # You can refine this based on place types
        }
        hospitals.append(hospital_info)
    
    return pd.DataFrame(hospitals)

# Example usage: Search for hospitals in New York by specialty
# result = search_hospitals(specialty="Cardiology", location="New York")
# st.write(result)

# Example usage: Get nearby hospitals in New York
# nearby_hospitals = get_nearby_hospitals("New York, NY")
# st.write(nearby_hospitals)
