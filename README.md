# Kenya Smart Agriculture & Market Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat-square&logo=jupyter)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

**Built by [Eve Otieno](https://github.com/EveMichelle)**

---

## Overview

An end-to-end machine learning platform that identifies food security risk across Kenya's 47 counties, forecasts food price changes, and analyses agricultural news sentiment — giving county governments, NGOs, and farmers intelligence to act before crises deepen.

Kenya has a food security problem that is not caused by lack of data. NASA has recorded daily weather for every county since 2000. FEWS NET has classified food security phases since 2009. KNBS has collected market prices every month. None of this data has ever been merged and used predictively. This project does exactly that.

**[Live App →](https://kenya-smart-agriculture.streamlit.app)** *(update after deployment)*  
**[Tableau Dashboard →](https://public.tableau.com)** *(update after publishing)*

---

## The Problem

| Problem | Impact |
|---|---|
| Food security phases are assessed manually and quarterly — too slow | Emergency response arrives after the crisis has peaked |
| Rainfall deficits drive food price spikes 2–3 months later, but no one connects the data | Farmers and traders get blindsided by price shocks |
| Hundreds of agricultural news articles published weekly, never synthesised | Policy makers miss early warning signals |

---

## Solution — Three Integrated ML Models

| Model | Question It Answers | Output |
|---|---|---|
| **Food Security Classifier** | Which counties are heading into food crisis? | IPC phase prediction per county |
| **Price Forecasting** | How will food prices change in the next 8 weeks? | CPI forecast with confidence intervals |
| **County Recommendation** | Which counties need the same intervention? | Ranked similar counties by weather + IPC profile |
| **NLP Sentiment** | What are farmers reading and worrying about? | Sentiment scores + topic clusters |

---

## Stakeholders

| Stakeholder | How They Use This |
|---|---|
| County Agricultural Officers | Monthly drought risk scores + IPC predictions per county |
| WFP Kenya & NGOs | Pre-position food stocks 2–3 months before price spikes |
| Smallholder Farmers | Which markets offer best prices |
| Kenya Ministry of Agriculture | National food security trend monitoring |
| KALRO | Weather-yield correlations for crop advisory updates |

---

## Data Sources

All datasets are raw and non-curated.

### NASA POWER Weather API
**Source:** [power.larc.nasa.gov](https://power.larc.nasa.gov/api/temporal/daily/point)  
**Fetch:** `python scripts/fetch_nasa.py`

| File | Contents |
|---|---|
| `kenya_weather_all_counties.csv` | Daily weather for 47 counties, 2000–2023 (409,811 rows) |

| Parameter | Description |
|---|---|
| `T2M` | Daily avg temperature at 2m (°C) |
| `PRECTOTCORR` | Corrected precipitation (mm/day) |
| `RH2M` | Relative humidity at 2m (%) |
| `ALLSKY_SFC_SW_DWN` | Solar radiation (MJ/m²/day) |
| `WS2M` | Wind speed at 2m (m/s) |

### FEWS NET IPC Food Security Classifications
**Source:** [fews.net/data/acute-food-insecurity](https://fews.net/data/acute-food-insecurity) → Download All Data → Filter Kenya

| File | Contents |
|---|---|
| `kenya_ipc.csv` | IPC phase (1–3) for all 47 counties at sub-county level (640 rows) |

### KNBS Consumer Price Index Reports
**Source:** [knbs.or.ke/cpi-and-inflation-rates](https://www.knbs.or.ke/cpi-and-inflation-rates/)

| File | Contents |
|---|---|
| `knbs_cpi_raw_text.csv` | Raw text extracted from 37 monthly PDF reports, 2020–2025 |

### Kenya Agricultural News
**Source:** [kenyanews.go.ke/category/agri](https://www.kenyanews.go.ke/category/agri/)  
**Scrape:** `python scripts/scrape_news.py`

| File | Contents |
|---|---|
| `kenya_agri_news_raw.csv` | 300 agricultural news headlines, 2025–2026 |

---

## Project Structure

```
kenya-smart-agriculture/
│
├── app/
│   ├── streamlit_app.py            # 5-page deployed web application
│   ├── trigger_alerts.py           # Drought + food crisis alert system
│   └── trigger_predictions.py      # Generate fresh county predictions
│
├── data/
│   ├── raw/
│   │   ├── weather/                # NASA POWER CSVs
│   │   ├── food_security/          # FEWS NET IPC CSV
│   │   ├── prices/                 # KNBS CPI raw text CSV
│   │   └── news/                   # Scraped news articles CSV
│   └── processed/                  # Cleaned and merged datasets
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_food_security_classification.ipynb
│   ├── 05_price_forecasting.ipynb
│   ├── 06_recommendation.ipynb
│   ├── 07_nlp_sentiment.ipynb
│   └── final_notebook.ipynb
│
├── scripts/
│   ├── fetch_nasa.py
│   ├── scrape_news.py
│   ├── extract_data.py
│   ├── prepare_data.py
│   ├── merge_data.py
│   ├── train_model1.py
│   ├── train_model2.py
│   └── train_model3.py
│
├── src/
│   ├── load_data.py
│   ├── clean_nasa.py
│   ├── clean_ipc.py
│   ├── clean_knbs.py
│   ├── clean_news.py
│   ├── features.py
│   ├── visualize.py
│   ├── train_classifier.py
│   ├── train_forecaster.py
│   ├── evaluate.py
│   ├── recommend.py
│   └── pipeline.py
│
├── figures/
├── models/saved/
├── presentation/
├── tableau/
│
├── constants.py
├── main.py
├── requirements.txt
├── PROJECT_PLAN.md
└── README.md
```

---

## Quick Start

```bash
# Clone
git clone https://github.com/EveMichelle/kenya-smart-agriculture.git
cd kenya-smart-agriculture

# Set up environment
conda create -n kenya-agri python=3.10
conda activate kenya-agri
pip install -r requirements.txt

# Add raw data to data/raw/ subfolders, then:
python main.py           # Run full pipeline
streamlit run app/streamlit_app.py   # Launch app
```

---

## Models

### Model 1 — Food Security Classification
- **Algorithm:** Logistic Regression (baseline) → XGBoost
- **Features:** NASA weather (SPI-3, rainfall, temperature, dry days)
- **Target:** IPC Phase per county (1=Minimal, 2=Stressed, 3=Crisis)

### Model 2 — Food Price Forecasting
- **Algorithm:** ARIMA (baseline) → Facebook Prophet
- **Features:** KNBS monthly CPI + lagged NASA rainfall
- **Target:** Monthly food CPI index

### Model 3 — County Recommendation
- **Algorithm:** Cosine similarity on weather + IPC feature vectors
- **Output:** Similar counties ranked by food security composite score

### Model 4 — NLP Sentiment *(stretch goal)*
- **Algorithm:** VADER (baseline) → DistilBERT → BERTopic
- **Data:** 300 Kenya News Agency agricultural headlines

---

## Evaluation Targets

| Model | Metric | Target |
|---|---|---|
| Food Security Classification | Weighted F1 | > 0.70 |
| Price Forecasting | MAPE | < 15% |
| County Recommendation | Precision@3 | > 0.60 |
| Sentiment NLP | Macro F1 | > 0.70 vs VADER baseline |

---

## Key Findings

*Updated as models are trained.*

---

## Recommendations

| Finding | Recommendation |
|---|---|
| SPI-3 < -1.0 predicts IPC Phase 3 in northern counties | Automate monthly drought alerts to county agricultural officers |
| 2–3 month lag between rainfall deficit and price spikes | Trigger food stock pre-positioning when SPI-3 drops below -0.5 |
| 49% of counties in Phase 3 (March 2026) | Prioritise Turkana, Garissa, Wajir, Mandera, Marsabit for intervention |

---

## Acknowledgments

- NASA Langley Research Center — POWER API (public domain)
- Famine Early Warning Systems Network (FEWS NET)
- Kenya National Bureau of Statistics (KNBS)
- Kenya News Agency

---

## License

MIT License — see [LICENSE](LICENSE) for details.