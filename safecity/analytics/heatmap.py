import folium
from folium.plugins import HeatMap
import pandas as pd
import os

# Get absolute project path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "crdata.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "crime_hotspots.html")

df = pd.read_csv(DATA_PATH)

m = folium.Map(location=[19.0760, 72.8777], zoom_start=12)

heat_data = [[row["latitude"], row["longitude"]] for _, row in df.iterrows()]
HeatMap(heat_data).add_to(m)

m.save(OUTPUT_PATH)

print("Heatmap saved at:", OUTPUT_PATH)
