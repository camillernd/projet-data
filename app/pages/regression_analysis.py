import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import shapiro

def regression_analysis_page():
    st.title("📊 Analyse de régression")

    # Ajouter un markdown pour accéder directement au dictionnaire de données
    st.markdown(
        """
        [📘 Voir le dictionnaire des données](#data_dictionary)
        """
    )
    
    file_path = "data/final_filtered_data_sample.csv"
    try:
        filtered_data = pd.read_csv(file_path)

        # Étapes préliminaires
        st.header("Étapes préliminaires")
        st.markdown(
            """
            Après notre épuration des données, nous nous retrouvons avec un échantillon de 1397 communes 
            pour lesquelles nous avons un jeu de données complet, au lieu des 1627 communes que compte le PVD au total.

            Nous avons choisi comme variable de réponse le **taux d’évolution annuel de la population**.
            Avant de construire le modèle, nous avons créé une **matrice de corrélation** comportant toutes nos variables explicatives. 
            Toute variable qui aurait une corrélation avec une autre supérieure à 0,85 serait retirée des observations 
            afin d’éviter au maximum le risque de multicolinéarité. Lors de cette étape, **aucune variable explicative n’a été retirée**.
            """
        )

        # Affichage des premières lignes
        st.header("Aperçu des données")
        st.write(filtered_data.head())

        # Suppression des colonnes inutiles
        data_for_regression = filtered_data.drop(columns=[
            'taux_evolution_due_solde_naturel', 'taux_evolution_due_solde_migratoire', 'code_insee'
        ])

        # Calcul de la matrice de corrélation
        correlation_matrix = data_for_regression.corr()

        # Identification des variables fortement corrélées
        highly_correlated = np.where((correlation_matrix > 0.85) & (correlation_matrix != 1))
        correlated_pairs = [
            (correlation_matrix.index[x], correlation_matrix.columns[y])
            for x, y in zip(*highly_correlated) if x < y
        ]

        # Affichage de la matrice de corrélation
        st.header("Matrice de corrélation")
        fig, ax = plt.subplots(figsize=(12, 10))
        cax = ax.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
        fig.colorbar(cax)
        ax.set_title("Matrice de corrélation des variables")
        st.pyplot(fig)

        # Affichage des paires fortement corrélées
        if correlated_pairs:
            st.subheader("Paires de variables fortement corrélées")
            for pair in correlated_pairs:
                st.write(f"{pair[0]} et {pair[1]}")

        # Construction du modèle
        st.header("Construction du modèle")
        st.markdown(
            """
            Au vu du grand nombre de prédicteurs, nous nous doutions que certains d’entre eux ne seraient pas significatifs, 
            nous avons donc procédé à une **sélection backward**. Cela signifie que nous avons commencé par générer un modèle 
            comportant toutes les variables explicatives pour ensuite retirer une à une celles ayant la plus grande p-value supérieure au seuil de 0,05.

            Cette sélection a permis de retirer 28 des 41 variables que nous avions choisies, faisant passer l’Akaike Information Criterion (AIC) 
            du modèle de **3067 à 3035**.
            """
        )

        # Séparation des variables prédicteurs et réponse
        X = data_for_regression.drop(columns=['taux_evolution'])
        y = data_for_regression['taux_evolution']

        # Ajout d'une constante aux prédicteurs
        X = sm.add_constant(X)

        # Fonction pour régression par élimination arrière avec logs
        def backward_regression_with_logging(X, y, significance_level=0.05):
            steps = []
            step_count = 1
            while True:
                model = sm.OLS(y, X).fit()
                aic = model.aic
                p_values = model.pvalues
                max_p_value = p_values.max()
                if max_p_value > significance_level:
                    excluded_feature = p_values.idxmax()
                    steps.append(f"Step {step_count}: Suppression de {excluded_feature}, AIC: {aic:.2f}")
                    X = X.drop(columns=[excluded_feature])
                    step_count += 1
                else:
                    break
            return model, steps

        # Lancer la régression par élimination arrière
        final_model, regression_steps = backward_regression_with_logging(X, y)

        # Affichage des étapes dans un menu déroulant
        st.subheader("Étapes de la régression")
        with st.expander("Voir les étapes de sélection backward"):
            for step in regression_steps:
                st.write(step)

        # Résumé du modèle final
        st.subheader("Résumé du modèle final")
        with st.expander("Voir les résultats complets de la régression"):
            st.text(final_model.summary())

        # Interprétation des résultats
        st.header("Interprétation des résultats")
        st.markdown(
            """
            L’analyse des résultats met en lumière plusieurs éléments significatifs influençant le taux d’évolution démographique des communes étudiées. 
            La constante du modèle est estimée à **-2,6937**, ce qui représente la valeur de base lorsque toutes les variables explicatives sont nulles. 
            Cela souligne une tendance démographique défavorable en l’absence de facteurs positifs.

            Parmi les variables explicatives, plusieurs ont montré une influence significative. Par exemple, le **nombre de cinémas** est associé 
            positivement au taux d’évolution démographique (**+0,1088**), indiquant que des infrastructures culturelles peuvent jouer un rôle attractif. 
            À l’inverse, le **nombre de conservatoires** (**-1,5047**) et de **musées** (**-0,2256**) présente un effet négatif, suggérant que ces équipements, 
            bien que symboliques, ne suffisent pas à stimuler une croissance démographique.

            Les données économiques confirment également leur importance. La **médiane du revenu disponible** est positivement corrélée (**+0,0001**) 
            avec le taux d’évolution, reflétant le rôle essentiel de la prospérité économique dans l’attractivité des communes. Par ailleurs, 
            la structure démographique des communes a également un effet notable. Une proportion plus élevée de jeunes de moins de 15 ans 
            stimule la croissance démographique (**+0,0914**), tandis que des tranches d’âge plus âgées, comme les 15-19 ans (**-0,0382**) 
            et les 45-59 ans (**-0,0678**), semblent avoir un effet inverse.

            Concernant les infrastructures de proximité, la présence de **supérettes et épiceries** a un impact positif significatif (**+0,0242**), 
            renforçant l’idée que la disponibilité des commerces de base influence l’attractivité locale. En revanche, un **nombre élevé d’écoles primaires** 
            est associé à une baisse du taux d’évolution démographique (**-0,0603**), ce qui peut refléter un certain déséquilibre dans l’offre scolaire.

            Enfin, les services de santé jouent un rôle clé : la **densité de médecins généralistes** (**+0,0185**) et de dentistes (**+0,0253**) 
            contribue positivement à l’évolution démographique. De même, les **festivals** (**+0,0380**) semblent renforcer l’attractivité des communes 
            en valorisant leur dynamisme culturel.

            Malgré un **R²** de **0,35**, indiquant que 35 % de la variance du taux d’évolution est expliquée par notre modèle, 
            cette étude souligne l’importance des facteurs économiques, culturels et démographiques dans la compréhension des dynamiques locales. 
            Le test de significativité globale du modèle (F-test) confirme que l’ensemble des prédicteurs retenus est statistiquement significatif.
            """
        )

        # Analyse des résidus
        st.header("Analyse des résidus")
        st.markdown(
            """
            - **Homoscédasticité** : Les résidus ont une moyenne nulle ainsi qu’une variance constante et indépendante, validant l’utilisation des tests de nullité sur les coefficients et le F-test.
            - **Normalité des résidus** : Le QQ plot montre que les résidus ne suivent pas une distribution normale.
            """
        )

        residuals = final_model.resid
        fitted = final_model.fittedvalues

        # Résidus vs valeurs ajustées
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(fitted, residuals, alpha=0.6)
        ax.axhline(0, color='red', linestyle='--')
        ax.set_title("Résidus vs Valeurs ajustées")
        ax.set_xlabel("Valeurs ajustées")
        ax.set_ylabel("Résidus")
        st.pyplot(fig)

        # QQ Plot
        st.subheader("QQ Plot (Normalité des résidus)")
        qq_fig = sm.qqplot(residuals, line='45', fit=True)
        st.pyplot(qq_fig)

        # Explication sur la faible valeur de R²
        st.header("Discussion sur le R²")
        st.markdown(
            """
            La valeur relativement faible du R² (**0,35**) indique que notre modèle explique uniquement 35 % de la variance du taux d’évolution démographique. 
            Nous avons choisi de nous concentrer sur des facteurs **économiques**, **socio-économiques**, et **environnementaux**, mais le taux d'évolution est une variable qui dépend d'autres facteurs. 

            Ceux que nous avons choisis expliquent à 35 % cette variation. En ajoutant d'autres facteurs, tels que des éléments politiques (par exemple, les investissements publics locaux) ou historiques, 
            nous pourrions espérer un modèle avec un R² plus élevé et une meilleure explication des variations observées.
            """
        )

        # Dictionnaire de données
        st.header("📘 Dictionnaire des données", anchor="data_dictionary")
        with st.expander("Voir le dictionnaire des données"):
            st.markdown(
                """
                - **code_insee** : Code Insee de la commune d'implantation de l'équipement, sans distinction des arrondissements pour Paris, Lyon et Marseille (respectivement 75056, 69123 et 13055) (Source : Défi-Data-Gouv)
                - **Bibliotheque** : Nombre de bibliothèques dans la commune. (Source : Défi-Data-Gouv)
                - **Cinema** : Nombre de cinémas dans la commune. (Source : Défi-Data-Gouv)
                - **Conservatoire** : Nombre de conservatoires dans la commune. (Source : Défi-Data-Gouv)
                - **Espace_protege** : Nombre d’espaces protégés dans la commune. (Source : Défi-Data-Gouv)
                - **Librairie** : Nombre de librairies dans la commune. (Source : Défi-Data-Gouv)
                - **Monument** : Nombre de monuments dans la commune. (Source : Défi-Data-Gouv)
                - **Musee** : Nombre de musées dans la commune. (Source : Défi-Data-Gouv)
                - **Parc_et_jardin** : Nombre de parcs et jardins dans la commune. (Source : Défi-Data-Gouv)
                - **Theatre** : Nombre de théâtres dans la commune. (Source : Défi-Data-Gouv)
                - **Etablissement_d'enseignement_superieur** : Nombre d’établissements d’enseignement supérieur dans la commune. (Source : Défi-Data-Gouv)
                - **GCD** : Valeurs possibles : ['6 - Rural à habitat dispersé', '5 - Bourgs ruraux', '4 - Ceintures urbaines', '2 - Centres urbains intermédiaires', '1 - Grands centres urbains', '7 - Rural à habitat très dispersé', '3 - Petites villes'] (Source : Défi-Data-Gouv)
                - **AAV** : Valeurs possibles : ['30 - Hors attraction des villes', '22 - Couronnes de 50 000 à moins de 200 000 hab.', '11 - Pôles de moins de 50 000 hab.', '23 - Couronnes de 200 000 à moins de 700 000 hab.', '21 - Couronnes de moins de 50 000 hab.', '12 - Pôles de 50 000 à moins de 200 000 hab.', '24 - Couronnes de 700 000 hab. ou plus', '13 - Pôles de 200 000 à moins de 700 000 hab.', '14 - Pôles de 700 000 hab. ou plus', NaN] (Source : Défi-Data-Gouv)
                - **mediane_du_revenu_disponible_par_uc_2020** : La médiane du revenu disponible correspond au niveau au-dessous duquel se situent 50 % de ces revenus. (Source : Observatoire des territoires)
                - **part_des_60-74_ans_2021** : Population de cette tranche d’âge rapportée à la population de la commune (Source : Observatoire des territoires)
                - **part_des_moins_de_15_ans_2021** : Population de cette tranche d’âge rapportée à la population de la commune (Source : Observatoire des territoires)
                - **part_des_15-29_ans_2021** : Population de cette tranche d’âge rapportée à la population de la commune (Source : Observatoire des territoires)
                - **part_des_30-44_ans_2021** : Population de cette tranche d’âge rapportée à la population de la commune (Source : Observatoire des territoires)
                - **part_des_45-59_ans_2021** : Population de cette tranche d’âge rapportée à la population de la commune (Source : Observatoire des territoires)
                - **nombre_grandes_surfaces_2023** : Nombre de grandes surfaces dans la commune. (Source : Observatoire des territoires)
                - **nombre_de_superettes_et_epieries** : Nombre de supérettes et épiceries dans la commune. (Source : Observatoire des territoires)
                - **nombre_boulangeries_et_patisseries** : Nombre de boulangeries et de pâtisseries dans la commune. (Source : Observatoire des territoires)
                - **nombre_ecoles_primaires_maternelles_elementaires** : Nombre d’écoles (primaires, maternelles, élémentaires) dans la commune. (Source : Observatoire des territoires)
                - **nombre_de_colleges** : Nombre de collèges dans la commune. (Source : Observatoire des territoires)
                - **nombre_de_lycees** : Nombre de lycées dans la commune. (Source : Observatoire des territoires)
                - **nombre_de_medecins_generalistes** : Nombre de médecins généralistes dans la commune. (Source : Observatoire des territoires)
                - **nombre_de_dentistes** : Nombre de dentistes dans la commune. (Source : Observatoire des territoires)
                - **nombre_de_pharmacies** : Nombre de pharmacies dans la commune. (Source : Observatoire des territoires)
                - **taux_evolution** : Taux d’évolution annuel moyen de la population communale sur une période donnée. (Source : Observatoire des territoires)
                - **taux_evolution_due_solde_migratoire** : Part du taux d’évolution annuel de la population attribuable au solde migratoire apparent. (Source : Observatoire des territoires)
                - **taux_evolution_due_solde_naturel** : Part du taux d’évolution annuel de la population attribuable au solde naturel. (Source : Observatoire des territoires)
                - **nombre_d_equipements_sportifs** : Nombre total d’infrastructures sportives accessibles au public dans la commune (Source : Observatoire des territoires)
                - **nombre_de_festivals** : Nombre de festivals ayant eu lieu dans la commune en 2019 (Source : Défi-Data-Gouv)
                """
            )

    except FileNotFoundError:
        st.error(f"Le fichier spécifié à '{file_path}' est introuvable. Veuillez vérifier le chemin.")
