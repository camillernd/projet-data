import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json

def influence_and_attractiveness_maps():
    st.title("Cartes des villes du programme")

    # Charger les fichiers
    aires_file = "./data/aires_attraction_enriched.csv"
    geojson_file = "./data/PVD.geojson"

    try:
        aires_data = pd.read_csv(aires_file, delimiter=";")
        with open(geojson_file, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
    except FileNotFoundError as e:
        st.error(f"Erreur : {e}")
        return

    # Créer une carte pour représenter l'échelle d'influence
    st.subheader("Carte des échelles d'influence (1-4)")
    influence_map = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="cartodbpositron")

    # Échelle de couleurs pour l'échelle d'influence
    influence_colors = {1: "#add8e6", 2: "#87CEEB", 3: "#FF7F7F", 4: "#FF4500"}

    def influence_style_function(feature):
        insee_com = feature["properties"]["insee_com"]
        row = aires_data[aires_data["Code"] == insee_com]
        if not row.empty:
            scale = row.iloc[0]["Echelle_influence"]
            return {"fillColor": influence_colors.get(scale, "#FFFFFF"), "color": "black", "weight": 1, "fillOpacity": 0.7}
        else:
            return {"fillColor": "#FFFFFF", "color": "black", "weight": 1, "fillOpacity": 0.3}

    folium.GeoJson(
        geojson_data,
        name="Echelle d'influence",
        style_function=influence_style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["lib_com"],
            aliases=["Commune :"],
            sticky=True,
        ),
    ).add_to(influence_map)
    st_folium(influence_map, width=1000, height=600)

    # Créer une carte pour les villes attractives et non attractives
    st.subheader("Carte des villes attractives (rouge) et non attractives (bleu)")
    attractiveness_map = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="cartodbpositron")

    def attractiveness_style_function(feature):
        insee_com = feature["properties"]["insee_com"]
        row = aires_data[aires_data["Code"] == insee_com]
        if not row.empty:
            is_attractive = row.iloc[0]["Dans_influence"]
            return {"fillColor": "red" if is_attractive else "blue", "color": "black", "weight": 1, "fillOpacity": 0.7}
        else:
            return {"fillColor": "#FFFFFF", "color": "black", "weight": 1, "fillOpacity": 0.3}

    folium.GeoJson(
        geojson_data,
        name="Attractivité",
        style_function=attractiveness_style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["lib_com"],
            aliases=["Commune :"],
            sticky=True,
        ),
    ).add_to(attractiveness_map)
    st_folium(attractiveness_map, width=1000, height=600)

