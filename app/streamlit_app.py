"""
app/streamlit_app.py — Kenya Smart Agriculture Platform
Deploy: streamlit run app/streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import ast
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title="Kenya Smart Agriculture",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #1565C0 0%, #0D47A1 100%);
    border-radius: 12px;
    padding: 20px;
    color: white;
    text-align: center;
    margin: 5px;
}
.crisis-badge {
    background-color: #EF5350;
    color: white;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}
.minimal-badge {
    background-color: #66BB6A;
    color: white;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}
.stressed-badge {
    background-color: #FFA726;
    color: white;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: bold;
}
.big-number {
    font-size: 2.5rem;
    font-weight: 800;
    color: #1565C0;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.image("https://flagcdn.com/w80/ke.png", width=60)
st.sidebar.title("🌾 Kenya Agriculture")
st.sidebar.caption("Market Intelligence Platform")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    ["🏠 Home", "🗺️ Food Security Map", "📈 Price Forecast",
     "🌱 Crop Recommendation", "📰 News Sentiment"],
)

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data = {}
    files = {
        "master":   "data/processed/master_dataset.csv",
        "ipc":      "data/processed/ipc_county.csv",
        "knbs":     "data/processed/knbs_cpi_structured.csv",
        "news":     "data/processed/news_sentiment.csv",
        "profiles": "data/processed/county_profiles.csv",
        "wfp":      "data/processed/wfp_prices_recent.csv",
    }
    for key, rel_path in files.items():
        full_path = os.path.join(base, rel_path)
        data[key] = pd.read_csv(full_path) if os.path.exists(full_path) else None
    return data

data = load_data()

# ── Crop scoring function ─────────────────────────────────────
CROPS = {
    "Maize":            {"rain_min":150,"rain_max":350,"t_min":18,"t_max":27,"drought":False},
    "Sorghum":          {"rain_min":70, "rain_max":220,"t_min":20,"t_max":35,"drought":True},
    "Millet (Finger)":  {"rain_min":60, "rain_max":180,"t_min":18,"t_max":35,"drought":True},
    "Beans":            {"rain_min":100,"rain_max":220,"t_min":15,"t_max":25,"drought":False},
    "Cowpeas":          {"rain_min":70, "rain_max":250,"t_min":20,"t_max":35,"drought":True},
    "Cassava":          {"rain_min":30, "rain_max":500,"t_min":25,"t_max":35,"drought":True},
    "Sweet Potato":     {"rain_min":130,"rain_max":350,"t_min":20,"t_max":30,"drought":False},
    "Potatoes (Irish)": {"rain_min":150,"rain_max":400,"t_min":10,"t_max":20,"drought":False},
    "Kale (Sukuma Wiki)":{"rain_min":100,"rain_max":350,"t_min":15,"t_max":25,"drought":False},
    "Pigeon Peas":      {"rain_min":80, "rain_max":250,"t_min":18,"t_max":35,"drought":True},
}

CROP_WFP = {
    "Maize":"Maize","Sorghum":"Sorghum","Millet (Finger)":"Millet (finger)",
    "Beans":"Beans","Cowpeas":"Cowpeas","Potatoes (Irish)":"Potatoes (Irish)",
    "Kale (Sukuma Wiki)":"Kale","Pigeon Peas":"Pigeon peas (dry)",
}

def score_crops(rainfall_mm, temp_c, drought_freq, season="MAM"):
    results = []
    for crop, req in CROPS.items():
        if season == "OND" and crop in ["Millet (Finger)"]:
            continue
        rain_score = 40
        if rainfall_mm < req["rain_min"]:
            rain_score = max(0, 40 - (req["rain_min"]-rainfall_mm)/req["rain_min"]*40)
        elif rainfall_mm > req["rain_max"]:
            rain_score = max(0, 40 - (rainfall_mm-req["rain_max"])/req["rain_max"]*20)

        temp_score = 35
        if temp_c < req["t_min"]:
            temp_score = max(0, 35 - (req["t_min"]-temp_c)*5)
        elif temp_c > req["t_max"]:
            temp_score = max(0, 35 - (temp_c-req["t_max"])*5)

        drought_score = 25 if (req["drought"] and drought_freq>0.3) else \
                        25 if (not req["drought"] and drought_freq<=0.2) else \
                        0  if (not req["drought"] and drought_freq>0.5) else 12

        results.append({
            "Crop": crop,
            "Score": round(rain_score+temp_score+drought_score, 1),
            "Drought Tolerant": "✅ Yes" if req["drought"] else "No",
            "wfp_key": CROP_WFP.get(crop)
        })
    return sorted(results, key=lambda x: -x["Score"])

# ────────────────────────────────────────────────────────────────
# HOME
# ────────────────────────────────────────────────────────────────
if page == "🏠 Home":
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1B5E20 0%,#2E7D32 50%,#1565C0 100%);
                border-radius:16px;padding:36px;text-align:center;margin-bottom:20px;color:white">
        <div style="font-size:3rem">🇰🇪 🌾</div>
        <div style="font-size:1.8rem;font-weight:800;margin:8px 0">Kenya Smart Agriculture Platform</div>
        <div style="font-size:0.95rem;opacity:0.9;max-width:700px;margin:0 auto">
            Using NASA satellite weather data to predict food security risk,
            forecast food prices, and recommend crops to farmers across all 47 counties in Kenya.
        </div>
    </div>""", unsafe_allow_html=True)
    st.info("📖 **How to use this app:** Navigate using the menu on the left. "
            "🗺️ Food Security Map shows which counties are in food crisis right now. "
            "📈 Price Forecast shows how food prices have changed and where they are heading. "
            "🌱 Crop Recommendation tells you what to plant based on your county weather and current market prices. "
            "📰 News shows what Kenyan farmers are reading and how they feel.")

    col1, col2, col3, col4 = st.columns(4)
    for col, num, label in [
        (col1, "47", "Counties Covered"),
        (col2, "409,811", "NASA Records"),
        (col3, "226", "WFP Markets"),
        (col4, "300", "News Articles"),
    ]:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="big-number">{num}</div>
                <div style="font-size:14px; opacity:0.9">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Model Results")
        results_df = pd.DataFrame({
            "Module": ["Food Security Classification","Price Forecasting",
                       "Crop Recommendation","NLP Sentiment"],
            "Model": ["XGBoost","Prophet","NASA + WFP","VADER"],
            "Score": ["F1 = 0.738 ✅","MAPE = 0.81% ✅",
                      "10 crops × 226 markets ✅","47.3% positive ✅"],
        })
        st.dataframe(results_df, use_container_width=True, hide_index=True)

        if data["ipc"] is not None:
            ipc = data["ipc"]
            phase_counts = ipc["ipc_phase"].value_counts().sort_index()
            fig = go.Figure(data=[go.Bar(
                x=["Phase 1 Minimal","Phase 2 Stressed","Phase 3 Crisis"],
                y=[phase_counts.get(1,0), phase_counts.get(2,0), phase_counts.get(3,0)],
                marker_color=["#66BB6A","#FFA726","#EF5350"],
                text=[phase_counts.get(1,0), phase_counts.get(2,0), phase_counts.get(3,0)],
                textposition="outside",
            )])
            fig.update_layout(title="IPC Food Security Phase Distribution (March 2026)",
                              height=300, margin=dict(t=40,b=20),
                              plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🔑 Key Findings")
        st.success("✅ **12 counties** in Phase 3 Crisis — all in northern arid zones")
        st.warning("⚠️ **NASA SPI-3** is the #1 predictor of food insecurity")
        st.info("📈 **Kenya CPI** rose 35% (2020→2025). Forecast: 148 by Jan 2026")
        st.success("📰 Agricultural news is **47% positive** overall")

        st.markdown("---")
        st.subheader("📦 Data Sources")
        sources = pd.DataFrame({
            "Dataset": ["NASA POWER","FEWS NET IPC","KNBS CPI","WFP Prices","Kenya News"],
            "Records": ["409,811","640","37 PDFs","19,005","300"],
            "Period": ["2000–2023","Mar 2026","2020–2025","2006–2026","2025–2026"],
        })
        st.dataframe(sources, use_container_width=True, hide_index=True)

# ────────────────────────────────────────────────────────────────
# FOOD SECURITY MAP
# ────────────────────────────────────────────────────────────────
elif page == "🗺️ Food Security Map":
    st.title("🗺️ Food Security Risk Map")
    st.caption("IPC phase per county — FEWS NET, March 2026")
    st.markdown("> 🍽️ **What does this mean?** The IPC scale measures how serious the food situation is in each county. Phase 1 (green) means people have enough food. Phase 2 (yellow) means some people are struggling. Phase 3 (red) means there is a serious food crisis and people need help urgently.")

    if data["ipc"] is not None:
        ipc = data["ipc"]
        phase_labels = {1:"Minimal",2:"Stressed",3:"Crisis"}
        phase_colours = {1:"🟢",2:"🟡",3:"🔴"}

        col1, col2, col3 = st.columns(3)
        for phase, label, col in [(1,"Minimal",col1),(2,"Stressed",col2),(3,"Crisis",col3)]:
            count = (ipc["ipc_phase"] == phase).sum()
            with col:
                colour = "#66BB6A" if phase==1 else "#FFA726" if phase==2 else "#EF5350"
                st.markdown(f"""
                <div style="background:{colour};border-radius:12px;padding:20px;
                            text-align:center;color:white;margin:5px">
                    <div style="font-size:2.5rem;font-weight:800">{count}</div>
                    <div style="font-size:14px">Phase {phase} — {label}</div>
                </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # County coordinates for scatter map
        COUNTY_COORDS = {
            "Mombasa":(-4.04,39.67),"Kwale":(-4.18,39.46),"Kilifi":(-3.51,39.91),
            "Tana River":(-1.50,39.50),"Lamu":(-2.27,40.90),"Taita Taveta":(-3.32,38.48),
            "Garissa":(-0.45,39.64),"Wajir":(1.75,40.06),"Mandera":(3.94,41.86),
            "Marsabit":(2.33,37.99),"Isiolo":(0.36,37.58),"Meru":(0.05,37.65),
            "Tharaka Nithi":(-0.20,37.80),"Embu":(-0.54,37.46),"Kitui":(-1.37,38.01),
            "Machakos":(-1.52,37.26),"Makueni":(-2.26,37.62),"Nyandarua":(-0.18,36.58),
            "Nyeri":(-0.42,36.95),"Kirinyaga":(-0.66,37.38),"Muranga":(-0.72,37.15),
            "Kiambu":(-1.03,36.81),"Turkana":(3.12,35.60),"West Pokot":(1.62,35.12),
            "Samburu":(1.22,36.90),"Trans Nzoia":(1.06,35.00),"Uasin Gishu":(0.51,35.27),
            "Elgeyo Marakwet":(0.78,35.52),"Nandi":(0.18,35.10),"Baringo":(0.67,36.08),
            "Laikipia":(0.36,36.78),"Nakuru":(-0.30,36.08),"Narok":(-1.09,35.87),
            "Kajiado":(-1.85,36.78),"Kericho":(-0.37,35.28),"Bomet":(-0.78,35.35),
            "Kakamega":(0.28,34.75),"Vihiga":(0.08,34.72),"Bungoma":(0.56,34.56),
            "Busia":(0.43,34.11),"Siaya":(-0.06,34.29),"Kisumu":(-0.10,34.76),
            "Homa Bay":(-0.52,34.45),"Migori":(-1.06,34.47),"Kisii":(-0.68,34.77),
            "Nyamira":(-0.57,34.93),"Nairobi":(-1.29,36.82),
        }

        # Try choropleth with shapefile, fallback to scatter map
        shp_path = "data/raw/kenya_shapefiles/gadm41_KEN_1.shp"
        try:
            import geopandas as gpd
            import json
            kenya_shp = gpd.read_file(shp_path)
            kenya_shp["county"] = kenya_shp["NAME_1"].replace({
                "Elgeyo-Marakwet":"Elgeyo Marakwet","Murang'a":"Muranga",
                "Trans-Nzoia":"Trans Nzoia","Homa-Bay":"Homa Bay",
            })
            kenya_geo = kenya_shp.merge(
                ipc[["county","ipc_phase","ipc_phase_label"]], on="county", how="left"
            )
            kenya_geo["ipc_phase"] = kenya_geo["ipc_phase"].fillna(1)
            geojson = json.loads(kenya_geo.to_json())

            fig_map = px.choropleth_mapbox(
                kenya_geo, geojson=geojson,
                locations=kenya_geo.index,
                color="ipc_phase",
                color_continuous_scale=[[0,"#66BB6A"],[0.5,"#FFA726"],[1,"#EF5350"]],
                range_color=[1,3],
                hover_name="county",
                hover_data={"ipc_phase_label":True,"ipc_phase":False},
                mapbox_style="carto-positron",
                zoom=5, center={"lat":0.5,"lon":37.5},
                opacity=0.8,
                title="Kenya Food Security Risk Map — IPC Phase by County (March 2026)",
                height=560,
            )
            fig_map.update_layout(
                margin=dict(t=40,b=0,l=0,r=0),
                coloraxis_colorbar=dict(
                    title="IPC Phase",
                    tickvals=[1,2,3],
                    ticktext=["Phase 1<br>Minimal","Phase 2<br>Stressed","Phase 3<br>Crisis"],
                )
            )
        except Exception:
            # Fallback to scatter map
            map_data = []
            for _, row in ipc.iterrows():
                county = row["county"]
                if county in COUNTY_COORDS:
                    lat, lon = COUNTY_COORDS[county]
                    map_data.append({
                        "County": county, "Latitude": lat, "Longitude": lon,
                        "Label": phase_labels.get(row["ipc_phase"],""),
                    })
            map_df = pd.DataFrame(map_data)
            fig_map = px.scatter_mapbox(
                map_df, lat="Latitude", lon="Longitude",
                color="Label", size=[15]*len(map_df),
                color_discrete_map={"Minimal":"#66BB6A","Stressed":"#FFA726","Crisis":"#EF5350"},
                hover_name="County",
                mapbox_style="carto-positron",
                zoom=5, center={"lat":0.5,"lon":37.5},
                height=550,
            )
        fig_map.update_layout(margin=dict(t=40,b=0,l=0,r=0))
        st.plotly_chart(fig_map, use_container_width=True)

        st.markdown("---")
        col1, col2 = st.columns([2,1])
        with col1:
            st.subheader("All Counties")
            display = ipc[["county","ipc_phase","ipc_phase_label"]].copy()
            display["Status"] = display["ipc_phase"].map(
                lambda x: f"{phase_colours.get(x,'')} {phase_labels.get(x,'')}")
            display = display.sort_values("ipc_phase",ascending=False)
            st.dataframe(display[["county","Status"]].rename(columns={"county":"County"}),
                         use_container_width=True, hide_index=True, height=400)
        with col2:
            st.subheader("🔴 Crisis Counties")
            crisis = sorted(ipc[ipc["ipc_phase"]==3]["county"].tolist())
            for c in crisis:
                st.markdown(f"🔴 **{c}**")
    else:
        st.warning("Run notebook 02 to generate processed data.")

# ────────────────────────────────────────────────────────────────
# PRICE FORECAST
# ────────────────────────────────────────────────────────────────
elif page == "📈 Price Forecast":
    st.title("📈 Kenya Food Price Forecast")
    st.caption("KNBS CPI 2020–2025 + 8-month Prophet forecast")
    st.markdown("> 📈 **What is the CPI?** The Consumer Price Index (CPI) tracks how much food prices have gone up or down. When CPI rises, food costs more. Kenya's CPI has gone up 35% since 2020 — meaning food that cost KES 100 in 2020 now costs KES 135. The forecast shows where prices are likely to go over the next 8 months.")

    if data["knbs"] is not None:
        knbs = data["knbs"].copy()
        knbs["date"] = pd.to_datetime(knbs["date"], errors="coerce")
        knbs = knbs.sort_values("date")

        latest   = knbs.iloc[-1]
        earliest = knbs.iloc[0]
        change   = (latest["overall_cpi"]-earliest["overall_cpi"])/earliest["overall_cpi"]*100

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.metric("Latest CPI",f"{latest['overall_cpi']:.2f}",
                      delta=f"{latest['overall_cpi']-knbs.iloc[-2]['overall_cpi']:.2f}")
        with col2:
            st.metric("Latest Inflation",f"{latest['yoy_inflation']:.1f}%")
        with col3:
            st.metric("Rise since Feb 2020",f"+{change:.1f}%")
        with col4:
            st.metric("Jan 2026 Forecast","147.67",delta="+2.79")

        st.markdown("---")

        # Historical CPI chart
        fig_cpi = go.Figure()
        fig_cpi.add_trace(go.Scatter(
            x=knbs["date"], y=knbs["overall_cpi"],
            mode="lines+markers", name="Historical CPI",
            line=dict(color="#1565C0",width=2.5),
            marker=dict(size=4),
            fill="tozeroy", fillcolor="rgba(21,101,192,0.08)",
        ))
        # Add 8-month forecast
        forecast_dates = pd.date_range("2025-06-01", periods=8, freq="MS")
        forecast_vals  = [145.01,145.04,145.03,145.30,145.90,146.36,147.09,147.67]
        lower = [144.75,144.74,144.61,144.71,145.02,145.18,145.65,145.87]
        upper = [145.26,145.37,145.50,145.98,146.91,147.71,148.74,149.72]

        fig_cpi.add_trace(go.Scatter(
            x=list(forecast_dates)+list(forecast_dates[::-1]),
            y=upper+lower[::-1],
            fill="toself", fillcolor="rgba(230,81,0,0.12)",
            line=dict(color="rgba(0,0,0,0)"), name="95% Confidence Interval",
        ))
        fig_cpi.add_trace(go.Scatter(
            x=forecast_dates, y=forecast_vals,
            mode="lines+markers", name="Prophet Forecast",
            line=dict(color="#E65100",width=2.5,dash="dash"),
            marker=dict(size=6,symbol="circle-open"),
        ))
        fig_cpi.add_vline(x=pd.Timestamp("2025-05-01").timestamp()*1000,
                          line_dash="dot", line_color="grey",
                          annotation_text="Last known data")
        fig_cpi.update_layout(
            title="Kenya Overall CPI — Historical + 8-Month Forecast",
            xaxis_title="Date", yaxis_title="CPI Index (Feb 2019 = 100)",
            height=420, plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h",yanchor="bottom",y=1.02),
        )
        st.plotly_chart(fig_cpi, use_container_width=True)
        st.caption("Model: Facebook Prophet | MAPE: 0.81% on 12-month holdout")

        # Inflation chart
        fig_inf = px.bar(knbs, x="date", y="yoy_inflation",
                         title="Year-on-Year Inflation Rate (%)",
                         color="yoy_inflation",
                         color_continuous_scale=["#66BB6A","#FFA726","#EF5350"],
                         labels={"yoy_inflation":"Inflation (%)","date":"Date"})
        fig_inf.update_layout(height=320, plot_bgcolor="rgba(0,0,0,0)",
                              paper_bgcolor="rgba(0,0,0,0)",
                              coloraxis_showscale=False)
        st.plotly_chart(fig_inf, use_container_width=True)

        # WFP commodity prices
        if data["wfp"] is not None:
            st.markdown("---")
            st.subheader("📦 Current WFP Market Prices")
            wfp = data["wfp"].copy()
            key_crops = ["Maize","Beans","Sorghum","Kale","Cowpeas","Potatoes (Irish)"]
            price_rows = []
            for crop in key_crops:
                crop_data = wfp[wfp["commodity"].str.contains(
                    crop.split(" ")[0], case=False, na=False)]
                if not crop_data.empty:
                    price_rows.append({
                        "Commodity": crop,
                        "Avg KES/kg": f"KES {crop_data['price'].mean():.0f}",
                        "Markets": crop_data["market"].nunique(),
                    })
            if price_rows:
                st.dataframe(pd.DataFrame(price_rows),
                             use_container_width=True, hide_index=True)
    else:
        st.warning("Run notebook 05 first.")

# ────────────────────────────────────────────────────────────────
# CROP RECOMMENDATION
# ────────────────────────────────────────────────────────────────
elif page == "🌱 Crop Recommendation":
    st.title("🌱 Farmer Crop & Market Recommendation")
    st.markdown("> *Enter your county and season — get personalised crop recommendations and current market prices.*")

    if data["profiles"] is not None:
        profiles = data["profiles"].drop_duplicates(subset=["county"]).reset_index(drop=True)
        counties = sorted(profiles["county"].dropna().unique().tolist())

        col1, col2 = st.columns(2)
        with col1:
            county = st.selectbox("📍 Select your county:", counties)
        with col2:
            season = st.selectbox("🌦️ Select season:",
                                  ["MAM — Long Rains (Mar–May)",
                                   "OND — Short Rains (Oct–Dec)"])
        season_code = "MAM" if "MAM" in season else "OND"

        if county:
            row = profiles[profiles["county"] == county].iloc[0]
            annual_rain  = float(row.get("annual_rainfall", 0) or 0)
            mean_temp    = float(row.get("mean_temp", 25) or 25)
            drought_freq = float(row.get("drought_frequency", 0.3) or 0.3)
            seasonal_rain = annual_rain / 12 * 3
            ipc_label    = str(row.get("ipc_phase_label", "Unknown"))

            st.markdown("---")
            col1,col2,col3,col4 = st.columns(4)
            with col1:
                st.metric("🌧️ Annual Rainfall", f"{annual_rain:.0f} mm")
            with col2:
                st.metric("🌡️ Mean Temperature", f"{mean_temp:.1f}°C")
            with col3:
                st.metric("🏜️ Drought Frequency", f"{drought_freq*100:.0f}%")
            with col4:
                icon = {"Minimal":"🟢","Stressed":"🟡","Crisis":"🔴"}.get(ipc_label,"⚪")
                st.metric("🍽️ Food Security", f"{icon} {ipc_label}")

            # Dynamic crop scoring
            st.markdown("---")
            scored = score_crops(seasonal_rain, mean_temp, drought_freq, season_code)

            st.subheader(f"🌱 Top Crop Recommendations — {county} — {season_code} Season")

            # Get WFP prices
            wfp_prices = {}
            if data["wfp"] is not None:
                wfp = data["wfp"]
                for crop_info in scored[:6]:
                    wfp_key = crop_info.get("wfp_key")
                    if wfp_key:
                        prices = wfp[wfp["commodity"].str.contains(
                            wfp_key.split("(")[0].strip(), case=False, na=False)]["price"]
                        if not prices.empty:
                            wfp_prices[crop_info["Crop"]] = f"KES {prices.mean():.0f}/kg"

            # Display top 6 crops as cards
            top6 = scored[:6]
            col_cards = st.columns(3)
            for i, crop_info in enumerate(top6):
                score   = crop_info["Score"]
                crop    = crop_info["Crop"]
                dt      = crop_info["Drought Tolerant"]
                price   = wfp_prices.get(crop, "N/A")
                colour  = "#66BB6A" if score >= 80 else "#FFA726" if score >= 60 else "#90A4AE"
                rank_emoji = ["🥇","🥈","🥉","4️⃣","5️⃣","6️⃣"][i]
                with col_cards[i % 3]:
                    st.markdown(f"""
                    <div style="background:{colour};border-radius:12px;padding:16px;
                                color:white;margin:6px;min-height:140px">
                        <div style="font-size:1.5rem">{rank_emoji}</div>
                        <div style="font-size:1.1rem;font-weight:700">{crop}</div>
                        <div style="font-size:0.9rem;opacity:0.9">
                            Score: {score}% | {dt}<br>
                            {f'Market: {price}' if price != 'N/A' else 'Price: N/A'}
                        </div>
                    </div>""", unsafe_allow_html=True)

            # Suitability bar chart
            st.markdown("---")
            all_crops = pd.DataFrame(scored)
            fig_crops = px.bar(
                all_crops, x="Score", y="Crop",
                orientation="h",
                color="Score",
                color_continuous_scale=["#EF5350","#FFA726","#66BB6A"],
                range_color=[0,100],
                title=f"Crop Suitability Scores — {county} ({season_code} Season)",
                labels={"Score":"Suitability Score (%)"},
            )
            fig_crops.add_vline(x=70, line_dash="dash", line_color="white",
                                annotation_text="Recommended threshold")
            fig_crops.update_layout(height=380, plot_bgcolor="rgba(0,0,0,0)",
                                    paper_bgcolor="rgba(0,0,0,0)",
                                    coloraxis_showscale=False,
                                    yaxis=dict(categoryorder="total ascending"))
            st.plotly_chart(fig_crops, use_container_width=True)
            st.caption("Scores based on NASA rainfall and temperature suitability against crop climate requirements.")
    else:
        st.warning("Run notebook 06 first.")

# ────────────────────────────────────────────────────────────────
# NEWS SENTIMENT
# ────────────────────────────────────────────────────────────────
elif page == "📰 News Sentiment":
    st.title("📰 Agricultural News Sentiment")
    st.caption("Kenya News Agency — 300 headlines, 2025–2026")
    st.markdown("> 📰 **What is sentiment analysis?** We read 300 news headlines from the Kenya News Agency and automatically scored whether each headline sounds positive, negative, or neutral. A positive score means the news is about good things happening in farming. A negative score means the news is about problems — like drought, disease outbreaks, or falling prices.")

    if data["news"] is not None:
        news = data["news"].copy()
        news["date"] = pd.to_datetime(news["date"], errors="coerce")

        pos = (news["vader_sentiment"]=="Positive").sum()
        neu = (news["vader_sentiment"]=="Neutral").sum()
        neg = (news["vader_sentiment"]=="Negative").sum()
        mean_score = news["vader_score"].mean()

        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div style="background:#66BB6A;border-radius:12px;padding:16px;
                        text-align:center;color:white">
                <div style="font-size:2rem;font-weight:800">{pos}</div>
                <div>🟢 Positive ({pos/len(news)*100:.0f}%)</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div style="background:#90A4AE;border-radius:12px;padding:16px;
                        text-align:center;color:white">
                <div style="font-size:2rem;font-weight:800">{neu}</div>
                <div>⚪ Neutral ({neu/len(news)*100:.0f}%)</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="background:#EF5350;border-radius:12px;padding:16px;
                        text-align:center;color:white">
                <div style="font-size:2rem;font-weight:800">{neg}</div>
                <div>🔴 Negative ({neg/len(news)*100:.0f}%)</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.metric("Mean VADER Score", f"{mean_score:.3f}",
                      delta="Net positive" if mean_score > 0 else "Net negative")

        st.markdown("---")
        col1,col2 = st.columns([3,2])

        with col1:
            # Sentiment pie chart
            fig_pie = px.pie(
                values=[pos,neu,neg],
                names=["Positive","Neutral","Negative"],
                color_discrete_sequence=["#66BB6A","#90A4AE","#EF5350"],
                title="Sentiment Distribution",
                hole=0.4,
            )
            fig_pie.update_layout(height=300,margin=dict(t=40,b=0),
                                  paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_pie, use_container_width=True)

            # Monthly sentiment trend
            news_valid = news.dropna(subset=["date"])
            news_valid["month"] = news_valid["date"].dt.to_period("M").astype(str)
            monthly = news_valid.groupby("month")["vader_score"].mean().reset_index()
            fig_trend = px.line(monthly, x="month", y="vader_score",
                                title="Monthly Sentiment Trend",
                                markers=True, color_discrete_sequence=["#E65100"])
            fig_trend.add_hline(y=0, line_dash="dot", line_color="grey")
            fig_trend.update_layout(height=280, plot_bgcolor="rgba(0,0,0,0)",
                                    paper_bgcolor="rgba(0,0,0,0)",
                                    xaxis_title="Month",
                                    yaxis_title="Mean VADER Score")
            st.plotly_chart(fig_trend, use_container_width=True)

        with col2:
            # Topic distribution
            if "topic_label" in news.columns:
                st.subheader("📌 News Topics")
                topic_counts = news["topic_label"].value_counts()
                fig_topics = px.bar(
                    x=topic_counts.values, y=topic_counts.index,
                    orientation="h",
                    color=topic_counts.values,
                    color_continuous_scale=["#90A4AE","#1565C0"],
                    title="Articles per Topic",
                )
                fig_topics.update_layout(height=280, showlegend=False,
                                         coloraxis_showscale=False,
                                         plot_bgcolor="rgba(0,0,0,0)",
                                         paper_bgcolor="rgba(0,0,0,0)",
                                         yaxis=dict(categoryorder="total ascending"))
                st.plotly_chart(fig_topics, use_container_width=True)

            # Top counties mentioned
            st.subheader("📍 Top Counties in Headlines")
            try:
                all_counties = []
                for val in news["counties_mentioned"].dropna():
                    counties_list = ast.literal_eval(val) if isinstance(val, str) else val
                    all_counties.extend(counties_list)
                if all_counties:
                    top_c = pd.DataFrame(
                        Counter(all_counties).most_common(8),
                        columns=["County","Mentions"]
                    )
                    fig_c = px.bar(top_c, x="Mentions", y="County",
                                   orientation="h",
                                   color="Mentions",
                                   color_continuous_scale=["#FFA726","#EF5350"],)
                    fig_c.update_layout(height=280, showlegend=False,
                                        coloraxis_showscale=False,
                                        plot_bgcolor="rgba(0,0,0,0)",
                                        paper_bgcolor="rgba(0,0,0,0)",
                                        yaxis=dict(categoryorder="total ascending"))
                    st.plotly_chart(fig_c, use_container_width=True)
            except:
                pass

        # Headlines table
        st.markdown("---")
        st.subheader("📋 Browse Headlines")
        filter_sent = st.selectbox("Filter by sentiment:",
                                   ["All","Positive","Neutral","Negative"])
        filtered = news if filter_sent == "All" else \
                   news[news["vader_sentiment"] == filter_sent]
        display_cols = [c for c in ["title_clean","date","vader_sentiment","vader_score"]
                        if c in filtered.columns]
        st.dataframe(
            filtered[display_cols].head(25).rename(
                columns={"title_clean":"Headline","vader_sentiment":"Sentiment",
                         "vader_score":"Score"}),
            use_container_width=True, hide_index=True, height=350
        )
    else:
        st.warning("Run notebook 07 first.")

# ── Footer ─────────────────────────────────────────────────────
st.sidebar.markdown("---")
st.sidebar.caption("Built by **Eve Otieno**")
st.sidebar.caption("NASA · FEWS NET · KNBS · WFP · KNA")
st.sidebar.caption("[GitHub](https://github.com/EveMichelle/kenya-smart-agriculture)")