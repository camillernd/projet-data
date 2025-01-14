import pandas as pd
import streamlit as st
import plotly.express as px

# Charger les fichiers
filtered_data_file = "filtered_data.csv"  # Fichier CSV contenant les revenus
pvd_file = "PVD.csv"  # Fichier CSV contenant les codes des villes PVD

# Lire et nettoyer les données
filtered_data = pd.read_csv(filtered_data_file, delimiter=";", encoding="utf-8", skiprows=1)
filtered_data.columns = ["Code", "Libellé", "Médiane du revenu disponible par UC 2020"]
pvd_data = pd.read_csv(pvd_file, delimiter=";", encoding="latin1")

# Nettoyage et préparation des données
pvd_codes = pvd_data["insee_com"].astype(str)
filtered_data["Code"] = filtered_data["Code"].astype(str)
filtered_data["PVD"] = filtered_data["Code"].isin(pvd_codes)

# Identifier les villes PVD et non-PVD
pvd_cities = filtered_data[filtered_data["Code"].isin(pvd_codes)]
non_pvd_cities = filtered_data[~filtered_data["Code"].isin(pvd_codes)]

# Calculer les moyennes
mean_pvd = pvd_cities["Médiane du revenu disponible par UC 2020"].astype(float).mean()
mean_non_pvd = non_pvd_cities["Médiane du revenu disponible par UC 2020"].astype(float).mean()

# Filtrage par département
filtered_data["Département"] = filtered_data["Code"].str[:2]
selected_department = st.sidebar.selectbox("Choisir un département (code INSEE)", ["Tous"] + sorted(filtered_data["Département"].unique()))

if selected_department != "Tous":
    filtered_data = filtered_data[filtered_data["Département"] == selected_department]
    pvd_cities = filtered_data[filtered_data["Code"].isin(pvd_codes)]
    non_pvd_cities = filtered_data[~filtered_data["Code"].isin(pvd_codes)]
    mean_pvd = pvd_cities["Médiane du revenu disponible par UC 2020"].astype(float).mean()
    mean_non_pvd = non_pvd_cities["Médiane du revenu disponible par UC 2020"].astype(float).mean()

# Filtrage par tranche de revenus
st.sidebar.write("### Filtrer par tranche de revenus")
min_revenue, max_revenue = st.sidebar.slider(
    "Sélectionner une tranche de revenus", 
    min_value=float(filtered_data["Médiane du revenu disponible par UC 2020"].min()),
    max_value=float(filtered_data["Médiane du revenu disponible par UC 2020"].max()),
    value=(float(filtered_data["Médiane du revenu disponible par UC 2020"].min()),
           float(filtered_data["Médiane du revenu disponible par UC 2020"].max()))
)
filtered_data = filtered_data[
    (filtered_data["Médiane du revenu disponible par UC 2020"].astype(float) >= min_revenue) &
    (filtered_data["Médiane du revenu disponible par UC 2020"].astype(float) <= max_revenue)
]

# Comparer des départements spécifiques
st.sidebar.write("### Comparer deux départements")
dep1 = st.sidebar.selectbox("Choisir le premier département", sorted(filtered_data["Département"].unique()))
dep2 = st.sidebar.selectbox("Choisir le second département", sorted(filtered_data["Département"].unique()))
if dep1 and dep2:
    dep1_data = filtered_data[filtered_data["Département"] == dep1]
    dep2_data = filtered_data[filtered_data["Département"] == dep2]
    compare_chart = px.scatter(
        pd.concat([dep1_data, dep2_data]),
        x="Code",
        y="Médiane du revenu disponible par UC 2020",
        color="Département",
        title=f"Comparaison des départements {dep1} et {dep2}",
        labels={"Code": "Code Commune", "Médiane du revenu disponible par UC 2020": "Revenu Médian"}
    )
    st.plotly_chart(compare_chart)

# Focus sur les extrêmes
st.write("### Focus sur les extrêmes")
top_n = st.slider("Nombre de communes à afficher", 1, 50, 10)
lowest_revenues = filtered_data.nsmallest(top_n, "Médiane du revenu disponible par UC 2020")
highest_revenues = filtered_data.nlargest(top_n, "Médiane du revenu disponible par UC 2020")
st.write("#### Communes avec les revenus les plus bas")
st.dataframe(lowest_revenues)
st.write("#### Communes avec les revenus les plus élevés")
st.dataframe(highest_revenues)

# Création du schéma avec Streamlit
st.title("Comparaison des revenus médians des villes PVD et non-PVD")

# Diagramme 1 : Bar chart classique
st.write("### Diagramme 1 : Bar chart classique")
st.bar_chart({
    "Villes PVD": [mean_pvd],
    "Villes non-PVD": [mean_non_pvd]
})

# Diagramme 2 : Pie chart avec Plotly
st.write("### Diagramme 2 : Répartition en pourcentage")
pie_data = pd.DataFrame({
    "Catégorie": ["Villes PVD", "Villes non-PVD"],
    "Moyenne": [mean_pvd, mean_non_pvd]
})
pie_chart = px.pie(pie_data, names="Catégorie", values="Moyenne", title="Répartition des revenus médians")
st.plotly_chart(pie_chart)

# Diagramme 3 : Box plot
st.write("### Diagramme 3 : Distribution des revenus médians")
box_data = pd.DataFrame({
    "Catégorie": ["Villes PVD"] * len(pvd_cities) + ["Villes non-PVD"] * len(non_pvd_cities),
    "Revenu": pd.concat([
        pvd_cities["Médiane du revenu disponible par UC 2020"].astype(float),
        non_pvd_cities["Médiane du revenu disponible par UC 2020"].astype(float)
    ])
})
box_chart = px.box(box_data, x="Catégorie", y="Revenu", title="Distribution des revenus médians")
st.plotly_chart(box_chart)

# Diagramme 4 : Scatter plot (dispersion)
st.write("### Diagramme 4 : Dispersion des revenus médians")
scatter_chart = px.scatter(
    filtered_data,
    x="Code",
    y="Médiane du revenu disponible par UC 2020",
    title="Dispersion des revenus médians",
    labels={"Code": "Code Commune", "Médiane du revenu disponible par UC 2020": "Revenu Médian"}
)
st.plotly_chart(scatter_chart)

# Diagramme 5 : Scatter plot coloré par appartenance au PVD
st.write("### Diagramme 5 : Dispersion colorée par appartenance au PVD")
scatter_chart_colored = px.scatter(
    filtered_data,
    x="Code",
    y="Médiane du revenu disponible par UC 2020",
    color="PVD",
    title="Dispersion des revenus médians (PVD vs Non-PVD)",
    labels={"Code": "Code Commune", "Médiane du revenu disponible par UC 2020": "Revenu Médian", "PVD": "Appartenance PVD"}
)
st.plotly_chart(scatter_chart_colored)
