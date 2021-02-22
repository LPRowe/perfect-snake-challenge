"""
Idea: For any arry of size (M by N) where either or both of M and N must be even 

          i.e. (3, 4) okay (4, 3) okay, (4, 4) okay, (3, 3) not okay
          
      The array can be subdivided into sections <= 36 nodes.
      
      A hamiltonian cycle can easily be calculated for each section. 
      
      Then take random adjacent edges (adjacent meaning different cycles but parallel and one unit distance apart)
      and swap the edges:
          
          _____               _____
         |_____|             |_  __|
          _____    becomes    _||__ 
         |_____|             |_____|
         
     Keep track of which edges belong to which cycles in a union_find data structure and continue
     this process until there is only one network of edges.
     
     This can easily be extended to M = N = odd if we exclude (0, 0) from the network.
     For the purpose of Snake this works fine, then only visit (0, 0) instead of (1, 1) when food
     exists at (0, 0).  So basically 2 very similar hamiltonian cycles that only differ by
     edges {((0, 1), (1, 1)), ((1, 1), (1, 0))} and {((0, 0), (0, 1)),((0, 0), (1,0))}
"""
import collections
import functools
import matplotlib.pyplot as plt
import random

class UnionFind:
    def __init__(self):
        self.group_id = 0
        self.group = {}
        self.id = {}
        
    def union(self, a, b):
        A, B = a in self.id, b in self.id
        if A and B and self.id[a] != self.id[b]:
            self.merge(a, b)
        elif A or B:
            self.add(a, b)
        else:
            self.create(a, b)
            
    def merge(self, a, b):
        obs, targ = sorted((self.id[a], self.id[b]), key = lambda i: len(self.group[i]))
        for node in self.group[obs]:
            self.id[node] = targ
        self.group[targ] |= self.group[obs]
        del self.group[obs]
        
    def add(self, a, b):
        a, b = (a, b) if a in self.id else (b, a)
        targ = self.id[a]
        self.group[targ] |= {b}
        self.id[b] = targ
        
    def create(self, a, b):
        self.group[self.group_id] = {a, b}
        self.id[a] = self.id[b] = self.group_id
        self.group_id += 1


class HamCycle:
    def __init__(self, R, C, max_size = 6, shuffle = True, display = True):
        """
        R, C: (Rows, Columns) in the array
        max_size: The maximum subarray size allowed, recommended 6 <= max_size <= 40 because of sub-cycle calc. times
        shuffle: Shuffles kernel windows before merging subcycles (if true makes fullcycle appear more random)
        display: If true plots the subdivided regions, subcycles and full cycles for the array
        """
        
        self.R = R
        self.C = C
        self.max_size = max_size
        
        print("Subdividing array")
        self.subarrays = self.subdivide(R-1, C-1, max_size)
        if display: self.show_subcycle_regions()
        
        print("Finding Subarray Hamiltonian Cycles")
        self.count = 1
        self.subcycles = [self.ham_cycle(*subarr) for subarr in self.subarrays]
        if display: self.show_subcycles()
        
        print("Combining subcycles into a full cycle")
        self.full_cycle = self.kernel_connect(shuffle = shuffle)
        if display: self.show_fullcycle()
        
        print("Converting full_cycle into a Directed Graph")
        self.graph = self.get_graph()
        
        print("Hamiltonian Cycle Complete!")
        
    def get_graph(self):
        g = collections.defaultdict(list)
        for a, b in self.full_cycle:
            g[a].append(b)
            g[b].append(a)
        
        start = (0, 0)
        finish = g[start][0]
        dag = {finish: start}
        while start != finish:
            a, b = g[start]
            if dag.get(a, (-1, -1)) == start:
                dag[start] = b
                start = b
            else:
                dag[start] = a
                start = a
        return dag
        
    def kernel_connect(self, shuffle = True):
        """
        1. Groups together subcycle edges in a union-find data structure.
        2. Creates a kernel (2 by 2 square with two parallel connected edges)
            i. parallel edges are vertical
            ii. parallel edges are horizontal
        3. Offsets each kernel to cover every location on the array.
        4. Shuffles the kernels (optional for a random path effect)
        5. While union-find has more than one network of edges:
            i.   Pop from kernel list
            ii.  check if parallel edges belong to different groups
            iii. If they do, reconnect the edges so vertical -> horizontal or vice versa
            iv.  Delete the old edges from the union-find data structure
            v.   Add the two new edges to the data structure, thus merging the two networks
        6. Return the list of edges in the union-find data structure, this should be a full-array
           Hamiltonian Cycle.
        """
        
        # 1. Add EDGES into a union-find data structure
        uf = UnionFind()
        for subcycle in self.subcycles:
            edges = list(zip(subcycle, subcycle[1:])) # points to edges
            for a, b in list(zip(edges, edges[1:])): # edges to network each node in uf is an EDGE not a point
                a, b = tuple(sorted(a)), tuple(sorted(b))
                uf.union(a, b)
                
        #print(uf.group)
        
        # 2-4. Create parallel and vertical kernels and shuffle
        kernels = []
        for i in range(self.R-1):
            for j in range(self.C-1):
                v1, v2 = ((i, j), (i+1, j)), ((i, j+1), (i+1, j+1))
                h1, h2 = ((i, j), (i, j+1)), ((i+1, j), (i+1, j+1))
                if v1 in uf.id and v2 in uf.id and uf.id[v1] != uf.id[v2]:
                    kernels.append((v1, v2, h1, h2))
                elif h1 in uf.id and h2 in uf.id and uf.id[h1] != uf.id[h2]:
                    kernels.append((v1, v2, h1, h2))
        if shuffle:
            random.shuffle(kernels)
        
        # 5. While union-find datastructure contains more than one network of edges
        #    pop from kernel, see if window contains two edges that are in different networks
        #    swap the connections to connect the two groups
        removed = set()
        while len(uf.group) > 1:
            v1, v2, h1, h2 = kernels.pop()
            if v1 in uf.id and v2 in uf.id:
                if uf.id[v1] != uf.id[v2]:
                    uf.union(h1, h2)
                    uf.union(v1, h1)
                    uf.union(v2, h2)
                    uf.id.pop(v1)
                    uf.id.pop(v2)
                    removed |= set([v1, v2])
            elif h1 in uf.id and h2 in uf.id:
                if uf.id[h1] != uf.id[h2]:
                    uf.union(v1, v2)
                    uf.union(v1, h1)
                    uf.union(v2, h2)
                    uf.id.pop(h1)
                    uf.id.pop(h2)
                    removed |= set([h1, h2])
        return [edge for edge in list(uf.id) if edge not in removed]
    
    def show_fullcycle(self):
        plt.figure('Full Cycle')
        for edge in self.full_cycle:
            a, b = edge
            plt.plot([a[1], b[1]], [a[0], b[0]], 'r-')
        plt.title("Full Hamiltonian Cycle")
        plt.show()
        
    def show_subcycles(self):
        plt.figure('Subcycles')
        for subcycle in self.subcycles:
            x = [p[1] for p in subcycle]
            y = [p[0] for p in subcycle]
            plt.plot(x, y, 'r-')
        plt.title("Subregion Hamiltonian Cycles")
        plt.show()
        
    def show_subcycle_regions(self):
        arr = [[0]*self.C for _ in range(self.R)]
        subs = self.subarrays[:]
        random.shuffle(subs)
        for k,(y1, x1, y2, x2) in enumerate(subs):
            for i in range(y1, y2+1):
                for j in range(x1, x2+1):
                    arr[i][j] = k
        plt.figure('subarray regions')
        plt.title("Subdivisions of Array")
        plt.imshow(arr)
        
    def subdivide(self, R, C, max_size):
        """
        splits array into subarrays that:
            1. have an even number of nodes
            2. have less than max_size nodes
            
        returns a list of [(y1, x1, y2, x2), ...] representing the bounds of the subarrays
        """
    
        def size(y1, x1, y2, x2):
            return (y2 - y1 + 1) * (x2 - x1 + 1)
        
        def helper(y1, x1, y2, x2):
            nonlocal max_size
            
            if size(y1, x1, y2, x2) <= max_size:
                return [(y1, x1, y2, x2)]
            
            # divide along horizontal
            if y2 - y1 > x2 - x1:
                y = (y1 + y2) // 2
                if (y - y1) & 1:
                    return helper(y1, x1, y, x2) + helper(min(y+1, y2), x1, y2, x2)
                return helper(y1, x1, max(y-1, y1), x2) + helper(y, x1, y2, x2)
            
            #divide along vertical
            x = (x1 + x2) // 2
            return helper(y1, x1, y2, x) + helper(y1, min(x+1, x2), y2, x2)
    
        return helper(0, 0, R, C)
    
    @functools.lru_cache(None)
    def get_edges(self, R, C):
        """Returns an edge-list for 4-directionally connected nodes in an array of dimensions (R, C)"""
        edges = collections.defaultdict(list)
        for i in range(R):
            for j in range(C):
                a = (i, j)
                if i:
                    edges[a].append((i-1, j))
                    edges[(i-1, j)].append(a)
                if j:
                    edges[a].append((i, j-1))
                    edges[(i, j-1)].append(a)
        return edges
    
    def ham_cycle(self, y1, x1, y2, x2):
        """
        Finds the hamiltonian cycle for a rectangle of (height, width)
        Returns the edge-list offset by (offset_y, offset_x)
        """
        
        def helper(node, visited, edges):
            nonlocal N, start
            if len(visited) == N and start in edges[node]:
                return [start]
            for neigh in edges[node]:
                if neigh not in visited:
                    v = visited.copy() | {neigh}
                    p = helper(neigh, v, edges)
                    if p[-1] != -1:
                        return [neigh] + p
            return [-1]
        
        @functools.lru_cache(None)
        def find_cycle(R, C):
            # Build edge list
            edges = self.get_edges(R, C)
            start = (0, 0)
            res = [start] + helper(start, {start}, edges)
            return res
            

        offset_y, offset_x = y1, x1
        R = y2 - y1 + 1
        C = x2 - x1 + 1 
        N = R * C
        
        # find cycle from (0, 0) through all nodes and back to (0, 0)
        start = (0, 0)
        res = find_cycle(R, C)
        
        # shift the path by offset_x and offset_y
        res = [(y+offset_y, x+offset_x) for y, x in res]
        
        #print(self.count,'/',len(self.subarrays))
        self.count += 1
        
        return res


if __name__ == "__main__":
    plt.close('all')
    R, C = 30, 30
    ham = HamCycle(R, C, max_size = 36, shuffle = True, display = False)

















