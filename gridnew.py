from animal import Animal, Cell, AnimalDict
from rabbit import Rabbit
from fox import Fox
from collections import defaultdict
import pygame as pg
from typing import Type

empty_animals = lambda: defaultdict(list) # type: ignore

class Grid:
    ''' Tracks animals in spatially partitioned grid '''
    grid_size = 100
    predation_distance = 5

    def __init__(self, num_rabbits: int, num_foxes: int, window_size: tuple[int, int]) -> None:
        self.cells: dict[Cell, AnimalDict] = defaultdict(empty_animals)
        self.animals = pg.sprite.Group()
        self.window_size = window_size
        self.init_animals(num_rabbits, num_foxes)

    def init_animals(self, num_rabbits: int, num_foxes: int) -> None:
        
        for _ in range(num_rabbits):
            self.add(Rabbit)

        for _ in range(num_foxes):
            self.add(Fox)

    def add(self, animal_class: Type[Animal], pos: None|pg.Vector2=None) -> None:
        animal = animal_class(self.window_size, self.grid_size)
        if pos:
            animal.init_pos(pos)
        self.animals.add(animal)
        self.cells[animal.cell][animal_class.__name__].append(animal)

    def update(self) -> None:
        self.animals.update(self.cells)
        for animals in list(self.cells.values()):
            self.handle_births(animals)
            #self.handle_predation(animals)
            #self.handle_starving(animals)

    def handle_births(self, animals: AnimalDict) -> None:
        for parent in animals['Rabbit'] + animals['Fox']:
            if parent.give_birth():
                self.add(parent.__class__, parent.pos)

    def handle_predation(self, animals: AnimalDict) -> None:
        raise(NotImplementedError)

    def draw(self, screen: pg.surface.Surface) -> None:
        self.animals.draw(screen)