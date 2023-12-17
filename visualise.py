import matplotlib.pyplot as plt
import numpy as np

def extract_spread(path,data_name,algs):
    spread = []
    for alg in algs:
        fileName = path+data_name+alg+".txt"
        with open(fileName,"r") as fread:
            for idx,line in enumerate(fread):
                if idx==0:
                    split = line.split()
                    spread.append([eval(x) for x in split])
                else:
                    break
    return spread

def plot_spread(path,data_name,algs):
    fsize = 14
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    spread_list = extract_spread(path,data_name,algs)
    for i,spread in enumerate(spread_list):
        ax.plot(spread, label=algs[i])

    ax.legend(fontsize=fsize)
    ax.set_xlabel('size of seed',fontsize=fsize)
    ax.set_ylabel('influence spread',fontsize=fsize)
    ax.set_title("influence spread for different seed sizes and algorithms",fontsize=fsize)
    ax.tick_params(axis="both",labelsize=fsize)
    plt.show()


def combine():
    file = "./results/enronlgim"
    fileX = [20,30,50]
    timing = []
    spread = []
    seeds = []
    for x in fileX:
        with open(f"{file}{x}.txt","r") as fread:
            i = 0
            for line in fread:
                if i==1:
                    split = line.split()
                    for value in split:
                        timing.append(eval(value))
                elif i==0:
                    split = line.split()
                    for value in split:
                        spread.append(eval(value))
                else:
                    split = line.split()
                    seeds.append(split)
                i += 1
            fread.close()
                    
    with open("./results/enronlgim.txt","w") as fwrite:
        fwrite.write(f"{spread[0]}")
        for i in range(1,len(spread)):
            fwrite.write(f"\t{spread[i]}")
        fwrite.write(f"\n")
        fwrite.write(f"{timing[0]}")
        for i in range(1,len(timing)):
            fwrite.write(f"\t{timing[i]}")
        fwrite.write(f"\n")
        for i in range(len(seeds)):
            fwrite.write(f"{seeds[i][0]}")
            for j in range(1,len(seeds[i])):
                fwrite.write(f"\t{seeds[i][j]}")
            fwrite.write(f"\n")
        fwrite.close()

def extract_time(path,data_name,algs):
    time_list = []
    for alg in algs:
        fileName = path+data_name+alg+".txt"
        with open(fileName,"r") as fread:
            for idx,line in enumerate(fread):
                if idx==1:
                    split = line.split()
                    if alg == "lgim" or alg=="mixedgreedy":
                        time_list.append([eval(x) for x in split])
                    else:
                        time_list.append([eval(x)/1000 for x in split])
                elif idx >1:
                    break
    return time_list

def plot_time(path,data_name,algs):
    fsize = 14
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    time_list = extract_time(path,data_name,algs)
    for i,time in enumerate(time_list):
        ax.plot(time, label=algs[i])

    ax.legend(fontsize=fsize)
    ax.set_xlabel('seed size',fontsize=fsize)
    ax.set_ylabel('run time (s)',fontsize=fsize)
    ax.set_title("run time for different algorithms for different seed sizes",fontsize=fsize)
    ax.tick_params(axis="both",labelsize=fsize)
    plt.show()

def plot_both(path,data_name,algs):
    fsize = 14
    fig = plt.figure()
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    spread_list = extract_spread(path,data_name,algs)
    for i,spread in enumerate(spread_list):
        ax1.plot(spread, label=algs[i])

    time_list = extract_time(path,data_name,algs)
    for i,time in enumerate(time_list):
        ax2.plot(time, label=algs[i])

    ax1.legend(fontsize=fsize)
    ax1.set_xlabel('size of seed',fontsize=fsize)
    ax1.set_ylabel('influence spread',fontsize=fsize)
    ax1.set_title("influence spread for different seed sizes and algorithms",fontsize=fsize)

    ax2.legend(fontsize=fsize)
    ax2.set_xlabel('seed size',fontsize=fsize)
    ax2.set_ylabel('run time (s)',fontsize=fsize)
    ax2.set_yscale('log')
    ax2.set_title("run time for different algorithms for different seed sizes",fontsize=fsize)
    ax1.tick_params(axis="both",labelsize=fsize)
    ax2.tick_params(axis="both",labelsize=fsize)

    plt.show()
    
    
def plot_time_bar(path,data_name,algs):
    fsize = 16
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    time_list = np.array(extract_time(path,data_name,algs))[:,-1]
    
    ax.bar(algs,time_list)
    ax.legend(fontsize=fsize)
    # ax.set_xlabel('seed size',fontsize=fsize)
    ax.set_ylabel('run time (s)',fontsize=fsize)
    ax.set_title("run time for different algorithms for different seed sizes as a barplot",fontsize=fsize)
    ax.tick_params(axis="both",labelsize=fsize)
    ax.set_yscale('log')
    plt.show()

    
