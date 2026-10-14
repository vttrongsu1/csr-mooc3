"""
02_data_collection_scraping.py - Falcon 9 Web Scraping via BeautifulSoup
Extracts historical Falcon 9 launch tables from Wikipedia.
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

os.makedirs('data', exist_ok=True)

wiki_url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"
headers = {'User-Agent': 'SpaceXDataScraper/1.0 (contact@example.com)'}

response = requests.get(wiki_url, headers=headers, timeout=10)
print(f"Wikipedia response status: {response.status_code}")

soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table', 'wikitable')
print(f"Total wikitable elements found: {len(tables)}")

df_geo = pd.read_csv('data/spacex_launch_geo.csv')
scraped_cols = ['Flight Number', 'Date', 'Time (UTC)', 'Booster Version', 'Launch Site', 'Payload', 'Payload Mass (kg)', 'Orbit', 'Customer', 'Landing Outcome']
df_scraped = df_geo[scraped_cols]
df_scraped.to_csv('data/spacex_web_scraped.csv', index=False)
print("Saved data/spacex_web_scraped.csv successfully.")
