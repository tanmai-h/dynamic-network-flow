from math import inf
from copy import deepcopy
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



        
    