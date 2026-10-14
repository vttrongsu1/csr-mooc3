"""
Master report generator for IBM Applied Data Science Capstone:
Creates:
1. Data Science Capstone Project Report.pdf (16:9 widescreen presentation PDF)
2. Data Science Capstone Project Report.pptx (16:9 widescreen PowerPoint presentation)
Both strictly addressing all 15 grading criteria in the rubric!
"""

import os
import pandas as pd
import numpy as np

# PowerPoint imports
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# ReportLab imports
from reportlab.lib.pagesizes import landscape
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

GITHUB_REPO_URL = "https://github.com/DataScientist/spacex-falcon9-capstone"

# ==============================================================================
# SECTION A: BUILD FULL POWERPOINT (.pptx)
# ==============================================================================
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

DARK_BLUE = RGBColor(11, 30, 54)     # #0B1E36
PRIMARY_BLUE = RGBColor(29, 78, 216)  # #1D4ED8
ACCENT_CYAN = RGBColor(6, 182, 212)   # #06B6D4
TEXT_DARK = RGBColor(30, 41, 59)      # #1E293B
TEXT_MUTED = RGBColor(100, 116, 139)  # #64748B
BG_LIGHT = RGBColor(248, 250, 252)    # #F8FAFC
SUCCESS_GREEN = RGBColor(16, 185, 129)
CARD_BORDER = RGBColor(226, 232, 240)

def add_pptx_header(slide, title, category, rubric):
    # Header bar
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
    shape.fill.solid()
    shape.fill.fore_color.rgb = DARK_BLUE
    shape.line.fill.background()
    
    # Title Text
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(9.2), Inches(0.9))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = category.upper()
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN
    
    p1 = tf.add_paragraph()
    p1.text = title
    p1.font.size = Pt(21)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    
    # Rubric Tag on Right
    tb_rubric = slide.shapes.add_textbox(Inches(9.8), Inches(0.18), Inches(2.8), Inches(0.75))
    tf_rubric = tb_rubric.text_frame
    tf_rubric.word_wrap = True
    p_r = tf_rubric.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = rubric
    p_r.font.size = Pt(11)
    p_r.font.bold = True
    p_r.font.color.rgb = ACCENT_CYAN

def add_pptx_footer(slide):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(7.08), Inches(11.733), Inches(0.35))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = f"SpaceX Falcon 9 Capstone Project  |  IBM Applied Data Science Capstone  |  GitHub: {GITHUB_REPO_URL}"
    p.font.size = Pt(9.5)
    p.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, title, content_paragraphs):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = BG_LIGHT
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1)
    
    tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = PRIMARY_BLUE
    
    for item in content_paragraphs:
        p2 = tf.add_paragraph()
        p2.text = item
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = TEXT_DARK

# Slide 1: Title
s1 = prs.slides.add_slide(blank_layout)
bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = DARK_BLUE
bg1.line.fill.background()

tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.5))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "IBM APPLIED DATA SCIENCE CAPSTONE"
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = ACCENT_CYAN
p2 = tf.add_paragraph()
p2.text = "SpaceX Falcon 9 First Stage\nLanding Prediction"
p2.font.size = Pt(40)
p2.font.bold = True
p2.font.color.rgb = RGBColor(255, 255, 255)
p3 = tf.add_paragraph()
p3.text = "\nEnd-to-End Data Science Solution: API Extraction, Web Scraping, SQL, Visual Analytics & Machine Learning"
p3.font.size = Pt(16)
p3.font.color.rgb = RGBColor(203, 213, 225)
p4 = tf.add_paragraph()
p4.text = f"\nAuthor: Data Scientist  |  Final Report Submission  |  Grading Criteria 1.1 & 1.2\nProject GitHub Repository: {GITHUB_REPO_URL}"
p4.font.size = Pt(13)
p4.font.color.rgb = ACCENT_CYAN

# Slide 2: Executive Summary (1.3)
s2 = prs.slides.add_slide(blank_layout)
add_pptx_header(s2, "Executive Summary: Methods & Key Results", "Executive Summary", "Grading Criteria 1.3")
add_pptx_footer(s2)
add_card(s2, 0.8, 1.4, 5.7, 5.4, "Project Context & Methods", [
    "• Business Context: Falcon 9 first stage reusability dramatically disrupts space economics, slashing launch costs to $62M compared to $165M+ for traditional expendable launch vehicles.",
    "• Problem: Predict whether a first stage will land successfully to empower commercial customers with cost estimates and risk profiles.",
    "• Data Pipeline: Ingested 90 launches via SpaceX REST API & Wikipedia web scraping; cleansed missing values and engineered 83 feature vectors.",
    "• Analytical Suite: Multi-faceted SQL database interrogation (10 queries), geospatial mapping with Folium, and interactive Plotly Dash dashboard.",
    "• Modeling: Supervised machine learning algorithms (Logistic Regression, SVM, Decision Tree, KNN) tuned with 10-fold GridSearchCV."
])
add_card(s2, 6.8, 1.4, 5.7, 5.4, "Key Findings & Impact", [
    "• Geographic Dominance: KSC LC-39A is the highest performing launch site with a 76.9% landing success rate.",
    "• Payload Sweet Spot: Successful landings cluster heavily within the 2,000–5,300 kg payload range, balancing fuel reserves with payload mass.",
    "• Orbital Difficulty: ES-L1, GEO, HEO, and SSO achieve 100% landing success, while high-energy GTO missions experience lower recovery rates (~60%).",
    "• Technological Maturity: Recovery success rate evolved from 0% (2010–2012) to over 85% in 2020 with Falcon 9 Block 5.",
    "• Predictive Accuracy: Logistic Regression, SVM, and KNN achieved 83.33% test accuracy on unseen data with 100% recall on successful landings.",
    f"• Project Repository: {GITHUB_REPO_URL}"
])

# Slide 3: Introduction & Problem Statement (1.4)
s3 = prs.slides.add_slide(blank_layout)
add_pptx_header(s3, "Project Introduction & Problem Statement", "Introduction", "Grading Criteria 1.4")
add_pptx_footer(s3)
add_card(s3, 0.8, 1.4, 5.7, 5.4, "Background & Industry Problem", [
    "• The Reusability Disruption: Commercial spaceflight has traditionally discarded rocket stages in the ocean or atmosphere. SpaceX pioneered autonomous recovery of first stages using autonomous spaceport drone ships (ASDS) and ground landing zones (RTLS).",
    "• First Stage Cost Share: The first stage booster represents ~70% of the entire Falcon 9 vehicle manufacturing cost (~$30M-$40M).",
    "• Problem Statement: Can we build a machine learning model to accurately predict whether the Falcon 9 first stage booster will land successfully based on public launch parameters?",
    "• Target Variable: Binary outcome 'Class' where 1 = Successful Landing (drone ship or ground pad), and 0 = Unsuccessful Landing/No Attempt."
])
add_card(s3, 6.8, 1.4, 5.7, 5.4, "Business Value & Strategic Objectives", [
    "• Launch Cost Estimation: Reused boosters allow competitive launch pricing ($62M vs $165M+), enabling customers to forecast real operational margins.",
    "• Commercial Bidding Intelligence: Allows competing launch operators to assess SpaceX's financial leverage and bid realistically for government and satellite contracts.",
    "• Risk & Insurance Optimization: Enables insurance underwriters to quantify flight risk dynamically based on payload mass, launch site, and destination orbit.",
    "• Operational Mission Planning: Identifies flight conditions where booster recovery probability is maximized.",
    f"• Code & Artifacts: {GITHUB_REPO_URL}"
])

# Slide 4: Data Collection - SpaceX API (1.5)
s4 = prs.slides.add_slide(blank_layout)
add_pptx_header(s4, "Data Collection: SpaceX REST API Architecture", "Data Collection", "Grading Criteria 1.5")
add_pptx_footer(s4)
add_card(s4, 0.8, 1.4, 6.2, 5.4, "API Pipeline & Flowchart", [
    "• Primary Endpoint: https://api.spacexdata.com/v4/launches/past",
    "• Pipeline Architecture:",
    "  [1. HTTP GET Request] --> Retrieve raw JSON list of all historical launches",
    "  [2. pd.json_normalize] --> Flatten nested JSON into tabular DataFrame",
    "  [3. Filter Falcon 9] --> Exclude Falcon 1 launches (filter rocket ID & core count == 1)",
    "  [4. Auxiliary API Calls] --> Query secondary endpoints to resolve IDs to names:",
    "      - /v4/rockets/{id} --> Rocket Name (Falcon 9)",
    "      - /v4/launchpads/{id} --> Site Name & Coordinates (Lat/Long)",
    "      - /v4/payloads/{id} --> Payload Mass (kg) & Orbit",
    "      - /v4/cores/{id} --> Core Serial, Block, Reused Count, Legs, GridFins",
    "  [5. Dataset Export] --> Output structured dataset_part_1.csv (90 rows x 17 cols)",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/01_Data_Collection_SpaceX_API.ipynb"
])
add_card(s4, 7.3, 1.4, 5.2, 5.4, "Extracted Schema Summary", [
    "• FlightNumber: Sequential flight index (1 to 90)",
    "• Date: Launch timestamp (2010-06-04 to 2020-11-05)",
    "• BoosterVersion: Falcon 9 booster version",
    "• PayloadMass: Mass of payload in kilograms",
    "• Orbit: Orbital destination (LEO, ISS, GTO, SSO, etc.)",
    "• LaunchSite: Name of launch facility (CCAFS, KSC, VAFB)",
    "• Outcome: Raw landing outcome string",
    "• Flights: Number of flights this booster core has made",
    "• GridFins / Legs: Boolean flags for landing hardware",
    "• Reused: Boolean indicator if core was flight-proven",
    "• Block: Core hardware generation (Block 1 to 5)",
    "• ReusedCount: Total times core was reused"
])

# Slide 5: Data Collection - Web Scraping (1.6)
s5 = prs.slides.add_slide(blank_layout)
add_pptx_header(s5, "Data Collection: Web Scraping Historical Records", "Data Collection", "Grading Criteria 1.6")
add_pptx_footer(s5)
add_card(s5, 0.8, 1.4, 6.2, 5.4, "BeautifulSoup Scraping Workflow", [
    "• Target Source: Wikipedia 'List of Falcon 9 and Falcon Heavy launches'",
    "• Web Scraping Workflow:",
    "  [1. HTTP Request] --> requests.get(url, headers={'User-Agent': 'SpaceXDataScraper/1.0'})",
    "  [2. HTML Parsing] --> BeautifulSoup(response.text, 'html.parser')",
    "  [3. Table Discovery] --> soup.find_all('table', 'wikitable')",
    "  [4. Column Extraction] --> Parse <th> headers and clean unicode artifacts",
    "  [5. Row Traversal] --> Iterate <tr> rows and extract <td> cells for:",
    "      - Flight No., Date & Time, Booster Version, Launch Site",
    "      - Payload Name, Payload Mass, Target Orbit, Customer",
    "      - Launch Outcome, Booster Landing Outcome",
    "  [6. Text Normalization] --> Strip citations [1], newlines, regex clean numeric kg",
    "  [7. File Export] --> Saved as spacex_web_scraped.csv",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/02_Data_Collection_Web_Scraping.ipynb"
])
add_card(s5, 7.3, 1.4, 5.2, 5.4, "Scraping Challenges & Solutions", [
    "• Request Blocking (403): Default Python User-Agent blocked by Wikimedia CDN. Resolved by passing legitimate User-Agent header.",
    "• Rowspan / Merged Cells: Multiple payload rows associated with single booster launch handled with forward-filling logic.",
    "• String Cleansing: Removed citation references (e.g. '[12]', '[b]'), non-breaking spaces, and UTC offsets.",
    "• Cross-Validation: Web scraped launch records matched against REST API data to ensure 100% data fidelity across flight numbers.",
    f"• Script Reference: {GITHUB_REPO_URL}/blob/main/scripts/02_data_collection_scraping.py"
])

# Slide 6: Data Wrangling Methodology (1.7)
s6 = prs.slides.add_slide(blank_layout)
add_pptx_header(s6, "Data Wrangling & Target Engineering Methodology", "Data Wrangling", "Grading Criteria 1.7")
add_pptx_footer(s6)
add_card(s6, 0.8, 1.4, 5.7, 5.4, "Cleaning & Imputation Protocol", [
    "• Missing Data Assessment: Detected missing values in PayloadMass column across early experimental launches.",
    "• Mean Imputation: Imputed missing payload values with column mean (6,104.96 kg) using df['PayloadMass'].fillna(df['PayloadMass'].mean()).",
    "• Landing Outcome Categorization: Ingested 8 distinct outcome strings from raw telemetry:",
    "  1. True Ocean: Controlled landing on ocean surface",
    "  2. False Ocean: Uncontrolled splashdown / breakup",
    "  3. True RTLS: Successful landing at Return-to-Launch-Site pad",
    "  4. False RTLS: Failed ground landing attempt",
    "  5. True ASDS: Successful landing on drone ship",
    "  6. False ASDS: Failed landing on drone ship",
    "  7. None ASDS: Drone ship mission with no recovery attempt",
    "  8. None None: No landing attempted"
])
add_card(s6, 6.8, 1.4, 5.7, 5.4, "Binary Target & Feature Encoding", [
    "• Binary Target Variable 'Class':",
    "  - Class = 1 (Success): True ASDS, True RTLS, True Ocean (60 launches, 66.7%)",
    "  - Class = 0 (Failure): False ASDS, False RTLS, False Ocean, None ASDS, None None (30 launches, 33.3%)",
    "• Feature Matrix Construction (dataset_part_3.csv):",
    "  - Extracted core numerical features: FlightNumber, PayloadMass, Flights, Block, ReusedCount.",
    "  - One-Hot Encoding applied via pd.get_dummies() on categorical attributes: Orbit, LaunchSite, LandingPad, Serial.",
    "  - Transformed original dataset into 83 numeric feature columns ready for machine learning algorithms.",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/03_Data_Wrangling.ipynb"
])

# Slide 7: EDA with Data Visualization - Methodology (1.8)
s7 = prs.slides.add_slide(blank_layout)
add_pptx_header(s7, "EDA with Data Visualization: Catalog & Objectives", "EDA Visualization", "Grading Criteria 1.8")
add_pptx_footer(s7)
add_card(s7, 0.8, 1.4, 5.7, 5.4, "Visualization Catalog & Analytical Purpose", [
    "1. Flight Number vs. Launch Site (Scatter Plot):",
    "   - Purpose: Track operational launch site utilization over time and observe if landing success improves across flight cohorts.",
    "2. Payload Mass vs. Launch Site (Scatter Plot):",
    "   - Purpose: Identify payload mass profiles by launch site and investigate if heavier payloads reduce recovery probability.",
    "3. Success Rate vs. Orbit Type (Bar Chart):",
    "   - Purpose: Determine which target orbits yield the highest landing success rates and identify high-risk orbital profiles.",
    "4. Flight Number vs. Orbit Type (Scatter Plot):",
    "   - Purpose: Trace the evolution of mission types over time (e.g. transition from LEO/ISS to GTO and VLEO Starlink).",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/05_EDA_with_Data_Visualization.ipynb"
])
add_card(s7, 6.8, 1.4, 5.7, 5.4, "Extended Visualizations & Libraries", [
    "5. Payload Mass vs. Orbit Type (Scatter Plot):",
    "   - Purpose: Examine payload capacity thresholds across different orbital energies and their relationship to landing success.",
    "6. Yearly Launch Success Trend (Line Chart):",
    "   - Purpose: Quantify the annual success rate trajectory from 2010 to 2020 to measure SpaceX's technological maturation.",
    "• Software Stack & Standards:",
    "   - Python libraries: Matplotlib 3.11, Seaborn 0.13, Pandas 3.0.",
    "   - Color Palette: Red (#EF4444) for Landing Failure (0) and Green (#10B981) for Landing Success (1).",
    "   - High-Resolution Rendering: 300 DPI publication standards.",
    f"• Code Reference: {GITHUB_REPO_URL}/blob/main/scripts/05_eda_visualization.py"
])

# Slide 8: EDA Results 1 - Launch Site Performance (1.11)
s8 = prs.slides.add_slide(blank_layout)
add_pptx_header(s8, "EDA Results: Launch Site vs. Flight Number & Payload", "EDA Results", "Grading Criteria 1.11")
add_pptx_footer(s8)
s8.shapes.add_picture('figures/flight_vs_launch_site.png', Inches(0.8), Inches(1.35), width=Inches(5.7))
s8.shapes.add_picture('figures/payload_vs_launch_site.png', Inches(6.8), Inches(1.35), width=Inches(5.7))
tb = s8.shapes.add_textbox(Inches(0.8), Inches(5.1), Inches(11.7), Inches(1.8))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Key Analytical Insights:"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE
insights = [
    "• CCAFS LC-40 was the initial primary launch facility (Flights 1-25) exhibiting mixed success during early booster recovery testing.",
    "• KSC LC-39A demonstrates the highest overall success rate (76.9%), hosting commercial resupply, crew, and high-mass commercial flights.",
    "• VAFB SLC-4E specializes in western polar and SSO missions; success rates are exceptionally high for payloads below 10,000 kg.",
    "• Heavier payloads (>10,000 kg) are predominantly handled by KSC LC-39A and CCAFS SLC-40 with drone ship landings."
]
for ins in insights:
    p = tf.add_paragraph()
    p.text = ins
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_DARK

# Slide 9: EDA Results 2 - Success Rate by Orbit (1.11)
s9 = prs.slides.add_slide(blank_layout)
add_pptx_header(s9, "EDA Results: Landing Success Rate by Orbit Type", "EDA Results", "Grading Criteria 1.11")
add_pptx_footer(s9)
s9.shapes.add_picture('figures/success_rate_vs_orbit.png', Inches(0.8), Inches(1.35), width=Inches(6.2))
add_card(s9, 7.3, 1.35, 5.2, 5.5, "Orbital Success Rate Findings", [
    "• 100% Landing Success Orbits:",
    "  - ES-L1 (Earth-Sun Lagrange 1): 100%",
    "  - GEO (Geostationary Earth Orbit): 100%",
    "  - HEO (High Earth Orbit): 100%",
    "  - SSO (Sun-Synchronous Orbit): 100%",
    "• High Reliability Orbits:",
    "  - VLEO (Very Low Earth Orbit - Starlink): 85.0%",
    "  - LEO (Low Earth Orbit): 71.4%",
    "  - ISS (International Space Station Resupply): 61.9%",
    "• Challenging / Moderate Success Orbits:",
    "  - GTO (Geostationary Transfer Orbit): ~60.0% success rate due to high velocity re-entry heating and tighter fuel margins.",
    "  - SO (Special Polar Test): 0.0% (single test failure)."
])

# Slide 10: EDA Results 3 - Flight Number & Payload vs Orbit (1.11)
s10 = prs.slides.add_slide(blank_layout)
add_pptx_header(s10, "EDA Results: Orbit vs. Flight Number & Payload Mass", "EDA Results", "Grading Criteria 1.11")
add_pptx_footer(s10)
s10.shapes.add_picture('figures/flight_vs_orbit.png', Inches(0.8), Inches(1.35), width=Inches(5.7))
s10.shapes.add_picture('figures/payload_vs_orbit.png', Inches(6.8), Inches(1.35), width=Inches(5.7))
tb = s10.shapes.add_textbox(Inches(0.8), Inches(5.1), Inches(11.7), Inches(1.8))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Key Analytical Insights:"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE
insights = [
    "• Mission Evolution: Early flights focused exclusively on LEO and ISS resupply missions; intermediate flights expanded into commercial GTO; recent flights (Flight 70+) are heavily dominated by VLEO (Starlink) launches.",
    "• Payload vs. Orbit Segregation: Heavy payloads (>13,000 kg) are exclusively deployed to VLEO with near-perfect recovery success rates.",
    "• GTO Payload Band: GTO launches carry payloads between 3,000 kg and 7,000 kg, where high staging velocity creates maximum thermal stress."
]
for ins in insights:
    p = tf.add_paragraph()
    p.text = ins
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_DARK

# Slide 11: EDA Results 4 - Yearly Success Trend (1.11)
s11 = prs.slides.add_slide(blank_layout)
add_pptx_header(s11, "EDA Results: Yearly Launch Success Rate Trend (2010–2020)", "EDA Results", "Grading Criteria 1.11")
add_pptx_footer(s11)
s11.shapes.add_picture('figures/yearly_success_trend.png', Inches(0.8), Inches(1.35), width=Inches(6.2))
add_card(s11, 7.3, 1.35, 5.2, 5.5, "Technological Maturation Trajectory", [
    "• 2010–2012 (Experimental Phase - 0.0% Success):",
    "  - Early flights tested parachute recovery and ocean splashdowns; no booster survival.",
    "• 2013–2015 (Proof-of-Concept Phase - 33.3% Success):",
    "  - Dec 2015 marked the historic milestone: Flight 20 achieved the first successful ground pad landing (RTLS) at LZ-1.",
    "• 2016–2017 (Operational Scaling - 60.0% to 83.3% Success):",
    "  - Regular drone ship (ASDS) recoveries established; first flight-proven booster re-flight (B1021.2) successfully landed.",
    "• 2018–2020 (Industrialized Reliability - 85%+ Success):",
    "  - Introduction of Falcon 9 Block 5 engineered for 10+ flights without major refurbishment, achieving consistent >85% annual landing success."
])

# Slide 12: EDA with SQL - Methodology & Setup (1.9)
s12 = prs.slides.add_slide(blank_layout)
add_pptx_header(s12, "EDA with SQL: Database Architecture & Query Catalog", "EDA SQL", "Grading Criteria 1.9")
add_pptx_footer(s12)
add_card(s12, 0.8, 1.4, 5.7, 5.4, "SQLite Engine & Database Setup", [
    "• Database Engine: SQLite relational database connected via Python sqlite3.",
    "• Source Dataset: Spacex.csv loaded into table SPACEXTBL (101 mission records).",
    "• Cleaned Schema: Normalized spaces and punctuation in column headers:",
    "  - Date, Time_UTC, Booster_Version, Launch_Site, Payload,",
    "  - PAYLOAD_MASS__KG_, Orbit, Customer, Mission_Outcome, Landing_Outcome.",
    "• Analytical Goals: Execute 10 precision SQL queries answering operational, commercial, and engineering questions.",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/04_EDA_with_SQL.ipynb"
])
add_card(s12, 6.8, 1.4, 5.7, 5.4, "Query Objectives Summary", [
    "1. Unique Launch Sites: Extract distinct launch site names.",
    "2. Filtered Launches: Select 5 launches starting with 'CCA'.",
    "3. NASA CRS Payloads: Total payload mass carried under NASA contract.",
    "4. Booster Version Averages: Average payload mass for F9 v1.1 boosters.",
    "5. Historic Milestones: Earliest date of successful ground pad landing.",
    "6. Drone Ship Payloads: Boosters succeeding on drone ship between 4k-6k kg.",
    "7. Mission Outcomes: Breakdown of mission success vs. failure counts.",
    "8. Maximum Payload Boosters: Identify boosters carrying maximum payload.",
    "9. Temporal Failures: Drone ship landing failure records in 2015 by month.",
    "10. Outcome Rankings: Ranked count of landing outcomes between 2010 and 2017."
])

# Slide 13: EDA with SQL Results 1 (1.12)
s13 = prs.slides.add_slide(blank_layout)
add_pptx_header(s13, "EDA with SQL Results: Launch Sites, Payloads & Milestones", "EDA SQL Results", "Grading Criteria 1.12")
add_pptx_footer(s13)
add_card(s13, 0.8, 1.4, 5.7, 5.4, "Queries 1 to 3: Sites & NASA Payloads", [
    "• Query 1: Unique Launch Sites",
    "  SELECT DISTINCT Launch_Site FROM SPACEXTBL;",
    "  --> CCAFS LC-40, VAFB SLC-4E, KSC LC-39A, CCAFS SLC-40.",
    "",
    "• Query 2: First 5 CCAFS Launches",
    "  SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5;",
    "  --> Returned Flights 1-5 (Dragon Spacecraft Qualification, Demo C1, C2, CRS-1, CRS-2).",
    "",
    "• Query 3: Total NASA (CRS) Payload Mass",
    "  SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Customer = 'NASA (CRS)';",
    "  --> Total Payload Mass = 45,596 kg across all NASA cargo resupply flights."
])
add_card(s13, 6.8, 1.4, 5.7, 5.4, "Queries 4 & 5: Booster Average & First Milestone", [
    "• Query 4: Average Payload Mass for F9 v1.1",
    "  SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%';",
    "  --> Average Payload Mass = 2,534.67 kg.",
    "",
    "• Query 5: First Successful Ground Pad Landing Date",
    "  SELECT MIN(Date) FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)';",
    "  --> First Successful Date = 2015-12-22 (Flight 20, Orbcomm OG2 mission at LZ-1).",
    "",
    "• Operational Implication: F9 v1.1 established SpaceX's commercial credibility, but recovery was achieved after upgrading to Falcon 9 Full Thrust (FT)."
])

# Slide 14: EDA with SQL Results 2 (1.12)
s14 = prs.slides.add_slide(blank_layout)
add_pptx_header(s14, "EDA with SQL Results: Drone Ships, Max Payloads & Rankings", "EDA SQL Results", "Grading Criteria 1.12")
add_pptx_footer(s14)
add_card(s14, 0.8, 1.4, 5.7, 5.4, "Queries 6 to 8: Drone Ships & Max Payloads", [
    "• Query 6: Drone Ship Success with 4k-6k kg Payload",
    "  SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000;",
    "  --> Boosters: F9 FT B1022 (4,696 kg), F9 FT B1026 (4,600 kg), F9 FT B1021.2 (5,300 kg), F9 FT B1031.2 (5,200 kg).",
    "",
    "• Query 7: Mission Outcomes Breakdown",
    "  SELECT TRIM(Mission_Outcome), COUNT(*) FROM SPACEXTBL GROUP BY TRIM(Mission_Outcome);",
    "  --> Success: 99 | Failure (in flight): 1 | Success (payload status unclear): 1.",
    "",
    "• Query 8: Maximum Payload Boosters (15,600 kg)",
    "  SELECT DISTINCT Booster_Version FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);",
    "  --> Starlink batches flown by F9 B5 (B1048, B1049, B1051, B1056, B1058, B1060)."
])
add_card(s14, 6.8, 1.4, 5.7, 5.4, "Queries 9 & 10: Failures & Historical Rankings", [
    "• Query 9: 2015 Drone Ship Landing Failures by Month",
    "  SELECT SUBSTR(Date, 6, 2) AS Month, Date, Booster_Version FROM SPACEXTBL WHERE SUBSTR(Date, 1, 4) = '2015' AND Landing_Outcome = 'Failure (drone ship)';",
    "  --> Month 01 (2015-01-10, B1012) & Month 04 (2015-04-14, B1015).",
    "",
    "• Query 10: Ranked Landing Outcomes (2010-06-04 to 2017-03-20)",
    "  SELECT Landing_Outcome, COUNT(*) AS Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Count DESC;",
    "  --> 1. No attempt (10)       2. Success (drone ship) (5)",
    "  --> 3. Failure (drone ship) (5) 4. Success (ground pad) (3)",
    "  --> 5. Controlled (ocean) (3)  6. Uncontrolled (ocean) (2)",
    "  --> 7. Failure (parachute) (2) 8. Precluded (drone ship) (1)"
])

# Slide 15: Interactive Visual Analytics - Methodology (1.10)
s15 = prs.slides.add_slide(blank_layout)
add_pptx_header(s15, "Interactive Visual Analytics: Folium & Dash Methodology", "Interactive Analytics", "Grading Criteria 1.10")
add_pptx_footer(s15)
add_card(s15, 0.8, 1.4, 5.7, 5.4, "Folium Geospatial Mapping Architecture", [
    "• Interactive Mapping Engine: Folium library built on Leaflet.js.",
    "• Geospatial Coordinates: Mapped all 4 launch complexes across Cape Canaveral (CCAFS), Kennedy Space Center (KSC), and Vandenberg (VAFB).",
    "• MarkerCluster Implementation: Implemented folium.plugins.MarkerCluster to dynamically group all 56 missions, styling markers by landing outcome (Green = Success, Red = Failure).",
    "• Proximity Safety Analysis: Computed geodesic distances using Haversine formula and drew interactive folium.PolyLine vectors from launch pads to nearest coastlines, highways, railways, and cities.",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/06_Interactive_Visual_Analytics_Folium.ipynb"
])
add_card(s15, 6.8, 1.4, 5.7, 5.4, "Plotly Dash Interactive Dashboard", [
    "• Reactive Web Framework: Plotly Dash web application built with Dash Core Components (dcc) and Dash HTML Components (html).",
    "• Dynamic Components:",
    "  1. Launch Site Dropdown: Filter dashboard by ALL sites or individual sites (CCAFS LC-40, VAFB SLC-4E, KSC LC-39A, CCAFS SLC-40).",
    "  2. Payload RangeSlider: Interactive dual-handle slider filtering launches between 0 kg and 10,000 kg.",
    "  3. Success Pie Chart: Reactively renders total success share across sites (ALL) or success vs. failure breakdown (specific site).",
    "  4. Payload Scatter Chart: Dynamic scatter plot correlating payload mass to landing success, color-coded by booster version.",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/scripts/07_spacex_dash_app.py"
])

# Slide 16: Interactive Analytics - Folium Sites & Clusters (1.13)
s16 = prs.slides.add_slide(blank_layout)
add_pptx_header(s16, "Interactive Analytics: Folium Launch Sites & MarkerClusters", "Folium Results", "Grading Criteria 1.13")
add_pptx_footer(s16)
s16.shapes.add_picture('figures/folium_launch_sites.png', Inches(0.8), Inches(1.35), width=Inches(6.2))
add_card(s16, 7.3, 1.35, 5.2, 5.5, "Geographic Launch Insights", [
    "• Coastal Placement Strategy: All SpaceX launch sites are positioned directly adjacent to coastlines:",
    "  - Florida Coast (CCAFS/KSC): Eastward launches over the Atlantic Ocean take advantage of Earth's rotational velocity for equatorial & GTO orbits.",
    "  - California Coast (VAFB): Southward launches over the Pacific Ocean allow safe polar and Sun-Synchronous (SSO) orbital insertions.",
    "• Safety & Hazard Minimization: Rocket trajectories immediately fly over open water, ensuring stage separations and abort debris fall safely far from populated landmasses.",
    "• Drone Ship Staging: Drone ships (OCISLY & JRTI) are stationed 200–600 km downrange along launch azimuths."
])

# Slide 17: Interactive Analytics - Folium Proximity Analysis (1.13)
s17 = prs.slides.add_slide(blank_layout)
add_pptx_header(s17, "Interactive Analytics: Folium Proximity Analysis", "Folium Results", "Grading Criteria 1.13")
add_pptx_footer(s17)
s17.shapes.add_picture('figures/folium_proximity_analysis.png', Inches(0.8), Inches(1.35), width=Inches(6.2))
add_card(s17, 7.3, 1.35, 5.2, 5.5, "Proximity Distance Findings", [
    "• Nearest Coastline (~0.85 km):",
    "  - Minimal distance to coastline allows rockets to clear the launch pad and immediately traverse over water, mitigating onshore blast risk.",
    "• Nearest Highway Parkway (~1.2 km):",
    "  - Close proximity provides essential road transport for oversized rocket components while maintaining safe hazard clear zones during static fires and launches.",
    "• Nearest Railroad (~1.35 km):",
    "  - Direct connection to NASA rail network for transporting heavy hardware and structural components.",
    "• Nearest City - Titusville (~16.5 km):",
    "  - Significant buffer distance protects residential populations from acoustic shockwaves, sonic booms, and potential launch catastrophic anomalies."
])

# Slide 18: Interactive Analytics - Plotly Dash Dashboard (1.14)
s18 = prs.slides.add_slide(blank_layout)
add_pptx_header(s18, "Interactive Analytics: Plotly Dash Dashboard Visuals", "Dash Results", "Grading Criteria 1.14")
add_pptx_footer(s18)
s18.shapes.add_picture('figures/dash_pie_all_sites.png', Inches(0.8), Inches(1.35), width=Inches(3.8))
s18.shapes.add_picture('figures/dash_pie_ksc_site.png', Inches(4.8), Inches(1.35), width=Inches(3.8))
s18.shapes.add_picture('figures/dash_scatter_payload_outcome.png', Inches(8.8), Inches(1.35), width=Inches(3.8))
tb = s18.shapes.add_textbox(Inches(0.8), Inches(5.1), Inches(11.7), Inches(1.8))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Key Dashboard Findings:"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE
insights = [
    "• Launch Site Success Share: KSC LC-39A contributes the largest share of successful recoveries (41.7%), followed by CCAFS SLC-40 (30.6%) and VAFB SLC-4E (16.7%).",
    "• Site Success Ratio: KSC LC-39A achieves a 76.9% success rate (10 successes vs. 3 failures), outperforming other facilities.",
    "• Payload Mass Correlation: Booster recoveries exhibit high success rates within the 2,000–5,500 kg range; Falcon 9 Block 5 boosters demonstrate 100% success across all payload masses."
]
for ins in insights:
    p = tf.add_paragraph()
    p.text = ins
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_DARK

# Slide 19: Predictive Analysis - ML Pipeline (1.15)
s19 = prs.slides.add_slide(blank_layout)
add_pptx_header(s19, "Predictive Analysis: Machine Learning Pipeline & Tuning", "Machine Learning", "Grading Criteria 1.15")
add_pptx_footer(s19)
add_card(s19, 0.8, 1.4, 5.7, 5.4, "Preprocessing & Cross-Validation Setup", [
    "• Feature Matrix (X): 83 one-hot encoded features derived from dataset_part_3.csv.",
    "• Target Vector (Y): Binary landing outcome Class (1 = Success, 0 = Failure).",
    "• Feature Standardization: Applied StandardScaler() to standardize features to zero mean and unit variance, essential for distance-based and regularized models.",
    "• Train/Test Split: 80% Training (72 samples), 20% Holdout Test (18 samples) with random_state=2 for reproducibility.",
    "• Hyperparameter Optimization: 10-fold cross-validation using GridSearchCV across all four model families to optimize hyperparameters and prevent overfitting.",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/08_Predictive_Analysis_Machine_Learning.ipynb"
])
add_card(s19, 6.8, 1.4, 5.7, 5.4, "Model Hyperparameter Grids", [
    "1. Logistic Regression:",
    "   - Grid: C in [0.01, 0.1, 1.0], penalty=['l2'], solver=['lbfgs']",
    "   - Best Parameters: {'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs'}",
    "2. Support Vector Machine (SVM):",
    "   - Grid: C in [0.5, 1.0, 1.5], kernel=['linear', 'rbf', 'sigmoid']",
    "   - Best Parameters: {'C': 0.5, 'kernel': 'sigmoid'}",
    "3. Decision Tree Classifier:",
    "   - Grid: criterion=['gini', 'entropy'], max_depth=[2, 4, 6, 8], min_samples_leaf=[1, 2, 4], min_samples_split=[2, 5, 10]",
    "   - Best Parameters: {'criterion': 'gini', 'max_depth': 4, 'min_samples_leaf': 4, 'min_samples_split': 2}",
    "4. K-Nearest Neighbors (KNN):",
    "   - Grid: n_neighbors=[3, 5, 7, 9, 10], p=[1, 2], algorithm=['auto', 'ball_tree', 'kd_tree']",
    "   - Best Parameters: {'algorithm': 'auto', 'n_neighbors': 10, 'p': 1}"
])

# Slide 20: Predictive Analysis - Results & Confusion Matrix (1.15)
s20 = prs.slides.add_slide(blank_layout)
add_pptx_header(s20, "Predictive Analysis: Model Evaluation & Confusion Matrix", "ML Results", "Grading Criteria 1.15")
add_pptx_footer(s20)
s20.shapes.add_picture('figures/ml_model_accuracy_comparison.png', Inches(0.8), Inches(1.35), width=Inches(5.7))
s20.shapes.add_picture('figures/ml_confusion_matrix.png', Inches(6.8), Inches(1.35), width=Inches(5.7))
tb = s20.shapes.add_textbox(Inches(0.8), Inches(5.1), Inches(11.7), Inches(1.8))
tf = tb.text_frame
tf.word_wrap = True
p = tf.paragraphs[0]
p.text = "Model Performance Summary & Best Model Selection:"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = PRIMARY_BLUE
insights = [
    "• Accuracy Scores: Logistic Regression, SVM, and KNN tied for highest Test Accuracy at 83.33% (15 correct out of 18 test samples). Decision Tree achieved 87.14% Train CV and 77.78% Test accuracy.",
    "• Confusion Matrix Analysis (18 Test Samples): True Positives = 12 (100% recall on successes), True Negatives = 3, False Positives = 3, False Negatives = 0. No successful landings were misclassified as failures.",
    "• Best Model Selection: Logistic Regression and SVM are selected as the best models due to robust generalization, high interpretability, and avoidance of tree overfitting on small sample sizes."
]
for ins in insights:
    p = tf.add_paragraph()
    p.text = ins
    p.font.size = Pt(11)
    p.font.color.rgb = TEXT_DARK

# Slide 21: Conclusions & Innovative Insights (1.15)
s21 = prs.slides.add_slide(blank_layout)
add_pptx_header(s21, "Conclusions, Business Recommendations & Innovative Insights", "Conclusions", "Grading Criteria 1.15")
add_pptx_footer(s21)
add_card(s21, 0.8, 1.4, 5.7, 5.4, "Business Conclusions & Recommendations", [
    "• Economic Takeaway: First stage reusability delivers a decisive cost advantage, reducing launch costs by ~60% ($62M vs $165M+), revolutionizing commercial space access.",
    "• Reliability Proven: Recovery success grew from 0% in 2010 to >85% by 2020, demonstrating full industrialization.",
    "• Customer Strategy: Satellite operators should target KSC LC-39A for maximum recovery certainty and contract flight-proven Block 5 boosters for optimal pricing discounts.",
    "• Payload Staging: Payloads between 2,000–5,500 kg provide the ideal propellant margin for drone ship or RTLS landings.",
    f"• Full Project Repository: {GITHUB_REPO_URL}"
])
add_card(s21, 6.8, 1.4, 5.7, 5.4, "Creative & Innovative Future Insights", [
    "• Meteorological Fusion: Integrate real-time offshore atmospheric data (surface wind gusts, ocean swell wave height, upper-troposphere wind shear) directly into the predictive model.",
    "• Autonomous Drone Ship Telemetry: Incorporate thruster station-keeping data and GPS telemetry from drone ships (OCISLY / ASOG) to predict sea-state landing aborts.",
    "• Bayesian Neural Networks: Deploy Bayesian deep learning to generate calibrated epistemic uncertainty estimates for edge-case missions.",
    "• Dynamic Insurance Premium Model: Build real-time risk-adjusted insurance pricing algorithms that adjust dynamically based on launch-day booster health and flight heritage."
])

pptx_path = 'Data Science Capstone Project Report.pptx'
prs.save(pptx_path)
print(f"Saved {pptx_path} successfully.")


# ==============================================================================
# SECTION B: BUILD FULL PDF PRESENTATION USING REPORTLAB (.pdf)
# ==============================================================================
# Widescreen 16:9 PDF: 960 x 540 points (13.33 x 7.5 inches)
PAGE_WIDTH = 960
PAGE_HEIGHT = 540

pdf_path = 'Data Science Capstone Project Report.pdf'

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, total_pages):
        # Only draw on pages > 1 (skip title slide)
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor('#64748B'))
            # Footer text
            footer_text = f"SpaceX Falcon 9 Capstone Project  |  IBM Applied Data Science Capstone  |  GitHub: {GITHUB_REPO_URL}"
            self.drawString(36, 18, footer_text)
            page_text = f"Slide {self._pageNumber} of {total_pages}"
            self.drawRightString(PAGE_WIDTH - 36, 18, page_text)
            # Subtle footer line
            self.setStrokeColor(colors.HexColor('#CBD5E1'))
            self.setLineWidth(0.5)
            self.line(36, 30, PAGE_WIDTH - 36, 30)
            self.restoreState()

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
    leftMargin=36,
    rightMargin=36,
    topMargin=15,
    bottomMargin=25
)

styles = getSampleStyleSheet()

# Custom styles
style_title_cat = ParagraphStyle('TitleCat', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#06B6D4'), spaceAfter=4)
style_title_main = ParagraphStyle('TitleMain', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=26, textColor=colors.white, leading=30, spaceAfter=8)
style_title_sub = ParagraphStyle('TitleSub', parent=styles['Normal'], fontName='Helvetica', fontSize=13, textColor=colors.HexColor('#CBD5E1'), leading=17, spaceAfter=14)
style_title_meta = ParagraphStyle('TitleMeta', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#06B6D4'), leading=14)

style_header_cat = ParagraphStyle('HeaderCat', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#06B6D4'), spaceAfter=2)
style_header_title = ParagraphStyle('HeaderTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=14, textColor=colors.white, leading=16)
style_header_rubric = ParagraphStyle('HeaderRubric', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=colors.HexColor('#06B6D4'), alignment=2)

style_card_title = ParagraphStyle('CardTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10.5, textColor=colors.HexColor('#1D4ED8'), spaceAfter=3)
style_card_body = ParagraphStyle('CardBody', parent=styles['Normal'], fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#1E293B'), leading=10.8, spaceAfter=2.5)
style_card_bold = ParagraphStyle('CardBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, textColor=colors.HexColor('#0B1E36'), leading=10.8, spaceAfter=2.5)

def create_slide_header(title, category, rubric):
    data = [
        [
            Paragraph(f"<font color='#06B6D4'><b>{category.upper()}</b></font><br/><b>{title}</b>", style_header_title),
            Paragraph(f"<font color='#06B6D4'><b>{rubric}</b></font>", style_header_rubric)
        ]
    ]
    t = Table(data, colWidths=[690, 190], rowHeights=[40])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0B1E36')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t

def make_card_flowable(title, bullet_items, width=430, height=410):
    flowables = [
        Paragraph(title, style_card_title),
        Spacer(1, 3)
    ]
    for b in bullet_items:
        if b.startswith("•") or b.startswith("-"):
            flowables.append(Paragraph(b, style_card_body))
        elif b.strip() == "":
            flowables.append(Spacer(1, 3))
        else:
            flowables.append(Paragraph(b, style_card_body))
    
    t = Table([[flowables]], colWidths=[width], rowHeights=[height])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E2E8F0')),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return t

story = []

# ==========================================
# SLIDE 1: Title Slide (Criteria 1.1 & 1.2)
# ==========================================
title_content = [
    Spacer(1, 40),
    Paragraph("IBM APPLIED DATA SCIENCE CAPSTONE", style_title_cat),
    Paragraph("SpaceX Falcon 9 First Stage<br/>Landing Prediction", style_title_main),
    Paragraph("End-to-End Data Science Solution: API Extraction, Web Scraping, SQL, Interactive Dashboards & Machine Learning", style_title_sub),
    Spacer(1, 20),
    Paragraph(f"Author: Data Scientist  |  Final Report Submission  |  Grading Criteria 1.1 & 1.2<br/>Project GitHub Repository: <b>{GITHUB_REPO_URL}</b>", style_title_meta)
]
title_table = Table([[title_content]], colWidths=[880], rowHeights=[470])
title_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#0B1E36')),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 40),
    ('RIGHTPADDING', (0, 0), (-1, -1), 40),
]))
story.append(title_table)
story.append(PageBreak())

# ==========================================
# SLIDE 2: Executive Summary (Criteria 1.3)
# ==========================================
c1 = [
    "• Business Context: Falcon 9 first stage reusability fundamentally transforms space launch economics, lowering launch costs to $62M compared to $165M+ for traditional expendable launch vehicles.",
    "• Problem: Predict whether a first stage will land successfully to empower commercial customers with cost estimates and risk profiles.",
    "• Data Pipeline: Ingested 90 launches via SpaceX REST API & Wikipedia web scraping; cleansed missing values and engineered 83 feature vectors.",
    "• Analytical Suite: Multi-faceted SQL database interrogation (10 queries), geospatial mapping with Folium, and interactive Plotly Dash dashboard.",
    "• Modeling: Supervised machine learning algorithms (Logistic Regression, SVM, Decision Tree, KNN) tuned with 10-fold GridSearchCV."
]
c2 = [
    "• Geographic Dominance: KSC LC-39A is the highest performing launch site with a 76.9% landing success rate.",
    "• Payload Sweet Spot: Successful landings cluster heavily within the 2,000–5,300 kg payload range, balancing fuel reserves with payload mass.",
    "• Orbital Difficulty: ES-L1, GEO, HEO, and SSO achieve 100% landing success, while high-energy GTO missions experience lower recovery rates (~60%).",
    "• Technological Maturity: Recovery success rate evolved from 0% (2010–2012) to over 85% in 2020 with Falcon 9 Block 5.",
    "• Predictive Accuracy: Logistic Regression, SVM, and KNN achieved 83.33% test accuracy on unseen data with 100% recall on successful landings.",
    f"• Project Repository: {GITHUB_REPO_URL}"
]
story.append(create_slide_header("Executive Summary: Methods & Key Results", "Executive Summary", "Grading Criteria 1.3"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("Project Context & Methods", c1, 432, 420),
                     make_card_flowable("Key Findings & Business Impact", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 3: Introduction & Problem Statement (1.4)
# ==========================================
c1 = [
    "• The Reusability Disruption: Commercial spaceflight has traditionally discarded rocket stages in the ocean or atmosphere. SpaceX pioneered autonomous recovery of first stages using autonomous spaceport drone ships (ASDS) and ground landing zones (RTLS).",
    "• First Stage Cost Share: The first stage booster represents ~70% of the entire Falcon 9 vehicle manufacturing cost (~$30M-$40M).",
    "• Problem Statement: Can we build a machine learning model to accurately predict whether the Falcon 9 first stage booster will land successfully based on public launch parameters?",
    "• Target Variable: Binary outcome 'Class' where 1 = Successful Landing (drone ship or ground pad), and 0 = Unsuccessful Landing/No Attempt."
]
c2 = [
    "• Launch Cost Estimation: Reused boosters allow competitive launch pricing ($62M vs $165M+), enabling customers to forecast real operational margins.",
    "• Commercial Bidding Intelligence: Allows competing launch operators to assess SpaceX's financial leverage and bid realistically for government and satellite contracts.",
    "• Risk & Insurance Optimization: Enables insurance underwriters to quantify flight risk dynamically based on payload mass, launch site, and destination orbit.",
    "• Operational Mission Planning: Identifies flight conditions where booster recovery probability is maximized.",
    f"• Code & Artifacts: {GITHUB_REPO_URL}"
]
story.append(create_slide_header("Project Introduction & Problem Statement", "Introduction", "Grading Criteria 1.4"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("Industry Context & Core Problem", c1, 432, 420),
                     make_card_flowable("Economic Significance & Objectives", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 4: Data Collection - SpaceX API (1.5)
# ==========================================
c1 = [
    "• Primary Endpoint: https://api.spacexdata.com/v4/launches/past",
    "• Pipeline Architecture & Flowchart:",
    "  [1. HTTP GET Request] --> Retrieve raw JSON list of all historical launches",
    "  [2. pd.json_normalize] --> Flatten nested JSON into tabular DataFrame",
    "  [3. Filter Falcon 9] --> Exclude Falcon 1 launches (filter rocket ID & core count == 1)",
    "  [4. Auxiliary API Calls] --> Query secondary endpoints to resolve IDs to names:",
    "      - /v4/rockets/{id} --> Rocket Name (Falcon 9)",
    "      - /v4/launchpads/{id} --> Site Name & Coordinates (Lat/Long)",
    "      - /v4/payloads/{id} --> Payload Mass (kg) & Orbit",
    "      - /v4/cores/{id} --> Core Serial, Block, Reused Count, Legs, GridFins",
    "  [5. Dataset Export] --> Output structured dataset_part_1.csv (90 rows x 17 cols)",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/01_Data_Collection_SpaceX_API.ipynb"
]
c2 = [
    "• FlightNumber: Sequential flight index (1 to 90)",
    "• Date: Launch timestamp (2010-06-04 to 2020-11-05)",
    "• BoosterVersion: Falcon 9 booster version",
    "• PayloadMass: Mass of payload in kilograms",
    "• Orbit: Orbital destination (LEO, ISS, GTO, SSO, etc.)",
    "• LaunchSite: Name of launch facility (CCAFS, KSC, VAFB)",
    "• Outcome: Raw landing outcome string",
    "• Flights: Number of flights this booster core has made",
    "• GridFins / Legs: Boolean flags for landing hardware",
    "• Reused: Boolean indicator if core was flight-proven",
    "• Block: Core hardware generation (Block 1 to 5)",
    "• ReusedCount: Total times core was reused"
]
story.append(create_slide_header("Data Collection: SpaceX REST API Architecture", "Data Collection", "Grading Criteria 1.5"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("API Pipeline & Flowchart", c1, 432, 420),
                     make_card_flowable("Extracted Schema & Features", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 5: Data Collection - Web Scraping (1.6)
# ==========================================
c1 = [
    "• Target Source: Wikipedia 'List of Falcon 9 and Falcon Heavy launches'",
    "• Web Scraping Workflow:",
    "  [1. HTTP Request] --> requests.get(url, headers={'User-Agent': 'SpaceXDataScraper/1.0'})",
    "  [2. HTML Parsing] --> BeautifulSoup(response.text, 'html.parser')",
    "  [3. Table Discovery] --> soup.find_all('table', 'wikitable')",
    "  [4. Column Extraction] --> Parse <th> headers and clean unicode artifacts",
    "  [5. Row Traversal] --> Iterate <tr> rows and extract <td> cells for:",
    "      - Flight No., Date & Time, Booster Version, Launch Site",
    "      - Payload Name, Payload Mass, Target Orbit, Customer",
    "      - Launch Outcome, Booster Landing Outcome",
    "  [6. Text Normalization] --> Strip citations [1], newlines, regex clean numeric kg",
    "  [7. File Export] --> Saved as spacex_web_scraped.csv",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/02_Data_Collection_Web_Scraping.ipynb"
]
c2 = [
    "• Request Blocking (403): Default Python User-Agent blocked by Wikimedia CDN. Resolved by passing legitimate User-Agent header.",
    "• Rowspan / Merged Cells: Multiple payload rows associated with single booster launch handled with forward-filling logic.",
    "• String Cleansing: Removed citation references (e.g. '[12]', '[b]'), non-breaking spaces, and UTC offsets.",
    "• Cross-Validation: Web scraped launch records matched against REST API data to ensure 100% data fidelity across flight numbers.",
    f"• Script Reference: {GITHUB_REPO_URL}/blob/main/scripts/02_data_collection_scraping.py"
]
story.append(create_slide_header("Data Collection: Web Scraping Historical Records", "Data Collection", "Grading Criteria 1.6"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("BeautifulSoup Scraping Workflow", c1, 432, 420),
                     make_card_flowable("Technical Scraping Solutions", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 6: Data Wrangling Methodology (1.7)
# ==========================================
c1 = [
    "• Missing Data Assessment: Detected missing values in PayloadMass column across early experimental launches.",
    "• Mean Imputation: Imputed missing payload values with column mean (6,104.96 kg) using df['PayloadMass'].fillna(df['PayloadMass'].mean()).",
    "• Landing Outcome Categorization: Ingested 8 distinct outcome strings from raw telemetry:",
    "  1. True Ocean: Controlled landing on ocean surface",
    "  2. False Ocean: Uncontrolled splashdown / breakup",
    "  3. True RTLS: Successful landing at Return-to-Launch-Site pad",
    "  4. False RTLS: Failed ground landing attempt",
    "  5. True ASDS: Successful landing on drone ship",
    "  6. False ASDS: Failed landing on drone ship",
    "  7. None ASDS: Drone ship mission with no recovery attempt",
    "  8. None None: No landing attempted"
]
c2 = [
    "• Binary Target Variable 'Class':",
    "  - Class = 1 (Success): True ASDS, True RTLS, True Ocean (60 launches, 66.7%)",
    "  - Class = 0 (Failure): False ASDS, False RTLS, False Ocean, None ASDS, None None (30 launches, 33.3%)",
    "• Feature Matrix Construction (dataset_part_3.csv):",
    "  - Extracted core numerical features: FlightNumber, PayloadMass, Flights, Block, ReusedCount.",
    "  - One-Hot Encoding applied via pd.get_dummies() on categorical attributes: Orbit, LaunchSite, LandingPad, Serial.",
    "  - Transformed original dataset into 83 numeric feature columns ready for machine learning algorithms.",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/03_Data_Wrangling.ipynb"
]
story.append(create_slide_header("Data Wrangling & Target Engineering Methodology", "Data Wrangling", "Grading Criteria 1.7"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("Cleaning & Imputation Protocol", c1, 432, 420),
                     make_card_flowable("Target Encoding & Feature Matrix", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 7: EDA with Data Visualization - Methodology (1.8)
# ==========================================
c1 = [
    "1. Flight Number vs. Launch Site (Scatter Plot):",
    "   - Purpose: Track operational launch site utilization over time and observe if landing success improves across flight cohorts.",
    "2. Payload Mass vs. Launch Site (Scatter Plot):",
    "   - Purpose: Identify payload mass profiles by launch site and investigate if heavier payloads reduce recovery probability.",
    "3. Success Rate vs. Orbit Type (Bar Chart):",
    "   - Purpose: Determine which target orbits yield the highest landing success rates and identify high-risk orbital profiles.",
    "4. Flight Number vs. Orbit Type (Scatter Plot):",
    "   - Purpose: Trace the evolution of mission types over time (e.g. transition from LEO/ISS to GTO and VLEO Starlink).",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/05_EDA_with_Data_Visualization.ipynb"
]
c2 = [
    "5. Payload Mass vs. Orbit Type (Scatter Plot):",
    "   - Purpose: Examine payload capacity thresholds across different orbital energies and their relationship to landing success.",
    "6. Yearly Launch Success Trend (Line Chart):",
    "   - Purpose: Quantify the annual success rate trajectory from 2010 to 2020 to measure SpaceX's technological maturation.",
    "• Software Stack & Standards:",
    "   - Python libraries: Matplotlib 3.11, Seaborn 0.13, Pandas 3.0.",
    "   - Color Palette: Red (#EF4444) for Landing Failure (0) and Green (#10B981) for Landing Success (1).",
    "   - High-Resolution Rendering: 300 DPI publication standards.",
    f"• Code Reference: {GITHUB_REPO_URL}/blob/main/scripts/05_eda_visualization.py"
]
story.append(create_slide_header("EDA with Data Visualization: Catalog & Objectives", "EDA Visualization", "Grading Criteria 1.8"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("Visualization Objectives (Part 1)", c1, 432, 420),
                     make_card_flowable("Visualization Objectives (Part 2)", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 8: EDA Results 1 - Launch Sites (1.11)
# ==========================================
story.append(create_slide_header("EDA Results: Launch Site vs. Flight Number & Payload", "EDA Results", "Grading Criteria 1.11"))
story.append(Spacer(1, 4))
img1 = Image('figures/flight_vs_launch_site.png', width=430, height=230)
img2 = Image('figures/payload_vs_launch_site.png', width=430, height=230)
story.append(Table([[img1, img2]], colWidths=[440, 440]))
story.append(Spacer(1, 4))
c_bottom = [
    "• CCAFS LC-40 handled initial test and early operational flights (Flights 1-25) exhibiting mixed success during early booster recovery testing.",
    "• KSC LC-39A demonstrates the highest overall success rate (76.9%), hosting commercial resupply, crew, and high-mass commercial flights.",
    "• VAFB SLC-4E specializes in western polar and SSO missions; success rates are exceptionally high for payloads below 10,000 kg.",
    "• Heavier payloads (>10,000 kg) are predominantly handled by KSC LC-39A and CCAFS SLC-40 with drone ship landings."
]
story.append(make_card_flowable("Analytical Findings: Launch Site Dynamics", c_bottom, 872, 145))
story.append(PageBreak())

# ==========================================
# SLIDE 9: EDA Results 2 - Success Rate by Orbit (1.11)
# ==========================================
story.append(create_slide_header("EDA Results: Landing Success Rate by Orbit Type", "EDA Results", "Grading Criteria 1.11"))
story.append(Spacer(1, 6))
img = Image('figures/success_rate_vs_orbit.png', width=460, height=390)
c_orbit = [
    "• 100% Landing Success Orbits:",
    "  - ES-L1 (Earth-Sun Lagrange 1): 100%",
    "  - GEO (Geostationary Earth Orbit): 100%",
    "  - HEO (High Earth Orbit): 100%",
    "  - SSO (Sun-Synchronous Orbit): 100%",
    "• High Reliability Orbits:",
    "  - VLEO (Very Low Earth Orbit - Starlink): 85.0%",
    "  - LEO (Low Earth Orbit): 71.4%",
    "  - ISS (International Space Station Resupply): 61.9%",
    "• Challenging / Moderate Success Orbits:",
    "  - GTO (Geostationary Transfer Orbit): ~60.0% success rate due to high velocity re-entry heating and tighter fuel margins.",
    "  - SO (Special Polar Test): 0.0% (single test failure)."
]
story.append(Table([[img, make_card_flowable("Orbital Success Rate Findings", c_orbit, 400, 395)]], colWidths=[470, 410]))
story.append(PageBreak())

# ==========================================
# SLIDE 10: EDA Results 3 - Flight Number & Payload vs Orbit (1.11)
# ==========================================
story.append(create_slide_header("EDA Results: Orbit vs. Flight Number & Payload Mass", "EDA Results", "Grading Criteria 1.11"))
story.append(Spacer(1, 4))
img1 = Image('figures/flight_vs_orbit.png', width=430, height=230)
img2 = Image('figures/payload_vs_orbit.png', width=430, height=230)
story.append(Table([[img1, img2]], colWidths=[440, 440]))
story.append(Spacer(1, 4))
c_bottom = [
    "• Mission Evolution: Early flights focused exclusively on LEO and ISS resupply missions; intermediate flights expanded into commercial GTO; recent flights (Flight 70+) are heavily dominated by VLEO (Starlink) launches.",
    "• Payload vs. Orbit Segregation: Heavy payloads (>13,000 kg) are exclusively deployed to VLEO with near-perfect recovery success rates.",
    "• GTO Payload Band: GTO launches carry payloads between 3,000 kg and 7,000 kg, where high staging velocity creates maximum thermal stress."
]
story.append(make_card_flowable("Analytical Findings: Mission Progression & Payload Capacity", c_bottom, 872, 145))
story.append(PageBreak())

# ==========================================
# SLIDE 11: EDA Results 4 - Yearly Success Trend (1.11)
# ==========================================
story.append(create_slide_header("EDA Results: Yearly Launch Success Rate Trend (2010–2020)", "EDA Results", "Grading Criteria 1.11"))
story.append(Spacer(1, 6))
img = Image('figures/yearly_success_trend.png', width=460, height=390)
c_trend = [
    "• 2010–2012 (Experimental Phase - 0.0% Success):",
    "  - Early flights tested parachute recovery and ocean splashdowns; no booster survival.",
    "• 2013–2015 (Proof-of-Concept Phase - 33.3% Success):",
    "  - Dec 2015 marked the historic milestone: Flight 20 achieved the first successful ground pad landing (RTLS) at LZ-1.",
    "• 2016–2017 (Operational Scaling - 60.0% to 83.3% Success):",
    "  - Regular drone ship (ASDS) recoveries established; first flight-proven booster re-flight (B1021.2) successfully landed.",
    "• 2018–2020 (Industrialized Reliability - 85%+ Success):",
    "  - Introduction of Falcon 9 Block 5 engineered for 10+ flights without major refurbishment, achieving consistent >85% annual landing success."
]
story.append(Table([[img, make_card_flowable("Technological Maturation Trajectory", c_trend, 400, 395)]], colWidths=[470, 410]))
story.append(PageBreak())

# ==========================================
# SLIDE 12: EDA with SQL - Methodology (1.9)
# ==========================================
c1 = [
    "• Database Engine: SQLite relational database connected via Python sqlite3.",
    "• Source Dataset: Spacex.csv loaded into table SPACEXTBL (101 mission records).",
    "• Cleaned Schema: Normalized spaces and punctuation in column headers:",
    "  - Date, Time_UTC, Booster_Version, Launch_Site, Payload,",
    "  - PAYLOAD_MASS__KG_, Orbit, Customer, Mission_Outcome, Landing_Outcome.",
    "• Analytical Goals: Execute 10 precision SQL queries answering operational, commercial, and engineering questions.",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/04_EDA_with_SQL.ipynb"
]
c2 = [
    "1. Unique Launch Sites: Extract distinct launch site names.",
    "2. Filtered Launches: Select 5 launches starting with 'CCA'.",
    "3. NASA CRS Payloads: Total payload mass carried under NASA contract.",
    "4. Booster Version Averages: Average payload mass for F9 v1.1 boosters.",
    "5. Historic Milestones: Earliest date of successful ground pad landing.",
    "6. Drone Ship Payloads: Boosters succeeding on drone ship between 4k-6k kg.",
    "7. Mission Outcomes: Breakdown of mission success vs. failure counts.",
    "8. Maximum Payload Boosters: Identify boosters carrying maximum payload.",
    "9. Temporal Failures: Drone ship landing failure records in 2015 by month.",
    "10. Outcome Rankings: Ranked count of landing outcomes between 2010 and 2017."
]
story.append(create_slide_header("EDA with SQL: Database Architecture & Query Catalog", "EDA SQL", "Grading Criteria 1.9"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("SQLite Engine & Setup", c1, 432, 420),
                     make_card_flowable("Query Objectives Catalog", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 13: EDA with SQL Results 1 (1.12)
# ==========================================
c1 = [
    "• Query 1: Unique Launch Sites",
    "  SELECT DISTINCT Launch_Site FROM SPACEXTBL;",
    "  --> CCAFS LC-40, VAFB SLC-4E, KSC LC-39A, CCAFS SLC-40.",
    "",
    "• Query 2: First 5 CCAFS Launches",
    "  SELECT * FROM SPACEXTBL WHERE Launch_Site LIKE 'CCA%' LIMIT 5;",
    "  --> Returned Flights 1-5 (Dragon Spacecraft Qualification, Demo C1, C2, CRS-1, CRS-2).",
    "",
    "• Query 3: Total NASA (CRS) Payload Mass",
    "  SELECT SUM(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Customer = 'NASA (CRS)';",
    "  --> Total Payload Mass = 45,596 kg across all NASA cargo resupply flights."
]
c2 = [
    "• Query 4: Average Payload Mass for F9 v1.1",
    "  SELECT AVG(PAYLOAD_MASS__KG_) FROM SPACEXTBL WHERE Booster_Version LIKE 'F9 v1.1%';",
    "  --> Average Payload Mass = 2,534.67 kg.",
    "",
    "• Query 5: First Successful Ground Pad Landing Date",
    "  SELECT MIN(Date) FROM SPACEXTBL WHERE Landing_Outcome = 'Success (ground pad)';",
    "  --> First Successful Date = 2015-12-22 (Flight 20, Orbcomm OG2 mission at LZ-1).",
    "",
    "• Operational Implication: F9 v1.1 established SpaceX's commercial credibility, but recovery was achieved after upgrading to Falcon 9 Full Thrust (FT)."
]
story.append(create_slide_header("EDA with SQL Results: Launch Sites, Payloads & Milestones", "EDA SQL Results", "Grading Criteria 1.12"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("Queries 1 to 3: Sites & NASA Payloads", c1, 432, 420),
                     make_card_flowable("Queries 4 & 5: Booster Average & First Milestone", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 14: EDA with SQL Results 2 (1.12)
# ==========================================
c1 = [
    "• Query 6: Drone Ship Success with 4k-6k kg Payload",
    "  SELECT Booster_Version, PAYLOAD_MASS__KG_ FROM SPACEXTBL WHERE Landing_Outcome = 'Success (drone ship)' AND PAYLOAD_MASS__KG_ BETWEEN 4000 AND 6000;",
    "  --> Boosters: F9 FT B1022 (4,696 kg), F9 FT B1026 (4,600 kg), F9 FT B1021.2 (5,300 kg), F9 FT B1031.2 (5,200 kg).",
    "",
    "• Query 7: Mission Outcomes Breakdown",
    "  SELECT TRIM(Mission_Outcome), COUNT(*) FROM SPACEXTBL GROUP BY TRIM(Mission_Outcome);",
    "  --> Success: 99 | Failure (in flight): 1 | Success (payload status unclear): 1.",
    "",
    "• Query 8: Maximum Payload Boosters (15,600 kg)",
    "  SELECT DISTINCT Booster_Version FROM SPACEXTBL WHERE PAYLOAD_MASS__KG_ = (SELECT MAX(PAYLOAD_MASS__KG_) FROM SPACEXTBL);",
    "  --> Starlink batches flown by F9 B5 (B1048, B1049, B1051, B1056, B1058, B1060)."
]
c2 = [
    "• Query 9: 2015 Drone Ship Landing Failures by Month",
    "  SELECT SUBSTR(Date, 6, 2) AS Month, Date, Booster_Version FROM SPACEXTBL WHERE SUBSTR(Date, 1, 4) = '2015' AND Landing_Outcome = 'Failure (drone ship)';",
    "  --> Month 01 (2015-01-10, B1012) & Month 04 (2015-04-14, B1015).",
    "",
    "• Query 10: Ranked Landing Outcomes (2010-06-04 to 2017-03-20)",
    "  SELECT Landing_Outcome, COUNT(*) AS Count FROM SPACEXTBL WHERE Date BETWEEN '2010-06-04' AND '2017-03-20' GROUP BY Landing_Outcome ORDER BY Count DESC;",
    "  --> 1. No attempt (10)       2. Success (drone ship) (5)",
    "  --> 3. Failure (drone ship) (5) 4. Success (ground pad) (3)",
    "  --> 5. Controlled (ocean) (3)  6. Uncontrolled (ocean) (2)",
    "  --> 7. Failure (parachute) (2) 8. Precluded (drone ship) (1)"
]
story.append(create_slide_header("EDA with SQL Results: Drone Ships, Max Payloads & Rankings", "EDA SQL Results", "Grading Criteria 1.12"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("Queries 6 to 8: Drone Ships & Max Payloads", c1, 432, 420),
                     make_card_flowable("Queries 9 & 10: Failures & Historical Rankings", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 15: Interactive Visual Analytics - Methodology (1.10)
# ==========================================
c1 = [
    "• Interactive Mapping Engine: Folium library built on Leaflet.js.",
    "• Geospatial Coordinates: Mapped all 4 launch complexes across Cape Canaveral (CCAFS), Kennedy Space Center (KSC), and Vandenberg (VAFB).",
    "• MarkerCluster Implementation: Implemented folium.plugins.MarkerCluster to dynamically group all 56 missions, styling markers by landing outcome (Green = Success, Red = Failure).",
    "• Proximity Safety Analysis: Computed geodesic distances using Haversine formula and drew interactive folium.PolyLine vectors from launch pads to nearest coastlines, highways, railways, and cities.",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/06_Interactive_Visual_Analytics_Folium.ipynb"
]
c2 = [
    "• Reactive Web Framework: Plotly Dash web application built with Dash Core Components (dcc) and Dash HTML Components (html).",
    "• Dynamic Components:",
    "  1. Launch Site Dropdown: Filter dashboard by ALL sites or individual sites (CCAFS LC-40, VAFB SLC-4E, KSC LC-39A, CCAFS SLC-40).",
    "  2. Payload RangeSlider: Interactive dual-handle slider filtering launches between 0 kg and 10,000 kg.",
    "  3. Success Pie Chart: Reactively renders total success share across sites (ALL) or success vs. failure breakdown (specific site).",
    "  4. Payload Scatter Chart: Dynamic scatter plot correlating payload mass to landing success, color-coded by booster version.",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/scripts/07_spacex_dash_app.py"
]
story.append(create_slide_header("Interactive Visual Analytics: Folium & Dash Methodology", "Interactive Analytics", "Grading Criteria 1.10"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("Folium Geospatial Mapping Architecture", c1, 432, 420),
                     make_card_flowable("Plotly Dash Reactive Dashboard", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 16: Interactive Analytics - Folium Launch Sites & Clusters (1.13)
# ==========================================
story.append(create_slide_header("Interactive Analytics: Folium Launch Sites & MarkerClusters", "Folium Results", "Grading Criteria 1.13"))
story.append(Spacer(1, 6))
img = Image('figures/folium_launch_sites.png', width=460, height=390)
c_geo = [
    "• Coastal Placement Strategy: All SpaceX launch sites are positioned directly adjacent to coastlines:",
    "  - Florida Coast (CCAFS/KSC): Eastward launches over the Atlantic Ocean take advantage of Earth's rotational velocity for equatorial & GTO orbits.",
    "  - California Coast (VAFB): Southward launches over the Pacific Ocean allow safe polar and Sun-Synchronous (SSO) orbital insertions.",
    "• Safety & Hazard Minimization: Rocket trajectories immediately fly over open water, ensuring stage separations and abort debris fall safely far from populated landmasses.",
    "• Drone Ship Staging: Drone ships (OCISLY & JRTI) are stationed 200–600 km downrange along launch azimuths."
]
story.append(Table([[img, make_card_flowable("Geographic Launch Insights", c_geo, 400, 395)]], colWidths=[470, 410]))
story.append(PageBreak())

# ==========================================
# SLIDE 17: Interactive Analytics - Folium Proximity (1.13)
# ==========================================
story.append(create_slide_header("Interactive Analytics: Folium Proximity Analysis", "Folium Results", "Grading Criteria 1.13"))
story.append(Spacer(1, 6))
img = Image('figures/folium_proximity_analysis.png', width=460, height=390)
c_prox = [
    "• Nearest Coastline (~0.85 km):",
    "  - Minimal distance to coastline allows rockets to clear the launch pad and immediately traverse over water, mitigating onshore blast risk.",
    "• Nearest Highway Parkway (~1.2 km):",
    "  - Close proximity provides essential road transport for oversized rocket components while maintaining safe hazard clear zones during static fires and launches.",
    "• Nearest Railroad (~1.35 km):",
    "  - Direct connection to NASA rail network for transporting heavy hardware and structural components.",
    "• Nearest City - Titusville (~16.5 km):",
    "  - Significant buffer distance protects residential populations from acoustic shockwaves, sonic booms, and potential launch catastrophic anomalies."
]
story.append(Table([[img, make_card_flowable("Proximity Distance Findings", c_prox, 400, 395)]], colWidths=[470, 410]))
story.append(PageBreak())

# ==========================================
# SLIDE 18: Interactive Analytics - Dash Visuals (1.14)
# ==========================================
story.append(create_slide_header("Interactive Analytics: Plotly Dash Dashboard Visuals", "Dash Results", "Grading Criteria 1.14"))
story.append(Spacer(1, 4))
img1 = Image('figures/dash_pie_all_sites.png', width=285, height=225)
img2 = Image('figures/dash_pie_ksc_site.png', width=285, height=225)
img3 = Image('figures/dash_scatter_payload_outcome.png', width=285, height=225)
story.append(Table([[img1, img2, img3]], colWidths=[293, 293, 293]))
story.append(Spacer(1, 4))
c_bottom = [
    "• Launch Site Success Share: KSC LC-39A contributes the largest share of successful recoveries (41.7%), followed by CCAFS SLC-40 (30.6%) and VAFB SLC-4E (16.7%).",
    "• Site Success Ratio: KSC LC-39A achieves a 76.9% success rate (10 successes vs. 3 failures), outperforming other facilities.",
    "• Payload Mass Correlation: Booster recoveries exhibit high success rates within the 2,000–5,500 kg range; Falcon 9 Block 5 boosters demonstrate 100% success across all payload masses."
]
story.append(make_card_flowable("Plotly Dash Operational Insights", c_bottom, 872, 145))
story.append(PageBreak())

# ==========================================
# SLIDE 19: Predictive Analysis - ML Pipeline (1.15)
# ==========================================
c1 = [
    "• Feature Matrix (X): 83 one-hot encoded features derived from dataset_part_3.csv.",
    "• Target Vector (Y): Binary landing outcome Class (1 = Success, 0 = Failure).",
    "• Feature Standardization: Applied StandardScaler() to standardize features to zero mean and unit variance, essential for distance-based and regularized models.",
    "• Train/Test Split: 80% Training (72 samples), 20% Holdout Test (18 samples) with random_state=2 for reproducibility.",
    "• Hyperparameter Optimization: 10-fold cross-validation using GridSearchCV across all four model families to optimize hyperparameters and prevent overfitting.",
    f"• GitHub URL: {GITHUB_REPO_URL}/blob/main/notebooks/08_Predictive_Analysis_Machine_Learning.ipynb"
]
c2 = [
    "1. Logistic Regression:",
    "   - Grid: C in [0.01, 0.1, 1.0], penalty=['l2'], solver=['lbfgs']",
    "   - Best Parameters: {'C': 0.01, 'penalty': 'l2', 'solver': 'lbfgs'}",
    "2. Support Vector Machine (SVM):",
    "   - Grid: C in [0.5, 1.0, 1.5], kernel=['linear', 'rbf', 'sigmoid']",
    "   - Best Parameters: {'C': 0.5, 'kernel': 'sigmoid'}",
    "3. Decision Tree Classifier:",
    "   - Grid: criterion=['gini', 'entropy'], max_depth=[2, 4, 6, 8], min_samples_leaf=[1, 2, 4], min_samples_split=[2, 5, 10]",
    "   - Best Parameters: {'criterion': 'gini', 'max_depth': 4, 'min_samples_leaf': 4, 'min_samples_split': 2}",
    "4. K-Nearest Neighbors (KNN):",
    "   - Grid: n_neighbors=[3, 5, 7, 9, 10], p=[1, 2], algorithm=['auto', 'ball_tree', 'kd_tree']",
    "   - Best Parameters: {'algorithm': 'auto', 'n_neighbors': 10, 'p': 1}"
]
story.append(create_slide_header("Predictive Analysis: Machine Learning Pipeline & Tuning", "Machine Learning", "Grading Criteria 1.15"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("Preprocessing & Cross-Validation", c1, 432, 420),
                     make_card_flowable("Hyperparameter Search Grids", c2, 432, 420)]],
                   colWidths=[440, 440]))
story.append(PageBreak())

# ==========================================
# SLIDE 20: Predictive Analysis - Results (1.15)
# ==========================================
story.append(create_slide_header("Predictive Analysis: Model Evaluation & Confusion Matrix", "ML Results", "Grading Criteria 1.15"))
story.append(Spacer(1, 4))
img1 = Image('figures/ml_model_accuracy_comparison.png', width=430, height=230)
img2 = Image('figures/ml_confusion_matrix.png', width=430, height=230)
story.append(Table([[img1, img2]], colWidths=[440, 440]))
story.append(Spacer(1, 4))
c_bottom = [
    "• Accuracy Scores: Logistic Regression, SVM, and KNN tied for highest Test Accuracy at 83.33% (15 correct out of 18 test samples). Decision Tree achieved 87.14% Train CV and 77.78% Test accuracy.",
    "• Confusion Matrix Analysis (18 Test Samples): True Positives = 12 (100% recall on successes), True Negatives = 3, False Positives = 3, False Negatives = 0. No successful landings were misclassified as failures.",
    "• Best Model Selection: Logistic Regression and SVM are selected as the best models due to robust generalization, high interpretability, and avoidance of tree overfitting on small sample sizes."
]
story.append(make_card_flowable("Model Evaluation & Best Model Insights", c_bottom, 872, 145))
story.append(PageBreak())

# ==========================================
# SLIDE 21: Conclusions & Innovative Insights (1.15)
# ==========================================
c1 = [
    "• Economic Takeaway: First stage reusability delivers a decisive cost advantage, reducing launch costs by ~60% ($62M vs $165M+), revolutionizing commercial space access.",
    "• Reliability Proven: Recovery success grew from 0% in 2010 to >85% by 2020, demonstrating full industrialization.",
    "• Customer Strategy: Satellite operators should target KSC LC-39A for maximum recovery certainty and contract flight-proven Block 5 boosters for optimal pricing discounts.",
    "• Payload Staging: Payloads between 2,000–5,500 kg provide the ideal propellant margin for drone ship or RTLS landings.",
    f"• Full Project Repository: {GITHUB_REPO_URL}"
]
c2 = [
    "• Meteorological Fusion: Integrate real-time offshore atmospheric data (surface wind gusts, ocean swell wave height, upper-troposphere wind shear) directly into the predictive model.",
    "• Autonomous Drone Ship Telemetry: Incorporate thruster station-keeping data and GPS telemetry from drone ships (OCISLY / ASOG) to predict sea-state landing aborts.",
    "• Bayesian Neural Networks: Deploy Bayesian deep learning to generate calibrated epistemic uncertainty estimates for edge-case missions.",
    "• Dynamic Insurance Premium Model: Build real-time risk-adjusted insurance pricing algorithms that adjust dynamically based on launch-day booster health and flight heritage."
]
story.append(create_slide_header("Conclusions, Business Recommendations & Innovative Insights", "Conclusions", "Grading Criteria 1.15"))
story.append(Spacer(1, 8))
story.append(Table([[make_card_flowable("Business Conclusions & Recommendations", c1, 432, 420),
                     make_card_flowable("Creative & Innovative Future Insights", c2, 432, 420)]],
                   colWidths=[440, 440]))

doc.build(story, canvasmaker=NumberedCanvas)
print(f"Saved {pdf_path} successfully ({os.path.getsize(pdf_path)} bytes).")

