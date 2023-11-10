import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import ICmodel as icm
import discountIC as dic
import greedyIC as gic

def run_model_with(G, k_max, p, mc, function):
    spread = []
    for k in tqdm(range(k_max)):
        S = function(k)
        spread.append(icm.IC(G, S, p, mc)[0])

    return spread

def main():
    G = nx.read_edgelist('data/Wiki-Vote.txt.gz', create_using=nx.DiGraph)

    k_max = 50
    p = 0.01
    mc = 20000

    algorithms = {'DegreeDiscountIC': lambda k: dic.DDIC(G, k, p),
                  'SingleDiscount': lambda k: dic.SD(G, k),
                  'Random': lambda k: dic.random_sd(G, k),
                #   greedy and new greedy are slow uncomment if you have some hours to spare
                #   'NewGreedy': lambda k: gic.NewGreedy(G, k, p),
                #   'Greedy': lambda k: gic.GeneralGreedy(G, k, p),
                }

    for name, algo in algorithms.items():
        data = run_model_with(G, k_max, p, mc, algo)
        plt.plot(data, label=name)

    plt.legend()
    plt.xlabel('seeds')
    plt.ylabel('influence spread')
    plt.show()

    return

if __name__ == "__main__":
    main()
