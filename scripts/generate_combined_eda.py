import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

df2 = pd.read_csv('data/dataset_part_2.csv')
sns.set_theme(style='whitegrid')
fig, axs = plt.subplots(2, 2, figsize=(14, 8.5), dpi=300)

# 1. Flight vs Site
sns.scatterplot(data=df2, x='FlightNumber', y='LaunchSite', hue='Class', palette={0: '#EF4444', 1: '#10B981'}, s=100, ax=axs[0, 0])
axs[0, 0].set_title('1. Flight Number vs. Launch Site', fontsize=12, fontweight='bold')
axs[0, 0].legend(title='Outcome', labels=['Fail (0)', 'Success (1)'], loc='center right')

# 2. Payload vs Site
sns.scatterplot(data=df2, x='PayloadMass', y='LaunchSite', hue='Class', palette={0: '#EF4444', 1: '#10B981'}, s=100, ax=axs[0, 1])
axs[0, 1].set_title('2. Payload Mass (kg) vs. Launch Site', fontsize=12, fontweight='bold')
axs[0, 1].legend(title='Outcome', labels=['Fail (0)', 'Success (1)'], loc='center right')

# 3. Success by Orbit
orbit_success = df2.groupby('Orbit')['Class'].mean().reset_index().sort_values(by='Class', ascending=False)
sns.barplot(data=orbit_success, x='Orbit', y='Class', palette='Blues_r', ax=axs[1, 0])
axs[1, 0].set_title('3. Landing Success Rate by Orbit Type', fontsize=12, fontweight='bold')
axs[1, 0].set_ylim(0, 1.15)
for p in axs[1, 0].patches:
    h = p.get_height()
    axs[1, 0].annotate(f'{h:.0%}', (p.get_x() + p.get_width()/2., h), ha='center', va='bottom', fontsize=8, fontweight='bold')

# 4. Yearly Trend
df2['Year'] = pd.to_datetime(df2['Date']).dt.year
yearly = df2.groupby('Year')['Class'].mean().reset_index()
axs[1, 1].plot(yearly['Year'], yearly['Class'], marker='o', linewidth=2.5, color='#0284C7')
axs[1, 1].fill_between(yearly['Year'], yearly['Class'], alpha=0.15, color='#0284C7')
axs[1, 1].set_title('4. Yearly Launch Success Rate Trend (2010-2020)', fontsize=12, fontweight='bold')
axs[1, 1].set_ylim(-0.05, 1.1)
axs[1, 1].set_xticks(yearly['Year'])
for _, r in yearly.iterrows():
    val = r['Class']
    axs[1, 1].annotate(f'{val:.0%}', (r['Year'], val), ha='center', va='bottom', xytext=(0, 4), textcoords='offset points', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('figures/eda_visualizations_combined.png', dpi=300)
plt.close()
print("Saved figures/eda_visualizations_combined.png successfully.")
