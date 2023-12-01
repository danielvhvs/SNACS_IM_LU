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


def CELFgreedy(G,k,p=0.01,mc=1000):  
    """
    Input:  graph object, number of seed nodes
    Output: optimal seed set, resulting spread, time for each iteration
    """
    # --------------------
    # Find the first node with greedy algorithm
    # --------------------
    # Calculate the first iteration sorted list
    marg_gain = [IC.IC(G,[node],p,mc)[0] for node in G.nodes]

    # Create the sorted list of nodes and their marginal gain 
    Q = sorted(zip(list(G.nodes),marg_gain), key=lambda x: x[1],reverse=True)

    # Select the first node and remove from candidate list
    S, spread = [Q[0][0]], Q[0][1]
    Q = Q[1:]
    
    # --------------------
    # Find the next k-1 nodes using the list-sorting procedure
    # --------------------
    for _ in range(k-1):    
        check, node_lookup = False, 0
        while not check:
            # Count the number of times the spread is computed
            node_lookup += 1
            
            # Recalculate spread of top node
            current = Q[0][0]
            
            # Evaluate the spread function and store the marginal gain in the list
            Q[0] = (current,IC.IC(G,S+[current],p,mc)[0] - IC.IC(G,S,p,mc)[0] )

            # Re-sort the list
            Q = sorted(Q, key = lambda x: x[1], reverse = True)

            # Check if previous top node stayed on top after the sort
            check = (Q[0][0] == current)

        # Select the next node
        spread += Q[0][1]
        S.append(Q[0][0])

        # Remove the selected node from the list
        Q = Q[1:]
    return S

def MixedGreedy(G,k,p=0.01,mc=1000):  
    """
    Input:  graph object, number of seed nodes
    Output: optimal seed set, resulting spread, time for each iteration
    """
    # --------------------
    # Find the first node with greedy algorithm
    # --------------------
    # Calculate the first iteration sorted list
    
    s = dict.fromkeys(list(G.nodes), 0)
    for i in range(mc):
        np.random.seed(i)
        success = np.random.uniform(0,1,len(G.edges)) < p
        x = list(G.edges)
        GprimeEdges = [x[t] for t in range(len(x)) if success[t]]
        Gprime = G.edge_subgraph(GprimeEdges)
        for j in G.nodes:
            try:
                s[j] += len(nx.descendants(Gprime,j))
            except nx.NetworkXError:
                s[j] += 0
        
    marg_gain = [s[node] for node in G.nodes]
    
    # Create the sorted list of nodes and their marginal gain 
    Q = sorted(zip(list(G.nodes),marg_gain), key=lambda x: x[1],reverse=True)

    # Select the first node and remove from candidate list
    S, spread = [Q[0][0]], Q[0][1]
    Q = Q[1:]
    
    # --------------------
    # Find the next k-1 nodes using the list-sorting procedure
    # --------------------
    for _ in range(k-1):    
        check, node_lookup = False, 0
        while not check:
            # Count the number of times the spread is computed
            node_lookup += 1
            
            # Recalculate spread of top node
            current = Q[0][0]
            
            # Evaluate the spread function and store the marginal gain in the list
            Q[0] = (current,IC.IC(G,S+[current],p,mc)[0] - IC.IC(G,S,p,mc)[0] )

            # Re-sort the list
            Q = sorted(Q, key = lambda x: x[1], reverse = True)

            # Check if previous top node stayed on top after the sort
            check = (Q[0][0] == current)

        # Select the next node
        spread += Q[0][1]
        S.append(Q[0][0])

        # Remove the selected node from the list
        Q = Q[1:]
    return S
