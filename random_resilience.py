import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import random

# === Load your data ===
edges_df = pd.read_csv("edges.csv")
G_original = nx.from_pandas_edgelist(edges_df, source="Source", target="Target")
total_nodes = len(G_original)

# === Simulation function ===
def run_removal_simulation(G, strategy="random", steps=30):
    G = G.copy()
    sizes = []
    node_order = []

    if strategy == "attack":
        # Degree-based attack
        node_order = sorted(G.degree, key=lambda x: x[1], reverse=True)
        node_order = [n for n, _ in node_order]
    elif strategy == "random":
        node_order = list(G.nodes())
        random.shuffle(node_order)
    else:
        raise ValueError("Strategy must be 'random' or 'attack'.")

    for i in range(0, total_nodes, total_nodes // steps):
        to_remove = node_order[:i]
        G.remove_nodes_from(to_remove)
        if len(G) == 0:
            sizes.append(0)
        else:
            largest_cc = max(nx.connected_components(G), key=len)
            sizes.append(len(largest_cc))
    return [i / total_nodes for i in range(0, total_nodes, total_nodes // steps)], sizes

# === Breakdown point finder ===
def find_breakdown_point(sizes, total_nodes):
    for i, size in enumerate(sizes):
        if size < 0.5 * total_nodes:
            return i
    return None

# === Run simulations ===
rand_x, rand_y = run_removal_simulation(G_original, "random")
atk_x, atk_y = run_removal_simulation(G_original, "attack")
rand_break = find_breakdown_point(rand_y, total_nodes)
atk_break = find_breakdown_point(atk_y, total_nodes)

# === Plot results ===
plt.figure(figsize=(10, 6))
plt.plot(rand_x, rand_y, label="Random Failure", marker='o')
plt.plot(atk_x, atk_y, label="Targeted Attack", marker='s')

if rand_break is not None:
    plt.axvline(rand_x[rand_break], color='blue', linestyle='--', label='Random Breakdown', alpha=0.5)
if atk_break is not None:
    plt.axvline(atk_x[atk_break], color='red', linestyle='--', label='Attack Breakdown', alpha=0.5)

plt.xlabel("Fraction of Nodes Removed")
plt.ylabel("Size of Largest Connected Component")
plt.title("Breakdown Threshold: Random vs Targeted")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
