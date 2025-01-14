import pandas as pd
import streamlit as st
import plotly.express as px

# Charger les fichiers
data_file = "etude_2_cas.csv"  # Fichier contenant toutes les communes

# Lire les données avec un encodage adapté
data = pd.read_csv(data_file, delimiter=";", encoding="latin1")

# Renommer les colonnes pour corriger les caractères mal encodés
data.rename(columns={
    "Libell�": "Libellé",
    "Médiane du revenu disponible par UC 2020": "Médiane du revenu disponible par UC 2020",
    "Nombre d'équipements sportifs 2023": "Nombre d'équipements sportifs 2023",
    "Taux d'équipements sportifs pour 1 000 habitants 2023": "Taux d'équipements sportifs pour 1 000 habitants 2023",
    "Nombre de supérettes et épieries": "Nombre de supérettes et épiceries",
    "Nombre boulangeries et patisseries": "Nombre boulangeries et pâtisseries",
    "Nombre écoles primaires maternelles élémentaires": "Nombre écoles primaires maternelles élémentaires",
    "Nombre grandes surfaces 2023": "Nombre grandes surfaces 2023"
}, inplace=True)

# Sélectionner les deux communes
saint_clement = data[data["Code"] == "34247"]
la_grand_combe = data[data["Code"] == "30132"]

# Combiner les deux communes pour comparaison
comparison_data = pd.concat([saint_clement, la_grand_combe])
comparison_data["Commune"] = comparison_data["Libellé"]

# Assurer que les colonnes numériques sont bien au format float
age_columns = [
    "Part des 60-74 ans 2021", 
    "Part des moins de 15 ans 2021", 
    "Part des 15-29 ans 2021", 
    "Part des 30-44 ans 2021", 
    "Part des 45-59 ans 2021"
]
service_columns = [
    "Nombre grandes surfaces 2023", 
    "Nombre de supérettes et épiceries", 
    "Nombre boulangeries et pâtisseries", 
    "Nombre écoles primaires maternelles élémentaires", 
    "Nombre de collèges", 
    "Nombre de lycées", 
    "Nombre de médecins généralistes", 
    "Nombre de dentistes", 
    "Nombre de pharmacies"
]
numeric_columns = [
    "Médiane du revenu disponible par UC 2020", 
    "Nombre d'équipements sportifs 2023", 
    "Taux d'équipements sportifs pour 1 000 habitants 2023"
]

existing_age_columns = [col for col in age_columns if col in comparison_data.columns]
existing_service_columns = [col for col in service_columns if col in comparison_data.columns]
existing_numeric_columns = [col for col in numeric_columns if col in comparison_data.columns]

for col in existing_numeric_columns + existing_age_columns + existing_service_columns:
    comparison_data[col] = pd.to_numeric(comparison_data[col], errors='coerce')

# Configurer l'interface Streamlit
st.title("Comparaison entre Saint-Clément-de-Rivière et La Grand-Combe")

# Diagrammes circulaires pour les tranches d'âge
st.header("Comparaison des tranches d'âge")
st.write("Diagrammes circulaires représentant les tranches d'âge des deux communes.")

col1, col2 = st.columns(2)
with col1:
    age_data_clement = saint_clement[existing_age_columns].iloc[0]
    age_pie_clement = px.pie(
        names=existing_age_columns, 
        values=age_data_clement,
        title="Saint-Clément-de-Rivière : Tranches d'âge",
        labels={"value": "Proportion (%)", "names": "Tranches d'âge"}
    )
    age_pie_clement.update_layout(legend_font_size=7)
    st.plotly_chart(age_pie_clement)

with col2:
    age_data_grand_combe = la_grand_combe[existing_age_columns].iloc[0]
    age_pie_grand_combe = px.pie(
        names=existing_age_columns, 
        values=age_data_grand_combe,
        title="La Grand-Combe : Tranches d'âge",
        labels={"value": "Proportion (%)", "names": "Tranches d'âge"}
    )
    age_pie_grand_combe.update_layout(legend_font_size=7)
    st.plotly_chart(age_pie_grand_combe)

# Diagrammes circulaires pour les services
st.header("Comparaison des services")
st.write("Diagrammes circulaires représentant les services des deux communes.")

col1, col2 = st.columns(2)
with col1:
    service_data_clement = saint_clement[existing_service_columns].iloc[0]
    service_pie_clement = px.pie(
        names=existing_service_columns, 
        values=service_data_clement,
        title="Saint-Clément-de-Rivière : Services",
        labels={"value": "Nombre", "names": "Types de services"}
    )
    service_pie_clement.update_layout(legend_font_size=7)
    st.plotly_chart(service_pie_clement)

with col2:
    service_data_grand_combe = la_grand_combe[existing_service_columns].iloc[0]
    service_pie_grand_combe = px.pie(
        names=existing_service_columns, 
        values=service_data_grand_combe,
        title="La Grand-Combe : Services",
        labels={"value": "Nombre", "names": "Types de services"}
    )
    service_pie_grand_combe.update_layout(legend_font_size=7)
    st.plotly_chart(service_pie_grand_combe)

# Comparaison des métriques clés
st.header("Comparaison des métriques clés")
st.write("Diagrammes comparant les métriques clés des deux communes.")

for column in existing_numeric_columns:
    bar_chart = px.bar(
        comparison_data,
        x="Commune",
        y=column,
        labels={"Commune": "Commune", column: column},
        title=f"Comparaison des communes pour {column}"
    )
    st.plotly_chart(bar_chart)

# Résumé des observations
st.header("Résumé des observations")
st.write("Utilisez les graphiques ci-dessus pour analyser les différences entre les deux communes.")
