import os
import json
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
import numpy as np
data = []
with open('results/gpt_results.jsonl', 'r') as f:
    for line in f:
        data.append(json.loads(line))
questions = []
for d in data:
    questions.append(d['response']['body']['choices'][0]['message']['content'])


if os.path.exists('embeddings.npy'):
    with open('embeddings.npy', 'rb') as f:
        embeddings = np.load(f)
else:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = embedder.encode(questions, show_progress_bar=True)

    with open('embeddings.npy', 'wb') as f:
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
