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
import concurrent.futures
import visualise
import argparse
import sys

def run_model_with(G, k_max, p, mc, function):
    spread = []
    seed_list = []
    time_list = []
    for k in tqdm(range(1,k_max+1)):
        start = time.time()
        S = function(k)
        end = time.time()
        seed_list.append(S)
        time_list.append((end-start)*1000)
        spread.append(icm.IC(G, S, p, mc)[0])
    return spread,seed_list,time_list

def save_runs(algorithms,G,k_max,p,mc,path):
    for name, algo in algorithms.items():
        st = time.time()
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
                    fwrite.write(f"\t{seed_list[i][j]}")
                fwrite.write(f"\n")
            fwrite.close()
        et = time.time()
        print(f'writing overhead {(et - st)}')
    return

def single_run(G,k,p,mc,path,name,algo):
    start = time.time()
    S = algo['algo'](G, k, *algo['args'])
    timing = time.time()-start
    spread = icm.IC(G, S, p, mc)[0]
    return S, timing, spread
    # with open(path+name+"spread.txt","w") as fwrite:
    #     fwrite.write(f"{k}\t{spread}\n")
    #     fwrite.close()
    # with open(path+name+"time.txt","w") as fwrite:
    #     fwrite.write(f"{k}\t{timing}\n")
    #     fwrite.close()
    # with open(path+name+"seed.txt","w") as fwrite:
    #     fwrite.write(f"{k}\t{S[0]}")
    #     for j in range(1,len(S)):
    #         fwrite.write(f"\t{S[j]}")
    #     fwrite.write(f"\n")
    #     fwrite.close()

def save_runs_2(algorithms,G,k_max,p,mc,path):
    st = time.time()
    for name, algo in algorithms.items():
        spread_list = []
        seed_list = []
        time_list = []
        with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
            futures = [executor.submit(single_run, G, i, p, mc, path, name, algo) for i in range(1,k_max+1)]
            for future in futures:
                seed, t, spread = future.result()
                seed_list.append(seed)
                time_list.append(t)
                spread_list.append(spread)

        with open(path+name+".txt","w") as fwrite:
            fwrite.write(f"{spread_list[0]}")
            for i in range(1,len(spread_list)):
                fwrite.write(f"\t{spread_list[i]}")
            fwrite.write(f"\n")
            fwrite.write(f"{time_list[0]}")
            for i in range(1,len(time_list)):
                fwrite.write(f"\t{time_list[i]}")
            fwrite.write(f"\n")
            for i in range(len(seed_list)):
                fwrite.write(f"{seed_list[i][0]}")
                for j in range(1,len(seed_list[i])):
                    fwrite.write(f"\t{seed_list[i][j]}")
                fwrite.write(f"\n")
            fwrite.close()
    print(time.time() - st)


def set_algorithms(G,p,mc,eps,l):
    algorithms = {
        'DegreeDiscountIC': {'algo': dic.DDIC, 'args': (p)},
                #   'SingleDiscount': {'algo': dic.SD, 'args': (p)},
                #   'Random': {'algo': dic.random_sd, 'args': (p)},
                  'imm': {'algo': imm.IMMartingales, 'args': (eps,l,p)},
                #   'lgim': {'algo': LGIM.LGIM, 'args': (p)},
    #             }
    # algorithms = {
                #   "mixedgreedy": {'algo': gic.MixedGreedy, 'args': (p, mc)},
                }
    return algorithms


def main():
    np.random.seed(42)
    k_max = 50
    p = 0.01
    mc = 20_000
    eps = 0.5
    l = 1

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--plot", help="whether to do runs or plot [run,spread,time,both]",default="run",type=str)
    args = parser.parse_args()
    plotting = args.plot

    if plotting=="run":
        G = nx.read_edgelist('./data/wiki-Vote.txt.gz', create_using=nx.DiGraph)
        path = "./results/wiki"
        algorithms = set_algorithms(G,p,mc,eps,l)
        print('wikivote for: ', algorithms)
        save_runs_2(algorithms,G,k_max,p,mc,path)
        print('wikivote done')
        # G = nx.read_edgelist('./data/email-Enron.txt.gz', create_using=nx.Graph)
        # algorithms = set_algorithms(G,p,mc,eps,l)
        # path = "./results/enron"
        # save_runs(algorithms,G,k_max,p,mc,path)

    elif plotting=="spread":
        visualise.plot_spread("./results/","wiki",["DegreeDiscountIC","SingleDiscount","imm","Random"])
    elif plotting=="time":
        visualise.plot_time("./results/","wiki",["DegreeDiscountIC","SingleDiscount","imm","Random"])
    elif plotting=="both":
        visualise.plot_both("./results/","wiki",["DegreeDiscountIC","SingleDiscount","imm","Random"])


    return

if __name__ == "__main__":
    main()
