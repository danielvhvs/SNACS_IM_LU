import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def random_sd(G: nx.Graph, k):
    return [random.randint(0, G.number_of_nodes()-1) for _ in range(k)]

def get_d(degree: list[list]|list[tuple]|nx.classes.reportviews.DegreeView) -> list:
    '''Get a list of degrees from a (converted) DegreeView'''
    return [d for v, d in degree]

def get_v(degree: list[list]|list[tuple]|nx.classes.reportviews.DegreeView) -> list:
    '''Get a list of verteces from a (converted) DegreeView'''
    return [v for v, d in degree]


def SD(G: nx.Graph, k: int) -> list[int]:
    seed = []

    dd = [list(d) for d in G.degree()]

    for _ in range(k):
        u = dd.pop(np.argmax(get_d(dd)))[0]
        seed.append(u)
        for v in G.neighbors(u):
            if v in seed:
                break
            for w in G.neighbors(v):
                if w in seed:
                    dd[get_v(dd).index(v)][1] -= 1

    return seed

def DDIC(G: nx.Graph, k: int,p: int = 0.01) -> list[int]:
    seed = []
    t = np.zeros(len(G))

    dd = [list(d) for d in G.degree()]

    for _ in range(k):
        u = dd.pop(np.argmax(get_d(dd)))[0]
        seed.append(u)
        for v in G.neighbors(u):
            if v in seed:
                break
            t[v] += 1
            d_v = G.degree(v)
            dd[get_v(dd).index(v)][1] = d_v - 2*t[v] - (d_v - t[v])*t[v]*p

    return seed