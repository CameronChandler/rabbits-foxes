import pygame as pg
from boidnew import Boid

FULL_SCREEN = False  
NUM_BOIDS = 100      
SPEED = 150          
WIDTH = 900          
HEIGHT = 600         
BGCOLOR = (0, 0, 0)  
FPS = 60             
SHOW_FPS = True      

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

    boids = pg.sprite.Group()
    for _ in range(NUM_BOIDS):
        boids.add(Boid(window.screen.get_size()))

    clock = pg.time.Clock()

    while True:
        if is_quit():
            pg.quit()
            return

        window.screen.fill(BGCOLOR)
        dt = clock.tick(FPS) / 1000

        boids.update(dt, boids)
        boids.draw(window.screen)
        
        if SHOW_FPS: 
            window.draw_fps(int(clock.get_fps()))

        pg.display.update()


if __name__ == '__main__':
    main()
    pg.quit()