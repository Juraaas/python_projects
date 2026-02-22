import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.decomposition import PCA
from umap import UMAP

def plot_clusters_pca(
        X: pd.DataFrame,
        labels,
        title: str = "Cluster Visualization (PCA)",
        save_path=None,
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

    if save_path:
        plt.savefig(save_path, dpi=150)

    plt.show()

def plot_rfm_distributions(
        rfm: pd.DataFrame,
        labels,
        features=("Recency", "Frequency", "Monetary"),
        save_path=None,
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

        if save_path:
            plt.savefig(save_path, dpi=150)

        plt.show()

def plot_cluster_sizes(labels,
                       save_path=None,):
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

    if save_path:
        plt.savefig(save_path, dpi=150)

    plt.show()

def plot_kmeans_analysis(results_df,
                         save_path=None,):

    fig, axes = plt.subplots(1, 2, figsize=(12,4))

    axes[0].plot(results_df["k"], results_df["inertia"], marker="o")
    axes[0].set_title("Elbow Method (Inertia vs k)")
    axes[0].set_xlabel("Number of clusters (k)")
    axes[0].set_ylabel("Inertia")

    axes[1].plot(results_df["k"], results_df["silhouette_score"], marker="o")
    axes[1].set_title("Silhouette Score vs k")
    axes[1].set_xlabel("Number of clusters (k)")
    axes[1].set_ylabel("Silhouette Score")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)

    plt.show()

def plot_clusters_umap(X,
                       labels,
                       title="UMAP Clustering",
                       save_path=None,):
    umap = UMAP(
        n_neighbors=15,
        min_dist=0.1,
        random_state=42,
    )

    components = umap.fit_transform(X)

    df_plot = pd.DataFrame({
        "UMAP1": components[:, 0],
        "UMAP2": components[:, 1],
        "Cluster": labels,
    }
    )
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        data=df_plot,
        x="UMAP1",
        y="UMAP2",
        hue="Cluster",
        palette="tab10",
        alpha=0.7
    )
    plt.title(title)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=150)

    plt.show()