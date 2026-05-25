# Project Plan — Kenya Smart Agriculture & Market Intelligence Platform

## Overview

| Item | Detail |
|---|---|
| **Project Name** | Kenya Smart Agriculture & Market Intelligence Platform |
| **Phase** | 5 — Capstone |
| **Scrum Master** | Eve Otieno |
| **Start Date** | May 7, 2026 |
| **Presentation Date** | May 27–28, 2026 |
| **Submission Deadline** | May 26, 2026 (midday) |
| **GitHub Repo** | https://github.com/YOUR_USERNAME/kenya-smart-agriculture |
| **Kanban Board** | *(add link)* |
| **Deployment Link** | https://kenya-smart-agriculture.streamlit.app |

---

## Problem Statement

Automate FEWS NET food security phase classification using NASA satellite weather data, forecast food prices using raw KNBS CPI data, and analyse agricultural news sentiment — delivering an end-to-end ML platform for Kenya's 47 counties.

---

## Dataset Sources

| Dataset | Source URL | Raw? | Status |
|---|---|---|---|
| NASA POWER Weather | https://power.larc.nasa.gov/api/temporal/daily/point | ✅ Yes | Fetched via Python script |
| FEWS NET IPC | https://fews.net/data/acute-food-insecurity | ✅ Yes | Downloaded |
| KNBS CPI Reports | https://www.knbs.or.ke/cpi-and-inflation-rates/ | ✅ Yes | PDF text extracted |
| Kenya Agri News | https://www.kenyanews.go.ke/category/agri/ | ✅ Yes | Scraped via BeautifulSoup |

---

## Agile Workflow (Kanban)

### Sprint 1 — Data Collection & Cleaning (Week 1)
| Task | Owner | Status |
|---|---|---|
| Set up GitHub repo and project structure | Eve | ✅ Done |
| Fetch NASA POWER data for all 47 counties | Eve | ✅ Done |
| Download FEWS NET IPC CSV | Eve | ✅ Done |
| Download KNBS CPI PDF reports | Eve | ✅ Done |
| Run news scraper (60 pages KNA) | Eve | ✅ Done |
| Write data cleaning pipeline (Notebook 02) | Eve | 🔄 In Progress |
| Write KNBS CPI regex extraction | Eve | 🔄 In Progress |

### Sprint 2 — EDA & Modelling (Week 2)
| Task | Owner | Status |
|---|---|---|
| Exploratory data analysis (Notebook 03) | Eve | ⬜ Backlog |
| County choropleth map | Eve | ⬜ Backlog |
| IPC classification baseline model | Eve | ⬜ Backlog |
| XGBoost classifier + SHAP | Eve | ⬜ Backlog |
| CPI price forecasting (ARIMA + Prophet) | Eve | ⬜ Backlog |
| Recommendation system | Eve | ⬜ Backlog |
| NLP sentiment analysis | Eve | ⬜ Backlog |

### Sprint 3 — Deployment & Presentation (Week 2-3)
| Task | Owner | Status |
|---|---|---|
| Streamlit app (5 pages) | Eve | ⬜ Backlog |
| Deploy to Streamlit Cloud | Eve | ⬜ Backlog |
| Tableau dashboard | Eve | ⬜ Backlog |
| Non-technical slides | Eve | ⬜ Backlog |
| Final README polish | Eve | ⬜ Backlog |
| Canvas submission | Eve | ⬜ Backlog |

---

## Stretch Goals (X-Factor)

| Goal | Description | Priority |
|---|---|---|
| NLP DistilBERT fine-tuning | Fine-tune on KNA headlines beyond VADER baseline | High |
| BERTopic topic modelling | Discover news topic clusters automatically | High |
| SHAP explainability | Feature importance for XGBoost IPC classifier | Medium |
| Streamlit interactive county map | Folium map embedded in Streamlit | Medium |
| Swahili NLP | AfroXLMR for Swahili agricultural text | Low |

---

## Submission Checklist

### Business Understanding
- [ ] Clearly explains problem in README
- [ ] Clearly explains problem in Notebook
- [ ] Clearly explains problem in Slides

### Data Understanding
- [ ] Data sources described in README
- [ ] Data sources described in Notebook
- [ ] All variables described in Notebook

### Data Preparation
- [ ] Cleaning code in Notebook or .py files

### Modelling
- [ ] Baseline model included
- [ ] Additional iterated models included
- [ ] Preferred model described in README, Notebook, Slides

### Evaluation
- [ ] Model validation in README, Notebook, Slides

### README
- [ ] Data science process steps
- [ ] Future improvements
- [ ] Repository navigation
- [ ] Reproduction instructions
- [ ] Links to presentation and sources

### Deployment
- [ ] Working deployment link in README
- [ ] Streamlit app functional
- [ ] Tableau dashboard published

### Presentation
- [ ] Introduction slide
- [ ] Data science process slides
- [ ] Future improvements slide
- [ ] Contact info slide
- [ ] Uncluttered visuals, light on text

---

## Daily Standup Log

| Date | Done | Today | Blockers |
|---|---|---|---|
| 07 May 2026 | Set up project structure, fetched NASA data | Start data cleaning | None |
| — | — | — | — |

---

*Flatiron School — Phase 5 Capstone | May 2026*
