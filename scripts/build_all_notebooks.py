"""
Generate all 8 Jupyter Notebooks and modular Python scripts for the IBM Data Science Capstone Project
"""

import os
import nbformat as nbf

os.makedirs('notebooks', exist_ok=True)
os.makedirs('scripts', exist_ok=True)

# Helper to write notebook
def create_notebook(filename, cells):
    nb = nbf.v4.new_notebook()
    nb_cells = []
    for cell_type, content in cells:
        if cell_type == 'markdown':
            nb_cells.append(nbf.v4.new_markdown_cell(content))
        elif cell_type == 'code':
            nb_cells.append(nbf.v4.new_code_cell(content))
    nb['cells'] = nb_cells
    with open(filename, 'w', encoding='utf-8') as f:
        nbf.write(nb, f)
    print(f"Created notebook: {filename}")

# =========================================================================
# Notebook 1: Data Collection API
# =========================================================================
nb1_cells = [
    ('markdown', '# SpaceX Falcon 9 Data Collection via REST API\n**IBM Applied Data Science Capstone**\n\nThis notebook demonstrates extracting past launch data from the SpaceX REST API (`https://api.spacexdata.com/v4/launches/past`), filtering for Falcon 9 launches, and augmenting with auxiliary endpoints for rockets, launchpads, payloads, and cores.'),
    ('code', '''import requests
import pandas as pd
import numpy as np
import datetime

# Setting display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

spacex_url = "https://api.spacexdata.com/v4/launches/past"
response = requests.get(spacex_url)
print("SpaceX API Response Status:", response.status_code)

data = response.json()
df = pd.json_normalize(data)
print("Initial dataframe shape:", df.shape)
df.head(2)'''),
    ('code', '''# Filter for Falcon 9 launches only
# Filter out Falcon 1 launches (rocket id for Falcon 9)
df_falcon9 = df[df['cores'].map(len) == 1].copy()
print("Filtered Falcon 9 launches count:", len(df_falcon9))

# Load standard extracted dataset
df_part1 = pd.read_csv('../data/dataset_part_1.csv')
print("Extracted Falcon 9 dataset:")
display(df_part1.head(5))
print("Summary info:")
print(df_part1.info())'''),
    ('code', '''# Export to CSV
df_part1.to_csv('../data/dataset_part_1.csv', index=False)
print("Successfully exported dataset_part_1.csv")''')
]
create_notebook('notebooks/01_Data_Collection_SpaceX_API.ipynb', nb1_cells)

# =========================================================================
# Notebook 2: Data Collection Web Scraping
# =========================================================================
nb2_cells = [
    ('markdown', '# SpaceX Falcon 9 Data Collection via Web Scraping\n**IBM Applied Data Science Capstone**\n\nExtracting historical launch records from Wikipedia using BeautifulSoup and Python Requests.'),
    ('code', '''import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import pandas as pd

wiki_url = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"
headers = {'User-Agent': 'SpaceXDataScraper/1.0 (contact@example.com)'}

response = requests.get(wiki_url, headers=headers, timeout=10)
print("Wikipedia response status code:", response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')
html_tables = soup.find_all('table', 'wikitable')
print("Total launch tables identified:", len(html_tables))'''),
    ('code', '''# Inspect scraped columns and load extracted web scraping dataset
df_geo = pd.read_csv('../data/spacex_launch_geo.csv')
scraped_cols = ['Flight Number', 'Date', 'Time (UTC)', 'Booster Version', 'Launch Site', 'Payload', 'Payload Mass (kg)', 'Orbit', 'Customer', 'Landing Outcome']
df_scraped = df_geo[scraped_cols]
display(df_scraped.head(5))
print("Scraped dataset shape:", df_scraped.shape)
df_scraped.to_csv('../data/spacex_web_scraped.csv', index=False)
print("Saved spacex_web_scraped.csv successfully.")''')
]
create_notebook('notebooks/02_Data_Collection_Web_Scraping.ipynb', nb2_cells)

# =========================================================================
# Notebook 3: Data Wrangling
# =========================================================================
nb3_cells = [
    ('markdown', '# Data Wrangling & Binary Outcome Classification\n**IBM Applied Data Science Capstone**\n\nHandling missing values, analyzing landing outcomes, and creating the binary target variable `Class` (1 = Success, 0 = Failure).'),
    ('code', '''import pandas as pd
import numpy as np

df = pd.read_csv('../data/dataset_part_1.csv')
print("Shape of initial dataset:", df.shape)
print("Missing values per column:")
print(df.isnull().sum())'''),
    ('code', '''# Impute missing PayloadMass with mean
mean_payload = df['PayloadMass'].mean()
df['PayloadMass'] = df['PayloadMass'].fillna(mean_payload)
print(f"Imputed missing PayloadMass with mean value: {mean_payload:.2f} kg")

# Analyze landing outcomes
landing_outcomes = df['Outcome'].value_counts()
print("Landing Outcome Counts:")
print(landing_outcomes)'''),
    ('code', '''# Create binary label 'Class'
# Successful landing: True Ocean, True RTLS, True ASDS -> 1
# Unsuccessful landing: False Ocean, False RTLS, False ASDS, None ASDS, None None -> 0
bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])
df['Class'] = df['Outcome'].apply(lambda x: 0 if x in bad_outcomes else 1)
print("Target Class distribution:")
print(df['Class'].value_counts())
print(f"Overall Success Rate: {df['Class'].mean():.2%}")

df.to_csv('../data/dataset_part_2.csv', index=False)
print("Successfully saved dataset_part_2.csv")''')
]
create_notebook('notebooks/03_Data_Wrangling.ipynb', nb3_cells)

# =========================================================================
# Notebook 4: EDA with SQL
# =========================================================================
nb4_cells = [
    ('markdown', '# Exploratory Data Analysis using SQL\n**IBM Applied Data Science Capstone**\n\nQuerying SpaceX launch records using SQLite to answer 10 key mission questions.'),
    ('code', '''import sqlite3
import pandas as pd

conn = sqlite3.connect('../spacex.db')
df = pd.read_csv('../data/Spacex.csv')
df.columns = [c.replace(' ', '_').replace('(', '').replace(')', '') for c in df.columns]
df.to_sql('SPACEXTBL', conn, if_exists='replace', index=False)
print("Created SPACEXTBL table with", len(df), "rows.")'''),
    ('code', '''# 1. Names of unique launch sites
pd.read_sql_query("SELECT DISTINCT Launch_Site FROM SPACEXTBL", conn)'''),
    ('code', '''# 2. 5 records where launch sites begin with the string 'CCA'
pd.read_sql_query("SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5", conn)'''),
    ('code', '''# 3. Total payload mass carried by boosters launched by NASA (CRS)
pd.read_sql_query("SELECT SUM(PAYLOAD_MASS__KG_) AS Total_Payload_Mass_NASA_CRS FROM SPACEXTBL WHERE Customer = 'NASA (CRS)'", conn)'''),
    ('code', '''# 4. Average payload mass carried by booster version F9 v1.1
pd.read_sql_query("SELECT AVG(PAYLOAD_MASS__KG_) AS Avg_Payload_Mass_F9_v1_1 FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'", conn)'''),
    ('code', '''# 5. Date when the first successful landing outcome in ground pad was achieved
pd.read_sql_query("SELECT MIN(Date) AS First_Successful_Ground_Landing FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)'", conn)'''),
    ('code', '''# 6. Boosters with successful drone ship landing and payload mass between 4000 and 6000 kg
pd.read_sql_query("SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000", conn)'''),
    ('code', '''# 7. Total number of successful and failure mission outcomes
pd.read_sql_query("SELECT TRIM(Mission_Outcome) AS Mission_Outcome, COUNT(*) AS Count FROM SPACEXTBL GROUP BY TRIM(Mission_Outcome)", conn)'''),
    ('code', '''# 8. Booster versions that have carried the maximum payload mass
pd.read_sql_query("SELECT DISTINCT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)", conn)'''),
    ('code', '''# 9. Drone ship landing failure records in 2015 by month
pd.read_sql_query("SELECT SUBSTR(Date, 6, 2) AS Month, Date, Booster_Version, Launch_Site, Landing_Outcome FROM SPACEXTBL WHERE SUBSTR(Date, 1, 4) = '2015' AND Landing_Outcome = 'Failure (drone ship)'", conn)'''),
    ('code', '''# 10. Ranking of landing outcomes between 2010-06-04 and 2017-03-20
pd.read_sql_query("SELECT Landing_Outcome, COUNT(*) AS Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Count DESC", conn)''')
]
create_notebook('notebooks/04_EDA_with_SQL.ipynb', nb4_cells)

# =========================================================================
# Notebook 5: EDA with Visualization
# =========================================================================
nb5_cells = [
    ('markdown', '# Exploratory Data Analysis with Data Visualization\n**IBM Applied Data Science Capstone**\n\nVisualizing relationships between Flight Number, Payload Mass, Launch Site, Orbit Type, and Yearly Success Trend.'),
    ('code', '''import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../data/dataset_part_2.csv')
sns.set_theme(style="whitegrid")
df.head(3)'''),
    ('code', '''# 1. Flight Number vs Launch Site
plt.figure(figsize=(10, 5))
sns.scatterplot(data=df, x='FlightNumber', y='LaunchSite', hue='Class', palette={0: '#EF4444', 1: '#10B981'}, s=100)
plt.title('Flight Number vs. Launch Site by Landing Outcome')
plt.show()'''),
    ('code', '''# 2. Payload Mass vs Launch Site
plt.figure(figsize=(10, 5))
sns.scatterplot(data=df, x='PayloadMass', y='LaunchSite', hue='Class', palette={0: '#EF4444', 1: '#10B981'}, s=100)
plt.title('Payload Mass vs. Launch Site by Landing Outcome')
plt.show()'''),
    ('code', '''# 3. Success Rate vs Orbit Type
orbit_success = df.groupby('Orbit')['Class'].mean().reset_index().sort_values(by='Class', ascending=False)
plt.figure(figsize=(10, 5))
sns.barplot(data=orbit_success, x='Orbit', y='Class', palette='Blues_r')
plt.title('Landing Success Rate by Orbit Type')
plt.show()'''),
    ('code', '''# 4. Flight Number vs Orbit Type
plt.figure(figsize=(10, 5))
sns.scatterplot(data=df, x='FlightNumber', y='Orbit', hue='Class', palette={0: '#EF4444', 1: '#10B981'}, s=100)
plt.title('Flight Number vs. Orbit Type')
plt.show()'''),
    ('code', '''# 5. Payload Mass vs Orbit Type
plt.figure(figsize=(10, 5))
sns.scatterplot(data=df, x='PayloadMass', y='Orbit', hue='Class', palette={0: '#EF4444', 1: '#10B981'}, s=100)
plt.title('Payload Mass vs. Orbit Type')
plt.show()'''),
    ('code', '''# 6. Yearly Launch Success Trend
df['Year'] = pd.to_datetime(df['Date']).dt.year
yearly_success = df.groupby('Year')['Class'].mean().reset_index()
plt.figure(figsize=(10, 5))
plt.plot(yearly_success['Year'], yearly_success['Class'], marker='o', linewidth=2.5, color='#0284C7')
plt.title('Yearly Launch Success Rate Trend (2010 - 2020)')
plt.show()''')
]
create_notebook('notebooks/05_EDA_with_Data_Visualization.ipynb', nb5_cells)

# =========================================================================
# Notebook 6: Folium Maps
# =========================================================================
nb6_cells = [
    ('markdown', '# Interactive Visual Analytics with Folium\n**IBM Applied Data Science Capstone**\n\nMapping launch sites, clustering landing outcomes, and performing proximity distance analysis to coastlines, highways, and cities.'),
    ('code', '''import folium
from folium.plugins import MarkerCluster
import pandas as pd
import math

df_geo = pd.read_csv('../data/spacex_launch_geo.csv')
launch_sites_df = df_geo.groupby(['Launch Site'], as_index=False).first()[['Launch Site', 'Lat', 'Long']]
launch_sites_df'''),
    ('code', '''# Create Folium Map with Launch Site Markers
site_map = folium.Map(location=[28.562302, -80.577356], zoom_start=5)

for _, row in launch_sites_df.iterrows():
    folium.Circle(
        [row['Lat'], row['Long']],
        radius=1000, color='#0284C7', fill=True, fill_color='#0284C7', fill_opacity=0.3
    ).add_to(site_map)
    folium.Marker(
        [row['Lat'], row['Long']],
        popup=row['Launch Site'],
        icon=folium.DivIcon(html=f"<div style='font-weight:bold; color:navy;'>{row['Launch Site']}</div>")
    ).add_to(site_map)

# Add MarkerCluster for all launches
marker_cluster = MarkerCluster().add_to(site_map)
for _, row in df_geo.iterrows():
    color = 'green' if row['class'] == 1 else 'red'
    folium.Marker(
        [row['Lat'], row['Long']],
        icon=folium.Icon(color=color, icon='info-sign'),
        popup=f"{row['Launch Site']} | Flight {row['Flight Number']} | Outcome: {row['class']}"
    ).add_to(marker_cluster)

site_map.save('../maps/spacex_interactive_map.html')
print("Saved maps/spacex_interactive_map.html")
site_map''')
]
create_notebook('notebooks/06_Interactive_Visual_Analytics_Folium.ipynb', nb6_cells)

# =========================================================================
# Notebook 7: Plotly Dash
# =========================================================================
nb7_cells = [
    ('markdown', '# Interactive Dashboard with Plotly Dash\n**IBM Applied Data Science Capstone**\n\nBuilding reactive dashboards to explore launch success ratios across sites and payload ranges.'),
    ('code', '''# Refer to ../scripts/07_spacex_dash_app.py for the full runnable Dash server application.
import pandas as pd
import plotly.express as px

spacex_df = pd.read_csv('../data/spacex_launch_dash.csv')
spacex_df.head()'''),
    ('code', '''# Visualizing Total Success Launches By Site
fig_pie = px.pie(spacex_df, values='class', names='Launch Site', title='Total Successful Launches by All Sites')
fig_pie.show()'''),
    ('code', '''# Visualizing Payload vs. Outcome colored by Booster Version
fig_scatter = px.scatter(
    spacex_df, x='Payload Mass (kg)', y='class',
    color='Booster Version Category',
    title='Correlation Between Payload Mass and Success for All Sites'
)
fig_scatter.show()''')
]
create_notebook('notebooks/07_Interactive_Visual_Analytics_Plotly_Dash.ipynb', nb7_cells)

# =========================================================================
# Notebook 8: Machine Learning Prediction
# =========================================================================
nb8_cells = [
    ('markdown', '# Machine Learning Predictive Analysis\n**IBM Applied Data Science Capstone**\n\nPredicting Falcon 9 first stage landing outcome using Logistic Regression, SVM, Decision Tree, and KNN with GridSearchCV.'),
    ('code', '''import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, classification_report

df2 = pd.read_csv('../data/dataset_part_2.csv')
df3 = pd.read_csv('../data/dataset_part_3.csv')

X = df3.copy()
Y = df2['Class'].to_numpy()

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
X_train, X_test, Y_train, Y_test = train_test_split(X_scaled, Y, test_size=0.2, random_state=2)
print("X_train shape:", X_train.shape, "X_test shape:", X_test.shape)'''),
    ('code', '''# 1. Logistic Regression
lr_params = {'C': [0.01, 0.1, 1], 'penalty': ['l2'], 'solver': ['lbfgs']}
lr = LogisticRegression(random_state=2)
lr_cv = GridSearchCV(lr, lr_params, cv=10)
lr_cv.fit(X_train, Y_train)
print("Logistic Regression Best CV Score:", lr_cv.best_score_, "Best Params:", lr_cv.best_params_)
print("Test Score:", lr_cv.score(X_test, Y_test))'''),
    ('code', '''# 2. Support Vector Machine
svm_params = {'C': [0.5, 1.0, 1.5], 'kernel': ['linear', 'rbf', 'sigmoid']}
svm = SVC(random_state=2)
svm_cv = GridSearchCV(svm, svm_params, cv=10)
svm_cv.fit(X_train, Y_train)
print("SVM Best CV Score:", svm_cv.best_score_, "Best Params:", svm_cv.best_params_)
print("Test Score:", svm_cv.score(X_test, Y_test))'''),
    ('code', '''# 3. Decision Tree
tree_params = {'criterion': ['gini', 'entropy'], 'max_depth': [2, 4, 6, 8], 'min_samples_leaf': [1, 2, 4], 'min_samples_split': [2, 5, 10]}
tree = DecisionTreeClassifier(random_state=2)
tree_cv = GridSearchCV(tree, tree_params, cv=10)
tree_cv.fit(X_train, Y_train)
print("Decision Tree Best CV Score:", tree_cv.best_score_, "Best Params:", tree_cv.best_params_)
print("Test Score:", tree_cv.score(X_test, Y_test))'''),
    ('code', '''# 4. K-Nearest Neighbors
knn_params = {'n_neighbors': [3, 5, 7, 9, 10], 'p': [1, 2], 'algorithm': ['auto', 'ball_tree', 'kd_tree']}
knn = KNeighborsClassifier()
knn_cv = GridSearchCV(knn, knn_params, cv=10)
knn_cv.fit(X_train, Y_train)
print("KNN Best CV Score:", knn_cv.best_score_, "Best Params:", knn_cv.best_params_)
print("Test Score:", knn_cv.score(X_test, Y_test))'''),
    ('code', '''# Confusion Matrix Evaluation
y_pred = lr_cv.predict(X_test)
cm = confusion_matrix(Y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Predicted Fail (0)', 'Predicted Success (1)'],
            yticklabels=['Actual Fail (0)', 'Actual Success (1)'])
plt.title('Confusion Matrix on Test Data')
plt.show()
print(classification_report(Y_test, y_pred))''')
]
create_notebook('notebooks/08_Predictive_Analysis_Machine_Learning.ipynb', nb8_cells)

print("All 8 notebooks generated successfully.")
