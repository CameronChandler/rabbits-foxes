from boids import Boid
import pygame as pg

'''
PyNBoids - a Boids simulation - github.com/Nikorasu/PyNBoids
This version uses a spatial partitioning grid to improve performance.
Copyright (c) 2021  Nikolaus Stromberg  nikorasu85@gmail.com
'''
FULL_SCREEN = False       # True for Fullscreen, or False for Window
NUM_BOIDS = 100             # How many boids to spawn, too many may slow fps
SPEED = 150             # Movement speed
WIDTH = 900             # Window Width (1200)
HEIGHT = 600            # Window Height (800)
BGCOLOR = (0, 0, 0)     # Background color in RGB
FPS = 60                # 30-90
SHOW_FPS = True          # frame rate debug


class BoidGrid:
    ''' Tracks boids in spatially partitioned grid '''

    def __init__(self):
        self.grid_size = 100
        self.dict = {}
    
    def getcell(self, pos):
        ''' finds the grid cell corresponding to given pos '''
        return (pos[0]//self.grid_size, pos[1]//self.grid_size)
    
    def add(self, boid, key):
        ''' boids add themselves to cells when crossing into new cell '''
        if key in self.dict:
            self.dict[key].append(boid)
        else:
            self.dict[key] = [boid]
    
    def remove(self, boid, key):
        ''' they also remove themselves from the previous cell '''
        if key in self.dict and boid in self.dict[key]:
            self.dict[key].remove(boid)
    
    def getnear(self, boid, key):
        ''' Returns a list of nearby boids within all surrounding 9 cells '''
        if key in self.dict:
            nearby = []
            for x in (-1, 0, 1):
                for y in (-1, 0, 1):
                    nearby += self.dict.get((key[0] + x, key[1] + y), [])
            nearby.remove(boid)
        return nearby

class Window:

    def __init__(self, full_screen: bool, show_fps: bool):
        self.screen = self.init_screen(full_screen)
        self.font = pg.font.Font(None, 30)

    def init_screen(self, full_screen: bool) -> pg.surface.Surface:
        pg.init()
        pg.display.set_caption('Rabbits and Foxes')
        pg.display.set_icon(pg.image.load('nboids.png'))
        
        if full_screen:
            curr_resolution = pg.display.Info().current_w, pg.display.Info().current_h
            pg.mouse.set_visible(False)
            return pg.display.set_mode(curr_resolution, pg.SCALED | pg.NOFRAME | pg.FULLSCREEN, vsync=1)

        return pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE | pg.SCALED, vsync=1)

    def draw_fps(self, fps: int):
        self.screen.blit(self.font.render(str(fps), True, [0, 200, 0]), (8, 8))

def is_quit() -> bool:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            return True
        if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            return True
    return False

def main():
    window = Window(FULL_SCREEN, SHOW_FPS)

    boidTracker = BoidGrid()
    boids = pg.sprite.Group()

    for n in range(NUM_BOIDS): 
        boids.add(Boid(boidTracker, window.screen))

    clock = pg.time.Clock()

    while True:
        if is_quit():
            pg.quit()
            return

        window.screen.fill(BGCOLOR)
        dt = clock.tick(FPS) / 1000
        # update boid logic, then draw them
        boids.update(dt, SPEED)
        boids.draw(window.screen)
        
        if SHOW_FPS: 
            window.draw_fps(int(clock.get_fps()))

        pg.display.update()

if __name__ == '__main__':
    main()
    pg.quit()
