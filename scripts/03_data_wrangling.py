"""
03_data_wrangling.py - Data Wrangling & Binary Outcome Classification
Cleans data, imputes missing values, and creates the binary target variable 'Class'.
"""

import pandas as pd
import numpy as np

df = pd.read_csv('data/dataset_part_1.csv')
print(f"Initial shape: {df.shape}")

# Impute missing PayloadMass with column mean
mean_payload = df['PayloadMass'].mean()
df['PayloadMass'] = df['PayloadMass'].fillna(mean_payload)
print(f"Mean payload imputed: {mean_payload:.2f} kg")

# Landing outcome classification
landing_outcomes = df['Outcome'].value_counts()
print("Landing Outcome Counts:")
print(landing_outcomes)

bad_outcomes = set(landing_outcomes.keys()[[1, 3, 5, 6, 7]])
df['Class'] = df['Outcome'].apply(lambda x: 0 if x in bad_outcomes else 1)

print(f"Class distribution:\n{df['Class'].value_counts()}")
print(f"Success Rate: {df['Class'].mean():.2%}")

df.to_csv('data/dataset_part_2.csv', index=False)
print("Saved data/dataset_part_2.csv successfully.")
