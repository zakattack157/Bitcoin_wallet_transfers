import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# Load edges and build the graph
edges_df = pd.read_csv("edges.csv")
G_original = nx.from_pandas_edgelist(edges_df, source="Source", target="Target")
total_nodes = len(G_original)

# === Generalized simulation ===
def run_removal_simulation(G, strategy="degree", steps=30):
    G = G.copy()
    sizes = []

    # Choose the node removal strategy
    if strategy == "degree":
        node_order = sorted(G.degree, key=lambda x: x[1], reverse=True)
    elif strategy == "betweenness":
        print("Calculating betweenness centrality... (can take a minute)")
        bc = nx.betweenness_centrality(G)
        node_order = sorted(bc.items(), key=lambda x: x[1], reverse=True)
    else:
        raise ValueError("Unsupported strategy.")

    node_order = [n for n, _ in node_order]

    for i in range(0, total_nodes, total_nodes // steps):
        G_sim = G.copy()
        to_remove = node_order[:i]
        G_sim.remove_nodes_from(to_remove)
        if len(G_sim) == 0:
            sizes.append(0)
        else:
            largest_cc = max(nx.connected_components(G_sim), key=len)
            sizes.append(len(largest_cc))
    return [i / total_nodes for i in range(0, total_nodes, total_nodes // steps)], sizes

# === Run both simulations ===
deg_x, deg_y = run_removal_simulation(G_original, strategy="degree")
bc_x, bc_y = run_removal_simulation(G_original, strategy="betweenness")

# === Plot ===
plt.figure(figsize=(10, 6))
plt.plot(deg_x, deg_y, label="Degree Attack", marker='o')
plt.plot(bc_x, bc_y, label="Betweenness Attack", marker='s')
plt.xlabel("Fraction of Nodes Removed")
plt.ylabel("Size of Largest Connected Component")
plt.title("Breakdown Comparison: Degree vs Betweenness Centrality")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
