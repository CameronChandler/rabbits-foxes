from math import sin, cos, atan2, radians, degrees
from random import randint
import pygame as pg
import numpy as np

SPEED = 150 
WIDTH, HEIGHT = 0, 1

class Boid(pg.sprite.Sprite):

    def __init__(self, window_size: tuple[int, int]):
        super().__init__()
        self.window_size = window_size
        self.pos = pg.Vector2((randint(50, self.window_size[WIDTH ] - 50), 
                               randint(50, self.window_size[HEIGHT] - 50)))
        self.init_image()
        self.t = 0

    
    def init_image(self) -> None:
        self.image = pg.Surface((15, 15)).convert()
        self.image.set_colorkey(0)
        self.color = pg.Color(0)
        self.color.hsva = (randint(0,360), 90, 90)
        pg.draw.polygon(self.image, self.color, ((7,0), (13,14), (7,11), (1,14), (7,0)))
        self.bSize = 17
        self.orig_image = pg.transform.rotate(self.image.copy(), -90)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt: float, boids) -> None:
        x_total = 0
        y_total = 0
        for boid in boids:
            x_total += boid.pos.x
            y_total += boid.pos.y

        centre = (x_total/len(boids), y_total/len(boids))

        self.t += 5*dt
        #self.pos.x += 5*dt + randint(-2, 1)
        #self.pos.y += np.sin(self.t) + randint(-1, 1)
        self.pos.x += -np.sign(self.pos.x - centre[0]) + randint(-10, 10)
        self.pos.y += -np.sign(self.pos.y - centre[1]) + randint(-10, 10)

        self.rect.center = self.pos