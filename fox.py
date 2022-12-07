#from math import sin, cos, atan2, radians, degrees
from animal import Animal
from random import randint
import pygame as pg
from typing import NamedTuple
import numpy as np

SPEED = 150 
WIDTH, HEIGHT = 0, 1

Cell = NamedTuple('Cell', [('x', int), ('y', int)])

class Fox(Animal):
    species = 'Fox'

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