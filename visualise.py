import matplotlib.pyplot as plt

def extract_spread(path,data_name,algs):
    for alg in algs:
        fileName = path+data_name+alg+".txt"
        with open(fileName,"r") as fread:
            for idx,line in enumerate(fread):
                

def plot_spread(path,data_name,algs):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    spread_list = extract_spread(path,data_name,algs)
    for i,spread in enumerate(spread_list):
        ax.plot(spread, label=algs[i])

    ax.legend()
    ax.xlabel('seeds')
    ax.ylabel('influence spread')
    plt.show()