import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

st.title("Dynamic Route Optimization and Emission Reduction")

# Input fields
start = st.text_input("Starting Point (latitude,longitude)", "37.7749,-122.4194")
end = st.text_input("Destination (latitude,longitude)", "37.8049,-122.2711")
vehicle_type = st.selectbox("Vehicle Type", ["Gasoline", "Diesel", "Electric"])
emission_factor = {"Gasoline": 120, "Diesel": 150, "Electric": 50}[vehicle_type]

if st.button("Optimize Route"):
    # Call Flask backends
    response = requests.post(
        "http://127.0.0.1:5000/optimize_route",
        json={"start": start, "end": end, "vehicle": {"emission_factor": emission_factor}}
    )
    data = response.json()

    # Display results
    st.write(f"Distance: {data['route']['distance'] / 1000} km")
    st.write(f"Emissions: {data['emissions']} g CO₂")
    st.write("Traffic Info:", data['traffic'])
    st.write("Weather Info:", data['weather'])

    # Visualize route
    map_data = folium.Map(location=[37.7749, -122.4194], zoom_start=12)
    folium.PolyLine(data['route']['geometry']['coordinates'], color="blue").add_to(map_data)
    folium_static(map_data)

    print("Test")