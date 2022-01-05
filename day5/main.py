import random
import pygame

pygame.init()

size = width, height = 600, 900

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

PALLETE = [
        (62, 146, 204),
        (154, 52, 142),
        (188, 231, 132),
        (252, 215, 173)
        ]

MULTI = 2

class RecursiveSquare(pygame.sprite.Sprite):
    def __init__(self, size, start, col=(255, 255, 255)):
        super().__init__()
        self.size = size
        self.start = pygame.Vector2(start)
        self.rect = pygame.Rect(self.start.x, self.start.y, self.size, self.size)
        self.col = col
        self.vel = random.randint(3, 10)

    def draw(self, screen):
        pygame.draw.rect(screen, self.col, self.rect, width = 2)

    def update(self):
        self.rect.move_ip(0, self.vel)
        if self.rect.top - self.start.y > 200:
            self.kill()
            side_size = self.size // MULTI
            if side_size > 1:
                for idx in range(MULTI):
                    start = (self.rect.left + idx * side_size + 1, self.rect.bottom - 1.5 * side_size)
                    sq = RecursiveSquare(side_size, start, \
                            col = self.col)
                    squares.add(sq)

SQ_SIZE = 100
squares = pygame.sprite.Group()

def generate_squares():
    for i in range(width//SQ_SIZE):
        sq = RecursiveSquare(SQ_SIZE, (i * SQ_SIZE + 1, -100), random.choice(PALLETE))
        squares.add(sq)

generate_squares()
start_time = pygame.time.get_ticks()

iteration = 0
running = True

while running:
    screen.fill(BLACK)

    if pygame.time.get_ticks() - start_time > 800:
        generate_squares()
        start_time = pygame.time.get_ticks()

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for sq_obj in squares:
        sq_obj.draw(screen)
        sq_obj.update()

    clock.tick(FPS)
    pygame.display.update()
