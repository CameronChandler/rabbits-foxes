from math import sin, cos, atan2, radians, degrees
from animal import Animal, AnimalDict
from random import randint
import pygame as pg
from typing import NamedTuple
import numpy as np

WIDTH, HEIGHT = 0, 1

Cell = NamedTuple('Cell', [('x', int), ('y', int)])

class Fox(Animal):
    species = 'Fox'
    speed = 1
    turn_speed = 2

    def __init__(self, window_size: tuple[int, int], grid_size: int):
        super().__init__(window_size, grid_size)
        
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
        x_total = 0
        y_total = 0
        
        for animal in neighbours[self.species]:
            x_total += animal.pos.x
            y_total += animal.pos.y

        centre = (x_total/(len(neighbours[self.species])+ 0.001), y_total/(len(neighbours[self.species])+ 0.001))

        return degrees(atan2(*(self.pos - centre)))