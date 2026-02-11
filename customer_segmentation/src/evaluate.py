from typing import Dict, Optional
import numpy as np

from sklearn.metrics import silhouette_score, davies_bouldin_score
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
