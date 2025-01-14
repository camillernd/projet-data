import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Load the uploaded data
filtered_data_path = '../data/final_filtered_data_sample.csv'
filtered_data = pd.read_csv(filtered_data_path)

# Display the first few rows and columns for clarity
filtered_data.head(), filtered_data.columns.tolist()

# Remove unwanted columns
data_for_regression = filtered_data.drop(columns=[
    'taux_evolution_due_solde_naturel', 'taux_evolution', 'code_insee'
])

# Compute the correlation matrix
correlation_matrix = data_for_regression.corr()

# Identify highly correlated variables (correlation > 0.85)
highly_correlated = np.where((correlation_matrix > 0.85) & (correlation_matrix != 1))
correlated_pairs = [(correlation_matrix.index[x], correlation_matrix.columns[y]) 
                    for x, y in zip(*highly_correlated) if x < y]

# Plot the correlation matrix for visualization
plt.figure(figsize=(12, 10))
plt.imshow(correlation_matrix, cmap='coolwarm', interpolation='nearest')
plt.colorbar()
plt.title('Correlation Matrix of Variables', fontsize=16)
plt.show()

# Return correlated pairs for inspection
correlated_pairs

# Separate predictors (X) and response variable (y)
X = data_for_regression.drop(columns=['taux_evolution_due_solde_migratoire'])
y = data_for_regression['taux_evolution_due_solde_migratoire']

# Add a constant to the predictors (for the intercept)
X = sm.add_constant(X)

# Perform backward regression
def backward_regression(X, y, significance_level=0.05):
    """
    Perform backward regression by iteratively removing the least significant variables.
    """
    while True:
        model = sm.OLS(y, X).fit()
        p_values = model.pvalues
        max_p_value = p_values.max()
        if max_p_value > significance_level:
            excluded_feature = p_values.idxmax()
            X = X.drop(columns=[excluded_feature])
        else:
            break
    return model

# Run backward regression
final_model = backward_regression(X, y)

# Summary of the final model
final_model_summary = final_model.summary()
final_model_summary

