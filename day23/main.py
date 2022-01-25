import pygame

pygame.init()

size = width, height = 700, 700

screen = pygame.display.set_mode(size)
FPS = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)

# colors
BLACK = (43, 48, 58)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 224, 102)
RED = (255, 0, 0)

running = True

while running:
    screen.fill(BLACK)

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
    pygame.display.update()
