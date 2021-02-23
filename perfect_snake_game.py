import time
import collections
import functools
import random

import numpy as np
import pygame

from cycle_growth import HamCycle
import settings

class Snake:
    def __init__(self, R, C, graph, start_length, centered = True, shortcuts = True):
        self.R = R
        self.C = C
        
        # Once he snake is max_length just chase tail
        self.chase_tail = False

        # a directed graph for a hamiltonian cycle of the map (the path the snake will follow)
        self.graph = graph 
        
        # spawn a snake head at a random location
        head = (R // 2, C // 2) if centered else self.spawn_snake(R, C)
        self.body = collections.deque([head])
        
        # Snake starts at snake_length
        for _ in range(start_length - 1):
            self.body.appendleft(self.graph[self.body[0]])
        
        self.food = self.spawn_food(R, C)
        self.on_food = False # True when the snake's head is on the food
        
        # If there is a shorter (and safe) path to food, break from Hamiltonian Cycle
        self.shortcuts = shortcuts
        self.cost = self.calc_cost(self.food) if shortcuts else collections.defaultdict(int) 
        
    def spawn_snake(self, R, C):
        return spawn(R, C)
        
    def spawn_food(self, R, C):
        snake_body = set(self.body)
        return spawn(R, C, choices=[(m, n) for m in range(R) for n in range(C) if (m, n) not in snake_body])
    
    def is_safe(self, new_head, food_found = 3):
        """
        Looks ahead snake.length + food_found steps:
            if snake never bites it's tail when following the ham path returns True
            if snake bites its tail then the path is not safe returns False
        """
        if self.chase_tail:
            return False
        
        temp_body = self.body.copy()
        temp_body.appendleft(new_head)
        temp_body_set = set(temp_body)
        for _ in range(len(temp_body)):
            temp_body.appendleft(self.graph[temp_body[0]])
            if food_found > 0:
                temp_body_set.remove(temp_body.pop())
            food_found -= 1
            if temp_body[0] in temp_body_set:
                return False
            temp_body_set.add(temp_body[0])
        return True
            
    def step(self):
        """Move the snake forward one step."""
        if not self.shortcuts or self.chase_tail:
            self.body.appendleft(self.graph[self.body[0]])
        else:
            i, j = self.body[0]
            new_head = min((pos for pos in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)) if pos not in self.body), 
                           key = lambda p: self.cost[p])
            if new_head == self.graph[self.body[0]] or self.is_safe(new_head):
                # Make sure short cut doesn't lead to potential death
                self.body.appendleft(new_head)
            else:
                self.body.appendleft(self.graph[self.body[0]])
        
        if not self.on_food:
            self.body.pop()
        
        # If snake found food, update food
        self.on_food = self.food == self.body[0]
        if self.on_food:
            self.food = self.spawn_food(self.R, self.C)
            if self.food == (-1, -1):
                self.chase_tail = True
            if self.shortcuts:
                self.cost = self.calc_cost(self.food)
    
    @functools.lru_cache(None)
    def calc_cost(self, food):
        """Returns a map of (i, j) -> steps to reach food if following the ham cycle"""
        if self.chase_tail:
            return collections.defaultdict(lambda: self.R * self.C)
        
        pos = self.graph[food]
        cost = collections.defaultdict(lambda: self.R * self.C)
        cost[food] = 0
        N = self.R * self.C
        steps = 1
        while steps <= N:
            cost[pos] = N - steps
            pos = self.graph[pos]
            steps += 1
        return cost
        
        
class Game():
    def __init__(self, **kwargs):
        pygame.init()
        
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
        
        # set display width and height
        if self.WIDTH is None:
            self.WIDTH, self.HEIGHT = self.C*self.BOX_WIDTH, self.R*self.BOX_WIDTH
        
        # Create 
        self.SURFACE = pygame.display.set_mode((self.HEIGHT, self.WIDTH))
        self.COL_WIDTH = self.WIDTH // self.C
        self.ROW_HEIGHT = self.HEIGHT // self.R
        
        # Hamiltonian cycle is HamCycle.graph
        self.HAM = HamCycle(self.R, self.C, max_size=self.MAX_SIZE, shuffle=self.SHUFFLE, display=False)
        
        # Draw grid and hamiltonian cycle
        self.GRID_SURFACE = self.get_grid_surface()
        self.HAM_SURFACE_GRID, self.HAM_SURFACE = self.get_ham_surface(self.HAM.graph)
        
        # Snake
        self.SNAKE = Snake(self.R, self.C, self.HAM.graph, self.SNAKE_LENGTH, 
                           centered=self.CENTER_SNAKE, shortcuts=self.SHORTCUTS)
        self.SNAKE_WIDTH = int(round(self.SNAKE_WIDTH * min(self.COL_WIDTH, self.ROW_HEIGHT), 0))
        
        # True when the game is running
        self.active = True           
        
        # Inputs are locked until time > input_lock
        self.input_lock = -1
        
        # Blank Screen
        self.BLANK = pygame.surfarray.make_surface(np.array([[(0,0,0) for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]))
        
    def temporary_lock(self):
        """Temporarily locks out keys to prevent accidental double key presses."""
        self.input_lock = time.time() + self.LOCK_TIME
        
    def get_grid_surface(self):
        """
        Returns a pygame surface with a grid that marks the rows and columns that the snake can move on.
        """
        arr = [[(0,0,0) for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        for i in range(0, self.HEIGHT, self.ROW_HEIGHT):
            for j in range(self.WIDTH):
                arr[i][j] = self.GRID_COLOR
        for j in range(0, self.WIDTH, self.COL_WIDTH):
            for i in range(self.HEIGHT):
                arr[i][j] = self.GRID_COLOR
        return pygame.surfarray.make_surface(np.array(arr))
    
    def get_ham_surface(self, graph, start = (0, 0)):
        """
        Creates a pygame surface showing the hamiltonian path.
        Returns ham_surface_with_grid, ham_surface_without_grid
        """
        ham_surface_grid = self.GRID_SURFACE.copy()
        ham_surface = pygame.surfarray.make_surface(np.array([[(0,0,0) for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]))
        path = [start, graph[start]]
        while path[-1] != start:
            path.append(graph[path[-1]])
        path = [self.map_to_grid(*p) for p in path]
        pygame.draw.lines(ham_surface, self.HAM_COLOR, True, path, self.HAM_WIDTH)
        pygame.draw.lines(ham_surface_grid, self.HAM_COLOR, True, path, self.HAM_WIDTH)
        return ham_surface_grid, ham_surface
    
    def map_to_grid(self, i, j):
        """
        Maps the grid point (row = i, col = j) to the center of the block representing (i, j)
        i.e. if the window is 100 by 100 pixels and there are 10 rows and 10 columns:
            (0, 0) -> (5, 5)
            (8, 5) -> (85, 55)
        """
        y = (self.ROW_HEIGHT // 2) + i * self.ROW_HEIGHT
        x = (self.COL_WIDTH // 2) + j * self.COL_WIDTH
        return (y, x)
        
    def run(self):
        """
        Main game loop.
        Handles input key presses, updating snake position, and drawing the background and snake.
        """
        
        # Set display icon and window name
        logo = pygame.image.load("./graphics/simple-logo.png")
        pygame.display.set_icon(logo)
        pygame.display.set_caption('Hamiltonian Snake')
        
        while self.active:
            time.sleep(self.SLEEP_TIME)
            self.get_events()
            keys = pygame.key.get_pressed()
            t = time.time()
            
            if t >= self.input_lock:
                if keys[pygame.K_UP]:
                    self.temporary_lock()
                    self.SLEEP_TIME -= 0.01
                    self.SLEEP_TIME = max(0, self.SLEEP_TIME)
                elif keys[pygame.K_DOWN]:
                    self.temporary_lock()
                    self.SLEEP_TIME += 0.01
                    self.SLEEP_TIME = min(0.3, self.SLEEP_TIME)
                elif keys[pygame.K_ESCAPE]:
                    self.temporary_lock()
                    self.active = False
                elif keys[pygame.K_g]:
                    self.UPDATE_BACKGROUND = True
                    self.temporary_lock()
                    self.SHOW_GRID = not self.SHOW_GRID
                    print("Show Grid",self.SHOW_GRID)
                elif keys[pygame.K_h]:
                    self.UPDATE_BACKGROUND = True
                    self.temporary_lock()
                    self.SHOW_PATH = not self.SHOW_PATH
                    print('Show Path', self.SHOW_PATH)
                elif keys[pygame.K_s]:
                    self.temporary_lock()
                    self.SHORTCUTS = not self.SHORTCUTS
                    self.SNAKE.shortcuts = self.SHORTCUTS
                    self.SNAKE.cost = self.SNAKE.calc_cost(self.SNAKE.food)
                    print('Shortcuts', self.SHORTCUTS)
                
            # Move snake forward one step
            self.SNAKE.step()
            
            # Draw the snake and board            
            self.draw()
    
        pygame.quit()
        
    def get_events(self):
        """Gets key and mouse inputs.  Deactivates game if input action was quit."""
        self.events = pygame.event.poll()
        if self.events.type == pygame.QUIT:
            self.active = False
        self.keys_press = pygame.key.get_pressed()
        self.mouse_press = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        
    def get_food_rect(self):
        """Returns [top, left, width, height] for the food object in pixels."""
        i, j = self.map_to_grid(*self.SNAKE.food)
        x0, y0 = j - self.SNAKE_WIDTH // 2, i - self.SNAKE_WIDTH // 2
        return [y0, x0, self.SNAKE_WIDTH, self.SNAKE_WIDTH]

    def draw(self):
        """Updates pygame display with background, snake and food."""
        if self.UPDATE_BACKGROUND:
            self.SURFACE.blit(self.BLANK, (0, 0)) # blank screen
            self.UPDATE_BACKGROUND = False
        
        # Draw grid and / or hamiltonian cycle
        if self.SHOW_PATH and self.SHOW_GRID:
            self.SURFACE.blit(self.HAM_SURFACE_GRID, (0, 0))
        elif self.SHOW_PATH:
            self.SURFACE.blit(self.HAM_SURFACE, (0, 0))
        elif self.SHOW_GRID:
            self.SURFACE.blit(self.GRID_SURFACE, (0, 0))
        else:
            self.SURFACE.blit(self.BLANK, (0, 0))
        
        # Draw snake
        pygame.draw.lines(self.SURFACE, self.SNAKE_COLOR, False, 
                          [self.map_to_grid(*segment) for segment in self.SNAKE.body], 
                          self.SNAKE_WIDTH
                          )
        
        # Draw apple
        self.SNAKE.food
        pygame.draw.rect(self.SURFACE, self.FOOD_COLOR, self.get_food_rect())
        
        # Update display
        pygame.display.flip()

def spawn(R, C, choices = None):
    """
    Returns a random location on a grid of dimensions (R, C).
    If Choices is given, randomly selects a position from choices (a list of positions (y, x)).
    """
    if choices is None:
        return random.randint(0, R-1), random.randint(0, C-1)
    elif len(choices) == 1:
        return (-1, -1)
    return random.choice(choices)

if __name__ == "__main__":
    g = Game(**settings.settings)
    g.run()