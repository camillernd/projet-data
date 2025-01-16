import streamlit as st

def data_processing_page():
    st.title("🛠️ Méthodologie de traitement des données")

    # Introduction au défi data.gouv
    st.header("Défi Data Gouv")
    st.markdown(
        """
        La communauté open data et l’équipe de data.gouv.fr proposent aux participants de développer (ou de mettre à contribution) 
        leurs compétences en réalisant des projets à partir de données ouvertes. Pour chaque défi sont formulés une problématique à résoudre, 
        des idées de réalisations possibles et une sélection de données ouvertes pour y parvenir.

        Certains de ces défis ont notamment été conçus pour être réalisés par des étudiantes et des étudiants dans le cadre de l’Open Data University.
        L’Open Data University est un programme porté par l’association Latitudes qui propose aux établissements de formation à la data de mobiliser leurs élèves 
        sur des challenges qui répondent à des enjeux sociaux et environnementaux grâce à la réutilisation de données ouvertes.
        """
    )

    # Illustration de la répartition des tâches
    st.header("Répartition des tâches")
    st.markdown(
        """
        Pour mener à bien le traitement des données, nous nous sommes répartis les tâches. 
        Chaque membre de l'équipe a pris en charge un ou plusieurs ensembles de données pour en assurer une analyse approfondie.
        """
    )
    st.image("assets/tableau_repartition.png", caption="Répartition des tâches dans l'équipe")

    # Description des données
    st.header("Description des données")
    st.markdown(
        """
        Chaque membre a rempli un tableau de description des données afin de documenter les acteurs impliqués, la thématique abordée, 
        les populations concernées, la temporalité et bien plus encore. Cette étape garantit une compréhension partagée et précise 
        des données analysées.
        """
    )
    st.image("assets/tableau_bilan.png", caption="Tableau de description des données")

    # Guide des fichiers
    st.header("Guide des fichiers")
    st.markdown(
        """
        En complément du tableau de description, un guide a été élaboré pour chaque fichier de données. 
        Ce guide sert de dictionnaire, expliquant le contenu des colonnes et leur signification. 
        Il s'agit d'une ressource clé pour assurer une utilisation cohérente et efficace des données.
        """
    )
    st.image("assets/guide.png", caption="Guide des fichiers de données")

    # Filtrage des données
    st.header("Filtrage des données")
    st.markdown(
        """
        La personne responsable du filtrage utilise le guide pour identifier les variables pertinentes. 
        Si nécessaire, des données supplémentaires provenant de sources externes, comme l'Observatoire des Territoires, sont intégrées. 
        Cette étape s'appuie sur des scripts Python exploitant des bibliothèques comme **pandas** pour faciliter le traitement.
        """
    )
    st.image("assets/commandes.png", caption="Commandes Python utilisées pour le filtrage des données")
