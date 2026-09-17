import streamlit as st
import folium
from streamlit_folium import st_folium 
import pandas as pd 
from ingest import fetch_traffic_speed, fetch_incidents
from dotenv import load_dotenv
import os

load_dotenv()

MAP_TILE = os.getenv("MAP_URL", "cartodbpositron")
MAP_ATTR = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>'

st.set_page_config(page_title="Singapore Traffic Ops Portal", layout="wide")
st.title("Real-Time Traffic Network & Asset Dashboard")

if st.button("Refresh Data"):
    st.cache_data.clear()

#fetch live data
speed_df = fetch_traffic_speed()
incidents_df = fetch_incidents()

#Top KPI metrics panel
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(("Monitored Segments"), len(speed_df))
with col2: 
    slow_segments = len(speed_df[speed_df["SpeedBand"] <= 2]) if "SpeedBand" in speed_df.columns else 0
    st.metric("Congested Segments (<20km/h)", slow_segments)
with col3:
    st.metric("Active Road Incidents", len(incidents_df))

# map Rendering
st.subheader("Network Speed Map & Incidents")
m = folium.Map(
    location=[1.3521, 103.8198],
    zoom_start=12,
    tiles=MAP_TILE,
    attr=MAP_ATTR
)
if not speed_df.empty:
    for _, row in speed_df.dropna(subset=["StartLat", "StartLon", "EndLat", "EndLon"]).iterrows():
        speed_band = row.get("SpeedBand", 4)
        color = "red" if speed_band <=2 else "orange" if speed_band <= 4 else "green"

        folium.PolyLine(
            locations=[[row["StartLat"], row["StartLon"]], [row["EndLat"], row["EndLon"]]],
            color=color,
            weight=4,
            opacity=0.8,
            popup=f"Road: {row.get('RoadName', 'N/A')}<br>Speed Band: {speed_band}"
        ).add_to(m)

if not incidents_df.empty:
    for _, row in incidents_df.dropna(subset=["Latitude", "Longitude"]).iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=row.get("Message", "Incident"),
            icon=folium.Icon(color="darkred", icon="warning", prefix="fa")
        ).add_to(m)

st_folium(m, width=1300, height=500)