import pandas as pd

from src.data_processing import preprocess_data
from src.models import MODELS
from src.evaluate import evaluate_clustering
from src.visualization import (
    plot_clusters_pca,
    plot_rfm_distributions,
    plot_cluster_sizes
)

DATA_PATH = "data/raw/online_retail.csv"
FEATURE_COLUMNS = ["Recency", "Frequency", "Monetary"]

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

if __name__ == "__main__":
    main()