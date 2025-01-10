import streamlit as st
import folium
from streamlit_folium import st_folium
import json

def beneficiaries_page():
    st.title("Bénéficiaires")
    st.write("Explorez la carte des communes bénéficiaires avec des couleurs par région.")

    # Charger le fichier GeoJSON
    geojson_file = "./data/PVD.geojson"
    try:
        with open(geojson_file, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        st.error(f"Le fichier {geojson_file} est introuvable. Vérifiez son emplacement.")
        return

    # Définir une palette de couleurs pour les régions
    region_colors = {
        "Auvergne-Rhône-Alpes": "blue",
        "Bourgogne-Franche-Comté": "green",
        "Bretagne": "purple",
        "Centre-Val de Loire": "orange",
        "Corse": "red",
        "Grand Est": "cyan",
        "Hauts-de-France": "pink",
        "Île-de-France": "yellow",
        "Normandie": "brown",
        "Nouvelle-Aquitaine": "darkgreen",
        "Occitanie": "darkblue",
        "Pays de la Loire": "gold",
        "Provence-Alpes-Côte d'Azur": "darkred",
    }

    # Créer une fonction de style pour attribuer des couleurs par région
    def style_function(feature):
        region_name = feature["properties"]["reg_name"]  # Nom de la région
        return {
            "fillColor": region_colors.get(region_name, "gray"),  # Couleur par région
            "color": "black",  # Bordure noire
            "weight": 1,  # Épaisseur des bordures
            "fillOpacity": 0.6,  # Opacité des couleurs
        }

    # Créer une carte Folium
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="cartodbpositron")

    # Ajouter les données GeoJSON avec le style par région
    folium.GeoJson(
        geojson_data,
        name="Communes",
        style_function=style_function,
        tooltip=folium.GeoJsonTooltip(
            fields=["lib_com", "reg_name"],  # Nom de la commune et région
            aliases=["Nom de la commune :", "Région :"],  # Alias pour le tooltip
            localize=True,
            sticky=True,
        ),
    ).add_to(m)

    # Ajouter un contrôle pour les couches
    folium.LayerControl().add_to(m)

    # Afficher la carte dans Streamlit
    st_folium(m, width=1000, height=600)
