# MSCS-634 Lab 3: Clustering Analysis Using K-Means and K-Medoids Algorithms

## Purpose

This lab applies and compares two partitional clustering algorithms, K-Means and
K-Medoids, on the Wine dataset from `sklearn.datasets`. The dataset (178 samples, 13
chemical-analysis features, 3 known cultivar classes) is standardized and clustered
with k=3 using each algorithm, then evaluated with the Silhouette Score (how
well-separated the clusters are, using no labels) and the Adjusted Rand Index / ARI
(how well the clusters line up with the true cultivar labels). Results are visualized
side by side with PCA-projected scatter plots, and the two algorithms' cluster shapes
and quality are compared.

## Dataset

The Wine dataset is loaded directly from `sklearn.datasets.load_wine()` - no external
file is needed. It contains 178 wine samples described by 13 numeric features
(alcohol, malic acid, magnesium, flavanoids, color intensity, proline, etc.) and a
label for which of 3 cultivars each sample belongs to. The features were standardized
with z-score normalization (`StandardScaler`) before clustering, since they span very
different numeric ranges (e.g. `proline` is in the hundreds, `hue` is under 2).

## Setup

```
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook MSCS_634_Lab3.ipynb
```

## Files

- `MSCS_634_Lab3.ipynb` - the lab notebook (data loading/prep, K-Means clustering,
  K-Medoids clustering, PCA-based visualization and comparison), executed with outputs
  saved.
- `requirements.txt` - Python packages needed to run the notebook (see Setup above).

## Key insights

- **K-Means slightly outperformed K-Medoids on this dataset**: Silhouette Score 0.285
  vs. 0.268, and Adjusted Rand Index 0.897 vs. 0.741. Both metrics favor K-Means, and
  the ARI gap is fairly large, meaning K-Means' cluster assignments lined up with the
  true cultivar labels noticeably more often than K-Medoids' did.
- The standardized Wine features form fairly compact, roughly convex, similarly-sized
  groups once scaled - exactly the setting where K-Means' mean-based centroids tend to
  do well. K-Medoids' advantages (robustness to outliers/noise, no dependence on a
  well-defined mean) mattered less here since the data is clean, continuous, and
  already outlier-free.
- In the PCA-projected scatter plots, both algorithms recover the same broad
  three-group structure, but disagree on some points near the boundary between the two
  closer classes. K-Means centroids land at the geometric mean of each cluster
  (possibly in low-density space between points), while K-Medoids medoids are always
  actual samples, making them more directly interpretable as "typical" cluster members
  at the cost of being more sensitive to which specific point gets picked.
- The first 2 principal components used for visualization only capture about 55% of
  the total variance in the standardized 13-dimensional data, so the 2D plots are a
  simplification - both clustering algorithms were actually run on the full
  13-dimensional standardized data, not the PCA projection.

## Challenges and decisions

- **K-Medoids library:** the "textbook" `sklearn_extra.cluster.KMedoids` class fails to
  import on this environment (Python 3.14) because it depends on the `distutils`
  module, which was removed from the Python standard library in 3.12. Rather than
  downgrade Python, this lab uses the actively-maintained
  [`kmedoids`](https://pypi.org/project/kmedoids/) package, which implements
  FasterPAM - a modern, faster exact algorithm for the same K-Medoids problem
  (partition-around-medoids). It works on a precomputed pairwise distance matrix
  instead of raw feature vectors, which is why the notebook computes
  `pairwise_distances(X)` before calling `kmedoids.fasterpam(...)`.
- **Visualizing 13-dimensional clusters:** since the standardized dataset has 13
  features, it can't be plotted directly. PCA was used purely for the final
  visualization step (projecting down to 2 components) - clustering itself was always
  performed on the full 13-dimensional standardized data, so the plots are a 2D
  approximation of higher-dimensional cluster structure rather than the actual basis
  for clustering.
- **Fixed random_state:** `random_state=42` was used for `KMeans`, `fasterpam`, and
  `PCA` so the notebook produces the same clusters and plots on every run rather than
  varying between executions.
