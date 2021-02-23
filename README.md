# perfect-snake-challenge
Bot plays a perfect game of snake by following a Hamiltonian Cycle and taking shortcuts when it is safe to do so.

# usage

Adjust settings.py to the desired initial conditions.  

<details>

<summary>Initial settings are as follows:</summary>


```python
settings = {
            # =============================================================================
            # WINDOW SETTINGS
            # =============================================================================
            "WIDTH": None,               # window width (pixels) if None will be calculated from pixels per column
            "HEIGHT": 1200,              # window height
            "COLUMN_WIDTH": 30,          # iff "WIDTH" is None each row and column will be "COLUMN_WIDTH" pixels wide
            
            # =============================================================================
            # GRID SETTINGS
            # =============================================================================
            "C": 40,                         # 4 <= C <= 400 and C must be even
            "R": 40,                         # 4 <= R <= 400 and R must be even
            "GRID_COLOR": (150, 150, 150),
            "GRID_THICKNESS": 1,
            "SHOW_GRID": False,              # Turn grid on / off
            "UPDATE_BACKGROUND": False,      # Switches true for one frame when grid or hamcycle changes
            
            # =============================================================================
            # GAME SPEED SETTINGS
            # =============================================================================
            "SLEEP_TIME": 0.02,          # sleep between iterations to reduce the frame rate
            "LOCK_TIME": 0.2,            # delay between allowed input actions (seconds)
            
            # =============================================================================
            # HAMILTONIAN CYCLE SETTINGS            
            # =============================================================================
            "SHUFFLE": True,              # shuffle the kernel windows before merging sybcycles (True = more random grid)
            "MAX_SIZE": 6,                # 6 <= MAX_SIZE <= 36 the maximum window size for the subdivided array
            "HAM_COLOR": (100, 200, 100), # color of the ham path
            "HAM_WIDTH": 1,               # width of the hamiltonian cycle path
            "SHOW_PATH": True,
            "SHORTCUTS": True,    # Allows snake to leave the path if it is safe and efficient to do so

            # =============================================================================
            # SNAKE AND FOOD SETTINGS
            # =============================================================================
            "SNAKE_WIDTH": 0.8,           # fraction of min(col_width, row_height)
            "SNAKE_COLOR": (0, 100, 0), 
            "CENTER_SNAKE": False,        # start with snake in center of map
            "SNAKE_LENGTH": 10,           # the start length of the snake
            "FOOD_COLOR": (175, 0, 0),
            }
```

</details>

# controls

up / down arrow keys: Speeds up / slows down game speed
g: show / hide grid
h: show / hide Hamiltonian cycle
s: on / off shortcuts (if off snake will strictly follow the Hamiltonian cycle)