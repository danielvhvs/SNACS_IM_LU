"""
source: https://hautahi.com/ic_comparison
"""

import numpy as np


def propagate_nx(g, new_active):
    targets = []
    for node in new_active:
        targets += g.neighbors(node)

    return targets


def IC(graph_object, S, p, mc):
    """
    Inputs: graph_object: 4 possible network representations
                - igraph object
                - Networkx object
                - E x 2 Pandas dataframe of directed edges. Columns: ['source','target']
                - dictionary with key=source node & values=out-neighbors
            S:  List of seed nodes
            p:  Disease propagation probability
            mc: Number of Monte-Carlo simulations,
    Output: Average number of nodes influenced by seed nodes in S
    """

    # Loop over the Monte-Carlo Simulations
    spread = []
    for i in range(mc):
        # Simulate propagation process
        new_active, A = S[:], S[:]
        while new_active:
            # 1. Find out-neighbors for each newly active node
            targets = propagate_nx(graph_object, new_active)

            # 2. Determine newly activated neighbors (set seed and sort for consistency)
            np.random.seed(i)
            success = np.random.uniform(0, 1, len(targets)) < p
            new_ones = list(np.extract(success, sorted(targets)))

            # 3. Find newly activated nodes and add to the set of activated nodes
            new_active = list(set(new_ones) - set(A))
            A += new_active

        spread.append(len(A))

    return (np.mean(spread), A)


def RanCas(graph_object, S, p):
    """
    Inputs: graph_object: 4 possible network representations
                - igraph object
                - Networkx object
                - E x 2 Pandas dataframe of directed edges. Columns: ['source','target']
                - dictionary with key=source node & values=out-neighbors
            S:  List of seed nodes
            p:  Disease propagation probability
    Output: Number of random vertices influenced by S
    """

    # Simulate propagation process
    new_active, A = S[:], S[:]
    while new_active:
        # 1. Find out-neighbors for each newly active node
        targets = propagate_nx(graph_object, new_active)

        # 2. Determine newly activated neighbors (set seed and sort for consistency)
        np.random.seed(0)
        success = np.random.uniform(0, 1, len(targets)) < p
        new_ones = list(np.extract(success, sorted(targets)))

        # 3. Find newly activated nodes and add to the set of activated nodes
        new_active = list(set(new_ones) - set(A))
        A += new_active

    return A
