from math import inf
from copy import deepcopy
from enum import Enum

class Regime(Enum):
    FREE_FLOW = 1
    TRANSIT = 2
    CONGESTED = 3

def regime(density):
    if k<=40:
        return Regime.FREE_FLOW
    if k<=65:
        return Regime.TRANSIT
    return Regime.CONGESTED
class Graph:
    def __init__(self, n):
        self.v = n
        self.e = {}
        self.adj_list = [set() for _ in  range(n)]

    def add_edge(self, u, v, wt):
        if u < 0 or u >= self.v or v < 0 or v >= self.v:
            return
        if (u,v) in self.e:
            return
        self.e[(u,v)] = wt
        self.adj_list[u].add(v)
        # self.adj_list[v].append(u)
        return self
    
    def change_edge_weight(self, edge, wt):
        if edge in self.e and wt > 0 :
            self.e[edge] = wt
            return self
        return

    def delete_edge(self, edge):
        try:
            del self.e[edge]
            self.adj_list[edge[0]].remove(edge[1])
        except:
            raise KeyError

    def neighbors(self, v):
        assert v >= 0 and v < self.v
        return self.adj_list[v]

    def __repr__(self):
        return f'Graph({self.v}, {self.e})'

    def __str__(self):
        return self.__repr__()

class Path:
    def __init__(self):
        self.p = []
        self._weight = 0
        self.path_wtls = []

    def push(self, v, wt):
        self.p.append(v)
        self._weight += wt
        self.path_wtls.append(wt)

    def pop(self):
        self.p.pop()
        self._weight -= self.path_wtls.pop()

    def __le__(self, p2):
        return self.weight <= p2.weight

    def __lt__(self, p2):
        return self.weight < p2.weight

    def __eq__(self, p2):
        return self.weight == p2.weight
    
    def __gt__(self, p2):
        return self.weight > p2.weight

    def __ge__(self, p2):
        return self.weight >= p2.weight

    def __iter__(self):
        self.curr_pos = 0
        return self

    def __next__(self):
        if self.curr_pos >= len(self.p)-1:
            raise StopIteration
        self.curr_pos += 1
        return (self.p[self.curr_pos], self.p[self.curr_pos+1])

    def __repr__(self):
        return f'Path({self.p}, {self.weight})'

    def __str__(self):
        return self.__repr__()

    @property
    def weight(self):
        return self._weight

def newSnapShot(E): 
    densities = {}
    for i in range(E):
        u,v,k = map(int, input().split())
        densities[(u,v)] = k
    
    return densities

def BNChangedRegime(bottle_necks, curr_dens, prev_dens):
    for edge in bottle_necks:
        if regime(curr_dens[edge]) != regime(prev_dens[edge]):
            return False
    return True

def excessCapacitiveChange(R, curr_cap, prev_cap):
    
    # def calCapacity(density):
    #     reg = regime(density)
    #     if reg == Regime.FREE_FLOW:
    #         return int(50*density-0.098*(density**2))
    #     elif reg == Regime.TRANSIT:
    #         return int(81.4*density-0.0913*(density**2))
    #     else: 
    #         return int(40*density-0.265*(density**2))
    
    # for edge in R:
    #     if calCapacity(prev_dens[edge]) - calCapacity(curr_dens[edge]) > R[edge]:
    #         return True
    # return False
    for edge in R:
        if pre_cap[edge] - curr_cap[edge] > R[edge]:
            return True
    return False

def getCapacities(g_in: Graph, g_out: Graph, density: dict) -> dict:
    try:
        assert g_in.v == g_out.v
        assert g_in.e.keys() == g_out.e.keys()
        assert g_in.e.keys() == density.keys()
    except:
        raise ValueError('Edges mismatch in the input arguments.')
    caps = {}
    for edge in g_in.e:
        if density[edge] <= 40:
            a = 50
            b = 0.098
        elif density[edge] <= 65:
            a = 81.4
            b = 0.913
        else:
            a = 40
            b = 0.265

        caps[edge] = (a**2)//(4*b)
        g_out.change_edge_weight(edge, (a - density[edge]*b)//1) 
    return caps

def EdmundsKarp(Caps: dict, paths):
    r = Caps.copy()
    f = []
    for path in paths:
        max_flow = inf
        for edge in path:
            if r[edge] < max_flow:
                max_flow = r[edge]
        for edge in path:
            r[edge] -= max_flow
        f.append(max_flow)
    return r, f
    
def DFS(g: Graph, src, dest):
    paths = []
    path = Path()
    path.push(src, 0)
    def dfs_util(g: Graph, src, dest, visited, path: Path, all_paths: list):
        if src==dest:
            all_paths.append(deepcopy(path))
        for u in g.neighbors(src):
            if not visited[u]:
                visited[u] = True
                path.push(u, g.e[(src, u)])
                dfs_util(g, u, dest, visited, path, all_paths)
                path.pop()
                visited[u] = False

    dfs_util(g, src, dest, [False for _ in range(g.v)], path, paths)             
    return paths

def getBottleNecks(R):
    pass

def AdaptiveEdmunds(g: Graph, source, destination):
    s = source
    t = destination
    D = newSnapShot()
    P = DFS(g, s,t)
    g_out = deepcopy(Graph)

    P.sort()
    C = getCapacities(g, g_out, D)
    R,F = EdmundsKarp(C,P)
    B = getBottleNecks(R)

    while True:
        D_prev = D
        D = newSnapShot()
        C_prev = C
        C = getCapacities(g, g_out, D)
        # I = IncomingTrafficFlow()
        
        if BNChangedRegime(B,D,D_prev) or excessCapacitiveChange(R, C, C_prev):
            R,F = EdmundsKarp(C,P)
            B = getBottleNecks(R)
        
        z = 0

        while(z < len(P)):
            # I = I - F[z]
            z += 1
        