from typing import Dict, Optional, List
import numpy as np
import pandas as pd

from sklearn.metrics import silhouette_score, davies_bouldin_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def evaluate_clustering(
        X: np.ndarray,
        labels: np.ndarray,
        model=None) -> Dict[str, Optional[float]]:
    """
    Evaluate clustering results using internal metrics.

    Parameters
    ----------
    X : np.ndarray
        Feature matrix used for clustering.
    labels : np.ndarray
        Cluster labels assigned to each sample.
    model : optional
        Fitted clustering model (used for inertia if available).

    Returns
    -------
    dict
        Dictionary with clustering evaluation metrics.
    """

    metrics = {
        "silhouette_score": None,
        "davies_bouldin_index": None,
        "inertia": None
    }

    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    if n_clusters > 1:
        metrics["silhouette_score"] = silhouette_score(X, labels)
        metrics["davies_bouldin_index"] = davies_bouldin_score(X, labels)

    if isinstance(model, KMeans):
        metrics["inertia"] = model.inertia_

    return metrics

def kmeans_cluster_analysis(
        X: pd.DataFrame,
        k_range: range,
        random_state: int = 42
) -> pd.DataFrame:
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    results = []

    for k in k_range:
        model = KMeans(n_clusters=k, random_state=random_state)
        labels = model.fit_predict(X_scaled)

        results.append({
            "k": k,
            "inertia": model.inertia_,
            "silhouette_score": silhouette_score(X_scaled, labels)
        })

    return pd.DataFrame(results)
