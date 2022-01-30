import pygame

from starfield import Star

pygame.init()

SIZE = WIDTH, HEIGHT = 800, 800

FPS = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)

# colors
BLACK = (43, 48, 58)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 224, 102)
RED = (255, 0, 0)

running = True

star_group = pygame.sprite.Group()
for _ in range(600):
    star_group.add(Star(WIDTH, HEIGHT, WHITE))

while running:
    screen.fill(BLACK)

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for star_object in star_group:
        star_object.update()
        star_object.draw(screen)

    clock.tick(FPS)
    pygame.display.update()
pygame.quit()
