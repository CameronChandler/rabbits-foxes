from boidold import Boid
from gridold import Grid
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
FPS = 60                # 30-9int(0
SHOW_FPS = True          # frame rate debug



class Window:

    def __init__(self, full_screen: bool):
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
    window = Window(FULL_SCREEN)

    boidTracker = Grid()
    boids = pg.sprite.Group()

    for _ in range(NUM_BOIDS): 
        boids.add(Boid(boidTracker, window.screen.get_size()))

    clock = pg.time.Clock()

    while True:
        if is_quit():
            pg.quit()
            return

        window.screen.fill(BGCOLOR)
        dt = clock.tick(FPS) / 1000
        
        boids.update(dt, SPEED)
        boids.draw(window.screen)
        
        if SHOW_FPS: 
            window.draw_fps(int(clock.get_fps()))

        pg.display.update()

if __name__ == '__main__':
    main()
    pg.quit()
