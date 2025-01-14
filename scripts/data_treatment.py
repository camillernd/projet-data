import pandas as pd
# If unidecode is not available, use an alternative approach to normalize text
import unicodedata

# Load the uploaded CSV file
file_path = '/mnt/data/base-des-lieux-et-des-equipements-culturels.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the file to understand its structure
data.head(), data.columns


# Step 1: Filter active rows based on 'Demographie_AP'
filtered_data = data[data['Demographie_AP'] == 'Actif']

# Step 2: Process 'Type équipement ou lieu' to get counts per commune for each type
type_counts = filtered_data.groupby(['code_insee', 'Type équipement ou lieu']).size().unstack(fill_value=0)
type_counts_file = '/mnt/data/type_counts_per_commune.csv'
type_counts.to_csv(type_counts_file)

# Step 3: Process 'GCD' and 'AAV' for dummy variables
# GCD
gcd_dummies = pd.get_dummies(filtered_data['GCD'], prefix='GCD', drop_first=True)
gcd_categories = list(filtered_data['GCD'].unique())

# AAV
aav_dummies = pd.get_dummies(filtered_data['AAV'], prefix='AAV', drop_first=True)
aav_categories = list(filtered_data['AAV'].unique())

# Step 4: Combine processed data
processed_data = filtered_data[['code_insee']].drop_duplicates().reset_index(drop=True)
processed_data = pd.concat([processed_data, gcd_dummies, aav_dummies], axis=1)

# Export processed data
processed_file = '/mnt/data/processed_data.csv'
processed_data.to_csv(processed_file, index=False)

# Return results
type_counts_file, processed_file, gcd_categories, aav_categories


# Remove rows with 'nan' in GCD or AAV columns
filtered_data_no_nan = filtered_data.dropna(subset=['GCD', 'AAV'])

# Step 2 (updated): Process 'Type équipement ou lieu' to get counts per commune for each type
type_counts_no_nan = filtered_data_no_nan.groupby(['code_insee', 'Type équipement ou lieu']).size().unstack(fill_value=0)
type_counts_no_nan_file = '/mnt/data/type_counts_per_commune_no_nan.csv'
type_counts_no_nan.to_csv(type_counts_no_nan_file)

# Step 3 (updated): Process 'GCD' and 'AAV' for dummy variables
# GCD
gcd_dummies_no_nan = pd.get_dummies(filtered_data_no_nan['GCD'], prefix='GCD', drop_first=True)
gcd_categories_no_nan = list(filtered_data_no_nan['GCD'].unique())

# AAV
aav_dummies_no_nan = pd.get_dummies(filtered_data_no_nan['AAV'], prefix='AAV', drop_first=True)
aav_categories_no_nan = list(filtered_data_no_nan['AAV'].unique())

# Step 4 (updated): Combine processed data
processed_data_no_nan = filtered_data_no_nan[['code_insee']].drop_duplicates().reset_index(drop=True)
processed_data_no_nan = pd.concat([processed_data_no_nan, gcd_dummies_no_nan, aav_dummies_no_nan], axis=1)

# Export updated processed data
processed_file_no_nan = '/mnt/data/processed_data_no_nan.csv'
processed_data_no_nan.to_csv(processed_file_no_nan, index=False)

# Return updated results
type_counts_no_nan_file, processed_file_no_nan, gcd_categories_no_nan, aav_categories_no_nan

# Load the uploaded files
type_counts_file_path = '/mnt/data/type_counts_per_commune_no_nan.csv'
processed_file_path = '/mnt/data/processed_data_no_nan.csv'

type_counts_df = pd.read_csv(type_counts_file_path)
processed_df = pd.read_csv(processed_file_path)

# Merge the two files on 'code_insee', removing rows with missing values
merged_df = pd.merge(type_counts_df, processed_df, on='code_insee', how='inner')

# Export the merged dataframe
merged_file_path = '/mnt/data/merged_data.csv'
merged_df.to_csv(merged_file_path, index=False)

# Return the merged file path
merged_file_path

# Re-load the data to ensure accuracy in handling missing values
type_counts_df = pd.read_csv(type_counts_file_path)
processed_df = pd.read_csv(processed_file_path)

# Merge the two files on 'code_insee', ensuring no missing values remain in any row
merged_df_cleaned = pd.merge(type_counts_df, processed_df, on='code_insee', how='inner').dropna()

# Export the fully cleaned merged dataframe
cleaned_merged_file_path = '/mnt/data/fully_cleaned_merged_data.csv'
merged_df_cleaned.to_csv(cleaned_merged_file_path, index=False)

# Return the cleaned merged file path
cleaned_merged_file_path


# Function to remove accents and replace spaces with underscores
def normalize_column_name(name):
    # Remove accents
    name = ''.join(
        char for char in unicodedata.normalize('NFD', name) if unicodedata.category(char) != 'Mn'
    )
    # Replace spaces with underscores
    return name.replace(' ', '_')

# Apply normalization to column names
merged_df_cleaned.columns = [normalize_column_name(col) for col in merged_df_cleaned.columns]

# Export the updated dataframe
updated_columns_file_path = '/mnt/data/updated_columns_cleaned_merged_data.csv'
merged_df_cleaned.to_csv(updated_columns_file_path, index=False)

# Return the updated file path
updated_columns_file_path


# Load the additional file with salary information
salary_file_path = '/mnt/data/merged_salaires_cult.csv'
salary_df = pd.read_csv(salary_file_path)

# Number of lines in the current merged file
current_line_count = len(merged_df_cleaned)

# Merge the salary data with the existing merged file on 'code_insee'
final_merged_df = pd.merge(merged_df_cleaned, salary_df, on='code_insee', how='inner')

# Number of lines in the new merged file
final_line_count = len(final_merged_df)

# Export the final merged dataframe
final_merged_file_path = '/mnt/data/final_merged_data.csv'
final_merged_df.to_csv(final_merged_file_path, index=False)

# Return results
current_line_count, final_line_count, final_merged_file_path

# Display the columns of the salary file to identify the issue
salary_df.columns.tolist()

# Reload the salary file with a semicolon as the separator
salary_df = pd.read_csv(salary_file_path, sep=';')

# Display the corrected columns
salary_df.columns.tolist()

# Merge the salary data with the existing merged file on 'code_insee', ensuring no missing values remain
final_merged_df = pd.merge(merged_df_cleaned, salary_df, on='code_insee', how='inner').dropna()

# Get the line counts before and after merging
final_line_count = len(final_merged_df)

# Export the final merged dataframe
final_merged_file_path = '/mnt/data/final_merged_with_salary_data.csv'
final_merged_df.to_csv(final_merged_file_path, index=False)

# Return the number of lines in the current and final merged file, and the final file path
current_line_count, final_line_count, final_merged_file_path

# Get the number of lines in the salary file
salary_line_count = len(salary_df)

salary_line_count
