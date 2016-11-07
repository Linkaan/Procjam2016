import pyximport
pyximport.install()
from level.pathfinding.cfindpath import cfind_path

def find_path(level, start, goal):
    return cfind_path(level, start, goal)
