import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ICmodel as icm
import discountIC as dic
import greedyIC as gic

def main():
    G = nx.gnm_random_graph(15000, 60000)
    print(list(nx.descendants(G,1)))
    return


if __name__ == "__main__":
    main()