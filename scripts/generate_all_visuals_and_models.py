import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report

os.makedirs('figures', exist_ok=True)
os.makedirs('maps', exist_ok=True)
os.makedirs('data', exist_ok=True)

# -------------------------------------------------------------
# 1. LOAD DATASETS
# -------------------------------------------------------------
df2 = pd.read_csv('data/dataset_part_2.csv')
df3 = pd.read_csv('data/dataset_part_3.csv')
df_dash = pd.read_csv('data/spacex_launch_dash.csv')
df_geo = pd.read_csv('data/spacex_launch_geo.csv')
df_sql = pd.read_csv('data/Spacex.csv')

print("Loaded datasets successfully.")

# -------------------------------------------------------------
# 2. EDA VISUALIZATIONS
# -------------------------------------------------------------
sns.set_theme(style='whitegrid')
plt.rcParams.update({'font.sans-serif': 'DejaVu Sans', 'font.size': 11})

# Fig 1: Flight Number vs Launch Site
plt.figure(figsize=(10, 5), dpi=300)
sns.scatterplot(
    data=df2, x='FlightNumber', y='LaunchSite', hue='Class',
    palette={0: '#EF4444', 1: '#10B981'}, s=120, alpha=0.9
)
plt.title('Flight Number vs. Launch Site (Colored by Landing Outcome)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Flight Number', fontsize=11, fontweight='bold')
plt.ylabel('Launch Site', fontsize=11, fontweight='bold')
plt.legend(title='Outcome', labels=['Failure (0)', 'Success (1)'], loc='center right', frameon=True)
plt.tight_layout()
plt.savefig('figures/flight_vs_launch_site.png', dpi=300)
plt.close()

# Fig 2: Payload Mass vs Launch Site
plt.figure(figsize=(10, 5), dpi=300)
sns.scatterplot(
    data=df2, x='PayloadMass', y='LaunchSite', hue='Class',
    palette={0: '#EF4444', 1: '#10B981'}, s=120, alpha=0.9
)
plt.title('Payload Mass (kg) vs. Launch Site (Colored by Landing Outcome)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Payload Mass (kg)', fontsize=11, fontweight='bold')
plt.ylabel('Launch Site', fontsize=11, fontweight='bold')
plt.legend(title='Outcome', labels=['Failure (0)', 'Success (1)'], loc='center right', frameon=True)
plt.tight_layout()
plt.savefig('figures/payload_vs_launch_site.png', dpi=300)
plt.close()

# Fig 3: Success Rate vs Orbit Type
orbit_success = df2.groupby('Orbit')['Class'].mean().reset_index().sort_values(by='Class', ascending=False)
plt.figure(figsize=(10, 5), dpi=300)
bar_ax = sns.barplot(data=orbit_success, x='Orbit', y='Class', palette='Blues_r')
plt.title('Landing Success Rate by Orbit Type', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Orbit Type', fontsize=11, fontweight='bold')
plt.ylabel('Success Rate', fontsize=11, fontweight='bold')
plt.ylim(0, 1.15)
for p in bar_ax.patches:
    height = p.get_height()
    bar_ax.annotate(f'{height:.1%}', (p.get_x() + p.get_width() / 2., height),
                    ha='center', va='bottom', xytext=(0, 4), textcoords='offset points',
                    fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/success_rate_vs_orbit.png', dpi=300)
plt.close()

# Fig 4: Flight Number vs Orbit
plt.figure(figsize=(10, 5), dpi=300)
sns.scatterplot(
    data=df2, x='FlightNumber', y='Orbit', hue='Class',
    palette={0: '#EF4444', 1: '#10B981'}, s=120, alpha=0.9
)
plt.title('Flight Number vs. Orbit Type', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Flight Number', fontsize=11, fontweight='bold')
plt.ylabel('Orbit Type', fontsize=11, fontweight='bold')
plt.legend(title='Outcome', labels=['Failure (0)', 'Success (1)'], loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig('figures/flight_vs_orbit.png', dpi=300)
plt.close()

# Fig 5: Payload vs Orbit
plt.figure(figsize=(10, 5), dpi=300)
sns.scatterplot(
    data=df2, x='PayloadMass', y='Orbit', hue='Class',
    palette={0: '#EF4444', 1: '#10B981'}, s=120, alpha=0.9
)
plt.title('Payload Mass (kg) vs. Orbit Type', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Payload Mass (kg)', fontsize=11, fontweight='bold')
plt.ylabel('Orbit Type', fontsize=11, fontweight='bold')
plt.legend(title='Outcome', labels=['Failure (0)', 'Success (1)'], loc='lower right', frameon=True)
plt.tight_layout()
plt.savefig('figures/payload_vs_orbit.png', dpi=300)
plt.close()

# Fig 6: Yearly Success Trend
df2['Year'] = pd.to_datetime(df2['Date']).dt.year
yearly_success = df2.groupby('Year')['Class'].mean().reset_index()
plt.figure(figsize=(10, 5), dpi=300)
plt.plot(yearly_success['Year'], yearly_success['Class'], marker='o', linewidth=3, markersize=8, color='#0284C7')
plt.fill_between(yearly_success['Year'], yearly_success['Class'], alpha=0.2, color='#0284C7')
plt.title('Yearly Launch Landing Success Rate Trend (2010 - 2020)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Year', fontsize=11, fontweight='bold')
plt.ylabel('Success Rate', fontsize=11, fontweight='bold')
plt.ylim(-0.05, 1.15)
plt.xticks(yearly_success['Year'])
for _, r in yearly_success.iterrows():
    val = r['Class']
    plt.annotate(f"{val:.1%}", (r['Year'], val),
                 ha='center', va='bottom', xytext=(0, 6), textcoords='offset points',
                 fontsize=9, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/yearly_success_trend.png', dpi=300)
plt.close()

print("Saved all EDA visualizations.")

# -------------------------------------------------------------
# 3. SQL QUERIES EXECUTION (SQLite)
# -------------------------------------------------------------
conn = sqlite3.connect('spacex.db')
# Clean columns for sqlite table
df_sql.columns = [c.replace(' ', '_').replace('(', '').replace(')', '') for c in df_sql.columns]
df_sql.to_sql('SPACEXTBL', conn, if_exists='replace', index=False)

sql_results = {}

# Query 1: Unique launch sites
sql_results['q1'] = pd.read_sql_query("SELECT DISTINCT Launch_Site FROM SPACEXTBL", conn)

# Query 2: 5 records where launch site begins with 'CCA'
sql_results['q2'] = pd.read_sql_query("SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5", conn)

# Query 3: Total payload mass carried by boosters sponsored by NASA (CRS)
sql_results['q3'] = pd.read_sql_query("SELECT SUM(PAYLOAD_MASS__KG_) AS Total_Payload_Mass_NASA_CRS FROM SPACEXTBL WHERE Customer = 'NASA (CRS)'", conn)

# Query 4: Average payload mass by booster version F9 v1.1
sql_results['q4'] = pd.read_sql_query("SELECT AVG(PAYLOAD_MASS__KG_) AS Avg_Payload_Mass_F9_v1_1 FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'", conn)

# Query 5: Date of first successful ground pad landing
sql_results['q5'] = pd.read_sql_query("SELECT MIN(Date) AS First_Successful_Ground_Landing FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)'", conn)

# Query 6: Boosters with drone ship success and payload between 4000 and 6000 kg
sql_results['q6'] = pd.read_sql_query("SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000", conn)

# Query 7: Total number of successful and failure mission outcomes
sql_results['q7'] = pd.read_sql_query("SELECT TRIM(Mission_Outcome) AS Mission_Outcome, COUNT(*) AS Count FROM SPACEXTBL GROUP BY TRIM(Mission_Outcome)", conn)

# Query 8: Booster versions that have carried maximum payload mass
sql_results['q8'] = pd.read_sql_query("SELECT DISTINCT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)", conn)

# Query 9: Drone ship landing failure records in 2015 by month
sql_results['q9'] = pd.read_sql_query("SELECT SUBSTR(Date, 6, 2) AS Month, Date, Booster_Version, Launch_Site, Landing_Outcome FROM SPACEXTBL WHERE SUBSTR(Date, 1, 4) = '2015' AND Landing_Outcome = 'Failure (drone ship)'", conn)

# Query 10: Ranked landing outcomes between 2010-06-04 and 2017-03-20
sql_results['q10'] = pd.read_sql_query("SELECT Landing_Outcome, COUNT(*) AS Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Count DESC", conn)

conn.close()

# Save SQL output summaries as text
with open('figures/sql_query_results.txt', 'w') as f:
    for q_name, res_df in sql_results.items():
        f.write(f"=== {q_name.upper()} ===\n")
        f.write(res_df.to_string(index=False))
        f.write("\n\n")

print("Executed and saved SQL queries.")

# -------------------------------------------------------------
# 4. DASHBOARD VISUALS (Dash equivalents)
# -------------------------------------------------------------
# Dash Pie Chart: Total Success Launches by Site
site_success_counts = df_dash[df_dash['class'] == 1].groupby('Launch Site')['class'].count().reset_index()
plt.figure(figsize=(8, 5), dpi=300)
colors = ['#3B82F6', '#10B981', '#F59E0B', '#8B5CF6']
plt.pie(site_success_counts['class'], labels=site_success_counts['Launch Site'],
        autopct='%1.1f%%', startangle=140, colors=colors,
        wedgeprops=dict(width=0.7, edgecolor='w', linewidth=2))
plt.title('Total Successful Launches by Launch Site (Plotly Dash)', fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig('figures/dash_pie_all_sites.png', dpi=300)
plt.close()

# Dash Pie Chart: KSC LC-39A Success vs Failure
ksc_df = df_dash[df_dash['Launch Site'] == 'KSC LC-39A']
ksc_counts = ksc_df['class'].value_counts()
plt.figure(figsize=(8, 5), dpi=300)
plt.pie(ksc_counts, labels=['Success (1)', 'Failure (0)'],
        autopct='%1.1f%%', startangle=140, colors=['#10B981', '#EF4444'],
        wedgeprops=dict(width=0.7, edgecolor='w', linewidth=2))
plt.title('Success vs. Failure for Site KSC LC-39A (Plotly Dash)', fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig('figures/dash_pie_ksc_site.png', dpi=300)
plt.close()

# Dash Scatter: Payload vs Outcome colored by Booster Version Category
plt.figure(figsize=(10, 5), dpi=300)
sns.scatterplot(
    data=df_dash, x='Payload Mass (kg)', y='class', hue='Booster Version Category',
    s=140, alpha=0.9, palette='tab10'
)
plt.title('Correlation between Payload Mass and Success for all Sites (Dash Scatter)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Payload Mass (kg)', fontsize=11, fontweight='bold')
plt.ylabel('Landing Outcome (0: Fail, 1: Success)', fontsize=11, fontweight='bold')
plt.yticks([0, 1], ['Failure (0)', 'Success (1)'])
plt.legend(title='Booster Version', loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.savefig('figures/dash_scatter_payload_outcome.png', dpi=300)
plt.close()

print("Generated Dash dashboard visuals.")

# -------------------------------------------------------------
# 5. FOLIUM MAP GENERATION & PROXIMITY VISUALS
# -------------------------------------------------------------
import folium
from folium.plugins import MarkerCluster

# Coordinates for launch sites
launch_sites_coords = {
    'CCAFS LC-40': [28.562302, -80.577356],
    'CCAFS SLC-40': [28.563197, -80.576820],
    'KSC LC-39A': [28.573255, -80.646895],
    'VAFB SLC-4E': [34.632834, -120.610745]
}

# Base Folium Map
site_map = folium.Map(location=[28.562302, -80.577356], zoom_start=5)
marker_cluster = MarkerCluster().add_to(site_map)

for _, row in df_geo.iterrows():
    color = 'green' if row['class'] == 1 else 'red'
    folium.Marker(
        location=[row['Lat'], row['Long']],
        icon=folium.Icon(color=color, icon='info-sign'),
        popup=f"{row['Launch Site']} | Flight {row['Flight Number']} | Outcome: {row['class']}"
    ).add_to(marker_cluster)

for site, coord in launch_sites_coords.items():
    folium.Circle(
        coord, radius=1000, color='#0284C7', fill=True, fill_color='#0284C7', fill_opacity=0.3
    ).add_to(site_map)
    folium.Marker(
        coord,
        icon=folium.DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html=f'<div style="font-size: 12px; font-weight: bold; color: #1E3A8A;">{site}</div>'
        )
    ).add_to(site_map)

site_map.save('maps/spacex_interactive_map.html')

# Generate rich high-resolution map visuals for slides
# 1. Launch Sites & Locations
plt.figure(figsize=(10, 5.5), dpi=300)
plt.subplot(1, 2, 1)
# Cape Canaveral / KSC Area
cc_sites = df_geo[df_geo['Launch Site'].str.contains('CCAFS|KSC')]
sns.scatterplot(data=cc_sites, x='Long', y='Lat', hue='class', palette={0: '#EF4444', 1: '#10B981'}, s=120, alpha=0.85)
for s, c in [('CCAFS LC-40', [28.562302, -80.577356]), ('KSC LC-39A', [28.573255, -80.646895])]:
    plt.plot(c[1], c[0], 'bo', markersize=12, fillstyle='none', markeredgewidth=2)
    plt.text(c[1] + 0.005, c[0] + 0.002, s, fontsize=9, fontweight='bold', color='#1E3A8A')
plt.title('Florida Space Coast: CCAFS & KSC Sites', fontsize=11, fontweight='bold')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(title='Outcome', labels=['Failure', 'Success'], loc='lower left')

plt.subplot(1, 2, 2)
# Vandenberg Space Force Base
vafb_sites = df_geo[df_geo['Launch Site'].str.contains('VAFB')]
sns.scatterplot(data=vafb_sites, x='Long', y='Lat', hue='class', palette={0: '#EF4444', 1: '#10B981'}, s=120, alpha=0.85)
plt.plot(-120.610745, 34.632834, 'bo', markersize=12, fillstyle='none', markeredgewidth=2)
plt.text(-120.610745 + 0.001, 34.632834 + 0.001, 'VAFB SLC-4E', fontsize=9, fontweight='bold', color='#1E3A8A')
plt.title('California West Coast: VAFB SLC-4E', fontsize=11, fontweight='bold')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(title='Outcome', labels=['Failure', 'Success'], loc='lower left')

plt.suptitle('Folium Interactive Analytics: Launch Site Geography & Outcomes', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/folium_launch_sites.png', dpi=300)
plt.close()

# 2. Folium Proximity Distance Diagram
plt.figure(figsize=(10, 5.5), dpi=300)
ksc_coord = np.array([-80.646895, 28.573255])
coast_coord = np.array([-80.5677, 28.5732]) # ~0.8 km east
highway_coord = np.array([-80.6555, 28.5732]) # Samuel C Phillips Pkwy ~1.2 km
railway_coord = np.array([-80.6541, 28.5739]) # NASA Railroad ~1.3 km
city_coord = np.array([-80.8077, 28.6123]) # Titusville ~16.5 km

plt.plot(ksc_coord[0], ksc_coord[1], 'r^', markersize=14, label='KSC LC-39A (Launch Site)')
plt.plot(coast_coord[0], coast_coord[1], 's', color='#0284C7', markersize=10, label='Coastline (~0.85 km)')
plt.plot(highway_coord[0], highway_coord[1], 'o', color='#F59E0B', markersize=10, label='Highway Parkway (~1.2 km)')
plt.plot(railway_coord[0], railway_coord[1], 'd', color='#8B5CF6', markersize=10, label='NASA Railroad (~1.35 km)')
plt.plot(city_coord[0], city_coord[1], 'P', color='#10B981', markersize=12, label='Nearest City - Titusville (~16.5 km)')

# Distance lines
for dest, label, col in [(coast_coord, '0.85 km (Coast)', '#0284C7'),
                         (highway_coord, '1.2 km (Highway)', '#F59E0B'),
                         (railway_coord, '1.35 km (Rail)', '#8B5CF6'),
                         (city_coord, '16.5 km (City)', '#10B981')]:
    plt.plot([ksc_coord[0], dest[0]], [ksc_coord[1], dest[1]], '--', color=col, linewidth=2)
    mid = (ksc_coord + dest) / 2
    plt.annotate(label, xy=mid, xytext=(0, 5), textcoords='offset points',
                 fontsize=9, fontweight='bold', color=col,
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor=col))

plt.title('Folium Geospatial Proximity Analysis from Launch Site (KSC LC-39A)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.legend(loc='lower left', frameon=True)
plt.tight_layout()
plt.savefig('figures/folium_proximity_analysis.png', dpi=300)
plt.close()

print("Generated Folium map and proximity visuals.")

# -------------------------------------------------------------
# 6. MACHINE LEARNING PREDICTIVE ANALYSIS
# -------------------------------------------------------------
X = df3.copy()
Y = df2['Class'].to_numpy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)

models = {
    'Logistic Regression': {
        'model': LogisticRegression(random_state=2),
        'params': {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
    },
    'SVM': {
        'model': SVC(random_state=2),
        'params': {'C': [0.5, 1.0, 1.5], 'kernel': ['linear', 'rbf', 'sigmoid']}
    },
    'Decision Tree': {
        'model': DecisionTreeClassifier(random_state=2),
        'params': {'criterion': ['gini', 'entropy'], 'max_depth': [2, 4, 6, 8], 'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 5, 10]}
    },
    'KNN': {
        'model': KNeighborsClassifier(),
        'params': {'n_neighbors': [3, 5, 7, 9, 10], 'p': [1, 2], 'algorithm': ['auto', 'ball_tree', 'kd_tree']}
    }
}

ml_results = []
best_models = {}

for name, cfg in models.items():
    clf = GridSearchCV(cfg['model'], cfg['params'], cv=10)
    clf.fit(X_train, Y_train)
    train_acc = clf.best_score_
    test_acc = clf.score(X_test, Y_test)
    y_pred = clf.predict(X_test)
    cm = confusion_matrix(Y_test, y_pred)
    best_models[name] = clf
    ml_results.append({
        'Model': name,
        'Train Accuracy (CV)': train_acc,
        'Test Accuracy': test_acc,
        'Best Params': str(clf.best_params_),
        'Confusion Matrix': cm
    })
    print(f"{name}: Train CV={train_acc:.4f}, Test={test_acc:.4f}, Best Params: {clf.best_params_}")

ml_df = pd.DataFrame(ml_results)

# Plot Model Comparison Bar Chart
plt.figure(figsize=(9, 5), dpi=300)
x_pos = np.arange(len(ml_df))
width = 0.35

plt.bar(x_pos - width/2, ml_df['Train Accuracy (CV)'], width, label='Train Accuracy (10-Fold CV)', color='#3B82F6')
plt.bar(x_pos + width/2, ml_df['Test Accuracy'], width, label='Test Accuracy (20% Holdout)', color='#10B981')

plt.xlabel('Classification Model', fontsize=11, fontweight='bold')
plt.ylabel('Accuracy Score', fontsize=11, fontweight='bold')
plt.title('Machine Learning Models Performance Comparison', fontsize=13, fontweight='bold', pad=12)
plt.xticks(x_pos, ml_df['Model'], fontsize=10, fontweight='bold')
plt.ylim(0, 1.15)
plt.legend(loc='lower right', frameon=True)

for i in range(len(ml_df)):
    plt.text(i - width/2, ml_df.loc[i, 'Train Accuracy (CV)'] + 0.02, f"{ml_df.loc[i, 'Train Accuracy (CV)']:.1%}", ha='center', fontsize=9, fontweight='bold')
    plt.text(i + width/2, ml_df.loc[i, 'Test Accuracy'] + 0.02, f"{ml_df.loc[i, 'Test Accuracy']:.1%}", ha='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('figures/ml_model_accuracy_comparison.png', dpi=300)
plt.close()

# Plot Confusion Matrix for Decision Tree / Best Model
plt.figure(figsize=(6, 5), dpi=300)
best_cm = ml_df.loc[0, 'Confusion Matrix']
sns.heatmap(best_cm, annot=True, fmt='d', cmap='Blues', cbar=False,
            xticklabels=['Predicted Fail (0)', 'Predicted Success (1)'],
            yticklabels=['Actual Fail (0)', 'Actual Success (1)'],
            annot_kws={'size': 14, 'weight': 'bold'})
plt.title('Confusion Matrix (Holdout Test Set)', fontsize=12, fontweight='bold', pad=12)
plt.ylabel('Actual Label', fontsize=11, fontweight='bold')
plt.xlabel('Predicted Label', fontsize=11, fontweight='bold')
plt.tight_layout()
plt.savefig('figures/ml_confusion_matrix.png', dpi=300)
plt.close()

print("Completed machine learning modeling and saved evaluation figures.")
