import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
import ICmodel as icm
import discountIC as dic
import greedyIC as gic
import imm
import LGIM
import time
import numpy as np

def run_model_with(G, k_max, p, mc, function):
    spread = []
    seed_list = []
    time_list = []
    for k in tqdm(range(k_max)):
        start = time.time()
        S = function(k)
        end = time.time()
        seed_list.append(S)
        time_list.append((end-start)*1000)
        spread.append(icm.IC(G, S, p, mc)[0])
    return spread,seed_list,time_list

def save_runs(algorithms,G,k_max,p,mc,path):
    for name, algo in algorithms.items():
        spread,seed_list,time_list = run_model_with(G, k_max, p, mc, algo)
        with open(path+name+".txt","w") as fwrite:
            fwrite.write(f"{spread[0]}")
            for i in range(1,len(spread)):
                fwrite.write(f"\t{spread[i]}")
            fwrite.write(f"\n")
            fwrite.write(f"{time_list[0]}")
            for i in range(1,len(time_list)):
                fwrite.write(f"\t{time_list[i]}")
            fwrite.write(f"\n")
            for i in range(len(seed_list)):
                fwrite.write(f"{seed_list[i][0]}")
                for j in range(1,len(seed_list[i])):
                    fwrite.write(f"\t{time_list[i][j]}")
                fwrite.write(f"\n")
            fwrite.close()
    return

def main():
    np.random.seed(42)
    G = nx.read_edgelist('./data/wiki-Vote.txt.gz', create_using=nx.DiGraph)

    k_max = 50
    p = 0.01
    mc = 20000
    eps = 0.5
    l = 1
    algorithms = {'DegreeDiscountIC': lambda k: dic.DDIC(G, k, p),
                  'SingleDiscount': lambda k: dic.SD(G, k),
                  'Random': lambda k: dic.random_sd(G, k),
                  'imm':lambda k: imm.IMMartingales(G,k,eps,l,p),
                  'Greedy': lambda k: gic.GeneralGreedy(G, k, p),
                  'MixedGreedy': lambda k: gic.NewGreedy(G, k, p),
                  'MixedGreedy': lambda k: gic.NewGreedy(G, k, p,mc),
                  'lgim': lambda k: LGIM.LGIM(G, k, p),
                }
    
    path = "./results/wiki"
    save_runs(algorithms,G,k_max,p,mc,path)
    
    G = nx.read_edgelist('./data/email-Enron.txt.gz', create_using=nx.Graph)
    algorithms = {'DegreeDiscountIC': lambda k: dic.DDIC(G, k, p),
                  'SingleDiscount': lambda k: dic.SD(G, k),
                  'Random': lambda k: dic.random_sd(G, k),
                  'imm':lambda k: imm.IMMartingales(G,k,eps,l,p),
                  'Greedy': lambda k: gic.GeneralGreedy(G, k, p),
                  'MixedGreedy': lambda k: gic.NewGreedy(G, k, p,mc),
                  'lgim': lambda k: LGIM.LGIM(G, k, p),
                }
    path = "./results/enron"
    save_runs(algorithms,G,k_max,p,mc,path)
    
    # plt.plot(spread, label=name)

    plt.legend()
    plt.xlabel('seeds')
    plt.ylabel('influence spread')
    plt.show()

    return

if __name__ == "__main__":
    main()
