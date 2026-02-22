import pandas as pd
import os

from src.data_processing import preprocess_data
from src.models import MODELS, kmeans_model
from src.evaluate import evaluate_clustering
from src.visualization import (
    plot_clusters_pca,
    plot_rfm_distributions,
    plot_cluster_sizes,
    plot_clusters_umap,
)
from src.evaluate import kmeans_cluster_analysis
from src.visualization import plot_kmeans_analysis

DATA_PATH = "data/raw/online_retail.csv"
FEATURE_COLUMNS = ["Recency", "Frequency", "Monetary"]
FINAL_N_CLUSTERS = 4
IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)

def main():
    print("Loading and preprocessing data...")
    rfm = preprocess_data(DATA_PATH)

    X = rfm[FEATURE_COLUMNS]

    results = []

    for model_name, model_fn in MODELS.items():
        print(f"\nRunning model: {model_name}")

        model = model_fn()

        labels = model.fit_predict(X)

        metrics = evaluate_clustering(
            X=X.values,
            labels=labels,
            model=model.named_steps.get("cluster")
        )

        results.append({
            "model": model_name,
            **metrics
        })

        plot_clusters_pca(
            X,
            labels,
            title=f"{model_name} clustering (PCA)"
        )

        plot_rfm_distributions(
            rfm,
            labels
        )

        plot_cluster_sizes(labels)

    results_df = pd.DataFrame(results)
    print("\nClustering results summary:")
    print(results_df)

    print(f"\nRunning FINAL model: KMeans (k={FINAL_N_CLUSTERS})")

    final_model = kmeans_model(n_clusters=FINAL_N_CLUSTERS)
    final_labels = final_model.fit_predict(X)

    rfm_final = rfm.copy()
    rfm_final["Cluster"] = final_labels

    cluster_profile = (
        rfm_final
        .groupby("Cluster")
        .agg({
            "Recency": ["mean", "median"],
            "Frequency": ["mean", "median"],
            "Monetary": ["mean", "median"],
            "CustomerID": "count"
        })
        .round(2)
    )
    print("\nFinal cluster profiles (RFM):")
    print(cluster_profile)

    cluster_names = {
    2: "VIP Customers",
    0: "Loyal Customers",
    3: "At-Risk Customers",
    1: "Inactive Customers"
}
    
    rfm_final["Segment"] = rfm_final["Cluster"].map(cluster_names)

    print("\nFinal segment distribution:")
    print(rfm_final["Segment"].value_counts())

    plot_clusters_pca(
        X,
        final_labels,
        title="Final customer segments (KMeans, PCA)",
        save_path=f"{IMAGES_DIR}/pca_clusters.png",
    )

    plot_rfm_distributions(
        rfm,
        final_labels,
        save_path=f"{IMAGES_DIR}/rfm_distributions.png",
    )

    plot_cluster_sizes(final_labels,
                       save_path=f"{IMAGES_DIR}/cluster_sizes.png",)
    
    plot_clusters_umap(
    X,
    final_labels,
    title="Final customer segments (UMAP)",
    save_path=f"{IMAGES_DIR}/umap_clusters.png",
)

    output_path = "data/processed/customer_segments.csv"
    rfm_final.to_csv(output_path, index=False)

    print(f"\nCustomer segments saved to: {output_path}")

if __name__ == "__main__":
    main()