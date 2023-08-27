# First, let's load the dataset to continue with the hybrid feature extraction
import pandas as pd
from scipy.stats import pearsonr
from sklearn.feature_selection import mutual_info_classif
import numpy as np


# Define function to load and preprocess the dataset
def load_and_preprocess_dataset(file_path):
    # Load the dataset
    df = pd.read_csv(file_path)
    # Drop any non-numeric columns for simplicity
    df = df.select_dtypes([np.number])
    return df

# Function to save the modified dataset with selected features
def save_modified_dataset(df, selected_features, save_path):
    # Keep only the selected features and the target column
    df_modified = df[selected_features + ['Phishing Status']]
    # Save the modified dataset
    df_modified.to_csv(save_path, index=False)


# Load the data
file_path = r"D:\Warwick\MSC_Code\dataset-ok\phishing-paper-1\Phishing_paper1.csv"
df = pd.read_csv(file_path)

# Drop any non-numeric columns for simplicity
df = df.select_dtypes([np.number])

# Separate features and labels
X = df.drop(columns=['Phishing Status'])
y = df['Phishing Status']

# Calculate Gain Ratios using mutual information
gain_ratios = mutual_info_classif(X, y)

# Calculate Correlations using Pearson correlation coefficient
correlations = []
for col in X.columns:
    correlation, _ = pearsonr(X[col], y)
    correlations.append(correlation)

# Convert to numpy arrays for easier manipulation
gain_ratios = np.array(gain_ratios)
correlations = np.array(correlations)

# Define thresholds (These are just example values, you can adjust them based on your understanding of the data)
theta = 0.2
theta1 = 0.1
theta2 = 0.2

# Initialize empty list to hold selected features
selected_features_hybrid = []

# Hybrid Feature Selection Algorithm
for i in range(len(X.columns)):
    if gain_ratios[i] > theta and correlations[i] > theta:
        selected_features_hybrid.append(X.columns[i])
    elif gain_ratios[i] > theta1 or abs(correlations[i]) > theta2:
        selected_features_hybrid.append(X.columns[i])

# Selected features
filtered_df = df[selected_features_hybrid + ['Phishing Status']]

print(selected_features_hybrid)

# Save the filtered DataFrame to a new CSV file
filtered_csv_path = r'D:\Warwick\MSC_Code\dataset-ok\phishing-paper-1\filtered_train.csv'
filtered_df.to_csv(filtered_csv_path, index=False)


valid_file_path = r'D:\Warwick\MSC_Code\dataset-ok\phishing-paper-1\valid.csv'
valid_save_path = r'D:\Warwick\MSC_Code\dataset-ok\phishing-paper-1\filtered_valid.csv'
df_valid = load_and_preprocess_dataset(valid_file_path)
save_modified_dataset(df_valid, selected_features_hybrid, valid_save_path)

# Load, modify, and save the test dataset
test_file_path = r'D:\Warwick\MSC_Code\dataset-ok\phishing-paper-1\test.csv'
test_save_path = r'D:\Warwick\MSC_Code\dataset-ok\phishing-paper-1\filtered_test.csv'
df_test = load_and_preprocess_dataset(test_file_path)
save_modified_dataset(df_test, selected_features_hybrid, test_save_path)