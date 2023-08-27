
import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif
from scipy.stats import spearmanr

# Load data
# You need to put your train.csv in the same directory as this script
df = pd.read_csv("train.csv")

# Drop rows containing NaN values
df.dropna(inplace=True)
df = df.drop(columns=['emailencoding'])
# Separate features and labels
X = df.drop("isphishing", axis=1)
y = df["isphishing"]

# Calculate Gain Ratio
def gain_ratio(X, y):
    mi = mutual_info_classif(X, y)
    entropy = -np.sum([(p * np.log2(p)) for p in np.unique(y, return_counts=True)[1] / len(y)])
    return mi / entropy

gain_ratios = gain_ratio(X, y)

# Calculate Spearman Correlation
def spearman_correlation(X, y):
    correlations = []
    for col in X.columns:
        coef, _ = spearmanr(X[col], y)
        correlations.append(coef)
    return np.array(correlations)

correlations = spearman_correlation(X, y)

# Print results
print("Gain Ratios:", gain_ratios)
print("Correlations:", correlations)
