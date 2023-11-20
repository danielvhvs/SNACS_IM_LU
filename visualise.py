import matplotlib.pyplot as plt

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
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    spread_list = extract_spread(path,data_name,algs)
    for i,spread in enumerate(spread_list):
        ax.plot(spread, label=algs[i])

    ax.legend()
    ax.set_xlabel('seeds')
    ax.set_ylabel('influence spread')
    plt.show()