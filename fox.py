from animal import Animal, AnimalDict
import pygame as pg
from typing import NamedTuple
import numpy as np

WIDTH, HEIGHT = 0, 1

Cell = NamedTuple('Cell', [('x', int), ('y', int)])

class Fox(Animal):
    species = 'Fox'
    max_speed = 2
    turn_speed = 2

    def __init__(self, window_size: tuple[int, int], grid_size: int, age: int | None=None):
        super().__init__(window_size, grid_size, age)
        
    def init_image(self) -> None:
        self.image = pg.Surface((15, 15)).convert()
        self.image.set_colorkey(0)
        self.color = pg.Color(0)
        self.color.hsva = (360, 90, 90) # type: ignore
        pg.draw.polygon(self.image, self.color, ((7,0), (13,14), (7,11), (1,14), (7,0)))
        self.bSize = 17
        self.orig_image = pg.transform.rotate(self.image.copy(), -90)
        self.rect = self.image.get_rect(center=self.pos)

    def choose_angle(self, neighbours: AnimalDict) -> float:
        # Move towards nearest rabbit
        if neighbours['Rabbit']:
            return self.angle_towards(neighbours['Rabbit'][0].pos) # type: ignore
        # Move away from nearest fox
        if neighbours['Fox']:
            return -self.angle_towards(neighbours['Fox'][0].pos) # type: ignore
        # Keep going
        return self.angle

    def give_birth(self) -> bool:
        if (self.energy < self.birth_energy) or (self.age < self.adult_age) or (self.time_since_last_birth < self.birth_recovery):
            return False
        
        if np.random.uniform() < 0.002:
            self.time_since_last_birth = 0
            return True

        return False

    def eaten(self):
        ''' Method called when fox eats a rabbit '''
        self.energy = 1
    
    def handle_energy(self) -> None:
        self.energy -= 0.0005