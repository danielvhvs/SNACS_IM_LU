import networkx as nx
from queue import PriorityQueue

def LFV(G: nx.Graph, u, p=0.01):
    val = 0
    for v in G.neighbors(u):
        val += p + (p * (p * len(set(G.neighbors(v)) - {u, v})))
    return val

def EIOS(G, S, SN, lfvlist: list, p=0.01):
    lfv = dict(lfvlist)
    ret = 0
    for u in S:
        val = 0
        im = 1 - p
        for _ in set(S) - {u}:
            im *= 1 - p
        for v in SN:
            val += p * lfv[v] * im
        ret += val
    return val

def select_source(G, pop, lfvlist):
    SN = set()

    lfv = list(lfvlist)

    for i in range(pop):
        new_source = max(lfv, key=lambda x: x[1])
        SN = SN | {new_source[0]}
        lfv.remove(new_source)
    return SN

def seek_ancestor_MAP(G: nx.Graph|nx.DiGraph, SN, thr, p=0.01):
    R = set()
    MAP = {}
    for v in SN:
        maxAP = {}.fromkeys(G.nodes(), 0)
        Q = PriorityQueue()
        maxAP[v] = 1
        visit = {}.fromkeys(G.nodes(), False)
        Q.put((-maxAP[v], v))

        while Q.qsize() > 0:
            u = Q.get()[1]
            if visit[u]:
                continue
            visit[u] = True
            new_ap = maxAP[u] * p
            for n in G.predecessors(u):
                if new_ap > thr:
                    R = R | {n}
                    if new_ap > maxAP[n] and not visit[n]:
                        maxAP[n] = new_ap
                        Q.put((-maxAP[n], n))
        MAP[v] = maxAP
    return R, MAP

def filter_candidates(G, SN, R: set, MAP, k, lfvlist):
    C = set()
    for _ in range(0, 2 * k):
        C = C | {max([(v, EIOS(G, v, SN, lfvlist)) for v in (R - C)], key=lambda x: x[1])[0]}
    return C

def select_seed(G, C, SN, MAP, k, lfvlist):
    S = set()
    Q = PriorityQueue()
    T = {}
    for v in C:
        inf = EIOS(G, {v}, SN, lfvlist)
        T[v] = 0
        Q.put((-inf, v))
    v = Q.get()[1]
    S = S | {v}
    for i in range(1, k):
        for j in range(0, 2 * k):
            v = Q.get()[1]
            if T[v] == i:
                S = S | {v}
                break
            else:
                Sv = EIOS(G, S | {v}, SN, lfvlist) - EIOS(G, S, SN, lfvlist)
                Q.put((-Sv, v))
                T[v] = i
    return list(S)


def LGIM(G: nx.DiGraph | nx.Graph, k, p=0.01):
    lowbound = 100
    upperbound = 600
    if isinstance(G, nx.DiGraph):
        threshold = 1 / max(G.in_degree(), key=lambda x: x[1])[1]
    elif isinstance(G, nx.Graph):
        threshold = 1 / max(G.degree(), key=lambda x: x[1])[1]

    x = 2 * G.number_of_edges() / G.number_of_nodes()
    pop = int(G.number_of_nodes() // (1 + x + x**2))

    pop = lowbound if pop <= lowbound else upperbound if pop >= upperbound else pop

    lfvlist = [(v, LFV(G, v)) for v in G.nodes]

    SN = select_source(G, pop, lfvlist)
    R, MAP = seek_ancestor_MAP(G, SN, threshold)
    C = filter_candidates(G, SN, R, MAP, k, lfvlist)
    S = select_seed(G, C, SN, MAP, k, lfvlist)
    return S
