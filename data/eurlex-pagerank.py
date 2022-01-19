import sys, csv
import networkx as nx
from networkx.algorithms.link_analysis.pagerank_alg import pagerank
from time import time

textsFilePath = sys.argv[1]
docsFilePath  = sys.argv[2]

keys = set()
with open(textsFilePath) as f:
    for line in f:
        keys.add(line.strip())

r = csv.reader(open(docsFilePath, 'r'))
w = csv.writer(sys.stdout)

columns = next(r)
celex_idx = columns.index("celex")
legal_basis_idx = columns.index("legal_basis")
relationships_idx = columns.index("relationships")

adj = dict()
rows = []

for row in r:
    celex = row[celex_idx]
    if celex not in keys: continue

    rows.append([celex])
    legal_basis = set(row[legal_basis_idx].split(";"))
    relationships = set(row[relationships_idx].split(";"))
    adjacent = set.union(legal_basis, relationships)
    adj[celex] = adjacent & keys

print("Generating graph", file=sys.stderr)

G = nx.Graph()
G.add_nodes_from(keys)
for u in keys:
    for v in adj[u]:
        assert u in G
        assert v in G
        G.add_edge(u, v)

print(f"Graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges", file=sys.stderr)

print("Starting PageRank", file=sys.stderr)

start = time()
rankVector = pagerank(G, alpha=0.85, max_iter=500, tol=1e-19)
finish = time()

print(f"Done PageRank, took {finish-start:.3f}s; got {len(rankVector)} ranks out of {len(rows)} documents", file=sys.stderr)

w.writerow(["celex", "rank"])

for row in rows:
    celex = row[celex_idx]
    rank = rankVector[celex]
    w.writerow([celex, f"{rank:.15f}"])
