# game-engine-3d

A 3d game engine written in python and c. Main program in python handles high-level proccesses, then uses ctypes to to render using c library SDL.

note: should only need gamebase.py, handle_inputs.py, and drawPolygons.so to run the program, other files are probably outdated

## Dependencies

python libraries
- math
- time
- random
- numpy
- ctypes
- pynput
- threading
- queue

c libraries
- stdio
- stdbool
- SDL2
- SDL_gfx
