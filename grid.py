from boid import Boid, Cell
from collections import defaultdict
import pygame as pg

GRID_SIZE = 100

class Grid:
    ''' Tracks boids in spatially partitioned grid '''
    grid_size = GRID_SIZE

    def __init__(self, num_boids: int, screen_size: tuple[int, int]):
        self.cells: dict[Cell, list[Boid]] = defaultdict(list)
        self.boids = pg.sprite.Group()

        for _ in range(num_boids): 
            boid = Boid(self, screen_size, self.grid_size)
            self.boids.add(boid)
            self.cells[boid.cell].append(boid)
    
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
        return nearby

    def update(self, dt: float) -> None:
        self.boids.update(dt)

    def draw(self, screen: pg.surface.Surface) -> None:
        self.boids.draw(screen)