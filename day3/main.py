from hashlib import new
import pygame
import random as rng

pygame.init()

size = width, height = 800, 800

screen = pygame.display.set_mode(size)
FPS = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
center_x, center_y = width // 2, height // 2

# constants - imaginary universe
C_CONST = 30
G_CONST = 6
dt = 0.1

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 255, 0)

class BlackHole(pygame.sprite.Sprite):
    def __init__(self, x, y, m = 3000):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.mass = m
        self.rs = 2 * G_CONST * self.mass / (C_CONST ** 2)

    def draw(self, screen):
        # draw black hole
        pygame.draw.circle(screen, WHITE, self.pos, self.rs)
        # draw photon orbit
        pygame.draw.circle(screen, YELLOW, self.pos, self.rs * 1.5 + 12, width = 8)
        # draw accretion disc
        pygame.draw.circle(screen, GRAY, self.pos, self.rs * 3, width = 11)

    def pull(self, photon):
        force = self.pos - photon.pos
        distance = force.length()
        fg = (G_CONST * self.mass) / (distance ** 2)
        force = force.normalize() * fg
        photon.vel += force
        photon.vel = photon.vel.normalize() * C_CONST

class Photon(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.vel = pygame.Vector2(-C_CONST, 0);

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, self.pos, 1)

    def update(self):
        delta_v = self.vel
        delta_v = delta_v * dt
        self.pos += delta_v

        # remove if out of bounds
        if self.pos.x < - 2 * width or self.pos.x > 2 * width or \
            self.pos.y < - 2 * height or self.pos.y > 2 * height:
            photons.remove(self)

# instantiation
bh = BlackHole(center_x, center_y)

# create photon particles
PH_LIMIT = 5000
photons = []
x_gen_range = list(range(-50, 0)) + list(range(width, width+50))
y_gen_range = list(range(-50, 0)) + list(range(width, height+50))
full_x_range = list(range(-50, width+50))
full_y_range = list(range(-50, height+50))

def generate_photon():
    if _ % 2 == 0:
        new_ph = Photon(rng.choice(x_gen_range), rng.choice(full_y_range))
    else:
        new_ph = Photon(rng.choice(full_x_range), rng.choice(y_gen_range))
    offset = 50
    if new_ph.pos.x > 0 and new_ph.pos.y > 0:
        new_ph.vel = - pygame.Vector2(rng.randint(0 + offset, width - offset), \
                rng.randint(0 + offset, height - offset)).normalize()
    else:
        new_ph.vel = pygame.Vector2(rng.randint(0 + offset, width - offset), \
                rng.randint(0 + offset, height - offset)).normalize()
    photons.append(new_ph)

for _ in range(PH_LIMIT):
    generate_photon()

running = True
while running:
    while len(photons) < PH_LIMIT:
        generate_photon()
    screen.fill(BLACK)
    bh.draw(screen)
    for ph in photons:
        bh.pull(ph)
        ph.draw(screen)
        ph.update()
        if (ph.pos - bh.pos).length() < 4:
            photons.remove(ph)

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(FPS)
    pygame.display.update()
