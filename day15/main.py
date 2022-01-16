import numpy as np
import pygame
from sandpiles import Sandpile

pygame.init()

size = width, height = 400, 400

screen = pygame.display.set_mode(size)
FPS = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

# colors
BLACK = (43, 48, 58)
RED = (255, 0, 0)

COL_1 = (12, 64, 254)
COL_2 = (117, 173, 232)
COL_3 = (210, 184, 1)
COL_4 = (95, 1, 1)

# create a sandpile filled with zeros
sp = Sandpile(np.zeros((400, 400)), topple = False)
sp.data[height // 2, width // 2] = 100000000

def form_image(sandpile, surface):
    pxarray = pygame.PixelArray(surface)
    for r in range(sandpile.row_count):
        for c in range(sandpile.col_count):
            if sandpile.data[r, c] == 0:
                pxarray[c, r] = COL_1
            elif sandpile.data[r, c] == 1:
                pxarray[c, r] = COL_2
            elif sandpile.data[r, c] == 2:
                pxarray[c, r] = COL_3
            elif sandpile.data[r, c] == 3:
                pxarray[c, r] = COL_4
            else:
                pxarray[c, r] = RED

running = True

while running:
    screen.fill(BLACK)

    form_image(sp, screen)
    for _ in range(100):
        sp.topple_once()

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
    pygame.display.update()
