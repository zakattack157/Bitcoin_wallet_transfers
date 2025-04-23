import pandas as pd
import networkx as nx
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt

# Load data
nodes_df = pd.read_csv("nodes.csv")  # Must have Id + modularity_class
edges_df = pd.read_csv("edges.csv")  # Must have Source + Target

# Create full graph
G = nx.from_pandas_edgelist(edges_df, source="Source", target="Target")
modularity_dict = dict(zip(nodes_df["Id"], nodes_df["modularity_class"]))
nx.set_node_attributes(G, modularity_dict, "modularity_class")

# Choose community to analyze
community_id = 104

# Extract nodes in this community
community_nodes = [n for n, d in G.nodes(data=True) if d.get("modularity_class") == community_id]
G_sub = G.subgraph(community_nodes)

# Adjacency matrix for community
A = nx.to_numpy_array(G_sub, nodelist=community_nodes)
labels = community_nodes

# Distance matrix (cosine distance between node connection vectors)
dist_matrix = pdist(A, metric="cosine")
linked = linkage(dist_matrix, method='ward')

# Plot dendrogram
plt.figure(figsize=(12, 6))
dendrogram(linked, labels=labels, leaf_rotation=90)
plt.title(f"Dendrogram for Community {community_id}")
plt.xlabel("Node ID")
plt.ylabel("Cosine Distance")
plt.tight_layout()
plt.show()
