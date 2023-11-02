import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ICmodel as IC

def GeneralGreedy(G: nx.Graph, k: int) -> list[int]:
    R = 20000
    seed = []
    for _ in range(k):
        s = np.zeros(len(G))
        for i in range(len(s)):
            if i in seed:
                continue
            s[i] += IC.IC(G,seed + [i],0.01,R)
        seed.append(np.argmax(s))
    return seed

def GeneralGreedy(G: nx.Graph, k: int,p: int = 0.01) -> list[int]:
    R = 20000
    seed = []
    for _ in range(k):
        s = np.zeros(len(G))
        for i in range(R):
            np.random.seed(i)
            success = np.random.uniform(0,1,len(G.edges)) < p
            GprimeEdges = list(np.extract(success, G.edges))
            Gprime = G.edge_subgraph(GprimeEdges)
            Rs = list(nx.descendants(Gprime,seed))
            for j in range(s):
                if j in Rs or j in seed:
                    continue
                s[j] += len(nx.descendants(Gprime,j))
        seed.append(np.argmax(s))
    return seed


