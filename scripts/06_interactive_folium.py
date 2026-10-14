"""
06_interactive_folium.py - Interactive Visual Analytics using Folium
Maps launch sites, clusters missions by landing outcome, and analyzes infrastructure proximity.
"""

import os
import folium
from folium.plugins import MarkerCluster
import pandas as pd

os.makedirs('maps', exist_ok=True)
df_geo = pd.read_csv('data/spacex_launch_geo.csv')

launch_sites = {
    'CCAFS LC-40': [28.562302, -80.577356],
    'CCAFS SLC-40': [28.563197, -80.576820],
    'KSC LC-39A': [28.573255, -80.646895],
    'VAFB SLC-4E': [34.632834, -120.610745]
}

site_map = folium.Map(location=[28.562302, -80.577356], zoom_start=5)
marker_cluster = MarkerCluster().add_to(site_map)

# Add launch markers
for _, row in df_geo.iterrows():
    color = 'green' if row['class'] == 1 else 'red'
    folium.Marker(
        location=[row['Lat'], row['Long']],
        icon=folium.Icon(color=color, icon='info-sign'),
        popup=f"{row['Launch Site']} | Flight {row['Flight Number']} | Outcome: {row['class']}"
    ).add_to(marker_cluster)

# Add launch site circles
for site, coord in launch_sites.items():
    folium.Circle(coord, radius=1000, color='#0284C7', fill=True, fill_color='#0284C7', fill_opacity=0.3).add_to(site_map)
    folium.Marker(
        coord,
        icon=folium.DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12px; font-weight: bold; color: #1E3A8A;">{site}</div>'
        )
    ).add_to(site_map)

# Proximity lines from KSC LC-39A to Coastline, Highway, City
ksc_coord = [28.573255, -80.646895]
coast_coord = [28.5732, -80.5677]
city_coord = [28.6123, -80.8077]

folium.PolyLine([ksc_coord, coast_coord], color='blue', weight=2.5, opacity=0.8).add_to(site_map)
folium.PolyLine([ksc_coord, city_coord], color='green', weight=2.5, opacity=0.8).add_to(site_map)

output_html = 'maps/spacex_interactive_map.html'
site_map.save(output_html)
print(f"Saved interactive map: {output_html}")
