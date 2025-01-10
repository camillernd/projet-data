import streamlit as st
from pages.home import home_page
from pages.initiative import initiative_page

# Définir les pages avec des emojis Unicode
home = st.Page(home_page, title="Home", icon="🏠")  # Appel de la fonction définie dans home.py
initiative = st.Page(initiative_page, title="L'Initiative", icon="💡")  # Appel de la fonction définie dans initiative.py

# Créer la barre de navigation
pg = st.navigation([home, initiative])

# Configurer l'application
st.set_page_config(page_title="Ma superbe application", page_icon="🚀")  # Emoji Unicode pour la fusée

# Exécuter la page sélectionnée
pg.run()
