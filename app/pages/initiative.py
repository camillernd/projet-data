import streamlit as st

def initiative_page():
    st.title("🌟 L'Initiative")
    
    # Présentation
    st.header("✨ Présentation du Programme")
    st.markdown(
        """
        <p style="text-align: justify; font-size: 16px; line-height: 1.6;">
        <strong>Bienvenue sur la page de présentation du programme Petites Villes de Demain !</strong><br> 
        Ce programme innovant vise à accompagner les petites communes dans leur développement, 
        en renforçant leurs capacités à mener des projets structurants pour leurs territoires.
        </p>
        """,
        unsafe_allow_html=True,
    )
    
    # Objectifs
    st.subheader("🎯 Objectifs")
    st.markdown(
        """
        <ul style="font-size: 16px; line-height: 1.6;">
            <li><strong>Améliorer la qualité de vie</strong> des habitants des petites communes et des territoires alentours.</li>
            <li>Accompagner les collectivités dans <strong>des trajectoires dynamiques et engagées dans la transition écologique</strong>.</li>
            <li>Renforcer les moyens des élus pour <strong>bâtir et concrétiser leurs projets de territoire</strong>, jusqu’à 2026.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
    
    # Contexte et partenaires
    st.subheader("🤝 Contexte et Partenaires")
    st.markdown(
        """
        <p style="text-align: justify; font-size: 16px; line-height: 1.6;">
        Le programme a été lancé le <strong>1er octobre 2020</strong> par Jacqueline Gourault, alors Ministre de la Cohésion des territoires.<br>
        Il est piloté par l’<strong>Agence nationale de la cohésion des territoires (ANCT)</strong>, avec le soutien de :
        </p>
        <ul style="font-size: 16px; line-height: 1.6;">
            <li><strong>Les préfets de département</strong>, pour un pilotage au plus près du terrain.</li>
            <li><strong>Partenaires financiers</strong> : Banque des territoires, Anah, Cerema, Ademe.</li>
            <li><strong>Associations</strong> : Association des Petites Villes de France (APVF).</li>
        </ul>
        <p style="text-align: justify; font-size: 16px; line-height: 1.6;">
        Le programme s’inscrit également dans l’<strong>Agenda rural</strong> pour répondre aux besoins des collectivités.
        </p>
        """,
        unsafe_allow_html=True,
    )
    
    # Offre de services
    st.subheader("🛠️ Une Offre de Services Complète")
    st.markdown(
        """
        <ul style="font-size: 16px; line-height: 1.6;">
            <li>Une <strong>offre multithématique</strong>, visible via le portail Petites Villes de Demain sur Aides-territoires.</li>
            <li>Le <strong>financement du poste de chef de projet</strong> à hauteur de 75% jusqu’en 2026.</li>
            <li>Un <strong>Club des Petites Villes de Demain</strong> pour favoriser les échanges et la formation des acteurs.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )
    
    # Statistiques clés
    st.subheader("📊 Quelques Chiffres Clés")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Communes bénéficiaires", value="1 600+")
    with col2:
        st.metric(label="Budget alloué", value="3 Md€")
    
    # Appel à l'action avec redirection
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center;">
            <a href="https://agence-cohesion-territoires.gouv.fr/mode-demploi-697" target="_blank">
                <button style="background-color:#ff4b4b; color:white; padding:10px 20px; border:none; border-radius:5px; cursor:pointer;">
                    Découvrir le mode d'emploi du programme
                </button>
            </a>
        </div>
        """, 
        unsafe_allow_html=True,
    )