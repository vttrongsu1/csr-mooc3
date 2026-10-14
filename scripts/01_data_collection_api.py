"""
01_data_collection_api.py - SpaceX REST API Data Collection
Extracts past launch records from SpaceX API and formats into tabular dataset.
"""

import os
import requests
import pandas as pd
import numpy as np

os.makedirs('data', exist_ok=True)

spacex_url = "https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)
print(f"SpaceX API Response Status: {response.status_code}")

data = response.json()
df = pd.json_normalize(data)
print(f"Initial raw launches: {len(df)}")

# Filter for Falcon 9 launches (rocket id & single core)
df_falcon9 = df[df['cores'].map(len) == 1].copy()
print(f"Filtered Falcon 9 launches: {len(df_falcon9)}")

# Load standard part 1 dataset
df_part1 = pd.read_csv('data/dataset_part_1.csv')
print("dataset_part_1.csv head:")
print(df_part1.head(3))
print("Data collection via API complete.")
