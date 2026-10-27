
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import confusion_matrix, adjusted_rand_score

# --------------------------------------------------
# 1. Load the Iris dataset
# --------------------------------------------------
iris = load_iris()

X = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

y_true = iris.target

print("Dataset Shape:", X.shape)
print("\nFirst five rows:")
print(X.head())

print("\nTrue Species Labels:")
print(iris.target_names)

# --------------------------------------------------
# 2. Standardize the features
# --------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# --------------------------------------------------
# 3. Apply K-Means clustering (k = 3)
# --------------------------------------------------
kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

y_clusters = kmeans.fit_predict(X_scaled)

print("\nK-Means clustering completed successfully!")

# --------------------------------------------------
# 4. Compare predicted clusters with true labels
# --------------------------------------------------
results = X.copy()

results["True Species"] = [
    iris.target_names[label] for label in y_true
]

results["Predicted Cluster"] = y_clusters

print("\nFirst 10 comparisons:")
print(results.head(10))

print("\nCluster counts:")
print(results["Predicted Cluster"].value_counts().sort_index())

# Cross-tabulation: true species vs predicted clusters
comparison = pd.crosstab(
    results["True Species"],
    results["Predicted Cluster"],
    rownames=["True Species"],
    colnames=["Predicted Cluster"]
)

print("\nTrue Species vs Predicted Clusters:")
print(comparison)

# Adjusted Rand Index measures clustering agreement
ari = adjusted_rand_score(y_true, y_clusters)

print(f"\nAdjusted Rand Index (ARI): {ari:.4f}")

# --------------------------------------------------
# 5. Visualize clusters using the first two features
# --------------------------------------------------
plt.figure(figsize=(9, 6))

plt.scatter(
    X_scaled[:, 0],
    X_scaled[:, 1],
    c=y_clusters,
    cmap="viridis",
    s=60,
    edgecolor="black",
    alpha=0.8
)

plt.xlabel("Standardized Sepal Length")
plt.ylabel("Standardized Sepal Width")
plt.title("K-Means Clustering of Iris Dataset (k=3)")
plt.colorbar(label="Predicted Cluster")
plt.tight_layout()
plt.show()

# --------------------------------------------------
# 6. Visualize clusters in 2D using PCA
# --------------------------------------------------
# K-Means used all four features.
# PCA projects those features into two dimensions
# only for visualization.
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

centers_pca = pca.transform(kmeans.cluster_centers_)

plt.figure(figsize=(9, 6))

plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=y_clusters,
    cmap="viridis",
    s=60,
    edgecolor="black",
    alpha=0.8,
    label="Data Points"
)

plt.scatter(
    centers_pca[:, 0],
    centers_pca[:, 1],
    marker="X",
    s=250,
    c="red",
    edgecolor="black",
    label="Cluster Centers"
)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Iris K-Means Clusters Visualized using PCA")
plt.legend()
plt.tight_layout()
plt.show()

# --------------------------------------------------
# 7. Visualize true species labels for comparison
# --------------------------------------------------
plt.figure(figsize=(9, 6))

scatter = plt.scatter(
    X_pca[:, 0],
    X_pca[:, 1],
    c=y_true,
    cmap="viridis",
    s=60,
    edgecolor="black",
    alpha=0.8
)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("True Iris Species Labels (PCA Projection)")

colorbar = plt.colorbar(scatter, ticks=[0, 1, 2])
colorbar.ax.set_yticklabels(iris.target_names)

plt.tight_layout()
plt.show()
