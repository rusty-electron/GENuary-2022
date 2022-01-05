import random
import pygame
import numpy as np

# TODO: find a better implementation of perlin noise
from perlin_noise import PerlinNoise

pygame.init()
size = width, height = 600, 600

screen = pygame.display.set_mode(size)
FPS = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 224, 102)
RED = (255, 0, 0)

PALLETES = [
        ((45, 46, 46), (251, 251, 251)),
        ((55, 57, 46), (25, 100, 126)),
        ((40, 83, 107), (194, 148, 138)),
        ((34, 42, 104), (226, 173, 242)),
        ((49, 24, 71), (236, 64, 103)),
        ((88, 129, 87), (163, 177, 138)),
        ]

left_x = int(width * -0.5)
right_x = int(width * 1.5)
top_y = int(height * -0.5)
bottom_y = int(height * 1.5)

resolution = int(width * 0.02)
num_columns = (right_x - left_x) // resolution
num_rows = (bottom_y - top_y) // resolution

grid = np.ones((num_rows, num_columns))

def gen_angles():
    for row in range(num_rows):
        for col in range(num_columns):
            noise_val = noise([col/num_columns, row/num_rows])
            angle = noise_val * 2 * np.pi
            grid[row][col] = angle

def draw_curve(start_x, start_y, steps = 10, step_len = 15, col = WHITE):
    for _ in range(steps):
        x_offset = start_x - left_x
        y_offset = start_y - top_y

        column_index = int(x_offset / resolution)
        row_index = int(y_offset / resolution)

        try:
            grid_angle = grid[row_index, column_index]
        except:
            return
        x_step = step_len * np.cos(grid_angle)
        y_step = step_len * np.sin(grid_angle)

        pygame.draw.line(screen, col, (start_x, start_y), (start_x + x_step, start_y + y_step))

        start_x += x_step
        start_y += y_step

running = True
iteration = 0
while running:
    COL_PAL = PALLETES[(iteration % len(PALLETES))]
    noise = PerlinNoise(octaves = 3.5, seed = random.randint(10, 100))
    gen_angles()
    screen.fill(COL_PAL[0])

    # show the flow field vectors
    # for idx, i in enumerate(np.arange(left_x, right_x, resolution)):
    #     for jdx,j in enumerate(np.arange(top_y, bottom_y, resolution)):
    #         size = 8
    #         pygame.draw.circle(screen, BLACK, (i, j), 1)
    #         pygame.draw.line(screen, BLACK, (i, j), (i + size*np.cos(grid[idx, jdx]), j + size * np.sin(grid[idx, jdx])))

    increment = 20
    for i in range(left_x, right_x, increment):
        for j in range(top_y, bottom_y, increment):
            draw_curve(i, j, steps = 25, step_len = 6, col = COL_PAL[1])
        pygame.display.update()

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
    pygame.display.update()
    iteration += 1
