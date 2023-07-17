# Import necessary libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import LabelEncoder

# Load the dataset
data = pd.read_csv('/content/Insurance multiple regression.csv')

# Check for null values
print(data.isnull().sum())

# Replace null values with median/mode as appropriate
median = data['charges'].median()
data['charges'] = data['charges'].fillna(median)
mode = data['region'].mode()[0]
data['region'] = data['region'].fillna(mode)

# Encode non-numeric features
labelencoder = LabelEncoder()
data['sex'] = labelencoder.fit_transform(data['sex'])
data['smoker'] = labelencoder.fit_transform(data['smoker'])
data['region'] = labelencoder.fit_transform(data['region'])

# Check for multicollinearity
X = data[['age', 'sex', 'bmi', 'children', 'smoker', 'region']]
y = data['charges']

vif = pd.DataFrame()
vif["VIF Factor"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif["features"] = X.columns

print(vif)

# Drop features with low correlation with y
corr = data.corr()['charges'].abs()
features_to_drop = corr[corr < 0.1].index.tolist()
if len(features_to_drop) > 0:
    print("Dropping features with low correlation with y:", features_to_drop)
    X = X.drop(features_to_drop, axis=1)

print("Features selected:", X.columns)

sns.pairplot(data, x_vars=X.columns, y_vars='charges', kind='reg')
plt.show()

# Identify and remove outliers
Q1 = X.quantile(0.25)
Q3 = X.quantile(0.75)
IQR = Q3 - Q1
outliers = ((X < (Q1 - 1.5 * IQR)) | (X > (Q3 + 1.5 * IQR))).any(axis=1)
X = X[~outliers]
y = y[~outliers]

# Plot distribution of X and y
sns.displot(X, kind='kde')
plt.show()

sns.displot(y, kind='kde')
plt.show()

sns.pairplot(data, x_vars=X.columns, y_vars='charges', kind='reg')
plt.show()