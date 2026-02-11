import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA

def plot_clusters_pca(
        X: pd.DataFrame,
        labels,
        title: str = "Cluster Visualization (PCA)"
):
    pca = PCA(n_components=2, random_state=42)
    components = pca.fit_transform(X)

    df_plot = pd.DataFrame({
        "PC1": components[:, 0],
        "PC2": components[:, 1],
        "Cluster": labels
    })

    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=df_plot,
        x="PC1",
        y="PC2",
        hue="Cluster",
        palette="tab10",
        alpha=0.7
    )
    plt.title(title)
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.legend(title="Cluster")
    plt.tight_layout()
    plt.show()

def plot_rfm_distributions(
        rfm: pd.DataFrame,
        labels,
        features=("Recency", "Frequency", "Monetary")
):
    df_plot = rfm.copy()
    df_plot["Cluster"] = labels

    for feature in features:
        plt.figure(figsize=(7, 4))
        sns.boxplot(
            data=df_plot,
            x="Cluster",
            y=feature
        )
        plt.title(f"{feature} distribution per cluster")
        plt.tight_layout()
        plt.show()

def plot_cluster_sizes(labels):
    cluster_counts = pd.Series(labels).value_counts().sort_index()

    plt.figure(figsize=(6, 4))
    sns.barplot(
        x=cluster_counts.index.astype(str),
        y=cluster_counts.values
    )
    plt.title("Cluster sizes")
    plt.xlabel("Cluster")
    plt.ylabel("Number of customers")
    plt.tight_layout()
    plt.show()