import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Stubble Burning Risk", layout="wide")
st.title("🔥 Stubble Burning Risk Dashboard")

df = pd.read_csv("dashboard_data.csv")

if df.empty:
    st.error("❌ DataFrame is empty.")
    st.stop()

st.write("✅ CSV Preview", df.head())
st.write("✅ Total Rows:", df.shape[0])

st.sidebar.header("🔎 Filters")
threshold = st.sidebar.slider("Risk Threshold (0.0 - 1.0)", 0.0, 1.0, 0.7)
st.write("✅ Threshold:", threshold)

high_risk = df[df['predicted_probability'] > threshold]

st.subheader("🗺️ High-Risk Locations Map")

# FIXED center to India region (Punjab/Haryana)
m = folium.Map(location=[29.5, 76.5], zoom_start=6)

for _, row in df.iterrows():
    color = "red" if row['predicted_probability'] > threshold else "blue"
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=4,
        color=color,
        fill=True,
        fill_opacity=0.7,
        tooltip=f"🔥 Risk: {row['predicted_probability']:.2f}, Event: {row['actual_event']}"
    ).add_to(m)

st_folium(m, width=1200)

st.subheader("📊 Summary")
col1, col2 = st.columns(2)
col1.metric("High-Risk Locations", len(high_risk))
col2.metric("Total Events", df['actual_event'].sum())

with st.expander("📋 Show Raw Data"):
    st.dataframe(df)
