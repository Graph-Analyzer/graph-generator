import numpy as np
from sklearn.cluster import KMeans


def calc_kmeans(
    coordinates: np.ndarray,
    clusters: int,
    seed: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    kmeans = KMeans(
        n_clusters=clusters,
        init="k-means++",
        n_init=1,
        random_state=seed,
    )
    kmeans.fit(coordinates)

    return kmeans.cluster_centers_, kmeans.labels_
