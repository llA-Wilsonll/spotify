"""
The purpose of this code is to perform clustering on the dataset of
The Beatles tracks that was prepared in process_dataset.py
More specifically:
    - Visualise the input data
    - Perform clustering analysis on the data
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
# from sklearn.cluster import MeanShift
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.preprocessing import normalize

# Changing settings so that whole DataFrame can be printed
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


"""
Prepare data set for modelling
"""
# Track Features
track_features_df = pd.read_pickle("./data/processed/track_features_processed.pkl")
print(track_features_df.columns)

# Extracting the features we want to perform cluster analysis on
data = track_features_df.loc[:, ['danceability', 'energy', 'key', 'loudness', 'mode',
                                 'speechiness', 'acousticness', 'instrumentalness', 'liveness',
                                 'valence', 'tempo', 'duration_ms']]

# Normalising the input data so the features are on the same scale
data_scaled = normalize(data, axis=0)
# Converting numpy array to pandas DataFrame
data_scaled = pd.DataFrame(data_scaled, columns=data.columns)


"""
Using KMeans and specifying 2 clusters
- To analyse whether the top songs get grouped together
"""
kmeans = KMeans(n_clusters=2, random_state=0)
kmeans.fit(data_scaled)
print(kmeans.labels_)


"""
Using Spectral Clustering and specifying 2 clusters
- To analyse whether the top songs get grouped together
"""
sc = SpectralClustering(n_clusters=2, assign_labels="discretize", random_state=0)
sc.fit(data_scaled)
print(sc.labels_)


"""
Joining cluster labels from KMeans and Spectral Clustering back onto base DataFrame
"""
track_features_df['cluster_kmeans'] = kmeans.labels_
track_features_df['cluster_sc'] = 1- sc.labels_
print(track_features_df)

# Converting columns to numeric before using describe
track_features_df[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                  'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']] = \
    track_features_df[['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
                       'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms']].apply(pd.to_numeric)

print("Describing observations in '0' cluster (using Spectral Clustering)")
print(track_features_df.loc[track_features_df['cluster_sc'] == 0, :].describe())
print("Describing observations in '1' cluster (using Spectral Clustering)")
print(track_features_df.loc[track_features_df['cluster_sc'] == 1, :].describe())


"""
Finding which variables contributed most to cluster splits
(maybe this is equivalent to finding which features vary most between clusters and least within the clusters)
"""


"""
Cluster Analysis on only two variables (for visualisation purposes)
"""


"""
Using Mean Shift 
"""
# ms = MeanShift()
# ms.fit(data_scaled)
# labels = ms.labels_
# cluster_centers = ms.cluster_centers_
#
# print(cluster_centers)
#
# n_clusters_ = len(np.unique(labels))
#
# print("Number of estimated clusters:", n_clusters_)

# plt.figure(figsize=(10, 7))
# plt.title("Dendrograms")
# dend = shc.dendrogram(shc.linkage(data_scaled, method='ward'))
# plt.show()

# plt.figure(figsize=(10, 7))
# plt.scatter(track_features_df['danceability'], track_features_df['energy'], track_features_df['liveness'])
# plt.show()
