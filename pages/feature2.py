import folium
import streamlit as st
from streamlit_folium import st_folium

# Create Map Object
m = folium.Map(location=[37.3352, -121.8806], zoom_start=13)

#Display in Streamlit
st.title("REPORTED POTHOLES IN YOUR AREA")
st_folium(m, width=725)