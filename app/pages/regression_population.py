import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt
from numpy import polyfit

def regression_population_page():
    st.title("Régression Linéaire : Facteurs culturels et sportifs vs Attractivité démographique")

    # Charger les fichiers CSV
    facteurs_file = "./data/facteurs_cult.csv"
    taux_evol_file = "./data/taux_evol.csv"

    try:
        facteurs_data = pd.read_csv(facteurs_file, delimiter=";", decimal='.')
        taux_evol_data = pd.read_csv(taux_evol_file, delimiter=";", decimal='.')
    except FileNotFoundError:
        st.error("Les fichiers nécessaires n'ont pas été trouvés. Veuillez vérifier les chemins.")
        return

    # Remplacer les valeurs 'N/A - résultat non disponible' par NaN pour les traiter comme manquantes
    facteurs_data = facteurs_data.replace('N/A - résultat non disponible', pd.NA)
    taux_evol_data = taux_evol_data.replace('N/A - résultat non disponible', pd.NA)

    # Vérifier la présence de la colonne 'Code' dans les deux fichiers
    if "Code" not in facteurs_data.columns or "Code" not in taux_evol_data.columns:
        st.error("La colonne 'Code' est manquante dans l'un des fichiers.")
        st.write("Colonnes disponibles dans facteurs_cult.csv :", facteurs_data.columns.tolist())
        st.write("Colonnes disponibles dans taux_evol.csv :", taux_evol_data.columns.tolist())
        return

    # Fusionner les données sur la colonne 'Code'
    data = pd.merge(facteurs_data, taux_evol_data, on="Code")

    # Sélectionner les colonnes pertinentes
    variables_explicatives = [
        "Taux d'équipements socio-culturels pour 10 000 habitants 2023",
        "Taux d'équipements sportifs pour 1 000 habitants 2023",
        "Nombre d'équipements sportifs 2023",
        "Nombre d'équipements socio-culturels 2023"
    ]
    y = data["Taux d'évolution annuel de la population 2015-2021"]

    # Convertir les colonnes en numériques
    data[variables_explicatives] = data[variables_explicatives].apply(pd.to_numeric, errors='coerce')
    y = pd.to_numeric(y, errors='coerce')

    # Retirer les lignes où toutes les variables explicatives sont nulles ou égales à zéro
    data = data[~(data[variables_explicatives].fillna(0).sum(axis=1) == 0)]

    # Filtrer y pour correspondre à data après nettoyage
    y = y[data.index]

    # Vérifier les données
    st.write("### Aperçu des données après nettoyage :")
    st.write(data.head())

    # Créer des scatter plots avec régression pour chaque variable explicative
    for variable in variables_explicatives[:3]:  # Ne prendre que les 3 premières pour les graphes
        fig, ax = plt.subplots()
        valid_indices = data[variable].notna() & y.notna()
        ax.scatter(data[variable][valid_indices], y[valid_indices], alpha=0.7, edgecolors="b", label="Données")

        # Calculer la régression linéaire
        slope, intercept = polyfit(data[variable][valid_indices], y[valid_indices], 1)
        ax.plot(data[variable], slope * data[variable] + intercept, color="red", label="Régression linéaire")

        # Calculer R²
        model = LinearRegression()
        X = data[variable][valid_indices].values.reshape(-1, 1)
        y_filtered = y[valid_indices]
        model.fit(X, y_filtered)
        y_pred = model.predict(X)
        r2 = r2_score(y_filtered, y_pred)

        # Ajouter les titres et légendes
        ax.set_xlabel(variable)
        ax.set_ylabel("Taux d'évolution annuel de la population 2015-2021")
        ax.set_title(f"Relation entre {variable} et l'attractivité démographique (R² = {r2:.4f})")
        ax.legend()
        st.pyplot(fig)
