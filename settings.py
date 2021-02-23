"""
A few additional notes on settings:
    
1. All default settings are stored in a dictionary in settings.py which is imported and then 
   unpacked as keyword input to the Game class.  
   
2. Number of rows (R) and number of columns (C) must be even.  
   This is because rectangular subarrays with an odd number of elements cannot have a Hamiltonian Cycle. 
   By setting R and C to even numbers the HamCycle.subdivide process can ensure that all subarrays 
   have an even number of elements.
   
3. You can either set the window WIDTH and HEIGHT in pixels <b>or</b> set the BOX_WIDTH in pixels.  
   If you set WIDTH to None and choose a BOX_WIDTH then the size of the window will adjust to fit the 
   row and column input values.  BOX_WIDTH is recommended as it avoids skewing of the grid when R &neq; C.
   
4. The game speed can be adjusted in game, but you can also choose a default game speed by adjusting SLEEP_TIME

5. Using a small MAX_SIZE (6) and SHUFFLE turned on makes the Hamiltonian Cycle appear more random 
   while a large MAX_SIZE (40) and SHUFFLE off makes the Hamiltonian Cycle appear very orderly
   
6. SHORTCUTS are changeable by tapping s key in game, when True it allows the snake to take 
   shortcuts and when False the snake must strictly follow the Hamiltonian Cycle.
   
7. SHOW_PATH toggles the Hamiltonian Cycle visibility on and off, can be changed in game with the h key.
"""

settings = {
            # =============================================================================
            # WINDOW SETTINGS
            # =============================================================================
            "WIDTH": 800,               # window width (pixels); change to None to autoscale window size
            "HEIGHT": 800,              # window height
            "BOX_WIDTH": 26,             # iff "WIDTH" is None each row and column will be "BOX_WIDTH" pixels wide
            
            # =============================================================================
            # GRID SETTINGS
            # =============================================================================
            "C": 100,                         # 4 <= C <= 400 and C must be even
            "R": 100,                         # 4 <= R <= 400 and R must be even
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