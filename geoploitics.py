from geopy.geocoders import Nominatim
import pandas as pd
import time
df=pd.read_csv("india_district_crime_2014_2023_30k.csv")

geolocator = Nominatim(user_agent="women_safety_app")

districts = df['District'].unique()

locations = []

for district in districts:
    try:
        location = geolocator.geocode(f"{district}, India")

        if location:
            locations.append({
                "District": district,
                "Latitude": location.latitude,
                "Longitude": location.longitude
            })

        print(f"Done: {district}")

        time.sleep(1)

    except Exception as e:
        print(f"Error with {district}: {e}")

location_df = pd.DataFrame(locations)

location_df.to_csv("district_coordinates.csv", index=False)