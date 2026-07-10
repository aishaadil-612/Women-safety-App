import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from geopy.geocoders import Nominatim
import time
import json
df= pd.read_csv('india_district_crime_2014_2023_30k.csv')
coords_df = pd.read_csv("district_coordinates.csv")
merged_df = df.merge(
    coords_df,
    on="District",
    how="left"
)
print(df.columns.tolist())
print(df.info())
print(df.tail())
print(df.head())
print(df.shape)
null = df.isnull().sum()
print(null)
dulpicates=df.duplicated().sum()
print(dulpicates)
df = df.drop_duplicates()
print(df.dtypes)
df['District'].str.strip().str.title()
df['Safety_Score'] = 100 - (
    df['Crime_Rate_per_100k'] /
    df['Crime_Rate_per_100k'].max()
) * 100
def risk_level(score):
    if score >= 70:
        return "High Risk"
    elif score >= 40:
        return "Medium Risk"
    else:
        return "Low Risk"
df['Risk_Level'] = merged_df['Crime_Rate_per_100k'].apply(risk_level)
print(df.head())
print(df.columns.tolist())

crime_risk = merged_df.groupby('Crime_Type')['Crime_Rate_per_100k'].mean()
print(crime_risk.sort_values(ascending=False))
rape_df = merged_df[df['Crime_Type'] == 'Rape']


yearly_risk = rape_df.groupby('Year')['Crime_Rate_per_100k'].mean()

print(yearly_risk)
yearly_risk.plot(marker='o')
plt.title('Rape Crime Rate Trend ')
plt.ylabel('Crime Rate per 100k')
plt.show()
print(coords_df.columns.tolist())
print(coords_df.head())
# plt.imsave("crime_rate.png")


# print(df['District'].unique())




# df = df.merge(coords_df, on="District", how="left")
print(merged_df.columns.tolist())

state_risk = merged_df.groupby('State')['Crime_Rate_per_100k'].mean().reset_index()
print(state_risk.head())
with open("IND_ADM1.geojson", "r", encoding="utf-8") as f:
    india_geo = json.load(f)
def risk_level(rate):
    if rate >= 22:
        return "High"
    elif rate >= 20:
        return "Medium"
    else:
        return "Low"
merged_df['Risk_Level'] = merged_df['Crime_Rate_per_100k'].apply(risk_level)

state_risk['Risk_Level'] = state_risk['Crime_Rate_per_100k'].apply(risk_level)
print("yeu",state_risk[['State', 'Crime_Rate_per_100k', 'Risk_Level']])
print("yoooo",state_risk['Risk_Level'].value_counts())
risk_dict ={
    "Uttar Pradesh": "High",
    "Rājasthān": "Medium",
    "Maharashtra": "High",
    "Madhya Pradesh": "Medium",
    "West Bengal": "High",
    "Odisha": "Low",
    "Delhi": "Medium",
    "Assam": "Low",
    "Haryāna": "High",
    "Bihār": "High",
    "Jhārkhand": "Medium",
    "Andhra Pradesh": "Low",
    "Telangāna": "Medium",
    "Chhattīsgarh": "Low",
    "Karnātaka": "High",
    "Gujarāt": "Medium",
    "Tamil Nādu": "High",
    "Punjab": "High",
    "Uttarākhand": "Low",
    "Himāchal Pradesh": "Low",
    "Kerala": "Medium",
    "Goa": "Low",
    "Tripura": "Low",
    "Meghālaya": "Low",
    "Manipur": "Medium",
    "Nāgāland": "Low",
    "Arunāchal Pradesh": "Low",
    "Mizoram": "Low",
    "Sikkim": "Low",
    "Jammu and Kashmīr": "Medium",
    "Chandīgarh": "Low",
    "Puducherry": "Low"
}# dict(
#     zip(
#         state_risk['State'],
#         state_risk['Risk_Level']
#     )
# )
print(state_risk.columns)
print(state_risk.head())
print(india_geo['features'][0]['properties'])

def get_color(state_name):
    risk = risk_dict.get(state_name, "Low")

    if  risk == "High":
        return "red"

    elif risk == "Medium":
        return "yellow"

    else:
        return "green"
import folium

india_map = folium.Map(
    location=[22.5, 78.9],
    zoom_start=5
)

folium.GeoJson(
    india_geo,
    style_function=lambda feature: {
        'fillColor': get_color(
            feature['properties']['shapeName']
        ),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['shapeName'],
        aliases=['State:']
    )
).add_to(india_map)

india_map.save("static/india_risk_map.html")
max_rate = merged_df['Crime_Rate_per_100k'].max()

merged_df['Safety_Score'] = 100 - (
    merged_df['Crime_Rate_per_100k'] / max_rate
) * 100

high_risk = (
    merged_df.groupby('State')['Crime_Rate_per_100k']
      .mean()
      .sort_values(ascending=False)
      .head(10)
)
high_risk = (
   merged_df.groupby('State')['Crime_Rate_per_100k']
      .mean()
      .sort_values(ascending=False)
      .head(10)
)

merged_df.to_csv("women_safety_data.csv")


