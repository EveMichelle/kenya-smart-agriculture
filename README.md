![Kenya Smart Agriculture](figures/logo.png)

## Team Members

**Eve Otieno**

# Kenya Smart Agriculture & Market Intelligence Platform

**County Risk Mapping · Food Price Forecasting · Food Security Classification · NLP News Intelligence**

**Using Machine Learning to Predict Where Kenya is Losing the Food Security Battle**

---

## Project Overview

An end-to-end machine learning platform that identifies food security risk across Kenya's 47 counties, forecasts food price changes, and analyses agricultural news sentiment — giving county governments, NGOs, and farmers precision intelligence to act before crises deepen.

---

## Business Understanding

**Problem:** Kenya's food security response is reactive. By the time a county is officially declared in food crisis, the situation has already been deteriorating for months. Three valuable datasets exist in isolation: NASA records daily weather for every county since 2000, FEWS NET manually classifies food security phases quarterly, and KNBS collects market prices monthly — but none of these are connected or used predictively.

**Solution:** Three integrated models that give county governments and NGOs actionable intelligence before crises peak:

| Model | Question It Answers | Output |
|---|---|---|
| **Model 1 — Food Security Classifier** | Which counties are heading into food crisis right now? | IPC phase prediction per county (Minimal / Stressed / Crisis) |
| **Model 2 — Price Forecasting** | How will food prices change in the next 2 months? | 8-week CPI forecast with confidence intervals |
| **Model 3 — County Recommendation** | Which counties need the same intervention strategy? | Ranked similar counties by weather-IPC profile |
| **Model 4 — NLP Sentiment** | What are farmers reading and worrying about? | News sentiment scores + topic clusters per county |

---

## Stakeholders

| Stakeholder | How They Use This |
|---|---|
| **County Agricultural Officers** | Monthly drought risk scores + IPC phase predictions per county |
| **WFP Kenya & NGOs** | Pre-position food stocks 2–3 months before price spikes |
| **Smallholder Farmers & Cooperatives** | Which markets offer best prices + which crops to plant |
| **Kenya Ministry of Agriculture** | National food security trend monitoring + policy response |
| **KALRO** | Weather-yield correlations for crop advisory updates |

---

## Data Sources

### Dataset 1 — NASA POWER Weather API

Source: [power.larc.nasa.gov](https://power.larc.nasa.gov/api/temporal/daily/point)

**Fetch using:** `python scripts/fetch_nasa.py` (auto-fetches all 47 counties)

| File | Contents |
|---|---|
| `kenya_weather_all_counties.csv` | Daily weather for 47 counties, 2000–2023 |

| Parameter | Description |
|---|---|
| `T2M` | Daily avg temperature at 2m (°C) |
| `PRECTOTCORR` | Corrected precipitation (mm/day) |
| `RH2M` | Relative humidity at 2m (%) |
| `ALLSKY_SFC_SW_DWN` | Solar radiation (MJ/m²/day) |
| `WS2M` | Wind speed at 2m (m/s) |

### Dataset 2 — FEWS NET IPC Food Security

Source: [fews.net/data/acute-food-insecurity](https://fews.net/data/acute-food-insecurity) → Download All Data → Filter Kenya

| File | Contents |
|---|---|
| `kenya_ipc.csv` | IPC phase (1/2/3) for all 47 counties at sub-county level |

### Dataset 3 — KNBS Consumer Price Index Reports

Source: [knbs.or.ke/cpi-and-inflation-rates](https://www.knbs.or.ke/cpi-and-inflation-rates/) → download monthly PDFs

| File | Contents |
|---|---|
| `knbs_cpi_raw_text.csv` | Raw text extracted from 37 monthly KNBS PDF reports (2021–2025) |

### Dataset 4 — Kenya Agricultural News (Scraped)

Source: [kenyanews.go.ke/category/agri](https://www.kenyanews.go.ke/category/agri/)

**Scrape using:** `python scripts/scrape_news.py`

| File | Contents |
|---|---|
| `kenya_agri_news_raw.csv` | 300 agricultural news headlines (2025–2026) |

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
│   │   ├── weather/                # NASA POWER CSVs (47 counties)
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
│   └── final_notebook.ipynb        # Complete project walkthrough
│
├── scripts/                        # Production pipeline runners
│   ├── fetch_nasa.py               # Fetch NASA data (run once)
│   ├── scrape_news.py              # Scrape news articles (run once)
│   ├── extract_data.py             # Step 1: Load & validate
│   ├── prepare_data.py             # Step 2: Clean & engineer features
│   ├── merge_data.py               # Step 3: Merge master dataset
│   ├── train_model1.py             # Step 4: IPC classifier
│   ├── train_model2.py             # Step 5: CPI forecaster
│   └── train_model3.py             # Step 6: Recommendation system
│
├── src/                            # Reusable Python modules
│   ├── __init__.py
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
├── figures/                        # Saved visualisation outputs
├── models/saved/                   # Serialised model artefacts (.pkl)
├── presentation/                   # Non-technical slides
├── tableau/                        # Tableau dashboard files + CSVs
│
├── constants.py                    # Shared paths, labels, county list
├── main.py                         # Run full pipeline: python main.py
├── requirements.txt
├── PROJECT_PLAN.md
├── .gitignore
└── README.md
```

---

## Quick Start

### Prerequisites
- Python 3.8+
- conda or virtualenv

### Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/kenya-smart-agriculture.git
cd kenya-smart-agriculture

# Create and activate environment
conda create -n kenya-agri python=3.10
conda activate kenya-agri

# Install dependencies
pip install -r requirements.txt
```

### Add Your Data

Place your 4 raw datasets in the correct folders:
```
data/raw/weather/kenya_weather_all_counties.csv
data/raw/food_security/kenya_ipc.csv
data/raw/prices/knbs_cpi_raw_text.csv
data/raw/news/kenya_agri_news_raw.csv
```

### Run the Full Pipeline

```bash
python main.py
```

### Run Notebooks Manually (CRISP-DM order)

```bash
jupyter lab
# Open: notebooks/final_notebook.ipynb
# Or run sequentially: 01 → 02 → 03 → 04 → 05 → 06 → 07
```

### Launch the App

```bash
streamlit run app/streamlit_app.py
```

### Run Alerts

```bash
python app/trigger_alerts.py
```

---

## Models

### Model 1 — Food Security Classification

- **Algorithm:** Logistic Regression (baseline) → XGBoost (primary)
- **Data:** NASA POWER weather features + FEWS NET IPC labels
- **Target:** IPC Phase per county (1=Minimal, 2=Stressed, 3=Crisis)
- **Key feature:** SPI-3 (Standardised Precipitation Index — 3-month drought signal)
- **Output:** County-level food security phase prediction

### Model 2 — Food Price Forecasting

- **Algorithm:** ARIMA(1,1,1) (baseline) → Facebook Prophet (primary)
- **Data:** KNBS CPI monthly food price index extracted from raw PDFs
- **Target:** Monthly overall CPI and commodity prices
- **Output:** 8-week price forecast with confidence intervals

### Model 3 — County Recommendation

- **Algorithm:** MinMaxScaler + Cosine Similarity (content-based filtering)
- **Data:** NASA weather profiles + IPC phases per county
- **Output:** Top similar counties ranked by weather-food security composite score

### Model 4 — NLP Sentiment & Topics (Stretch Goal)

- **Algorithm:** VADER (baseline) → DistilBERT (primary) → BERTopic (topics)
- **Data:** 300 scraped Kenya News Agency agricultural headlines
- **Output:** Sentiment score per article + topic clusters

---

## Key Metrics

| Metric | Definition | Used In |
|---|---|---|
| **SPI-3** | (rainfall - 3-month mean) / std — drought severity index | Model 1 primary feature |
| **IPC Phase** | Food security classification 1–3 (FEWS NET standard) | Model 1 target |
| **MAPE** | Mean Absolute Percentage Error | Model 2 evaluation |
| **Weighted F1** | F1 score weighted by class frequency (handles imbalance) | Model 1 evaluation |
| **Precision@3** | How often top 3 recommended counties are relevant | Model 3 evaluation |
| **VADER Compound** | Sentiment score -1 (negative) to +1 (positive) | Model 4 baseline |

---

## Model Evaluation

| Model | Metric | Baseline | Primary Model | Target |
|---|---|---|---|---|
| Food Security Classification | Weighted F1 | — | — | > 0.70 |
| Price Forecasting | MAPE | — | — | < 15% |
| County Recommendation | Precision@3 | — | — | > 0.60 |
| Sentiment NLP | Macro F1 | — | — | > 0.70 |

*Results updated as models are trained.*

---

## Recommendations

| Finding | Recommendation |
|---|---|
| SPI-3 < -1.0 predicts IPC Phase 3 in northern counties | Deploy automated monthly drought alerts to county agricultural officers |
| 2–3 month lag between rainfall deficit and price spikes | Trigger food stock pre-positioning when SPI-3 drops below -0.5 |
| 49% of counties in Phase 3 (March 2026 snapshot) | Prioritise Turkana, Garissa, Wajir, Mandera, Marsabit for immediate intervention |
| Negative news sentiment spikes precede IPC assessments | Use news sentiment as early warning signal for field verification |

---

## Live Dashboard

**[Streamlit App](https://kenya-smart-agriculture.streamlit.app)** *(update after deployment)*
**[Tableau Dashboard](https://public.tableau.com)** *(update after publishing)*

---

## Acknowledgments

- NASA Langley Research Center for the POWER API (public domain)
- Famine Early Warning Systems Network (FEWS NET) for IPC data
- Kenya National Bureau of Statistics (KNBS) for monthly CPI reports
- Kenya News Agency for publicly accessible agricultural news

---

## License

This project is licensed under the **MIT License**.

*Data Science Capstone — Phase 5 | Flatiron School | May 2026*
