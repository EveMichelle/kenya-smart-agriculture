"""
app/streamlit_app.py — Kenya Smart Agriculture Platform
=========================================================
Deploy: streamlit run app/streamlit_app.py

Pages:
  1. Home / Overview
  2. Food Security Risk Map
  3. Price Forecast
  4. County Intelligence Report
  5. News Sentiment Feed
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Kenya Smart Agriculture",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Sidebar navigation ────────────────────────────────────────
st.sidebar.image("https://flagcdn.com/w80/ke.png", width=60)
st.sidebar.title("🌾 Kenya Agriculture")
st.sidebar.caption("Market Intelligence Platform")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "🗺️ Food Security Map",
        "📈 Price Forecast",
        "🏘️ County Report",
        "📰 News Sentiment",
    ],
)

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = {}
    files = {
        "master": "data/processed/master_dataset.csv",
        "ipc":    "data/processed/ipc_clean.csv",
        "knbs":   "data/processed/knbs_cpi_structured.csv",
        "news":   "data/processed/news_clean.csv",
    }
    for key, rel_path in files.items():
        full_path = os.path.join(base, rel_path)
        if os.path.exists(full_path):
            data[key] = pd.read_csv(full_path)
        else:
            data[key] = None
    return data

data = load_data()

# ── HOME ──────────────────────────────────────────────────────
if page == "🏠 Home":
    st.title("🌾 Kenya Smart Agriculture & Market Intelligence Platform")
    st.caption("Phase 5 Capstone | Data Science Programme | May 2026")

    st.markdown("""
    This platform uses **NASA satellite weather data** to predict food security risk,
    forecast commodity prices, and analyse agricultural news sentiment across
    all **47 counties in Kenya**.
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Counties Covered", "47")
    with col2:
        st.metric("NASA Weather Records", "409,811")
    with col3:
        st.metric("CPI Reports Analysed", "37")
    with col4:
        st.metric("News Articles", "300")

    st.divider()
    st.subheader("📊 Data Sources")
    sources = pd.DataFrame({
        "Dataset":      ["NASA POWER", "FEWS NET IPC", "KNBS CPI", "Kenya News"],
        "Records":      ["409,811 rows", "640 rows", "5,607 text rows", "300 articles"],
        "Period":       ["2000–2023", "Mar 2026", "2021–2025", "2025–2026"],
        "Module":       ["All ML modules", "Classification", "Forecasting", "NLP"],
    })
    st.dataframe(sources, use_container_width=True, hide_index=True)

# ── FOOD SECURITY MAP ─────────────────────────────────────────
elif page == "🗺️ Food Security Map":
    st.title("🗺️ Food Security Risk Map")
    st.caption("Predicted IPC Phase per county based on NASA weather features")

    if data["ipc"] is not None:
        ipc = data["ipc"]
        if "ipc_phase" in ipc.columns and "county" in ipc.columns:
            phase_labels = {1: "Minimal", 2: "Stressed", 3: "Crisis"}
            ipc["Phase"] = ipc["ipc_phase"].map(phase_labels)

            col1, col2 = st.columns([2, 1])

            with col1:
                phase_counts = ipc["ipc_phase"].value_counts().sort_index()
                st.bar_chart(phase_counts)

            with col2:
                st.markdown("**IPC Phase Key:**")
                st.markdown("🟢 **Phase 1** — Minimal (food secure)")
                st.markdown("🟡 **Phase 2** — Stressed")
                st.markdown("🔴 **Phase 3** — Crisis")

            st.subheader("County-Level IPC Phases")
            county_ipc = (
                ipc.groupby("county")["ipc_phase"]
                .agg(lambda x: x.mode()[0])
                .reset_index()
                .sort_values("ipc_phase", ascending=False)
            )
            county_ipc["Phase Label"] = county_ipc["ipc_phase"].map(phase_labels)
            st.dataframe(county_ipc, use_container_width=True, hide_index=True)
    else:
        st.warning("Run notebook 02 to generate processed data first.")

# ── PRICE FORECAST ────────────────────────────────────────────
elif page == "📈 Price Forecast":
    st.title("📈 Food Price Forecast")
    st.caption("KNBS CPI commodity price trends — 2021 to 2025")

    if data["knbs"] is not None:
        knbs = data["knbs"]
        price_cols = [c for c in knbs.columns
                      if c not in ["date", "month", "year", "source_file",
                                   "food_cpi_change", "yoy_inflation"]]

        col = st.selectbox("Select commodity / index:", price_cols)

        if col and col in knbs.columns:
            knbs["date"] = pd.to_datetime(knbs["date"], errors="coerce")
            plot_data = knbs.dropna(subset=[col]).sort_values("date")
            st.line_chart(plot_data.set_index("date")[col])
            st.caption(f"Source: Kenya National Bureau of Statistics (KNBS) CPI Reports")
    else:
        st.warning("Run notebook 02 to generate processed data first.")

# ── COUNTY REPORT ─────────────────────────────────────────────
elif page == "🏘️ County Report":
    st.title("🏘️ County Intelligence Report")

    if data["master"] is not None:
        counties = sorted(data["master"]["county"].dropna().unique().tolist())
        county = st.selectbox("Select county:", counties)

        if county:
            county_data = data["master"][data["master"]["county"] == county]

            col1, col2, col3 = st.columns(3)
            with col1:
                rain = county_data["total_rainfall"].mean()
                st.metric("Avg Monthly Rainfall", f"{rain:.1f} mm" if not np.isnan(rain) else "N/A")
            with col2:
                temp = county_data["mean_temp"].mean()
                st.metric("Avg Temperature", f"{temp:.1f}°C" if not np.isnan(temp) else "N/A")
            with col3:
                if "ipc_phase_county" in county_data.columns:
                    phase = county_data["ipc_phase_county"].dropna()
                    if len(phase):
                        phase_val = int(phase.mode()[0])
                        labels = {1: "Minimal 🟢", 2: "Stressed 🟡", 3: "Crisis 🔴"}
                        st.metric("Food Security", labels.get(phase_val, str(phase_val)))

            st.subheader(f"Rainfall Over Time — {county}")
            rain_ts = county_data.groupby(["year", "month"])["total_rainfall"].mean().reset_index()
            rain_ts["date"] = pd.to_datetime(rain_ts[["year", "month"]].assign(day=1))
            st.line_chart(rain_ts.set_index("date")["total_rainfall"])
    else:
        st.warning("Run notebook 02 to generate processed data first.")

# ── NEWS SENTIMENT ────────────────────────────────────────────
elif page == "📰 News Sentiment":
    st.title("📰 Agricultural News Sentiment")
    st.caption("Kenya News Agency agricultural headlines — 2025 to 2026")

    if data["news"] is not None:
        news = data["news"]

        if "vader_sentiment" in news.columns:
            col1, col2, col3 = st.columns(3)
            for col, label, colour in [
                ("Positive", "🟢 Positive", "#66BB6A"),
                ("Neutral",  "⚪ Neutral",  "#BDBDBD"),
                ("Negative", "🔴 Negative", "#EF5350"),
            ]:
                count = (news["vader_sentiment"] == col).sum()
                with [col1, col2, col3][["Positive", "Neutral", "Negative"].index(col)]:
                    st.metric(label, count)

        st.subheader("Latest Headlines")
        display_cols = [c for c in ["title_clean", "date", "vader_sentiment", "url"]
                        if c in news.columns]
        st.dataframe(
            news[display_cols].head(20).rename(columns={"title_clean": "Headline"}),
            use_container_width=True, hide_index=True
        )
    else:
        st.warning("Run notebook 02 to generate processed data first.")

# ── Footer ────────────────────────────────────────────────────
st.sidebar.divider()
st.sidebar.caption("Kenya Smart Agriculture Platform")
st.sidebar.caption("Phase 5 Capstone | May 2026")
st.sidebar.caption("Data: NASA POWER · FEWS NET · KNBS · KNA")
