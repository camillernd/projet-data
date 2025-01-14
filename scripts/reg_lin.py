import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import statsmodels.api as sm

# Set Streamlit page configuration
st.set_page_config(page_title="Multiple Linear Regression Analysis", layout="wide")

# Title of the app
st.title("Multiple Linear Regression Analysis on Communes Data")

# Load the data
@st.cache_data
def load_data():
    return pd.read_csv('FILTERED/communes_pvd_informations.csv', sep=';')

data = load_data()

# Preprocess the data
def preprocess_data(df):
    numeric_columns = [
        'taux_evolution',
        'nombre_d_equipements_culturels',
        'nombre_d_equipements_sportifs',
        'nombre_de_festivals'
    ]
    
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    df.fillna(0, inplace=True)
    return df

data = preprocess_data(data)

# Display the data
st.subheader("Dataset")
st.write("Displaying the first few rows of the dataset:")
st.dataframe(data.head())

# Pairplot to visualize relationships
st.subheader("Pairplot of Variables")
st.write("Visualizing the relationships between variables:")
sns.pairplot(data[['taux_evolution', 'nombre_d_equipements_culturels', 'nombre_d_equipements_sportifs', 'nombre_de_festivals']])
st.pyplot(plt.gcf())
plt.clf()

# Correlation matrix
st.subheader("Correlation Matrix")
st.write("Calculating the correlation matrix:")
corr_matrix = data[['taux_evolution', 'nombre_d_equipements_culturels', 'nombre_d_equipements_sportifs', 'nombre_de_festivals']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0)
st.pyplot(plt.gcf())
plt.clf()

# Prepare data for regression
X = data[['nombre_d_equipements_culturels', 'nombre_d_equipements_sportifs', 'nombre_de_festivals']]
y = data['taux_evolution']

# Add a constant to the model (intercept)
X = sm.add_constant(X)

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the model using statsmodels
model_sm = sm.OLS(y_train, X_train).fit()

# Make predictions
y_pred = model_sm.predict(X_test)

# Display the model summary
st.subheader("Regression Model Summary")
st.text(model_sm.summary())

# Model evaluation
st.subheader("Model Evaluation")
st.write(f"Mean Squared Error (MSE): {mean_squared_error(y_test, y_pred):.4f}")
st.write(f"R-squared: {r2_score(y_test, y_pred):.4f}")

# Residuals plot
st.subheader("Residuals Plot")
residuals = y_test - y_pred
plt.figure(figsize=(10, 6))
sns.scatterplot(x=y_pred, y=residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title('Residuals vs Predicted Values')
st.pyplot(plt.gcf())
plt.clf()

# Q-Q plot for residuals
st.subheader("Q-Q Plot of Residuals")
sm.qqplot(residuals, line='45')
plt.title('Q-Q Plot')
st.pyplot(plt.gcf())
plt.clf()
