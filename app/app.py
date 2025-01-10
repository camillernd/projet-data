import streamlit as st
from pages.home import home_page
from pages.initiative import initiative_page
from pages.beneficiaries import beneficiaries_page

# Définir les pages avec des emojis Unicode
home = st.Page(home_page, title="Home", icon="🏠")
initiative = st.Page(initiative_page, title="L'Initiative", icon="💡")
beneficiaries = st.Page(beneficiaries_page, title="Bénéficiaires", icon="🗺️")  # Nouvelle page avec une icône de carte

# Créer la barre de navigation
pg = st.navigation([home, initiative, beneficiaries])

# Configurer l'application
st.set_page_config(page_title="Ma superbe application", page_icon="🚀")

# Exécuter la page sélectionnée
pg.run()
