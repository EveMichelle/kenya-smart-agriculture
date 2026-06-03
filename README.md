# Kenya Smart Agriculture & Market Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange?style=flat-square&logo=jupyter)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red?style=flat-square&logo=streamlit)
![Tableau](https://img.shields.io/badge/Tableau-Public-blue?style=flat-square&logo=tableau)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**Built by [Eve Otieno](https://github.com/EveMichelle)**

---

## 🌐 Live Deployments

| Platform | Link |
|---|---|
| 🚀 **Streamlit App** | [kenya-smart-agriculture.streamlit.app](https://kenya-smart-agriculture.streamlit.app) |
| 📊 **Tableau Dashboard** | [public.tableau.com — Kenya Smart Agriculture](https://public.tableau.com/app/profile/eve.michelle/viz/KenyaSmartAgricultureMarketIntelligenceDashboard/Dashboard1) |

---

## Overview

An end-to-end machine learning platform that identifies food security risk across Kenya's 47 counties, forecasts food price changes, recommends crops to farmers, and analyses agricultural news sentiment — giving county governments, NGOs, and farmers intelligence to act before crises deepen.

Kenya has a food security problem that is not caused by lack of data. NASA (National Aeronautics and Space Administration) has recorded daily weather for every county since 2000. FEWS NET (Famine Early Warning Systems Network) has classified food security phases since 2009. KNBS (Kenya National Bureau of Statistics) has collected market prices every month. WFP (World Food Programme) monitors prices across 226 markets. None of this data has ever been merged and used predictively at scale. This project does exactly that.

---

## The Problem

| Problem | Impact |
|---|---|
| Food security phases are assessed manually and quarterly — too slow | Emergency response arrives after the crisis has peaked |
| Rainfall deficits drive food price spikes 2–3 months later, but no one connects the data | Farmers and traders get blindsided by price shocks |
| Hundreds of agricultural news articles published weekly, never synthesised | Policy makers miss early warning signals |

---

## Solution — Four Integrated ML Modules

| Module | Question It Answers | Model | Result |
|---|---|---|---|
| **Food Security Classifier** | Which counties are heading into food crisis? | XGBoost | F1 = 0.738 ✅ |
| **Price Forecasting** | How will food prices change in the next 8 months? | Prophet | MAPE = 0.81% ✅ |
| **Crop & Market Recommendation** | What should I plant and where should I sell? | NASA + WFP | 10 crops × 226 markets ✅ |
| **NLP Sentiment** | What are farmers reading and worrying about? | VADER | 47.3% positive ✅ |

---

## Key Findings

| Finding | Recommendation |
|---|---|
| 12 counties in IPC Phase 3 Crisis (March 2026) — all northern arid zones | Prioritise Turkana, Garissa, Wajir, Mandera, Marsabit for immediate intervention |
| NASA SPI-3 (Standardised Precipitation Index) is the #1 predictor of food insecurity | Deploy automated monthly drought alerts when SPI-3 drops below -1.0 |
| 2–3 month lag between rainfall deficit and price spikes | Pre-position food stocks when SPI-3 drops below -0.5 |
| Kenya CPI rose 35% from 2020 to 2025 (107 → 144) | Prophet forecasts CPI reaching 148 by January 2026 |
| Negative news sentiment spikes precede IPC assessments | Use news sentiment as early warning signal for field verification |

---

## Data Sources

All datasets are raw and non-curated.

| Dataset | Source | Records | Period |
|---|---|---|---|
| NASA POWER Weather | [power.larc.nasa.gov](https://power.larc.nasa.gov) | 409,811 rows | 2000–2023 |
| FEWS NET IPC | [fews.net](https://fews.net/data/acute-food-insecurity) | 640 rows | Mar 2026 |
| KNBS CPI Reports | [knbs.or.ke](https://www.knbs.or.ke/cpi-and-inflation-rates/) | 37 PDFs → 64 records | 2020–2025 |
| WFP Food Prices | [WFP VAM](https://dataviz.vam.wfp.org/economic/prices) | 19,005 rows, 226 markets | 2006–2026 |
| Kenya Agri News | [kenyanews.go.ke](https://www.kenyanews.go.ke/category/agri/) | 300 articles | 2025–2026 |

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
│   └── processed/                  # Cleaned and merged datasets
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
│   ├── extract_data.py
│   ├── prepare_data.py
│   ├── merge_data.py
│   ├── train_food_security.py
│   ├── train_price_forecast.py
│   └── train_recommendation.py
├── src/                            # 14 reusable Python modules
├── figures/                        # 24 saved visualisations
├── models/saved/                   # Trained XGBoost model files
├── tableau/                        # Tableau dashboard CSV files
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
| WFP Kenya & NGOs | Pre-position food stocks 2–3 months before price spikes |
| Smallholder Farmers | Which crops to plant + which markets offer best prices |
| Kenya Ministry of Agriculture | National food security trend monitoring |
| KALRO | Weather-yield correlations for crop advisory updates |

---

## Acknowledgments

- NASA Langley Research Center — POWER API (public domain)
- Famine Early Warning Systems Network (FEWS NET)
- Kenya National Bureau of Statistics (KNBS)
- World Food Programme (WFP)
- Kenya News Agency

## License

MIT License — see [LICENSE](LICENSE) for details.