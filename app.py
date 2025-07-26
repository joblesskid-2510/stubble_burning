import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Basic page setup
st.set_page_config(page_title="Stubble Burning Risk", layout="wide")
st.title("🔥 Stubble Burning Risk Dashboard")

# Load data
try:
    df = pd.read_csv("dashboard_data.csv", dtype={"latitude": float, "longitude": float})
except Exception as e:
    st.error(f"❌ Failed to load CSV: {e}")
    st.stop()

# Check if DataFrame is valid
if df.empty:
    st.error("❌ DataFrame is empty.")
    st.stop()

if df[['latitude', 'longitude']].isnull().any().any():
    st.error("❌ Latitude or Longitude contains missing values!")
    st.dataframe(df[['latitude', 'longitude']].isnull().sum())
    st.stop()

# Preview CSV
st.write("✅ CSV Preview", df.head())
st.write("✅ Total Rows:", df.shape[0])

# Sidebar threshold selector
st.sidebar.header("🔎 Filters")
threshold = st.sidebar.slider("Risk Threshold (0.0 - 1.0)", 0.0, 1.0, 0.7)
st.write("✅ Threshold:", threshold)

# Filter high-risk locations
high_risk = df[df['predicted_probability'] > threshold]

# Map Section
st.subheader("🗺️ High-Risk Locations Map")

m = folium.Map(location=[29.5, 76.5], zoom_start=6)

if high_risk.empty:
    folium.Marker(
        location=[29.5, 76.5],
        popup="⚠️ No high-risk data points found for this threshold.",
        icon=folium.Icon(color="gray")
    ).add_to(m)
else:
    for _, row in high_risk.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=4,
            color="red",
            fill=True,
            fill_opacity=0.7,
            tooltip=f"🔥 Risk: {row['predicted_probability']:.2f}, Event: {row['actual_event']}"
        ).add_to(m)

st_folium(m, width=1200)

# Summary section
st.subheader("📊 Summary")
col1, col2 = st.columns(2)
col1.metric("High-Risk Locations", len(high_risk))
col2.metric("Total Events", int(df['actual_event'].sum()))

# Raw data preview
with st.expander("📋 Show Raw Data"):
    st.dataframe(df)
