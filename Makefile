# Makefile — Kenya Smart Agriculture
# Usage: make <target>

.PHONY: setup data clean train app help

help:
	@echo ""
	@echo "Kenya Smart Agriculture — Available Commands"
	@echo "============================================"
	@echo "  make setup    Install all dependencies"
	@echo "  make data     Fetch NASA POWER data for all 47 counties"
	@echo "  make news     Run the news scraper"
	@echo "  make clean    Run the full data cleaning pipeline"
	@echo "  make train    Train all models"
	@echo "  make app      Launch the Streamlit app"
	@echo "  make test     Run basic data validation checks"
	@echo ""

setup:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Downloading NLTK data..."
	python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
	@echo "Setup complete."

data:
	@echo "Fetching NASA POWER weather data for all 47 Kenya counties..."
	@echo "Estimated time: 45-90 minutes"
	python scripts/fetch_nasa.py

news:
	@echo "Running Kenya agricultural news scraper..."
	python scripts/scrape_news.py

clean:
	@echo "Running data cleaning pipeline..."
	jupyter nbconvert --to notebook --execute notebooks/02_data_cleaning.ipynb \
		--output notebooks/02_data_cleaning_executed.ipynb
	@echo "Cleaning complete. Check data/processed/ for output files."

train:
	@echo "Training food security classification model..."
	jupyter nbconvert --to notebook --execute notebooks/04_food_security_classification.ipynb \
		--output notebooks/04_food_security_classification_executed.ipynb
	@echo "Training price forecasting model..."
	jupyter nbconvert --to notebook --execute notebooks/05_price_forecasting.ipynb \
		--output notebooks/05_price_forecasting_executed.ipynb
	@echo "Training complete. Check models/saved/ for artefacts."

app:
	@echo "Launching Streamlit app..."
	streamlit run app/streamlit_app.py

test:
	@echo "Running data validation checks..."
	python -c "\
import pandas as pd, os; \
files = { \
  'NASA Weather':     'data/raw/weather/kenya_weather_all_counties.csv', \
  'FEWS NET IPC':     'data/raw/food_security/kenya_ipc.csv', \
  'KNBS CPI':         'data/raw/prices/knbs_cpi_raw_text.csv', \
  'News Articles':    'data/raw/news/kenya_agri_news_raw.csv', \
}; \
all_ok = True; \
print(''); \
print('Dataset Status:'); \
[print(f'  OK  {k}' if os.path.exists(v) else (setattr(__builtins__, '_', None) or print(f'  MISSING  {k} → {v}'))) for k, v in files.items()]; \
print(''); \
"
