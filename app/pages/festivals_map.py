import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json

def festivals_map_page():
    st.title("Carte des Festivals et des Petites Villes")
    st.write("Cette carte affiche en rouge les petites villes ayant accueilli un festival, et en bleu les autres.")

    # Charger les données GeoJSON (petites villes)
    geojson_file = "./data/PVD.geojson"
    with open(geojson_file, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # Charger les données des festivals
    festivals_file = "./data/festivals.csv"
    festivals_data = pd.read_csv(festivals_file, delimiter=";", encoding="utf-8-sig")

    
    festivals_data.columns = festivals_data.columns.str.strip()  # Supprime les espaces autour des noms
    festivals_data.columns = festivals_data.columns.str.lower()  # Convertit tous les noms en minuscules


    # Identifier les codes INSEE des communes ayant accueilli un festival
    festival_communes = festivals_data["code insee commune"].unique()

    
    # Créer une fonction de style pour colorer les villes
    def style_function(feature):
        insee_code = feature["properties"]["insee_com"]  # Code INSEE dans le GeoJSON
        if insee_code in festival_communes:
            return {"fillColor": "red", "color": "black", "weight": 1, "fillOpacity": 0.6}
        else:
            return {"fillColor": "blue", "color": "black", "weight": 1, "fillOpacity": 0.6}

    # Créer une carte Folium
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="cartodbpositron")

    # Ajouter les données GeoJSON avec le style
    folium.GeoJson(
        geojson_data,
        name="Petites Villes",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["lib_com"],  # Nom des communes
            aliases=["Nom de la commune :"],  # Texte affiché
            localize=True,
            sticky=True,
        ),
    ).add_to(m)

    # Ajouter un contrôle pour les couches
    folium.LayerControl().add_to(m)

    # Afficher la carte dans Streamlit
    st_folium(m, width=1000, height=600)
