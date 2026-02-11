from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering

def kmeans_model(n_clusters: int=4, random_state=42) -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("cluster", KMeans(
            n_clusters=n_clusters,
            random_state=random_state
        ))
    ])

def agglomerative_model(n_clusters: int=4) -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("cluster", AgglomerativeClustering(
            n_clusters=n_clusters,
            linkage="ward"
        ))
    ])

def dbscan_model(eps: float = 0.5, min_samples: int = 5) -> Pipeline:
    return Pipeline([
        ("scaler", StandardScaler()),
        ("cluster", DBSCAN(
            eps=eps,
            min_samples=min_samples
        ))
    ])

MODELS = {
    "KMeans": kmeans_model,
    "Agglomerative": agglomerative_model,
    "DBSCAN": dbscan_model
}