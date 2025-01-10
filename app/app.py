import streamlit as st
from pages.home import home_page
from pages.initiative import initiative_page
from pages.beneficiaries import beneficiaries_page
from pages.festivals_map import festivals_map_page  # Nouvelle page

# Définir les pages
home = st.Page(home_page, title="Home", icon="🏠")
initiative = st.Page(initiative_page, title="L'Initiative", icon="💡")
beneficiaries = st.Page(beneficiaries_page, title="Bénéficiaires", icon="🗺️")
festivals_map = st.Page(festivals_map_page, title="Festivals et Petites Villes", icon="🎭")  # Nouvelle page

# Créer la barre de navigation
pg = st.navigation([home, initiative, beneficiaries, festivals_map])

# Configurer l'application
st.set_page_config(page_title="Ma superbe application", page_icon="🚀")

# Exécuter la page sélectionnée
pg.run()
