import streamlit as st

def home_page():
    st.title("🏡 Home")
    
    # Ajouter le texte principal
    st.header("🌟 Introduction")
    st.markdown(
        """
        <p style="text-align: justify; font-size: 16px; line-height: 1.6;">
        Les petites villes jouent un rôle essentiel dans la structuration du territoire français, 
        particulièrement dans les zones rurales. Elles assurent une centralité indispensable pour 
        les habitants en leur offrant un accès aux services de santé, à l’éducation, aux équipements 
        sportifs et culturels, et aux commerces. Cependant, ces petites villes font face à des défis 
        multiples, notamment la désertification, le vieillissement de la population, et le déclin 
        économique. Depuis 2020, l’État a lancé le programme <strong>« Petites Villes de Demain » (PVD)</strong> 
        pour soutenir ces territoires et revitaliser leur cadre de vie.
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="text-align: justify; font-size: 16px; line-height: 1.6;">
        Malgré les efforts déployés, les petites villes françaises demeurent hétérogènes : certaines 
        connaissent un essor démographique, tandis que d’autres subissent un déclin marqué. Cette 
        situation soulève la question des facteurs qui influencent cette dynamique démographique. 
        Quels sont les éléments <strong>socio-économiques</strong>, <strong>environnementaux</strong> et 
        <strong>culturels</strong> qui favorisent ou freinent l’attractivité de ces territoires ? 
        Comprendre ces déterminants est crucial pour orienter les politiques publiques et optimiser 
        les actions du programme PVD.
        </p>
        """,
        unsafe_allow_html=True,
    )
    
    st.subheader("🎯 Objectifs du projet")
    st.markdown(
        """
        <ul style="font-size: 16px; line-height: 1.6;">
            <li>Identifier les facteurs qui influencent la <strong>dynamique démographique</strong> des petites villes.</li>
            <li>Comparer les spécificités de certaines communes, notamment celles intégrées au programme 
            <strong>PVD</strong>, avec d’autres ne bénéficiant pas de ce dispositif.</li>
            <li>Proposer des outils interactifs et des visualisations pour faciliter la compréhension des enjeux territoriaux.</li>
        </ul>
        """,
        unsafe_allow_html=True,
    )