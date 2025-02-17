import streamlit as st
from pages.home import home_page
from pages.initiative import initiative_page
from pages.beneficiaries import beneficiaries_page
from pages.regression_analysis import regression_analysis_page
from pages.etude_de_cas import etude_de_cas_page
from pages.data_processing import data_processing_page

# Définir les pages
home = st.Page(home_page, title="Home", icon="🏠")
initiative = st.Page(initiative_page, title="L'Initiative", icon="💡")
beneficiaries = st.Page(beneficiaries_page, title="Bénéficiaires", icon="🗺️")
etude_de_cas = st.Page(etude_de_cas_page, title="Étude de cas", icon="🔍")
regression_analysis = st.Page(regression_analysis_page, title="Analyse de régression", icon="📊")
data_processing = st.Page(data_processing_page, title="Traitement des données", icon="🛠️")



# Créer la barre de navigation
pg = st.navigation([home, initiative, beneficiaries, etude_de_cas, regression_analysis, data_processing])

# Configurer l'application
st.set_page_config(page_title="Projet Data Science", page_icon="📈")

# Exécuter la page sélectionnée
pg.run()
