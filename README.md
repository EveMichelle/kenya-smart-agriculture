<div align="center">

<img src="figures/02_ipc_kenya_choropleth.png" width="120" alt="Kenya Smart Agriculture Logo"/>

# Kenya Smart Agriculture & Market Intelligence Platform

**Using NASA satellite weather data to predict food security risk, forecast food prices, and recommend crops to farmers across all 47 counties in Kenya**

[![Streamlit App](https://img.shields.io/badge/Live_App-kenya--smart--agriculture.streamlit.app-brightgreen?style=for-the-badge&logo=streamlit)](https://kenya-smart-agriculture.streamlit.app)
[![Tableau](https://img.shields.io/badge/Tableau-Dashboard-blue?style=for-the-badge&logo=tableau)](https://public.tableau.com/app/profile/eve.michelle/viz/KenyaSmartAgricultureMarketIntelligenceDashboard/Dashboard1)
[![GitHub](https://img.shields.io/badge/GitHub-EveMichelle-black?style=for-the-badge&logo=github)](https://github.com/EveMichelle/kenya-smart-agriculture)
[![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-eve--michelle-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/eve-michelle)

**Built by [Eve Otieno](https://github.com/EveMichelle) — Data Scientist, Nairobi, Kenya 🇰🇪**

</div>

---

## Overview

An end-to-end machine learning platform that identifies food security risk, forecasts food prices, recommends crops to farmers, and analyses agricultural news sentiment across all 47 counties in Kenya — using NASA satellite weather data as the primary signal.

Kenya's food security problem is not caused by a lack of data. NASA has recorded daily weather for every county since 2000. FEWS NET has classified food security phases since 2009. KNBS has collected market prices monthly. WFP monitors prices across 226 markets. **None of this data had ever been merged and used predictively at scale. This project does exactly that.**

---

## Skills Demonstrated

| Area | Tools & Methods |
|---|---|
| Data Engineering | NASA API, PDF extraction, web scraping, multi-source merging |
| Machine Learning | XGBoost, cross-validation, SHAP explainability |
| Time Series Forecasting | Facebook Prophet, ARIMA, holdout evaluation |
| Natural Language Processing | VADER sentiment scoring, TF-IDF, K-Means topic modelling |
| Geospatial Analytics | Choropleth mapping, county-level risk profiling across 47 counties |
| Dashboard Development | Streamlit (deployed), Tableau Public |
| Model Explainability | SHAP feature importance, business-level finding translation |
| Software Engineering | Modular src/ library, reusable scripts, annual update pipeline |

---

## Results Snapshot

| Module | Model | Metric | Result |
|---|---|---|---|
| 🗺️ Food Security Classification | XGBoost | Weighted F1 | **0.738** ✅ |
| 📈 Price Forecasting | Facebook Prophet | MAPE | **0.81%** ✅ |
| 🌱 Crop & Market Recommendation | NASA + WFP | Coverage | **10 crops × 226 markets** ✅ |
| 📰 NLP Sentiment Analysis | VADER + TF-IDF | Sentiment distribution | **47.3% positive** ✅ |

409,811 NASA weather records · 47 counties · 5 data sources · 8 notebooks · 1 deployed app

---

## Key Findings

| # | Finding | Recommendation |
|---|---|---|
| 1 | **12 counties in IPC Phase 3 Crisis** (March 2026) — Turkana, Garissa, Wajir, Mandera, Marsabit and 7 others | Prioritise these counties for immediate intervention |
| 2 | **NASA SPI-3 is the strongest predictor** of food insecurity | Deploy automated monthly drought alerts when SPI-3 drops below -1.0 |
| 3 | **2–3 month lag** between rainfall deficit and price spikes | Pre-position WFP food stocks when SPI-3 drops below -0.5 |
| 4 | **Kenya CPI rose 35%** since 2020 (107 → 144) | Forecast to reach 148 by January 2026 — continued price pressure expected |
| 5 | **Negative news sentiment spikes precede IPC assessments** | Integrate news monitoring as an early warning signal for field verification |

---

## App Screenshots

### 🏠 Home — Overview & Food Security Map
> *47 counties coloured by IPC phase. 12 counties in Phase 3 Crisis as of March 2026.*

![Home Page](figures/Screenshot%202026-06-03%20165606.png)

---

### 🌱 Crop & Market Recommendation
> *Select any county and season — get personalised crop recommendations backed by NASA weather data and live WFP market prices.*

![Crop Recommendation](figures/Screenshot%202026-06-03%20165239.png)

---

### 📰 Agricultural News Sentiment
> *300 Kenya News Agency headlines scored with VADER. 47% positive. Government Programmes most positive (0.42). Dairy & Macadamia most negative.*

![News Sentiment](figures/Screenshot%202026-06-03%20165507.png)

---

### 📈 Kenya Food Price Forecast
> *Facebook Prophet 8-month CPI forecast. MAPE = 0.81% on the 12-month evaluation period.*

![Price Forecast](figures/Screenshot%202026-06-03%20165020.png)

---

## Architecture

```
Data Sources
─────────────────────────────────────────
NASA POWER (409,811 rows)   FEWS NET IPC
KNBS CPI (37 PDFs)          WFP Markets
Kenya News Agency (300 articles)
                │
                ▼
    Data Cleaning & Feature Engineering
    (notebooks 01–03, src/ modules)
                │
                ▼
┌──────────────────────────────────────┐
│  Food Security Classification        │  XGBoost · Weighted F1 = 0.738
│  Food Price Forecasting              │  Prophet · MAPE = 0.81%
│  Crop & Market Recommendation        │  NASA + WFP · 47 counties
│  NLP Sentiment Analysis              │  VADER + TF-IDF · 300 articles
└──────────────────────────────────────┘
                │
                ▼
    Streamlit App (deployed)  +  Tableau Dashboard
```

---

## The Problem

| Problem | Impact |
|---|---|
| Food security phases assessed manually and quarterly | Emergency response arrives after the crisis has peaked |
| Rainfall deficits drive price spikes 2–3 months later | Farmers and traders get blindsided by price shocks |
| Hundreds of agricultural news articles published weekly, never synthesised | Policy makers miss early warning signals |

---

## Data Sources

All 5 datasets are raw and non-curated.

| Dataset | Source | Records | Period |
|---|---|---|---|
| NASA POWER Weather | [power.larc.nasa.gov](https://power.larc.nasa.gov) | 409,811 rows | 2000–2023 |
| FEWS NET IPC | [fews.net](https://fews.net) | 640 rows | Mar 2026 |
| KNBS CPI Reports | [knbs.or.ke](https://knbs.or.ke) | 37 PDFs → 64 records | 2020–2025 |
| WFP Food Prices | [WFP VAM](https://data.humdata.org/dataset/wfp-food-prices-for-kenya) | 19,005 rows, 226 markets | 2006–2026 |
| Kenya Agri News | [kenyanews.go.ke](https://kenyanews.go.ke) | 300 articles | 2025–2026 |

---

## Project Structure

```
kenya-smart-agriculture/
├── app/
│   ├── streamlit_app.py            # 5-page deployed web application
│   ├── trigger_alerts.py           # Drought + food crisis alert system
│   └── trigger_predictions.py      # Generate fresh county predictions
├── data/
│   ├── raw/                        # All 5 raw datasets
│   └── processed/                  # 9 cleaned and merged files
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_food_security_classification.ipynb
│   ├── 05_price_forecasting.ipynb
│   ├── 06_recommendation.ipynb
│   ├── 07_nlp_sentiment.ipynb
│   └── 08_results.ipynb
├── scripts/
│   ├── fetch_nasa.py
│   ├── scrape_news.py
│   ├── train_food_security.py
│   ├── train_price_forecast.py
│   └── train_recommendation.py
├── src/                            # 14 reusable Python modules
├── figures/                        # 24 saved visualisations
├── models/saved/                   # Trained XGBoost .pkl files
├── tableau/                        # 5 Tableau dashboard CSV files
├── constants.py
├── main.py
└── requirements.txt
```

---

## Quick Start

```bash
git clone https://github.com/EveMichelle/kenya-smart-agriculture.git
cd kenya-smart-agriculture
conda create -n kenya-agri python=3.9
conda activate kenya-agri
pip install -r requirements.txt
python main.py
python -m streamlit run app/streamlit_app.py
```

---

## Stakeholders

| Stakeholder | How They Use This |
|---|---|
| County Agricultural Officers | Monthly drought risk scores + IPC predictions per county |
| WFP Kenya and NGOs | Pre-position food stocks 2–3 months before price spikes |
| Smallholder Farmers | Which crops to plant and which markets offer the best prices |
| Kenya Ministry of Agriculture | National food security trend monitoring |
| KALRO | Weather-yield correlations for crop advisory updates |

---

## Future Improvements

- Incorporate satellite vegetation indices (NDVI) alongside weather data
- Add county-level crop yield prediction
- Integrate seasonal weather forecasts for forward-looking recommendations
- Build SMS-based crop recommendations for farmers without internet access
- Deploy automated monthly model retraining pipeline as new data arrives

---

## Acknowledgments

- [NASA Langley Research Center](https://power.larc.nasa.gov) — POWER API (public domain)
- [Famine Early Warning Systems Network (FEWS NET)](https://fews.net)
- [Kenya National Bureau of Statistics (KNBS)](https://knbs.or.ke)
- [World Food Programme (WFP)](https://data.humdata.org/dataset/wfp-food-prices-for-kenya)
- [Kenya News Agency](https://kenyanews.go.ke)

---

MIT License © 2026 Eve Otieno

⭐ Star this repo &nbsp;|&nbsp; 🐛 Report an issue &nbsp;|&nbsp; 🔗 [Live App](https://kenya-smart-agriculture.streamlit.app)