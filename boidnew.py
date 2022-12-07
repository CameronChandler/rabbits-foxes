#from math import sin, cos, atan2, radians, degrees
from random import randint
import pygame as pg
from typing import NamedTuple
import numpy as np

SPEED = 150 
WIDTH, HEIGHT = 0, 1

Cell = NamedTuple('Cell', [('x', int), ('y', int)])

class Boid(pg.sprite.Sprite):

    def __init__(self, window_size: tuple[int, int], grid_size: int):
        super().__init__()
        self.window_size = window_size
        self.grid_size = grid_size
        self.pos = pg.Vector2((randint(50, self.window_size[WIDTH ] - 50), 
                               randint(50, self.window_size[HEIGHT] - 50)))
        self.dir = pg.Vector2(1, 0)
        self.ang = randint(0, 360)
        self.init_image()
        self.t = 0

    def init_image(self) -> None:
        self.image = pg.Surface((15, 15)).convert()
        self.image.set_colorkey(0)
        self.color = pg.Color(0)
        self.color.hsva = (randint(0, 360), 90, 90) # type: ignore
        pg.draw.polygon(self.image, self.color, ((7,0), (13,14), (7,11), (1,14), (7,0)))
        self.bSize = 17
        self.orig_image = pg.transform.rotate(self.image.copy(), -90)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, dt: float, cells: dict[Cell, list["Boid"]]) -> None: # type: ignore
        old_cell = self.cell
        neighbours = self.get_neighbours(cells)

        self.move(dt, neighbours)

        new_cell = self.cell
        if old_cell != new_cell:
            cells[old_cell].remove(self)
            cells[new_cell].append(self)

        self.image = pg.transform.rotate(self.orig_image, -self.ang)
        self.dir = pg.Vector2(1, 0).rotate(self.ang).normalize()
        #self.pos += self.dir * dt * (SPEED + (7 - ncount) * 5)

        self.rect.center = self.pos # type: ignore

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
    
    def get_neighbours(self, cells: dict[Cell, list["Boid"]]) -> list["Boid"]:
        ''' Returns a list of nearby boids within all surrounding 9 cells '''
        nearby: list[Boid] = []
        for x in (-1, 0, 1):
            for y in (-1, 0, 1):
                nearby += cells.get(Cell(self.cell.x + x, self.cell.y + y), [])
        nearby.remove(self)
        return nearby

    @property
    def cell(self) -> Cell:
        ''' xy coords to cell '''
        return Cell(int(self.pos.x//self.grid_size), int(self.pos.y//self.grid_size))