import sys, csv
import networkx as nx
from networkx.algorithms.link_analysis.pagerank_alg import pagerank
from time import time

r = csv.reader(sys.stdin)
w = csv.writer(sys.stdout)

columns = next(r)
celex_idx = columns.index("celex")
legal_basis_idx = columns.index("legal_basis")
relationships_idx = columns.index("relationships")

adj = dict()
rows = []

for row in r:
    rows.append(row)
    celex = row[celex_idx]
    legal_basis = set(row[legal_basis_idx].split(";"))
    relationships = set(row[relationships_idx].split(";"))
    adjacent = set.union(legal_basis, relationships)
    adj[celex] = adjacent

print("Making edges consistent", file=sys.stderr)

keys = set(adj.keys())
for k in keys:
    adj[k] = adj[k] & keys

print("Generating graph", file=sys.stderr)

G = nx.Graph()
G.add_nodes_from(keys)
for u in keys:
    for v in adj[u]:
        G.add_edge(u, v)

print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges", file=sys.stderr)

print("Starting PageRank", file=sys.stderr)

start = time()
rank = pagerank(G, alpha=0.85, max_iter=1000, tol=1e-19)
finish = time()

print(f"Done PageRank, took {finish-start:.3f}s; got {len(rank)} ranks out of {len(rows)} documents", file=sys.stderr)

columns.append("rank")
w.writerow(columns)

for row in rows:
    celex = row[celex_idx]
    row.append(f"{rank[celex]:.15f}")
    w.writerow(row)
