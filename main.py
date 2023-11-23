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
        print(S)
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
                    fwrite.write(f"\t{seed_list[i][j]}")
                fwrite.write(f"\n")
            fwrite.close()
    return

def single_run(G,k,p,mc,path,name,algo):
    start = time.time()
    S = algo(k)
    timing = time.time()-start
    spread = icm.IC(G, S, p, mc)[0]
    with open(path+name+"spread.txt","a") as fwrite:
        fwrite.write(f"{k}\t{spread}\n")
        fwrite.close()
    with open(path+name+"time.txt","a") as fwrite:
        fwrite.write(f"{k}\t{timing}\n")
        fwrite.close()
    with open(path+name+"seed.txt","a") as fwrite:
        fwrite.write(f"{k}\t{S[0]}")
        for j in range(1,len(S)):
            fwrite.write(f"\t{S[j]}")
        fwrite.write(f"\n")
        fwrite.close()

def save_runs_2(algorithms,G,k_max,p,mc,path):
    for name, algo in algorithms.items():
        func = lambda item : single_run(G,item,p,mc,path,name,algo)
        items = [i for i in range(1,k_max+1)]
        executor = concurrent.futures.ThreadPoolExecutor(50)
        futures = [executor.submit(func, item) for item in items]
        concurrent.futures.wait(futures)
    return
    
def run_model_with_2(G, k_max, p, mc, function):
    spread = []
    seed_list = []
    time_list = []
    k = k_max
    start = time.time()
    S = function(k)
    print(S)
    end = time.time()
    seed_list.append(S)
    time_list.append((end-start)*1000)
    spread.append(icm.IC(G, S, p, mc)[0])
    return spread,seed_list,time_list

def save_runs_3(algorithms,G,k_max,p,mc,path):
    for name, algo in algorithms.items():
        start = time.time()
        S = algo(k_max)
        timing = time.time()-start
        spread = icm.IC(G, S, p, mc)[0]
        with open(path+name+str(k_max)+"spread.txt","w") as fwrite:
            fwrite.write(f"{spread}\n")
            fwrite.close()
        with open(path+name+str(k_max)+"time.txt","w") as fwrite:
            fwrite.write(f"{timing}\n")
            fwrite.close()
        with open(path+name+str(k_max)+"seed.txt","w") as fwrite:
            fwrite.write(f"{S[0]}")
            for j in range(1,len(S)):
                fwrite.write(f"\t{S[j]}")
            fwrite.write(f"\n")
            fwrite.close()
    return

def set_algorithms(G,p,mc,eps,l):
    # algorithms = {'DegreeDiscountIC': lambda k: dic.DDIC(G, k, p),
    #               'SingleDiscount': lambda k: dic.SD(G, k),
    #               'Random': lambda k: dic.random_sd(G, k),
    #               'imm':lambda k: imm.IMMartingales(G,k,eps,l,p),
    #               'lgim': lambda k: LGIM.LGIM(G, k, p),
    #             }
    algorithms = {
                  'lgim': lambda k: LGIM.LGIM(G, k, p),
                # 'Random': lambda k: dic.random_sd(G, k),
                #   'mixedgreedy':lambda k: gic.MixedGreedy(G,k,p,mc),
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
    parser.add_argument("-r", "--running", help="whether to do runs or plot [run,spread,time,both]",default="run",type=str)
    parser.add_argument("-k", "--kvalue", help="the seed size to find",default=None,type=int)
    parser.add_argument("-p", "--plot_data", help="the data to plot",default="wiki",type=str)
    args = parser.parse_args()
    running = args.running
    kvalue = args.kvalue
    plot_data = args.plot_data
    
    if kvalue==None:
        sr_func = save_runs
    else:
        sr_func = save_runs_3
        k_max = kvalue
    
    if running=="run":
        G = nx.read_edgelist('./data/wiki-Vote.txt.gz', create_using=nx.DiGraph)
        path = "./results/wiki"
        algorithms = set_algorithms(G,p,mc,eps,l)
        sr_func(algorithms,G,k_max,p,mc,path)
        G = nx.read_edgelist('./data/email-Enron.txt.gz', create_using=nx.Graph)
        algorithms = set_algorithms(G,p,mc,eps,l)
        path = "./results/enron"
        sr_func(algorithms,G,k_max,p,mc,path)
    elif running=="wiki":
        G = nx.read_edgelist('./data/wiki-Vote.txt.gz', create_using=nx.DiGraph)
        path = "./results/wiki"
        algorithms = set_algorithms(G,p,mc,eps,l)
        sr_func(algorithms,G,k_max,p,mc,path)
    elif running=="enron":
        G = nx.read_edgelist('./data/email-Enron.txt.gz', create_using=nx.Graph)
        algorithms = set_algorithms(G,p,mc,eps,l)
        path = "./results/enron"
        sr_func(algorithms,G,k_max,p,mc,path)
    
    wiki = ["DegreeDiscountIC","SingleDiscount","imm","Random","lgim"]
    enron = ["DegreeDiscountIC","SingleDiscount","imm","Random"]
    alg_list = enron
    if running=="spread":
        visualise.plot_spread("./results/",plot_data,alg_list)
    elif running=="time":
        visualise.plot_time("./results/",plot_data,alg_list)
    elif running=="both":
        visualise.plot_both("./results/",plot_data,alg_list)
    
    
    return

if __name__ == "__main__":
    main()
