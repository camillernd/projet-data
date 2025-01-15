import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from scipy.stats import shapiro

# Load the uploaded data
filtered_data_path = '../data/final_filtered_data_sample.csv'
filtered_data = pd.read_csv(filtered_data_path)

# Display the first few rows and columns for clarity
filtered_data.head(), filtered_data.columns.tolist()

# Remove unwanted columns
data_for_regression = filtered_data.drop(columns=[
    'taux_evolution_due_solde_naturel', 'taux_evolution_due_solde_migratoire', 'code_insee'
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
plt.savefig('../figures/corr_mat.png')
plt.close()

# Return correlated pairs for inspection
correlated_pairs

# Separate predictors (X) and response variable (y)
X = data_for_regression.drop(columns=['taux_evolution'])
y = data_for_regression['taux_evolution']

# Add a constant to the predictors (for the intercept)
X = sm.add_constant(X)

# Perform backward regression with logging
def backward_regression_with_logging(X, y, significance_level=0.05):
    """
    Perform backward regression with logging of each step.
    """
    steps = []  # To store the log of steps
    step_count = 1  # Step counter
    while True:
        model = sm.OLS(y, X).fit()
        aic = model.aic  # Get AIC of the model
        p_values = model.pvalues
        max_p_value = p_values.max()
        if max_p_value > significance_level:
            excluded_feature = p_values.idxmax()
            steps.append(f"Step {step_count}: Removing {excluded_feature}, AIC: {aic:.2f}\n")
            X = X.drop(columns=[excluded_feature])
            step_count += 1
        else:
            break
    return model, steps

# Run the updated backward regression
final_model, regression_steps = backward_regression_with_logging(X, y)

# Print each step
for step in regression_steps:
    print(step)

# Summary of the final model
print(final_model.summary())

# Plot regression line for a single predictor
key_predictor = 'part_des_30-44_ans_2021'  # Example: replace with the most significant variable
plt.figure(figsize=(10, 6))
plt.scatter(X[key_predictor], y, alpha=0.6, label='Actual Data')
plt.plot(
    X[key_predictor],
    sm.OLS(y, X[["const", key_predictor]]).fit().predict(X[["const", key_predictor]]),
    color='red',
    label='Regression Line'
)
plt.title(f'Regression Line: {key_predictor} vs taux_evolution_population_annuel')
plt.xlabel(key_predictor)
plt.ylabel('taux_evolution_population_annuel')
plt.legend()
plt.savefig('../figures/example_lin_reg.png')
plt.close()

# Residuals analysis plots
residuals = final_model.resid
fitted = final_model.fittedvalues

# Residuals vs Fitted Plot
plt.figure(figsize=(10, 6))
plt.scatter(fitted, residuals, alpha=0.6)
plt.axhline(0, color='red', linestyle='--')
plt.title('Residuals vs Fitted')
plt.xlabel('Fitted values')
plt.ylabel('Residuals')
plt.savefig('../figures/res_vs_fit.png')
plt.close()

# QQ Plot
sm.qqplot(residuals, line='45', fit=True)
plt.title('Normal Q-Q')
plt.savefig('../figures/qqplot.png')
plt.close()

"""# Residual diagnostics checks
# Check if residuals mean is approximately 0
residuals_mean = np.mean(residuals)
print(f"Residuals mean: {residuals_mean:.4f}")

# Check constant variance assumption using residuals vs fitted plot
residuals_variance = np.var(residuals)
print(f"Residuals variance: {residuals_variance:.4f}")

# Check normality of residuals using Shapiro-Wilk test
shapiro_test_stat, shapiro_p_value = shapiro(residuals)
print(f"Shapiro-Wilk test statistic: {shapiro_test_stat:.4f}, p-value: {shapiro_p_value:.4f}")
if shapiro_p_value > 0.05:
    print("Residuals are normally distributed (fail to reject H0).")
else:
    print("Residuals are not normally distributed (reject H0).")
"""