import pandas as pd
import streamlit as st
import plotly.express as px

def etude_de_cas_page():
    # Charger les fichiers
    data_file = "data/etude_2_cas.csv"  # Fichier contenant toutes les communes

    # Lire les données avec un encodage adapté
    data = pd.read_csv(data_file, delimiter=";", encoding="latin1", low_memory=False)

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

    def configure_pie_chart(fig):
        fig.update_traces(
            textinfo="value",
            textfont_size=16,
            marker=dict(line=dict(color='#000000', width=1))
        )
        fig.update_layout(
            legend_font_size=12,
            height=500,
            width=500,
        )
        return fig

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
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        age_pie_clement = configure_pie_chart(age_pie_clement)
        st.plotly_chart(age_pie_clement)

    with col2:
        age_data_grand_combe = la_grand_combe[existing_age_columns].iloc[0]
        age_pie_grand_combe = px.pie(
            names=existing_age_columns, 
            values=age_data_grand_combe,
            title="La Grand-Combe : Tranches d'âge",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        age_pie_grand_combe = configure_pie_chart(age_pie_grand_combe)
        st.plotly_chart(age_pie_grand_combe)

    st.header("Résumé des tranches d'âge")
    st.write("""
    Les tranches d'âge des deux communes révèlent des différences significatives. 
    À **Saint-Clément-de-Rivière**, on observe une proportion importante de personnes âgées entre 60 et 74 ans (26,8 %), indiquant une population vieillissante, typique des communes résidentielles attractives pour les retraités. 
    En revanche, **La Grand-Combe** présente une répartition plus équilibrée avec une part légèrement plus importante des moins de 15 ans et des jeunes adultes (15-29 ans), témoignant d'une population plus jeune et active.
    """)

    # Diagrammes circulaires pour les services
    st.header("Comparaison des services")
    st.write("Diagrammes circulaires représentant les services des deux communes.")

    # Saint-Clément-de-Rivière : Services
    service_data_clement = saint_clement[existing_service_columns].iloc[0]
    service_pie_clement = px.pie(
        names=existing_service_columns, 
        values=service_data_clement,
        title="Saint-Clément-de-Rivière : Services",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    service_pie_clement = configure_pie_chart(service_pie_clement)
    st.plotly_chart(service_pie_clement)

    # La Grand-Combe : Services
    service_data_grand_combe = la_grand_combe[existing_service_columns].iloc[0]
    service_pie_grand_combe = px.pie(
        names=existing_service_columns, 
        values=service_data_grand_combe,
        title="La Grand-Combe : Services",
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    service_pie_grand_combe = configure_pie_chart(service_pie_grand_combe)
    st.plotly_chart(service_pie_grand_combe)

    st.header("Résumé des services")
    st.write("""
    Les services disponibles diffèrent fortement entre les deux communes. 
    **Saint-Clément-de-Rivière** bénéficie d’un accès plus large aux services, avec un nombre supérieur de dentistes (8 contre 2) et de médecins généralistes (7 contre 3), reflétant une infrastructure médicale bien développée. De plus, cette commune dispose de 4 boulangeries et pâtisseries contre 3 à La Grand-Combe, renforçant son caractère attractif pour les familles. Cependant, **La Grand-Combe** se distingue par un plus grand nombre d’écoles primaires (5 contre 3), un facteur essentiel pour les familles avec enfants. Ces différences mettent en évidence une disparité dans la qualité et l’étendue des services offerts dans ces deux communes.
    """)

    # Comparaison des métriques clés
    st.header("Comparaison des métriques clés")
    st.write("Diagrammes comparant les métriques clés des deux communes.")

    for column in existing_numeric_columns:
        bar_chart = px.bar(
            comparison_data,
            x="Commune",
            y=column,
            labels={"Commune": "Commune", column: column},
            title=f"Comparaison des communes pour {column}",
            text_auto=True,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        bar_chart.update_traces(width=0.4)
        st.plotly_chart(bar_chart)

    st.header("Résumé des métriques clés")
    st.write("""
    Les métriques clés mettent en évidence des écarts notables. La **médiane du revenu disponible** est nettement plus élevée à **Saint-Clément-de-Rivière** (34,31k€ contre 15,18k€ à La Grand-Combe), reflétant un écart socio-économique significatif entre les deux communes. En termes d'équipements sportifs, bien que Saint-Clément-de-Rivière ait un nombre légèrement plus élevé (19 contre 16), le **taux d'équipements sportifs pour 1 000 habitants** reste relativement proche (3,8 pour Saint-Clément-de-Rivière et 3,2 pour La Grand-Combe). Cela souligne que, malgré un nombre total moindre, La Grand-Combe maintient une densité d’équipements suffisante pour sa population.
    """)

    # Observations finales sur le programme PVD
    st.header("Observations finales")
    st.write("""
    Il est intéressant de noter que **La Grand-Combe** fait partie du programme PVD (Petites Villes de Demain), contrairement à **Saint-Clément-de-Rivière**. 
    Cela peut s'expliquer par les critères de sélection du programme, qui priorisent les communes présentant des besoins socio-économiques importants et un potentiel de revitalisation. 
    Bien que Saint-Clément-de-Rivière dispose d'infrastructures de qualité et d'une population aisée, les défis de La Grand-Combe, notamment liés à son passé industriel et à son niveau de revenu médian plus faible, justifient son inclusion dans le programme. 
    Cette analyse met en évidence la nécessité d'adapter les politiques publiques aux spécificités locales pour répondre efficacement aux besoins des différentes communes.
    """)
