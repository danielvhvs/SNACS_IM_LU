import networkx as nx


def NAV(G: nx.Graph, u, p=0.01):
    val = 0
    for v in G.neighbors(u):
        val += p + (p * (p * len(set(G.neighbors(v)) - {u, v})))
    return val


def EIOS(G, S, SN, p=0.01):
    ret = 0

    for u in S:
        val = 0

        im = 1 - p

        for _ in set(S) - {u}:
            im *= 1 - p

        for v in SN:
            val += p * NAV(G, v) * im

        ret += val
    return val


def select_source(G, pop):
    SN = set()

    navlist = [(v, NAV(G, v)) for v in G.nodes]

    for i in range(1, pop):
        new_source = max(navlist, key=lambda x: x[1])

        SN = SN | {new_source[0]}

        navlist.remove(new_source)
    return SN


def seek_ancestor_MAP(G, SN, thr, p=0.01):
    R = set()
    MAP = {}
    for v in SN:
        maxAP = {}.fromkeys(G.nodes(), 0)
        Q = []
        maxAP[v] = 1
        visit = {}.fromkeys(G.nodes(), False)
        Q.append((v, maxAP[v]))

        while len(Q) > 0:
            u, ap = Q.pop()
            if visit[u] == True:
                continue
            visit[u] = True
            for n in G.neighbors(u):
                new_ap = maxAP[u] * p
                if new_ap > thr:
                    R = R | {n}
                    if new_ap > maxAP[n] and visit[n] == False:
                        maxAP[n] = new_ap
                        Q.append((n, maxAP[n]))
                        Q.sort(key=lambda x: x[1], reverse=True)
        MAP[v] = maxAP
    return R, MAP


def filter_candidates(G, SN, R: set, MAP, k):
    C = set()
    for _ in range(2 * k):
        C = C | {max([(v, EIOS(G, v, SN)) for v in (R - C)], key=lambda x: x[1])[0]}
    return C


def select_seed(G, C, SN, MAP, k):
    S = set()
    Q = []
    T = {}
    for v in C:
        inf = EIOS(G, {v}, SN)
        T[v] = 0
        Q.append((v, -inf))
        Q.sort()
    v = Q.pop()[0]
    S = S | {v}
    for i in range(2, k):
        for j in range(1, 2 * k):
            v = Q.pop()[0]
            if T[v] == i:
                S = S | {v}
                break
            else:
                Sv = EIOS(G, S | {v}, SN) - EIOS(G, S, SN)
                Q.append((v, -Sv))
                Q.sort()
                T[v] = i
    return S


def LGIM(G: nx.DiGraph | nx.Graph, k, p=0.01):
    lowbound = 1
    upperbound = 100
    S = set()
    if type(G) == nx.DiGraph:
        threshold = 1 / max(G.in_degree(), key=lambda x: x[1])[1]
    elif type(G) == nx.Graph:
        threshold = 1 / max(G.degree(), key=lambda x: x[1])[1]

    x = 2 * G.number_of_edges() / G.number_of_nodes()
    pop = int(G.number_of_nodes() // (1 + x + x**2))
    print(pop)

    pop = lowbound if pop <= lowbound else upperbound if pop >= upperbound else pop

    SN = select_source(G, pop)
    R, MAP = seek_ancestor_MAP(G, SN, threshold)
    C = filter_candidates(G, SN, R, MAP, k)
    S = select_seed(G, C, SN, MAP, k)
    return S
