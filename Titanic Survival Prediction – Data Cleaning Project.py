import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, OneHotEncoder

# Load dataset
df = pd.read_csv("train.csv")

# Display first five rows
print(df.head())

# Dataset dimensions
print("Dataset Shape:", df.shape)

# Column names and data types
print("\nDataset Information:")
df.info()

# Statistical summary of numerical columns
print("\nNumerical Statistics:")
print(df.describe())

# Statistical summary including categorical columns
print("\nComplete Statistical Summary:")
print(df.describe(include="all"))

# Count missing values in each column
print("\nMissing Values:")
print(df.isnull().sum())

# Work on the original dataset
df_clean = df.copy()

# Mean imputation example
if df_clean["Fare"].isnull().any():
    fare_mean = df_clean["Fare"].mean()
    df_clean["Fare"] = df_clean["Fare"].fillna(fare_mean)

# Median imputation for Age
age_median = df_clean["Age"].median()
df_clean["Age"] = df_clean["Age"].fillna(age_median)

# Mode imputation for Embarked
embarked_mode = df_clean["Embarked"].mode()[0]
df_clean["Embarked"] = df_clean["Embarked"].fillna(embarked_mode)

# Check missing values after imputation
print("Missing values after imputation:")
print(df_clean.isnull().sum())

label_encoder = LabelEncoder()

df_clean["Sex_Encoded"] = label_encoder.fit_transform(df_clean["Sex"])

print("Sex encoding:")
print(dict(zip(
    label_encoder.classes_,
    label_encoder.transform(label_encoder.classes_)
)))

print(df_clean[["Sex", "Sex_Encoded"]].head())


onehot_encoder = OneHotEncoder(
    handle_unknown="ignore",
    sparse_output=False
)

embarked_encoded = onehot_encoder.fit_transform(
    df_clean[["Embarked"]]
)

embarked_columns = onehot_encoder.get_feature_names_out(
    ["Embarked"]
)

embarked_df = pd.DataFrame(
    embarked_encoded,
    columns=embarked_columns,
    index=df_clean.index
)

# Add encoded columns to the dataset
df_clean = pd.concat([df_clean, embarked_df], axis=1)

print(df_clean[["Embarked"] + list(embarked_columns)].head())
