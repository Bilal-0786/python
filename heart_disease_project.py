import os
import warnings
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    roc_curve,
    roc_auc_score
)

warnings.filterwarnings("default")
RANDOM_STATE = 42
DATA_FILE = "heart.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


df = pd.read_csv(DATA_FILE)

df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)


df.replace(
    ["?", "NA", "N/A", "na", "null", "None", ""],
    np.nan,
    inplace=True
)

print("=" * 60)
print("HEART DISEASE DATASET")
print("=" * 60)
print("Dataset shape:", df.shape)
print("\nFirst five rows:")
print(df.head())
print("\nDataset information:")
df.info()
print("\nMissing values:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

possible_targets = [
    "target",
    "heartdisease",
    "heart_disease",
    "num",
    "condition",
    "output",
    "diagnosis",
    "class"
]

target_col = next(
    (col for col in possible_targets if col in df.columns),
    None
)

if target_col is None:
    raise ValueError(
        "Target column not found. Available columns: "
        + str(df.columns.tolist())
        + ". Set target_col manually for your dataset."
    )

print("\nSelected target column:", target_col)


for col in df.columns:
    converted = pd.to_numeric(df[col], errors="coerce")
    original_nonmissing = df[col].notna().sum()

    if original_nonmissing > 0:
        convertible = converted.notna().sum()
        if convertible / original_nonmissing >= 0.90:
            df[col] = converted


df = df.dropna(subset=[target_col]).copy()



df.drop_duplicates(inplace=True)

y_raw = df[target_col]

if pd.api.types.is_numeric_dtype(y_raw):
    unique_targets = set(y_raw.unique())

    if unique_targets.issubset({0, 1}):
        y = y_raw.astype(int)
    else:
        
        y = (y_raw > 0).astype(int)
else:
    normalized_target = y_raw.astype(str).str.strip().str.lower()

    target_mapping = {
        "0": 0, "1": 1,
        "no": 0, "yes": 1,
        "false": 0, "true": 1,
        "negative": 0, "positive": 1,
        "absent": 0, "present": 1,
        "no disease": 0, "disease": 1,
        "no heart disease": 0,
        "heart disease": 1
    }

    y = normalized_target.map(target_mapping)

    if y.isnull().any():
        raise ValueError(
            "Target contains unrecognized labels: "
            + str(normalized_target.unique().tolist())
            + ". Define an appropriate target mapping."
        )

    y = y.astype(int)

if y.nunique() != 2:
    raise ValueError(
        "This implementation requires a binary target."
    )


X = df.drop(columns=[target_col]).copy()
y = pd.Series(y.to_numpy(), index=X.index, name="target")


empty_columns = X.columns[X.isnull().all()].tolist()
if empty_columns:
    print("\nDropping entirely empty columns:", empty_columns)
    X.drop(columns=empty_columns, inplace=True)

cleaned_df = X.copy()
cleaned_df["target"] = y
cleaned_df.to_csv(
    os.path.join(OUTPUT_DIR, "heart_cleaned.csv"),
    index=False
)

print("\nCleaned dataset shape:", cleaned_df.shape)
print("\nTarget distribution:")
print(y.value_counts().sort_index())
print("\nTarget meaning: 0 = no disease, 1 = disease present")

plt.figure(figsize=(7, 5))
sns.countplot(x=y)
plt.title("Heart Disease Class Distribution")
plt.xlabel("Target (0 = No Disease, 1 = Disease)")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "target_distribution.png"),
    dpi=300
)
plt.show()

numeric_for_corr = X.select_dtypes(include=np.number)

if numeric_for_corr.shape[1] >= 2:
    plt.figure(figsize=(12, 8))
    correlation = numeric_for_corr.corr()
    sns.heatmap(
        correlation,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )
    plt.title("Feature Correlation Heatmap")
    plt.tight_layout()
    plt.savefig(
        os.path.join(OUTPUT_DIR, "correlation_heatmap.png"),
        dpi=300
    )
    plt.show()

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=RANDOM_STATE,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

numeric_features = X.select_dtypes(
    include=np.number
).columns.tolist()

categorical_features = X.select_dtypes(
    exclude=np.number
).columns.tolist()

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_features),
    ("categorical", categorical_pipeline, categorical_features)
])

models = {
    "Logistic Regression": Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", LogisticRegression(
            max_iter=2000,
            random_state=RANDOM_STATE
        ))
    ]),

    "Decision Tree": Pipeline([
        ("preprocessor", preprocessor),
        ("classifier", DecisionTreeClassifier(
            max_depth=5,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=RANDOM_STATE
        ))
    ])
}

metrics = []
trained_models = {}
predictions = {}
probabilities = {}

for name, model in models.items():
    print("\n" + "=" * 60)
    print(name.upper())
    print("=" * 60)

    model.fit(X_train, y_train)

    
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]

    trained_models[name] = model
    predictions[name] = y_pred
    probabilities[name] = y_prob

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(
        y_test, y_pred, zero_division=0
    )
    recall = recall_score(
        y_test, y_pred, zero_division=0
    )
    f1 = f1_score(
        y_test, y_pred, zero_division=0
    )
    auc = roc_auc_score(y_test, y_prob)

    metrics.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1,
        "ROC-AUC": auc
    })

    print(f"Accuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(f"ROC-AUC  : {auc:.4f}")

    print("\nClassification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=["No Disease", "Disease"],
        zero_division=0
    ))

    
    cm = confusion_matrix(y_test, y_pred, labels=[0, 1])

    plt.figure(figsize=(6, 5))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=["No Disease", "Disease"],
        yticklabels=["No Disease", "Disease"]
    )
    plt.title(f"{name} - Confusion Matrix")
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")
    plt.tight_layout()

    safe_name = name.lower().replace(" ", "_")
    plt.savefig(
        os.path.join(
            OUTPUT_DIR, f"{safe_name}_confusion_matrix.png"
        ),
        dpi=300
    )
    plt.show()


plt.figure(figsize=(8, 6))

for name, y_prob in probabilities.items():
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)

    plt.plot(
        fpr,
        tpr,
        label=f"{name} (AUC = {auc:.3f})"
    )

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random Classifier"
)

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curve - Model Comparison")
plt.legend()
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "roc_curve_comparison.png"),
    dpi=300
)
plt.show()

metrics_df = pd.DataFrame(metrics).set_index("Model")

print("\n" + "=" * 60)
print("FINAL MODEL COMPARISON")
print("=" * 60)
print(metrics_df.round(4))

metrics_df.to_csv(
    os.path.join(OUTPUT_DIR, "model_comparison.csv")
)

metrics_df.plot(
    kind="bar",
    figsize=(11, 6),
    ylim=(0, 1.05)
)

plt.title("Performance Comparison of ML Models")
plt.ylabel("Score")
plt.xticks(rotation=0)
plt.legend(loc="lower right")
plt.tight_layout()
plt.savefig(
    os.path.join(OUTPUT_DIR, "model_metrics_comparison.png"),
    dpi=300
)
plt.show()

print("\n5-Fold Cross-Validation Accuracy")

for name, model in trained_models.items():
    scores = cross_val_score(
        model,
        X_train,
        y_train,
        cv=5,
        scoring="accuracy"
    )

    print(
        f"{name}: {scores.mean():.4f} "
        f"+/- {scores.std():.4f}"
    )

for name, model in trained_models.items():
    safe_name = name.lower().replace(" ", "_")
    model_path = os.path.join(
        OUTPUT_DIR, f"{safe_name}.joblib"
    )
    joblib.dump(model, model_path)
    print("Saved:", model_path)

prediction_df = pd.DataFrame({
    "Actual": y_test.to_numpy()
})

for name in trained_models:
    safe_name = name.lower().replace(" ", "_")
    prediction_df[f"{safe_name}_prediction"] = predictions[name]
    prediction_df[f"{safe_name}_probability"] = probabilities[name]

prediction_df.to_csv(
    os.path.join(OUTPUT_DIR, "test_predictions.csv"),
    index=False
)

best_model_name = max(
    metrics,
    key=lambda row: row["ROC-AUC"]
)["Model"]

best_model = trained_models[best_model_name]

joblib.dump(
    best_model,
    os.path.join(OUTPUT_DIR, "best_model.joblib")
)

print("\nBest model by test ROC-AUC:", best_model_name)
print("All results saved in:", OUTPUT_DIR)

print("\nIMPORTANT:")
print("This is an educational classification project,")
print("not a medically validated diagnostic system.")
