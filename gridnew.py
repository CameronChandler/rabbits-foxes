from boidnew import Boid, Cell
from rabbit import Rabbit
from collections import defaultdict
import pygame as pg

GRID_SIZE = 100

class Grid:
    ''' Tracks boids in spatially partitioned grid '''
    grid_size = GRID_SIZE

    def __init__(self, num_rabbits: int, num_foxes: int, window_size: tuple[int, int]) -> None:
        self.cells: dict[Cell, list[Boid]] = defaultdict(list)
        self.boids = pg.sprite.Group()
        self.window_size = window_size
        self.init_animals(num_rabbits, num_foxes)

    def init_animals(self, num_rabbits: int, num_foxes: int) -> None:

        for _ in range(num_rabbits):
            boid = Rabbit(self.window_size, self.grid_size)
            self.boids.add(boid)
            self.cells[boid.cell].append(boid)

        for _ in range(num_foxes):
            boid = Boid(self.window_size, self.grid_size)
            self.boids.add(boid)
            self.cells[boid.cell].append(boid)

    def update(self, dt: float) -> None:
        self.boids.update(dt, self.cells)

    def draw(self, screen: pg.surface.Surface) -> None:
        self.boids.draw(screen)