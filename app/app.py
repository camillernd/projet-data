import streamlit as st
from pages.home import home_page
from pages.initiative import initiative_page
from pages.beneficiaries import beneficiaries_page

from pages.regression_analysis import regression_analysis_page

# Définir les pages
home = st.Page(home_page, title="Home", icon="🏠")
initiative = st.Page(initiative_page, title="L'Initiative", icon="💡")
beneficiaries = st.Page(beneficiaries_page, title="Bénéficiaires", icon="🗺️")
regression_analysis = st.Page(regression_analysis_page, title="Analyse de régression", icon="📊")


# Créer la barre de navigation
pg = st.navigation([home, initiative, beneficiaries, regression_analysis])

# Configurer l'application
st.set_page_config(page_title="Projet Data Science", page_icon="📈")

# Exécuter la page sélectionnée
pg.run()
