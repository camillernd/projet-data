import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import shapiro

def regression_analysis_page():
    st.title("📊 Analyse de régression")

    # Charger directement le fichier CSV
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

        # Affichage des étapes
        st.subheader("Étapes de la régression")
        for step in regression_steps:
            st.write(step)

        # Résumé du modèle final
        st.subheader("Résumé du modèle final")
        st.text(final_model.summary())

        # Interprétation des résultats
        st.header("Interprétation des résultats")
        st.markdown(
            """
            - **B0** : La constante du modèle est de **-2,6937**, indiquant une valeur de base lorsque toutes les autres variables sont nulles.
            - **Variables significatives (Bj)** :
                - Nombre de cinémas : Positivement associé (**+0,1088**).
                - Nombre de conservatoires : Négativement associé (**-1,5047**).
                - Nombre de musées : Impact négatif (**-0,2256**).
                - Médiane du revenu : Positivement associé (**+0,0001**).
                - Part des moins de 15 ans : Effet positif (**+0,0914**).
                - Part des 15-19 ans : Effet négatif (**-0,0382**).
                - Part des 30-44 ans : Impact positif (**+0,0509**).
                - Part des 45-59 ans : Effet négatif (**-0,0678**).
                - Nombre de supérettes et épiceries : Positivement associé (**+0,0242**).
                - Nombre d’écoles primaires : Effet négatif (**-0,0603**).
                - Nombre de médecins généralistes : Positivement associé (**+0,0185**).
                - Nombre de dentistes : Effet positif (**+0,0253**).
                - Nombre de festivals : Impact positif (**+0,0380**).

            - **R²** : Le R² du modèle est de **0,35**, ce qui indique que notre modèle n’explique qu’environ 35 % de la variance du taux d’évolution de la démographie des communes du PVD.

            - **F-test** : La p-value pour le test de significativité du modèle est extrêmement faible, confirmant que le modèle est significatif.
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
            Cela s’explique par la complexité de cette variable, qui est influencée par un grand nombre de facteurs très divers. 

            Ici, nous avons pris en compte la **proximité des grandes villes**, mais nous n’avons pas inclus d’autres types de facteurs environnementaux comme 
            la **proximité de la mer**, des **stations de ski**, ou encore des **caractéristiques climatiques**. En ajoutant ces variables, 
            ainsi que des facteurs politiques (par exemple, les investissements publics locaux) et historiques, 
            nous pourrions espérer un modèle avec un R² plus élevé et une meilleure explication des variations observées.
            """
        )

    except FileNotFoundError:
        st.error(f"Le fichier spécifié à '{file_path}' est introuvable. Veuillez vérifier le chemin.")