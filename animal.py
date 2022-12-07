from math import sin, cos, atan2, radians, degrees
from random import randint
import pygame as pg
from typing import NamedTuple
import numpy as np
from collections import defaultdict
from abc import abstractmethod

WIDTH, HEIGHT = 0, 1
ANTICLOCKWISE, CLOCKWISE = -1, 1

Cell = NamedTuple('Cell', [('x', int), ('y', int)])
AnimalDict = dict[str, list['Animal']]

class Animal(pg.sprite.Sprite):

    # Number of nearest animals of a given species to "see"
    nearest_k = 5
    margin = 40
    speed: int
    turn_speed: int
    birth_dist_from_parent = 5

    def __init__(self, window_size: tuple[int, int], grid_size: int):
        super().__init__()
        self.window_size = window_size
        self.window_centre = pg.Vector2(self.window_size[0]/2, self.window_size[1]/2)
        self.grid_size = grid_size
        self.species = type(self).__name__
        self.init_pos()

    def init_pos(self, pos: None|pg.Vector2=None) -> None:
        if pos:
            d = self.birth_dist_from_parent
            self.pos += pg.Vector2(np.random.uniform(-d, d), np.random.uniform(-d, d))
        else:
            self.pos = pg.Vector2((randint(50, self.window_size[WIDTH ] - 50), 
                                   randint(50, self.window_size[HEIGHT] - 50)))
        self.angle = randint(0, 360)
        self.init_image()
        self.old_cell = self.cell

    def init_image(self) -> None:
        self.image = pg.Surface((15, 15)).convert()
        self.image.set_colorkey(0)
        self.color = pg.Color(0)
        self.color.hsva = (randint(0, 360), 90, 90) # type: ignore
        pg.draw.polygon(self.image, self.color, ((7,0), (13,14), (7,11), (1,14), (7,0)))
        self.bSize = 17
        self.orig_image = pg.transform.rotate(self.image.copy(), -90)
        self.rect = self.image.get_rect(center=self.pos)

    def update_cells(self, cells: dict[Cell, AnimalDict]) -> None:
        new_cell = self.cell

        if self.old_cell != new_cell:
            cells[self.old_cell][self.species].remove(self)
            cells[     new_cell][self.species].append(self)

        self.old_cell = new_cell

    def angle_towards(self, other: pg.Vector2) -> float:
        ''' Calculate angle towards other position '''
        return degrees(atan2(*(self.pos - other))) - 90

    def signed_angle_diff(self, target_angle: float) -> float:
        ''' Calculate signed difference between two angles. Returns value in [-180, 180] '''
        return (self.angle - target_angle + 180) % 360 - 180

    def update(self, cells: dict[Cell, AnimalDict]) -> None: # type: ignore
        ''' Update call '''
        neighbours = self.get_neighbours(cells)

        target_angle, near_edges = self.handle_edges()
        if not near_edges:
            target_angle = self.choose_angle(neighbours)

        self.image = pg.transform.rotate(self.orig_image, self.angle)

        self.update_position(target_angle)

        self.update_cells(cells)

    def update_position(self, target_angle: float) -> None:
        ''' Make move towards target_angle '''
        angle_diff = self.signed_angle_diff(target_angle)
        turn_direction = np.sign(angle_diff)
        turn_magnitude = 1 - abs(angle_diff) / 180 # in [0, 1]

        self.angle += turn_magnitude * self.turn_speed * turn_direction
        self.angle %= 360

        self.pos.x += self.speed * cos(radians(self.angle))
        self.pos.y -= self.speed * sin(radians(self.angle))

        self.rect.center = self.pos # type: ignore

    def handle_edges(self) -> tuple[float, bool]:
        ''' Returns target angle and bool True if animal was near edges '''
        if min(self.x, self.window_size[WIDTH]  - self.x,
               self.y, self.window_size[HEIGHT] - self.y) < self.margin:
            return self.angle_towards(self.window_centre), True
        return self.angle, False

    @abstractmethod
    def choose_angle(self, neighbours: AnimalDict) -> float:...

    @abstractmethod
    def give_birth(self) -> bool:...
    
    def get_neighbours(self, cells: dict[Cell, AnimalDict]) -> AnimalDict:
        ''' Returns a list of nearby animals within all surrounding 9 cells '''
        neighbours: AnimalDict = defaultdict(list)
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                animals = cells.get(Cell(self.cell.x + x, self.cell.y + y), {})
                neighbours['Rabbit'] += animals.get('Rabbit', [])
                neighbours['Fox']    += animals.get('Fox', [])
        neighbours[self.species].remove(self)
        
        neighbours['Fox']    = sorted(neighbours['Fox'],    key=lambda fox: fox.pos.distance_to(self.pos))[:self.nearest_k]
        neighbours['Rabbit'] = sorted(neighbours['Rabbit'], key=lambda fox: fox.pos.distance_to(self.pos))[:self.nearest_k]
        return neighbours

    @property
    def x(self) -> float:
        return self.rect.centerx # type: ignore

    @property
    def y(self) -> float:
        return self.rect.centery # type: ignore

    @property
    def cell(self) -> Cell:
        ''' xy coords to cell '''
        return Cell(int(self.pos.x//self.grid_size), int(self.pos.y//self.grid_size))