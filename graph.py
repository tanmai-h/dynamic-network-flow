from math import inf
from 
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
        self.path_wt = inf

    def push(self, v, wt):
        self.p.append(v)
        self.path_wt += wt

    def __le__(self, p2: Path):
        return self.path_wt <= p2.path_wt

    def __lt__(self, p2: Path):
        return self.path_wt < p2.path_wt

    def __eq__(self, p2: Path):
        return self.path_wt == p2.path_wt
    
    def __gt__(self, p2: Path):
        return self.path_wt > p2.path_wt

    def __ge__(self, p2: Path):
        return self.path_wt >= p2.path_wt

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


def DFS(g: Graph, src, dest):
    paths = []
    def dfs_util(g: Graph, src, dest, visited, path: Path):
        if src==dest:
            return path
        for u in g.neighbors(src):
            if not visited[u]:
                visited[u] = True
                path.push(u, g.e[(src, u)])
                dfs_util(g, u, dest, visited, path)

        
    