import streamlit as st
import pydeck as pdk
# CREATING FUNCTION FOR MAPS


def draw_map(data, lat, lon, zoom):
    st.write(pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": lat,
            "longitude": lon,
            "zoom": zoom,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position=["lon", "lat"],
                radius=10000,
                elevation_scale=40,
                elevation_range=[0, 10000],
                pickable=True,
                extruded=True,
            ),
        ]
    ))