#from math import sin, cos, atan2, radians, degrees
from boidnew import Boid
from random import randint
import pygame as pg
from typing import NamedTuple
import numpy as np

SPEED = 150 
WIDTH, HEIGHT = 0, 1

Cell = NamedTuple('Cell', [('x', int), ('y', int)])

class Rabbit(Boid):

    def __init__(self, window_size: tuple[int, int], grid_size: int):
        super().__init__(window_size, grid_size)
        
    def init_image(self) -> None:
        self.image = pg.Surface((15, 15)).convert()
        self.image.set_colorkey(0)
        self.color = pg.Color(0)
        self.color.hsva = (90, 90, 90) # type: ignore
        pg.draw.polygon(self.image, self.color, ((7,0), (13,14), (7,11), (1,14), (7,0)))
        self.bSize = 17
        self.orig_image = pg.transform.rotate(self.image.copy(), -90)
        self.rect = self.image.get_rect(center=self.pos)

    def move(self, dt: float, neighbours: list["Boid"]) -> None:
        x_total = 0
        y_total = 0
        
        for boid in neighbours:
            x_total += boid.pos.x
            y_total += boid.pos.y

        centre = (x_total/(len(neighbours)+ 0.001), y_total/(len(neighbours)+ 0.001))

        self.t += 5*dt
        self.pos.x += -np.sign(self.pos.x - centre[0]) + randint(-1, 1)
        self.pos.y += -np.sign(self.pos.y - centre[1]) + randint(-1, 1)
    