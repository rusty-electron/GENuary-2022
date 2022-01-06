import random
import pygame

pygame.init()

size = width, height = 600, 600
center_x = width // 2
center_y = height // 2

screen = pygame.display.set_mode(size)
FPS = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

class Circle(pygame.sprite.Sprite):
    def __init__(self, start, radius, color):
        super().__init__()
        self.start = start
        self.radius = radius
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.start, self.radius)
        pygame.draw.circle(screen, BLACK, self.start, self.radius, width=1)

# colors
BLACK = (0, 0, 0)
SOFT_BLACK = (43, 48, 58)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 224, 102)
RED = (255, 0, 0)

COLORS = [
        (232, 219, 125),
        (85, 140, 140),
        (229, 205, 200),
        (25, 133, 161),
        (252, 208, 161),
        (175, 210, 233),
        (200, 29, 37),
        (236, 5, 142),
        (222, 186, 111),
        ]

# initialize
circles_grp = pygame.sprite.Group()
CURRENT_RADIUS = 50
CURRENT_POS = [center_x + random.randint(5, 10), center_y + random.randint(5, 10)]
CURRENT_COL = random.choice(COLORS)
PUSH = 6
DIRECTION = (random.randint(-2, 2) * PUSH, random.randint(-2, 2) * PUSH)

start_time = pygame.time.get_ticks()

running = True
while running:
    screen.fill(SOFT_BLACK)

    for c in circles_grp:
        c.draw(screen)

    # draw every 80 ms
    if (pygame.time.get_ticks() - start_time) > 80:
        if CURRENT_RADIUS > 3:
            CURRENT_RADIUS -= 5
            offset = 15
            CURRENT_POS = (CURRENT_POS[0] + random.randint(-offset, offset) + DIRECTION[0], CURRENT_POS[1] + random.randint(-offset, offset) + DIRECTION[1])

            next_circ = Circle(CURRENT_POS, CURRENT_RADIUS, CURRENT_COL)
            circles_grp.add(next_circ)
            start_time = pygame.time.get_ticks()
        else:
            # if one series has ended, reset the radius and start another
            CURRENT_COL = random.choice(COLORS)
            CURRENT_RADIUS = 50
            CURRENT_POS = [center_x + random.randint(-80, 80), center_y + random.randint(-80, 80)]
            DIRECTION = (random.randint(-2, 2) * PUSH, random.randint(-2, 2) * PUSH)

        if len(circles_grp) > 3000:
            circles_grp = circles_grp[-3000:]

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # press R to reset the canvas
                circles_grp.empty()
                CURRENT_RADIUS = 50
                CURRENT_POS = [center_x + random.randint(5, 10), center_y + random.randint(5, 10)]
                CURRENT_COL = random.choice(COLORS)

                start_time = pygame.time.get_ticks()

    clock.tick(FPS)
    pygame.display.update()
