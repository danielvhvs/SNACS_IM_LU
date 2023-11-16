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

            GprimeEdges = list(np.extract(success, G.edges))
            Gprime = G.edge_subgraph(GprimeEdges)
            RsL = [nx.descendants(Gprime,node) for node in seed]
            Rs = set(x for lst in RsL for x in lst)
            for j in G.nodes():
                if j in Rs or j in seed:
                    continue
                s[j] += len(nx.descendants(Gprime,j))
        seed.append(max(s, key=lambda key: s[key]))
    return seed

import networkx as nx
import heapq

def independent_cascade_model(graph, seeds):
    """
    Simulates the independent cascade model on the graph with the given seed nodes.
    Returns the set of activated nodes.
    """
    activated_nodes = set(seeds)
    newly_activated = set(seeds)

    while newly_activated:
        newly_activated_next = set()

        for node in newly_activated:
            neighbors = set(graph.neighbors(node)) - activated_nodes
            for neighbor in neighbors:
                if should_activate(graph, node, neighbor):
                    newly_activated_next.add(neighbor)

        activated_nodes.update(newly_activated_next)
        newly_activated = newly_activated_next

    return activated_nodes

def should_activate(graph, source, target):
    """
    Determines whether the target node should be activated by the source node in the independent cascade model.
    Returns True if activation occurs, False otherwise.
    """
    probability = graph[source][target].get('probability', 0.1)  # default probability is 0.1
    return random.random() < probability

def celf(graph, k):
    """
    Finds a seed set with k nodes using the CELF algorithm for influence maximization.
    Returns the seed set and its influence spread.
    """
    heap = []
    seed_set = set()

    for node in graph.nodes:
        marginal_gain = calculate_marginal_gain(graph, seed_set, node)
        heapq.heappush(heap, (-marginal_gain, node))

    for _ in range(k):
        current_node = heapq.heappop(heap)[1]
        seed_set.add(current_node)

        for node in graph.nodes:
            if node not in seed_set:
                marginal_gain = calculate_marginal_gain(graph, seed_set, node)
                heapq.heappush(heap, (-marginal_gain, node))

    influence_spread = len(independent_cascade_model(graph, seed_set))
    return seed_set, influence_spread

def calculate_marginal_gain(graph, seed_set, node):
    """
    Calculates the marginal gain of adding a node to the seed set.
    """
    if node in seed_set:
        return 0

    current_influence = len(independent_cascade_model(graph, seed_set))
    new_seed_set = seed_set.copy()
    new_seed_set.add(node)
    new_influence = len(independent_cascade_model(graph, new_seed_set))

    return new_influence - current_influence

# Example usage:
# Create a graph (you can replace this with your own graph)
G = nx.erdos_renyi_graph(100, 0.1)

# Set edge probabilities (you can replace this with your own probabilities)
for edge in G.edges():
    G[edge[0]][edge[1]]['probability'] = 0.2

# Find a seed set with k nodes using CELF algorithm
k = 5
seed_set, influence_spread = celf(G, k)

print(f"Seed set: {seed_set}")
print(f"Influence spread: {influence_spread}")
