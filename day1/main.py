import sys, time
import pygame
import numpy as np

numbers = np.random.randint(low = 1, high = 1000, size = 10000)
lvl = np.zeros_like(numbers)

pygame.init()
size = width, height = 800, 800

screen = pygame.display.set_mode(size)

center_x, center_y = width // 2, height // 2

clock = pygame.time.Clock()

# constants
WHITE = (255, 255, 255)
BLACK = (50, 50, 44)
BLUE = (93, 183, 222)
RED = (214, 73, 51)

running = True
iteration = 0
angle = 0
numbers_size = len(numbers)
idx_vals = np.arange(numbers_size)
sleeping = []

while running:
    screen.fill(BLACK)
    print(len(sleeping))

    # calculate 2d coordinates
    x_vals = numbers * np.sin((2 * np.pi * idx_vals)/(numbers_size - 1) + angle)
    y_vals = numbers * np.cos((2 * np.pi * idx_vals)/(numbers_size - 1) + angle)

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for pos, (x, y) in enumerate(zip(x_vals, y_vals)):
            if lvl[pos] == 0:
                pygame.draw.circle(screen, WHITE, (x/2 + center_x, y/2 + center_y), 1)
            elif lvl[pos] == 1:
                pygame.draw.circle(screen, BLUE, (x/2 + center_x, y/2 + center_y), 1)
            elif lvl[pos] == 2:
                pygame.draw.circle(screen, RED, (x/2 + center_x, y/2 + center_y), 1)
            elif lvl[pos] > 2:
                if (np.random.randn() <= 0.2):
                    lvl[pos] += np.iinfo(np.int32).min # smallest possible int32 value
                    sleeping.append(pos)
                else:
                    if len(sleeping) > 0:
                        awake = np.random.choice(sleeping, size = 1)
                        lvl[awake] = 0
                        sleeping.remove(awake)

    if iteration % 5 == 0:
        # how many will evolve
        evolve_num = np.random.randint(3, 50, size=1)
        # which will evolve
        evolve_idxs = np.random.choice(idx_vals, size = evolve_num)
        lvl[evolve_idxs] += 1

    iteration += 1
    pygame.display.update()
    clock.tick(30)
    angle = (angle + np.pi/400) % (2 * np.pi)

pygame.quit()
