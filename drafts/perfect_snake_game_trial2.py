import collections
import heapq
import math
import random

import pygame

# Find clear paths to food
# for each clear path, if it has a clear path to the current tail, then take it
# otherwise keep searching for other clear paths to food
# if all paths have been exhaused
# find any clear path to touch tail


# use a hash map to keep track of snake's body part -> steps before it disappears
# use a running counter of steps so that hashmap[node] - count is number of steps when it will disappear

# use a queue to keep track of the order of the snakes body, pop the tail (and delete from hashmap)
# and append to head the new position

# over constrained when not alloewd to visit the same point twice
# allow the snake to visit the same point a second time (but not a third time)
# so long as it does not hit the body

# change visited to a path and cannot visit the same point twice or step on visited[-body_length:]


class Game():
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
        
    def run():
        pass
    
    def draw():
        pass
        
    
class Segment():
    def __init__(self):
        pass
    
    
def spawn_food(snake, rows, cols):
    global food
    food = random_loc(rows, cols)
    while food in snake.body:
        food = random_loc(rows, cols)

def random_loc(rows, cols):
    return random.randint(0, cols-1), random.randint(0, rows-1)

class PQNode:
    def __init__(self, heuristic, position, visited, steps, counter):
        self.h = heuristic
        self.p = position
        self.v = visited
        self.s = steps
        self.c = counter
        
    def __lt__(self, other):
        return (self.h, len(self.v)) < (other.h, len(other.v))

class PathFinder:
    """
    Performs an exhaustive search from start to target and back to tail.
    1. If such a path exists, returns path from start to target.
    2. If such a path deos not exist, returns path from start to tail.
    Uses priority queue and a_star like heuristic to reduce runtime.
    Prunes search through early stoppping if any solution that meets criteria 1 is found.
    """
    def __init__(self, start, target, tail, obstacles, steps):
        self.start = start
        self.target = target
        self.tail = tail
        self.obstacles = obstacles
        self.steps = steps
        self.found_food = False
        
    def is_path_to_tail(self, start, visited, steps):
        """
        Perform BFS from start to find any path from start to self.tail.
        start can be either food and visited are the nodes stepped on to reach the food
        or start can be self.start and visited is empty.
        
        Return True if a path exists from start to self.tail.
        """
        q = [(start, steps, visited)]
        while q:
            next_level = []
            for p, s, visited in q:
                for neigh in graph[p]:
                    if neigh == self.tail:
                        return True
                    
                    if neigh not in visited[-len(self.obstacles):] and self.obstacles[neigh] <= s:
                        v = visited[:]
                        v.append(neigh)
                        next_level.append((neigh, s+1, v))
            q = next_level
        return False
    
    def exhaustive_search(self):
        node = PQNode(self.heuristic(self.start, self.start, self.target),
                      self.start, [], self.steps, collections.defaultdict(int))
        q = [node] # (h) heuristic, (p) position, (v) visited path, (s) steps taken - offset included, (c) count for each space
        while q:
            node = heapq.heappop(q)
            p, v, s, c = node.p, node.v, node.s, node.c
            
            # if we reached the food, check if a path exists from food to tail
            if p == self.target:
                if self.is_path_to_tail(p, v.copy(), s):
                    v.append(self.target)
                    self.found_food = True
                    return v
            
            for neigh in graph[p]:
                if (neigh not in v[-len(self.obstacles):]) and (self.obstacles[neigh] <= s) and (c[neigh] < 2):
                    v_ = v.copy()
                    v_.append(neigh)
                    c_ = c.copy()
                    c_[neigh] += 1
                    next_node = PQNode(self.heuristic(neigh, self.start, self.target),
                                       neigh,
                                       v_,
                                       s + 1,
                                       c_
                                       )
                    heapq.heappush(q, next_node)
        
        # No safe path to food and back to tail was found, find path directly to tail
        self.target = self.tail
        return self.exhaustive_search()
    
    @staticmethod
    def manhattan(row1, col1, row2, col2):
        return abs(row1 - row2) + abs(col1 - col2)
    
    def heuristic(self, position, origin, target):
        """
        Evenly balanced f(x) + g(x) heuristic is guaranteed to seek the shortest path first
        while still reducing the overall search space.
        
        position: (int(row), int(col)) current position
        origin: (row, col) Initial starting position
        target: (row, col) Target position
        """
        return self.manhattan(*position, *origin) + self.manhattan(*position, *target)
    
class Snake():
    def __init__(self, start_position):
        self.pos = start_position
        self.tail = start_position
        self.body = collections.deque([start_position])
        self.obstacles = collections.defaultdict(int)
        self.obstacles[start_position] = 0
        self.steps = 0
        self.safe_path = []
    
    def step(self):
        tail_return = self.tail
        self._seek_path()
        self._follow_safe_path()
        self._update_obstacles()
        self._seek_path_to_tail(tail_return)
        self._update_obstacles()
        
        
    def _seek_path(self):
        """Finds a safe path for the snake to reach food from the current position."""
        solver = PathFinder(self.pos, food, self.tail, self.obstacles, self.steps)
        v = solver.exhaustive_search()
        self.safe_path = v
        print(v, self.pos)
        
    def _seek_path_to_tail(self, tail_return):
        """Finds a safe path for the snake to reach tail from the current position."""
        solver = PathFinder(self.pos, tail_return, self.tail, self.obstacles, self.steps)
        v = solver.exhaustive_search()
        print(v, self.pos)
        self.safe_path = v
        
    def _follow_safe_path(self):
        self.body.appendleft(self.safe_path[0]) # add new head
        for i in range(1, len(self.safe_path)):
            self.body.pop()
            self.body.appendleft(self.safe_path[i])
        self.tail = self.body[-1]
        self.pos = self.body[0]
        
    def _update_obstacles(self):
        self.obstacles = collections.defaultdict(int)
        for i in range(len(self.body)+1):
            self.obstacles[self.body[-i]] = i
        
def show_grid(snake, R, C):
    arr = [[0]*C for _ in range(R)]
    arr[food[0]][food[1]] = 2
    for i, j in snake.body:
        arr[i][j] = 1
    for row in arr:
        print(row)
    print()
    
if __name__ == "__main__":
    global grid, graph, food
    
    settings = {"WIDTH": 800,
                "HEIGHT": 800,
                "ROWS": 6,
                "COLUMNS": 6,
                "SLEEP_TIME": 0,
                "LOCK_TIME": 0.2
                }
    
    #g = Game()
    #g.run()
    
    R, C = settings["ROWS"], settings["COLUMNS"]
    s = Snake(random_loc(R, C))
    spawn_food(s, R, C)
        
    graph = collections.defaultdict(list)
    for i in range(R):
        for j in range(C):
            a = (i, j)
            if i:
                b = (i-1, j)
                graph[a].append(b)
                graph[b].append(a)
            if j:
                b = (i, j-1)
                graph[a].append(b)
                graph[b].append(a)
    
    show_grid(s, R, C)
    for _ in range(30):
        s.step()
        spawn_food(s, R, C)
        show_grid(s, R, C)
    
    print(len(s.body))
    
    
    
    
    
    
    
    
    
    
    
    
    
    