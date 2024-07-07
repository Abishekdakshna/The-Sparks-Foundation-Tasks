# -*- coding: utf-8 -*-
"""Task-2 Clustering

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ksOjg4DYuvGopkknYG4hhbAoVIzZN3gO
"""

import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix
import scipy.cluster.hierarchy as sch
from sklearn.preprocessing import LabelEncoder

# Load the Iris dataset from a CSV file
df = pd.read_csv('/content/Iris.csv')

# Visualizing the input data using pair plot
print("Visualizing the input data:")
sns.pairplot(df, hue='Species', palette='bright')
plt.show()

# Preprocessing: Drop 'Id' and 'Species' columns, convert to numeric
if 'Id' in df.columns:
    df.drop(columns=['Id'], inplace=True)
df.drop(columns=['Species'], inplace=True)
df = df.apply(pd.to_numeric, errors='coerce')
df.dropna(inplace=True)

# Hierarchical clustering dendrogram
print("Visualizing the input data hierarchy using dendrogram:")
plt.figure(figsize=(10, 7))
dendrogram = sch.dendrogram(sch.linkage(df, method='ward'))
plt.title('Dendrogram')
plt.xlabel('Samples')
plt.ylabel('Euclidean Distances')
plt.show()

# Elbow method to find the optimum number of clusters
wcss = []  # Within-cluster sums of squares
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    kmeans.fit(df)
    wcss.append(kmeans.inertia_)

# Plot the elbow graph
plt.figure(figsize=(10, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.title('Elbow Method to Determine Optimum Number of Clusters')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.show()

# Apply k-means to the dataset with the optimal number of clusters (3)
optimal_clusters = 3
kmeans = KMeans(n_clusters=optimal_clusters, init='k-means++', max_iter=300, n_init=10, random_state=0)
y_kmeans = kmeans.fit_predict(df)

# Visualize the clusters
plt.figure(figsize=(10, 6))
plt.scatter(df.values[y_kmeans == 0, 0], df.values[y_kmeans == 0, 1], s=100, c='red', label='Cluster 1')
plt.scatter(df.values[y_kmeans == 1, 0], df.values[y_kmeans == 1, 1], s=100, c='blue', label='Cluster 2')
plt.scatter(df.values[y_kmeans == 2, 0], df.values[y_kmeans == 2, 1], s=100, c='green', label='Cluster 3')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='yellow', label='Centroids')
plt.title('Clusters of Iris Data')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()

# Visualize the clusters with all features using pair plot
df['Cluster'] = y_kmeans
sns.pairplot(df, hue='Cluster', palette='bright')
plt.show()

# Assuming the dataset has a 'Species' column for true labels
df = pd.read_csv('/content/Iris.csv')
true_labels = df['Species']
le = LabelEncoder()
true_labels = le.fit_transform(true_labels)

# Calculating accuracy and confusion matrix
accuracy = accuracy_score(true_labels, y_kmeans)
conf_matrix = confusion_matrix(true_labels, y_kmeans)

print(f"Accuracy: {accuracy}")
print("Confusion Matrix:")
print(conf_matrix)