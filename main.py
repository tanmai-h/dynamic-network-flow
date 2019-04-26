from math import inf

def newSnapShot():
    '''
        returns the traffic at the present time
    '''
    pass
def getCapacties(k, a, b):
    '''
        k = traffic density (vehicles/mile)
        a,b > 0
        q = traffic flow = vk 
        v = a -bk, avg velocity
    '''
    qmax = a**a / (4*b)     #max flow q for given (a,b) => a^2 /(4b)
    return qmax

def _sort(edges):
    ''' 
    list of paths sorted by either length or time, depending
    upon the approach 
    '''
    pass

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
