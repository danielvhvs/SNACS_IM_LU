import numpy as np
import networkx as nx
import ICmodel as IC
import random

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
            x = list(G.edges)
            GprimeEdges = [x[t] for t in range(len(x)) if success[t]]
            Gprime = G.edge_subgraph(GprimeEdges)
            RsL = [nx.descendants(Gprime,node) for node in seed]
            Rs = set(x for lst in RsL for x in lst)
            for j in G.nodes:
                if j in Rs or j in seed:
                    continue
                try:
                    s[j] += len(nx.descendants(Gprime,j))
                except nx.NetworkXError:
                    s[j] += 0
        seed.append(max(s, key=lambda key: s[key]))
    return seed


# def CELFgreedy(G,k,R):
