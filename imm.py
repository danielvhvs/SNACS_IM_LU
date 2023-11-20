import networkx as nx
import ICmodel as IC
import numpy as np
import math
import random
from collections import defaultdict

def NchooseK(n,k):
    return math.factorial(n)/(math.factorial(n-k)*math.factorial(k))

def lambda_prime(eps,k,l,n):
    left = (2.0 + 2.0 / 3.0 * eps)
    right = np.log(NchooseK(n, k)) + l*np.log(n) + np.log(np.log2(n))
    numerator = left*right*n
    return numerator / eps**2

def lambda_star(eps,k,l,n):
    a = (l*np.log(n)+np.log(2))**(1/2)
    b = ((1-1/np.e)*(np.log(NchooseK(n,k))+l*np.log(n)+np.log(2)))**(1/2)
    return 2*n*((1-1/np.e)*a+b)**2*eps**(-2)

def node_selection(G,Rset,k):
    seed = []
    spread = 0
    degree = defaultdict(int)
    boolList = [True for _ in range(len(Rset))]
    RsetIndices = defaultdict(list)
    for idx,RR in enumerate(Rset):
        for x in RR:
            degree[x] += 1
            RsetIndices[x].append(idx)
            
    for _ in range(k):
        node_max = max(degree, key=degree.get)
        seed.append(node_max)
        spread = spread + (len(G.nodes) * degree[node_max] / len(Rset))
        degree[node_max] = -1
        idxList = RsetIndices[node_max]
        for j in idxList:
            if boolList[j]:
                RR = Rset[j]
                for item in RR:
                    if item == node_max:
                        continue
                    degree[item] -= 1
                boolList[j] = False
    return seed,spread

def generate_RR(G,p):
    RR = []
    success = np.random.uniform(0,1,len(G.edges)) < p
    x = list(G.edges)
    GprimeEdges = [x[t] for t in range(len(x)) if success[t]]
    Gprime = G.edge_subgraph(GprimeEdges)
    v = random.choice(list(Gprime.nodes))
    RRset = nx.ancestors(Gprime,v)
    RR = list(RRset)
    return RR

def sampling(G,k,eps,l,p):
    n = len(G.nodes)
    Rset = []
    LB  = 1
    epsPrime = 2.0**(1/2)*eps
    maxRounds = int(max(max(np.log2(n), 1.0) - 1.0, 1.0))
    for i in range(1,maxRounds+1):
        x = n/2.0**i
        theta_i = lambda_prime(epsPrime, k, l, n)/x
        while len(Rset) <= theta_i:
            RR = generate_RR(G,p)
            Rset.append(RR)
        Si,frac = node_selection(G,Rset,k)
        # frac = Fraction_R(Si,Rset)
        if n*frac >= (1+epsPrime) * x:
            LB = n*frac/(1+epsPrime)
            break
    theta = lambda_star(epsPrime, k, l, n)/LB
    while len(Rset) <= theta:
            RR = generate_RR(G,p)
            Rset.append(RR)
    return Rset

def IMMartingales(G,k,eps,l,p):
    l = l * (1+np.log(2)/np.log(len(G.nodes)))
    Rset = sampling(G,k,eps,l,p)
    seed,frac = node_selection(G,Rset,k)
    return seed