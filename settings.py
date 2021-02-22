






settings = {
            # =============================================================================
            # WINDOW SETTINGS
            # =============================================================================
            "WIDTH": 1000,               # window width (pixels)
            "HEIGHT": 1000,              # window height
            
            # =============================================================================
            # GAME SPEED SETTINGS
            # =============================================================================
            "SLEEP_TIME": 0.1,           # sleep between iterations to reduce the frame rate
            "LOCK_TIME": 0.2,            # delay between allowed input actions (seconds)
            
            # =============================================================================
            # HAMILTONIAN CYCLE SETTINGS            
            # =============================================================================
            "SHUFFLE": True,              # shuffle the kernel windows before merging sybcycles (True = more random grid)
            "MAX_SIZE": 6,                # 6 <= MAX_SIZE <= 36 the maximum window size for the subdivided array
            "HAM_COLOR": (100, 255, 100), # color of the ham path
            "HAM_WIDTH": 2,               # width of the hamiltonian cycle path
            "SHOW_PATH": True,

            # =============================================================================
            # SNAKE AND FOOD SETTINGS
            # =============================================================================
            "SNAKE_WIDTH": 0.8,           # fraction of min(col_width, row_height)
            "SNAKE_COLOR": (0, 125, 0), 
            "CENTER_SNAKE": False,        # start with snake in center of map
            "SNAKE_LENGTH": 10,           # the start length of the snake
            "FOOD_COLOR": (175, 0, 0),
            
            # =============================================================================
            # GRID SETTINGS
            # =============================================================================
            "C": 20,
            "R": 20,
            "GRID_COLOR": (150, 150, 150),
            "GRID_THICKNESS": 1,
            "SHOW_GRID": True               # Turn grid on / off
            }