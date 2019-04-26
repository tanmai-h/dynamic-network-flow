from math import inf
import random

def newSnapShot():
    '''
        returns the traffic at the present time
    '''
    n,e = map(int, input().split())
    G = [[] for _ in range(n)]
    for i in range(e):
        u,v,w = map(int, input().split())
        G[u].append((v,w))

    matrix = [[None for _ in range(n)] for _ in range(n)]
    for u in range(n):
        for v,w in G[u]:
            matrix[u][v] =  random.randint(35,80)
    
    return matrix   #Density matrix

def getCapacties(G, D):
    C = D.copy()
    c = 0
    for u in range(len(G)):
        for v,w in G[u]:
            d = D[u][v]
            if d <= 40:
                c = 6378
            elif d >= 40 and d <= 65:
                c = 1815
            else:
                c = 1510
            C[u][v] = c
    
    return C    #capacities

def _sort(Graph, L):
    ''' 
    list of paths sorted by length
    '''

    edges = []
    for u in Graph:
        for v in Graph[u]:
            edges.append((u,v))
    edges = sorted(edges, lambda x,y : L[x][y])

    return edges
    
def BNChangedRegime(B,C,CX,R):
    # B= bottlnecks, C = capacties, R=from edmonkarp residual cap

    for (u,v) in B:
        pass

def excessCapacityChange():
    pass

def IncomingTrafficFlow():
    '''
        gives the influx of
        traffic at the source in the present snapshot
    ''' 


def DFS(G,s,t,visited,curr,paths):
    visited[s] = True
    if s == t:
        paths.append(curr)
        pass
    else:
        for u in range(len(G)):
            for v in G[u]:
                if visited[v] == False:
                    DFS(G,v,t,visited,curr+[v],paths)
                                        
def setup(n,p):
    '''
    D : Density Matrix
    L : Length Matrix
    R : Residual Graph Matrix
    F : List of Maximum Flows in p graded paths
    BN : List of bottleneck edges from the most recent run of the flow algorithm
    V  : Set of visited points from source in residual graph
    '''
    matrix = [[None for _ in range(n)] for _ in range(n)]
    D,L,R = matrix.copy()
    BN = []
    F = [None for _ in range(p)]
    V = []

    return D,L,R,BN,F,V

def getBottlenecks(R):
    V = DFS(R)
    
    for i in V:
        for  (u,v) in Graph: #u=i
            if R[u][v] == 0:
                BN.append((u,v))
    
    return BN

def EdmondKarp(C,P):
    '''
        C = capacties
        P = edge list from DFS
    '''
    R = C
    for path in P:
        maxFlow = inf
    
        for path in P:
            for (u,v) in path:
                maxFlow = min(maxFlow, R[u][v])

        for path in P:
            for (u,v) in path:
                R[u][v] = R[u][v] - maxFlow
        
        F.append(max)

    return R,F
    
def AdaptiveEdmondKarp():
    s = source
    t = destination
    D = newSnapShot()
    P = DFS(s,t,L)
    P = _sort(P)
    C = getCapacties(D)
    CX = C
    R,F = EdmondKarp(C,P)
    B = getBottleNecks(R)

    while True:
        D = newSnapShot()
        C = getCapacties(D)
        I = IncomingTrafficFlow()
        
        if  (BNChangedRegime(B,C,CX,R) == True or excessCapacityChange(R,C,CX) == True):
            P = _sort(P)
            R,F = EdmondKarp(C,P)
            B = getBottleNecks(R)
            CX = C
        
        z = 0
        
        while (I > 0 and z < total_paths):
            #Direct F[z] amount of Flow through path P[z]            
            I = I - F[z]
            z = z + 1

def DFS(g: Graph, )
