import streamlit as st
from pages.home import home_page
from pages.initiative import initiative_page
from pages.beneficiaries import beneficiaries_page
from pages.festivals_map import festivals_map_page
from pages.regression_population import regression_population_page
from pages.attraction_correlation import attraction_correlation_page  # Importer la nouvelle page
from pages.influence_and_attractiveness_maps import influence_and_attractiveness_maps

# Définir les pages
home = st.Page(home_page, title="Home", icon="🏠")
initiative = st.Page(initiative_page, title="L'Initiative", icon="💡")
beneficiaries = st.Page(beneficiaries_page, title="Bénéficiaires", icon="🗺️")
festivals_map = st.Page(festivals_map_page, title="Festivals et Petites Villes", icon="🎭")
regression_population = st.Page(regression_population_page, title="Régression Population", icon="📈")
attraction_correlation = st.Page(attraction_correlation_page, title="Corrélation Attraction", icon="📊")  # Ajouter la nouvelle page
influence_maps = st.Page(influence_and_attractiveness_maps, title="Cartes d'influence et attractivité", icon="🗺️")

pg = st.navigation([home, initiative, beneficiaries, festivals_map, regression_population, attraction_correlation, influence_maps])  # Ajouter la nouvelle page

# Configurer l'application
st.set_page_config(page_title="Ma superbe application", page_icon="🚀")

# Exécuter la page sélectionnée
pg.run()
