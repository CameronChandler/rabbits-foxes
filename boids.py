from math import sin, cos, atan2, radians, degrees
from random import randint
import pygame as pg

'''
PyNBoids - a Boids simulation - github.com/Nikorasu/PyNBoids
This version uses a spatial partitioning grid to improve performance.
Copyright (c) 2021  Nikolaus Stromberg  nikorasu85@gmail.com
'''
FULL_SCREEN = True       # True for Fullscreen, or False for Window
NUM_BOIDS = 100             # How many boids to spawn, too many may slow fps
SPEED = 150             # Movement speed
WIDTH, HEIGHT = 0, 1

class Boid(pg.sprite.Sprite):

    def __init__(self, grid, window_size: tuple[int, int]):  #, cHSV=None
        super().__init__()
        self.grid = grid
        self.window_size = window_size
        self.image = pg.Surface((15, 15)).convert()
        self.image.set_colorkey(0)
        self.color = pg.Color(0)  # preps color so we can use hsva
        self.color.hsva = (randint(0,360), 90, 90) #if cHSV is None else cHSV # randint(5,55)
        pg.draw.polygon(self.image, self.color, ((7,0), (13,14), (7,11), (1,14), (7,0)))
        self.bSize = 17
        self.orig_image = pg.transform.rotate(self.image.copy(), -90)
        self.dir = pg.Vector2(1, 0)  # sets up forward direction
        self.rect = self.image.get_rect(center=(randint(50, self.window_size[WIDTH ] - 50), 
                                                randint(50, self.window_size[HEIGHT] - 50)))
        self.ang = randint(0, 360)  # random start angle, & position ^
        self.pos = pg.Vector2(self.rect.center)
        self.grid_lastpos = self.grid.getcell(self.pos)
        self.grid.add(self, self.grid_lastpos)

    def update(self, dt, speed):
        selfCenter = pg.Vector2(self.rect.center)
        turnDir = xvt = yvt = yat = xat = 0
        turnRate = 120 * dt  # about 120 seems ok
        margin = 42
        self.ang = self.ang + randint(-4, 4)
        # Grid update stuff
        self.grid_pos = self.grid.getcell(self.pos)
        if self.grid_pos != self.grid_lastpos:
            self.grid.add(self, self.grid_pos)
            self.grid.remove(self, self.grid_lastpos)
            self.grid_lastpos = self.grid_pos
        # get nearby boids and sort by distance
        near_boids = self.grid.getnear(self, self.grid_pos)
        neiboids = sorted(near_boids, key=lambda i: pg.Vector2(i.rect.center).distance_to(selfCenter))
        del neiboids[7:]  # keep 7 closest, dump the rest
        # when boid has neighborS (walrus sets ncount)
        if (ncount := len(neiboids)) > 1:
            nearestBoid = pg.Vector2(neiboids[0].rect.center)
            for nBoid in neiboids:  # adds up neighbor vectors & angles for averaging
                xvt += nBoid.rect.centerx
                yvt += nBoid.rect.centery
                yat += sin(radians(nBoid.ang))
                xat += cos(radians(nBoid.ang))
            tAvejAng = degrees(atan2(yat, xat))
            targetV = (xvt / ncount, yvt / ncount)
            # if too close, move away from closest neighbor
            if selfCenter.distance_to(nearestBoid) < self.bSize: 
                targetV = nearestBoid
            tDiff = targetV - selfCenter  # get angle differences for steering
            tDistance, tAngle = pg.math.Vector2.as_polar(tDiff)
            # if boid is close enough to neighbors, match their average angle
            if tDistance < self.bSize*5: 
                tAngle = tAvejAng
            # computes the difference to reach target angle, for smooth steering
            angleDiff = (tAngle - self.ang) + 180
            if abs(tAngle - self.ang) > .5: 
                turnDir = (angleDiff / 360 - (angleDiff // 360)) * 360 - 180
            # if boid gets too close to target, steer away
            if tDistance < self.bSize and targetV == nearestBoid: 
                turnDir = -turnDir
        # Avoid edges of screen by turning toward the edge normal-angle
        sc_x, sc_y = self.rect.centerx, self.rect.centery
        if min(sc_x, sc_y, self.window_size[WIDTH ] - sc_x, self.window_size[HEIGHT] - sc_y) < margin:
            if sc_x < margin: 
                tAngle = 0
            elif sc_x > self.window_size[WIDTH ] - margin: 
                tAngle = 180
            if sc_y < margin: 
                tAngle = 90
            elif sc_y > self.window_size[HEIGHT] - margin: 
                tAngle = 270
            angleDiff = (tAngle - self.ang) + 180  # increase turnRate to keep boids on screen
            turnDir = (angleDiff / 360 - (angleDiff // 360)) * 360 - 180
            edgeDist = min(sc_x, sc_y, self.window_size[WIDTH ] - sc_x, self.window_size[HEIGHT] - sc_y)
            turnRate = turnRate + (1 - edgeDist / margin) * (20 - turnRate) #turnRate=minRate, 20=maxRate
        if turnDir != 0:  # steers based on turnDir, handles left or right
            self.ang += turnRate * abs(turnDir) / turnDir
        self.ang %= 360  # ensures that the angle stays within 0-360
        # Adjusts angle of boid image to match heading
        self.image = pg.transform.rotate(self.orig_image, -self.ang)
        self.rect = self.image.get_rect(center=self.rect.center)  # recentering fix
        self.dir = pg.Vector2(1, 0).rotate(self.ang).normalize()
        self.pos += self.dir * dt * (speed + (7 - ncount) * 5)  # movement speed

        # Actually update position of boid
        self.rect.center = self.pos