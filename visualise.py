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
    ax.set_xlabel('size of seed')
    ax.set_ylabel('influence spread')
    ax.set_title("influence spread for different seed sizes and algorithms")
    plt.show()
    
    
    
def extract_time(path,data_name,algs):
    spread = []
    for alg in algs:
        fileName = path+data_name+alg+".txt"
        with open(fileName,"r") as fread:
            for idx,line in enumerate(fread):
                if idx==1:
                    split = line.split()
                    spread.append([eval(x) for x in split])
                elif idx >1:
                    break
    return spread

def plot_time(path,data_name,algs):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    spread_list = extract_spread(path,data_name,algs)
    for i,spread in enumerate(spread_list):
        ax.plot(spread, label=algs[i])

    ax.legend()
    ax.set_xlabel('seed size')
    ax.set_ylabel('run time (s)')
    ax.set_title("run time for different algorithms for different seed sizes")

    plt.show()