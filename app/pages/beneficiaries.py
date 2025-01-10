import streamlit as st
import folium
from streamlit_folium import st_folium
import json

def beneficiaries_page():
    st.title("Bénéficiaires")
    st.write("Explorez la carte des communes bénéficiaires.")

    # Charger le fichier GeoJSON
    geojson_file = "./data/PVD.geojson"
    try:
        with open(geojson_file, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
    except FileNotFoundError:
        st.error(f"Le fichier {geojson_file} est introuvable. Vérifiez son emplacement.")
        return

    # Créer une carte Folium
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="cartodbpositron")

    # Ajouter les données GeoJSON avec les noms des communes (lib_com)
    folium.GeoJson(
        geojson_data,
        name="Communes",
        tooltip=folium.GeoJsonTooltip(
            fields=["lib_com"],  # Champ contenant le nom de la commune
            aliases=["Nom de la commune :"],  # Texte affiché dans le tooltip
            localize=True,
            sticky=True,
        ),
    ).add_to(m)

    # Ajouter un contrôle pour les couches
    folium.LayerControl().add_to(m)

    # Afficher la carte dans Streamlit
    st_folium(m, width=1000, height=600)
