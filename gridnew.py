from animal import Cell, AnimalDict
from rabbit import Rabbit
from fox import Fox
from collections import defaultdict
import pygame as pg

GRID_SIZE = 100

empty_animals = lambda: defaultdict(list) # type: ignore

class Grid:
    ''' Tracks animals in spatially partitioned grid '''
    grid_size = GRID_SIZE

    def __init__(self, num_rabbits: int, num_foxes: int, window_size: tuple[int, int]) -> None:
        self.cells: dict[Cell, AnimalDict] = defaultdict(empty_animals)
        self.animals = pg.sprite.Group()
        self.window_size = window_size
        self.init_animals(num_rabbits, num_foxes)

    def init_animals(self, num_rabbits: int, num_foxes: int) -> None:
        
        for _ in range(num_rabbits):
            rabbit = Rabbit(self.window_size, self.grid_size)
            self.animals.add(rabbit)
            self.cells[rabbit.cell]['Rabbit'].append(rabbit)

        for _ in range(num_foxes):
            fox = Fox(self.window_size, self.grid_size)
            self.animals.add(fox)
            self.cells[fox.cell]['Fox'].append(fox)

    def update(self) -> None:
        self.animals.update(self.cells)

    def draw(self, screen: pg.surface.Surface) -> None:
        self.animals.draw(screen)