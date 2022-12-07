from boidold import Boid
from typing import NamedTuple
from collections import defaultdict
import pygame as pg

GRID_SIZE = 100
Cell = NamedTuple('Cell', [('x', int), ('y', int)])

class Grid:
    ''' Tracks boids in spatially partitioned grid '''
    grid_size = GRID_SIZE

    def __init__(self):
        self.cells: dict[Cell, list[Boid]] = defaultdict(list)
    
    def get_cell(self, pos: pg.math.Vector2) -> Cell:
        ''' xy coords to cell '''
        return Cell(int(pos[0]//self.grid_size), int(pos[1]//self.grid_size))
    
    def add(self, boid: Boid, cell: Cell):
        ''' Add boid to cell '''
        self.cells[cell].append(boid)
    
    def remove(self, boid: Boid, cell: Cell):
        ''' Remove boid from cell '''
        self.cells[cell].remove(boid)
    
    def get_near(self, boid: Boid, cell: Cell) -> list[Boid]:
        ''' Returns a list of nearby boids within all surrounding 9 cells '''
        nearby: list[Boid] = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                nearby += self.cells.get(Cell(cell.x + x, cell.y + y), [])
        nearby.remove(boid)
        return nearby