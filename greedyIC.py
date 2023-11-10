import numpy as np
import networkx as nx
import ICmodel as IC

def GeneralGreedy(G: nx.Graph, k: int, p: int = 0.01) -> list[int]:
    R = 20000
    seed = []
    for _ in range(k):
        s = {}
        for v in G.nodes():
            if v in seed:
                continue
            s[v] = IC.IC(G,seed + [v],p,R)[0]
        seed.append(max(s, key=lambda key: s[key]))
    return seed

def NewGreedy(G: nx.Graph, k: int, p: int = 0.01) -> list[int]:
    R = 20000
    seed = []
    for _ in range(k):
        s = dict.fromkeys(list(G.nodes), 0)
        for i in range(R):
            np.random.seed(i)
            success = np.random.uniform(0,1,len(G.edges)) < p
            GprimeEdges = list(np.extract(success, G.edges))
            Gprime = G.edge_subgraph(GprimeEdges)
            Rs = list(nx.descendants(Gprime,seed))
            for j in G.nodes():
                if j in Rs or j in seed:
                    continue
                s[j] += len(nx.descendants(Gprime,j))
        seed.append(max(s, key=lambda key: s[key]))
    return seed
