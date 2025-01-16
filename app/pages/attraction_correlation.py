import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def attraction_correlation_page():
    st.title("Analyse de l'attractivité démographique par proximité des grandes villes")

    # Charger les fichiers CSV
    enriched_file = "./data/aires_attraction_enriched.csv"
    taux_evol_file = "./data/taux_evol_filtered.csv"

    try:
        enriched_data = pd.read_csv(enriched_file, delimiter=";")
        taux_evol_data = pd.read_csv(taux_evol_file, delimiter=";")
    except FileNotFoundError as e:
        st.error(f"Erreur : {e}")
        return

    # Fusionner les fichiers sur le Code
    data = pd.merge(enriched_data, taux_evol_data, left_on="Code", right_on="Code", how="inner")

    # Convertir la colonne "Taux d'évolution annuel de la population" en numérique
    data["Taux d'évolution annuel de la population 2015-2021"] = pd.to_numeric(
        data["Taux d'évolution annuel de la population 2015-2021"], errors="coerce"
    )

    # Supprimer les lignes avec des valeurs NaN
    data = data.dropna(subset=["Taux d'évolution annuel de la population 2015-2021", "Echelle_influence"])

    # Ajouter une colonne pour indiquer si la ville est attractive ou non (taux > 0)
    data["Attractive"] = data["Taux d'évolution annuel de la population 2015-2021"] > 0

    # Séparer les données attractives et non attractives
    attractive_data = data[data["Attractive"] == True]
    non_attractive_data = data[data["Attractive"] == False]

    # Créer un dictionnaire pour la légende des échelles
    echelle_legende = {
        4: "T45_20 : Commune appartenant à la couronne d'un pôle de 700 000 habitants ou plus",
        3: "T02_20 : Commune appartenant à la couronne d'un pôle entre 50 000 et 200 000 habitants",
        2: "T01_10 : Commune appartenant à un pôle de moins de 50 000 habitants",
        1: "T00_30 : Commune isolée hors influence des pôles"
    }

    # Fonction pour créer un camembert
    def create_pie_chart(data, title):
        counts = data["Echelle_influence"].value_counts().sort_index()
        labels = [echelle_legende[key] for key in counts.index]
        fig, ax = plt.subplots()
        ax.pie(
            counts,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 10}
        )
        ax.set_title(title)
        st.pyplot(fig)

    # Camembert pour les villes attractives
    st.subheader("Villes attractives (Taux d'évolution > 0)")
    create_pie_chart(attractive_data, "Répartition des échelles d'influence pour les villes attractives")

    # Camembert pour les villes non attractives
    st.subheader("Villes non attractives (Taux d'évolution ≤ 0)")
    create_pie_chart(non_attractive_data, "Répartition des échelles d'influence pour les villes non attractives")

    # Légende des échelles
    st.subheader("Légende des échelles d'influence")
    for key, value in echelle_legende.items():
        st.write(f"**{key}** : {value}")
