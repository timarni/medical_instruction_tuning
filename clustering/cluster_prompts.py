# Script to convert prompts into embeddings and cluster them
# Script from Bastien

import os
import json
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
import numpy as np
data = []

name_of_prompts = "task_x_subtopics"
path_to_prompts = "../results/parsed_prompts_" + name_of_prompts + ".json"
path_to_embeddings = "embeddings_pp_" + name_of_prompts + ".npy"

# Control test mode
test_mode = True  # Set to False to load all data

# Load prompts
with open(path_to_prompts, 'r') as f:
    for i, line in enumerate(f):
        if test_mode and i >= 5:  # Only load first 5 entries in test mode
            break
        data.append(json.loads(line))

questions = []
for d in data:
    questions.append(d['prompt'])


if os.path.exists(path_to_embeddings):
    with open(path_to_embeddings, 'rb') as f:
        embeddings = np.load(f)
else:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embedder.encode(questions, show_progress_bar=True)

    with open(path_to_embeddings, 'wb') as f:
        np.save(f, embeddings)

# Reduce dimensionality to 5 or 10 dimensions
umap_reducer = umap.UMAP(n_components=5, random_state=42)
reduced_embeddings = umap_reducer.fit_transform(embeddings)

clusterer = hdbscan.HDBSCAN(min_cluster_size=5, min_samples=1, metric='euclidean')
cluster_labels = clusterer.fit_predict(reduced_embeddings)

# Print the clusters and their associated sentences
num_clusters = len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)  # Exclude noise label (-1)
print(f"Number of clusters found: {num_clusters}")

print("I found that the users often ask about the same thing, I don't know what to do with this information, maybe we only use one question per cluster ? We'll see, but first interesting thing to note")
# Print sentences grouped by clusters
for cluster in range(num_clusters):
    # Find indices of elements belonging to the current cluster
    cluster_indices = [i for i, label in enumerate(cluster_labels) if label == cluster]
    
    # Only print out small clusters
    if len(cluster_indices) <= 4:
        print(f"Cluster {cluster} (size: {len(cluster_indices)}):")
        for i in cluster_indices:
            print(f" - {questions[i]}")

import matplotlib.pyplot as plt

# Reduce to 2D for visualization
umap_2d = umap.UMAP(n_components=2, random_state=42)
embedding_2d = umap_2d.fit_transform(embeddings)

# Plot clusters
plt.figure(figsize=(10, 8))
plt.scatter(embedding_2d[:, 0], embedding_2d[:, 1], c=cluster_labels, cmap='Spectral', s=50)
plt.colorbar()
plt.title("Sentence Clusters based on Sentence Embeddings (I haven't found this useful honestly)")
plt.show()
