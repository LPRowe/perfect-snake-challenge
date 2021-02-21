import collections
import matplotlib.pyplot as plt

# 1. subdivide large array into smaller arrays (containing an even number of nodes) that are small enough
# to brute force a hamiltonian cycle solutoin

# 2. Create a graph connecting the subarrays bidirectionally

# 3. Find a main hamiltonian cycle that visits every subarray

# 4. 



def subdivide(R, C, max_size = 36):
    """splits array into subarrays of manageable size"""
    
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
    
    
def ham_cycle(edges, odd = False):
    def helper(visited, path):
        nonlocal res
        if len(path) == (N - odd) and start in edges[path[-1]]:
            res = path
        if res:
            return None
        for neigh in edges[path[-1]]:
            if neigh not in visited:
                v = visited.copy() | {neigh}
                helper(v, path + [neigh])
    N = R * C
    res = None        
    start = (0, 1) if odd else (0, 0)
    helper({start}, [start])
    return res



def get_edges(R, C):
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

def get_edges_odd(R, C):
    '''gets all 4 directionally connected edges but skips anything connected to (0, 0)'''
    edges = collections.defaultdict(list)
    for i in range(R):
        for j in range(C):
            a = (i, j)
            if i > 1 or (i and j):
                edges[a].append((i-1, j))
                edges[(i-1, j)].append(a)
            if j > 1 or (j and i):
                edges[a].append((i, j-1))
                edges[(i, j-1)].append(a)
    return edges

def shape(subregion):
    y1, x1, y2, x2 = subregion
    return (y2 - y1 + 1, x2 - x1 + 1)

if __name__ == "__main__":
    plt.close('all')
    R, C = 10, 8
    sub = subdivide(R-1, C-1)
    
    arr = [[0]*C for _ in range(R)]
    for k,(y1, x1, y2, x2) in enumerate(sub):
        for i in range(y1, y2+1):
            for j in range(x1, x2+1):
                arr[i][j] = k
    plt.imshow(arr)
    
    
    for region in sub:
        X, Y = shape(region)
        if X&1 and Y&1:
            print(X, Y)
    print('subs:',len(sub))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    