"""
05_eda_visualization.py - Exploratory Data Analysis with Visualization
Generates all 6 required EDA figures using Seaborn & Matplotlib.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs('figures', exist_ok=True)
sns.set_theme(style='whitegrid')
df = pd.read_csv('data/dataset_part_2.csv')

# 1. Flight Number vs Launch Site
plt.figure(figsize=(10, 5), dpi=300)
sns.scatterplot(data=df, x='FlightNumber', y='LaunchSite', hue='Class', palette={0: '#EF4444', 1: '#10B981'}, s=100)
plt.title('Flight Number vs. Launch Site by Landing Outcome')
plt.savefig('figures/flight_vs_launch_site.png', dpi=300)
plt.close()

# 2. Payload Mass vs Launch Site
plt.figure(figsize=(10, 5), dpi=300)
sns.scatterplot(data=df, x='PayloadMass', y='LaunchSite', hue='Class', palette={0: '#EF4444', 1: '#10B981'}, s=100)
plt.title('Payload Mass vs. Launch Site by Landing Outcome')
plt.savefig('figures/payload_vs_launch_site.png', dpi=300)
plt.close()

# 3. Success Rate vs Orbit Type
orbit_success = df.groupby('Orbit')['Class'].mean().reset_index().sort_values(by='Class', ascending=False)
plt.figure(figsize=(10, 5), dpi=300)
sns.barplot(data=orbit_success, x='Orbit', y='Class', palette='Blues_r')
plt.title('Landing Success Rate by Orbit Type')
plt.ylim(0, 1.1)
plt.savefig('figures/success_rate_vs_orbit.png', dpi=300)
plt.close()

# 4. Flight Number vs Orbit
plt.figure(figsize=(10, 5), dpi=300)
sns.scatterplot(data=df, x='FlightNumber', y='Orbit', hue='Class', palette={0: '#EF4444', 1: '#10B981'}, s=100)
plt.title('Flight Number vs. Orbit Type')
plt.savefig('figures/flight_vs_orbit.png', dpi=300)
plt.close()

# 5. Payload vs Orbit
plt.figure(figsize=(10, 5), dpi=300)
sns.scatterplot(data=df, x='PayloadMass', y='Orbit', hue='Class', palette={0: '#EF4444', 1: '#10B981'}, s=100)
plt.title('Payload Mass vs. Orbit Type')
plt.savefig('figures/payload_vs_orbit.png', dpi=300)
plt.close()

# 6. Yearly Success Trend
df['Year'] = pd.to_datetime(df['Date']).dt.year
yearly_success = df.groupby('Year')['Class'].mean().reset_index()
plt.figure(figsize=(10, 5), dpi=300)
plt.plot(yearly_success['Year'], yearly_success['Class'], marker='o', linewidth=2.5, color='#0284C7')
plt.title('Yearly Launch Success Rate Trend (2010 - 2020)')
plt.ylim(-0.05, 1.1)
plt.savefig('figures/yearly_success_trend.png', dpi=300)
plt.close()

print("All EDA visualization figures generated and saved.")
