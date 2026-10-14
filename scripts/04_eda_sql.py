"""
04_eda_sql.py - Exploratory Data Analysis with SQLite
Executes all 10 SQL analytical queries on SpaceX mission dataset.
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect('spacex.db')
df = pd.read_csv('data/Spacex.csv')
df.columns = [c.replace(' ', '_').replace('(', '').replace(')', '') for c in df.columns]
df.to_sql('SPACEXTBL', conn, if_exists='replace', index=False)

queries = {
    "1. Unique Launch Sites": "SELECT DISTINCT Launch_Site FROM SPACEXTBL",
    "2. 5 records where launch sites begin with 'CCA'": "SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5",
    "3. Total payload mass carried by NASA (CRS)": "SELECT SUM(PAYLOAD_MASS__KG_) AS Total_Payload_Mass_NASA_CRS FROM SPACEXTBL WHERE Customer = 'NASA (CRS)'",
    "4. Average payload mass carried by F9 v1.1": "SELECT AVG(PAYLOAD_MASS__KG_) AS Avg_Payload_Mass_F9_v1_1 FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%'",
    "5. Date of first successful ground pad landing": "SELECT MIN(Date) AS First_Successful_Ground_Landing FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)'",
    "6. Boosters with drone ship success and payload 4000-6000 kg": "SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000",
    "7. Total number of successful and failure mission outcomes": "SELECT TRIM(Mission_Outcome) AS Mission_Outcome, COUNT(*) AS Count FROM SPACEXTBL GROUP BY TRIM(Mission_Outcome)",
    "8. Boosters carrying maximum payload mass": "SELECT DISTINCT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL)",
    "9. 2015 drone ship landing failures by month": "SELECT SUBSTR(Date, 6, 2) AS Month, Date, Booster_Version, Launch_Site, Landing_Outcome FROM SPACEXTBL WHERE SUBSTR(Date, 1, 4) = '2015' AND Landing_Outcome = 'Failure (drone ship)'",
    "10. Ranked landing outcomes between 2010-06-04 and 2017-03-20": "SELECT Landing_Outcome, COUNT(*) AS Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Count DESC"
}

for title, q in queries.items():
    print(f"\n{'='*60}\n{title}\n{'='*60}")
    res = pd.read_sql_query(q, conn)
    print(res.to_string(index=False))

conn.close()
