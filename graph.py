from math import inf
from copy import deepcopy
from enum import Enum
from random import randint
class Regime(Enum):
    FREE_FLOW = 1
    TRANSIT = 2
    CONGESTED = 3

def regime(k):
    if k<=40:
        return Regime.FREE_FLOW
    if k<=65:
        return Regime.TRANSIT
    return Regime.CONGESTED

def stdize(edge):
    if edge[0] <= edge[1]:
        return edge
    return (edge[1], edge[0])

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
        # self.e[(v,u)] = wt
        self.adj_list[u].add(v)
        self.adj_list[v].add(u)
        return self
    
    def change_edge_weight(self, e, wt):
        edge = self.e[stdize((edge))]
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

    def get_edge_weight(self, edge):
        return self.e[stdize(edge)]

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
        res =  (self.p[self.curr_pos], self.p[self.curr_pos+1])
        self.curr_pos += 1
        return res
    def __repr__(self):
        return f'Path({self.p}, {self.weight})'

    def __str__(self):
        return self.__repr__()

    @property
    def weight(self):
        return self._weight

def newSnapShot(E): 
    densities = {}
    try:
        for i in range(E):
            u,v,k = list(map(int, input().split()))
            densities[(u,v)] = k
    except:
        print('New Input not provided! Using last input snapshot')
    return densities
# def newSnapShot(E): 
#     densities = {}
#     for i in range(E):
#         u,v = list(map(int, input().split()))
#         densities[(u,v)] = randint(20,100)
#     print(densities)
#     return densities

def InfluxTraffic():
    a = 0
    try:
        a = int(input())
    except:
        pass
    return a

def BNChangedRegime(bottle_necks, curr_dens, prev_dens):
    for edge in bottle_necks:
        if regime(curr_dens[edge]) != regime(prev_dens[edge]):
            return True
    return False

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
        if prev_cap[edge] - curr_cap[edge] > R[edge]:
            return True
    return False


def getCapacities(g_in: Graph, density: dict) -> dict:
    try:
        assert g_in.e.keys() == density.keys()
    except:
        raise ValueError('Edges mismatch in the input arguments.')
    caps = {}
    for edge in g_in.e:
        r = regime(density[edge])
        if r == Regime.FREE_FLOW:
            caps[edge] = 6378
        elif r == Regime.TRANSIT:
            caps[edge] = 1814
        else:
            caps[edge] = 1509
    return caps

def EdmundsKarp(Caps: dict, paths):
    r = Caps.copy()
    f = []
    for path in paths: 
        max_flow = inf
        for edge in path:
            if r[stdize(edge)] < max_flow:
                max_flow = r[stdize(edge)]
        for edge in path:
            r[stdize(edge)] -= max_flow
        f.append(max_flow)
    return r, f
    
def DFS(g: Graph, src, dest):
    paths = []
    path = Path()
    path.push(src, 0)
    def dfs_util(g: Graph, src, dest, visited, path: Path, all_paths: list):
        # print(path)
        if src==dest:
            all_paths.append(deepcopy(path))
        for u in g.neighbors(src):
            if not visited[u]:
                visited[u] = True
                path.push(u, g.get_edge_weight((src, u)))
                dfs_util(g, u, dest, visited, path, all_paths)
                path.pop()
                visited[u] = False

    dfs_util(g, src, dest, [False for _ in range(g.v)], path, paths)             
    return paths

def getBottleNecks(R, P, src, dest):
    BN = set()
    for path in P:
        for edge in path:
            if R[stdize(edge)] == 0:
                BN.add(stdize(edge))
                break
    return BN

def AdaptiveEdmunds(g: Graph, source, destination, loopCount=inf):
    z = 0
    s = source
    t = destination
    i = 0
    i += InfluxTraffic()
    D = newSnapShot(len(g.e))
    P = DFS(g, s,t)
    P.sort()
    print('All paths:')
    for p  in P:
        print(p)
    print()
    C = getCapacities(g, D)
    R,F = EdmundsKarp(C,P)
    B = getBottleNecks(R, P, s, t)
    for flow in F:
        if i >= flow:
            i -= flow
        else:
            i = 0
            break
    print('*** Flows ***')
    print()
    for edge in R:    
        print(f'Edge: {edge}, Flow: {C[edge] - R[edge]}, Max Capacity: {C[edge]}')
    print('Remainig Influx on source:', i)
    print()

    while z<loopCount or i>0:
        D_prev = D
        i += InfluxTraffic()
        D = newSnapShot(len(g.e)) or D_prev
        C_prev = C
        C = getCapacities(g, D)
        
        if BNChangedRegime(B,D,D_prev) or excessCapacitiveChange(R, C, C_prev):
            print('Ran Again!')
            R,F = EdmundsKarp(C,P)
            B = getBottleNecks(R, P, s, t)
        
        for flow in F:
            if i >= flow:
                i -= flow
            else:
                i = 0
                break
        for edge in R:
            print(f'Edge: {edge}, Flow: {max(C[edge] - R[edge], 0)}, Max Capacity: {C[edge]}')
        print(f'Bottlenecks: {B}')
        print('Remainig Influx on source:', i)
        print()
        z += 1

def main():
    v,e = list(map(int, input().split()))
    g = Graph(v)
    for _ in range(e):
        u,v,w = list(map(int, input().split()))
        g.add_edge(u,v,w)
    s, d = list(map(int, input().split()))
    AdaptiveEdmunds(g,s, d, 8)

if __name__ == '__main__':
    main()