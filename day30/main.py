import pygame
import random

pygame.init()

SIZE = WIDTH, HEIGHT = 800, 800

FPS = 30
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)

vec = pygame.math.Vector2

# colors
BLACK = (43, 48, 58)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 224, 102)
RED = (255, 0, 0)

FISH_IMG_PATH = "./fish_scaled.png"

class Boid(pygame.sprite.Sprite):
    def __init__(self, position = None, size = (12, 15), debug = False):
        super().__init__()
        if position == None:
            self.position = (random.randint(0, WIDTH), random.randint(0, HEIGHT))
        else:
            self.position = position

        self.debug = debug
        self.speed = 5
        self.angle = random.randint(0, 360) # in degrees
        # self.angle = 135

        self.image = pygame.image.load(FISH_IMG_PATH)
        self.image = pygame.transform.scale(self.image, size)
        self.image = pygame.transform.rotate(self.image, self.angle + 180)

        self.rect = self.image.get_rect()
        self.rect.center = self.position
        if self.debug:
            self.image.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD)


    def update(self):
        self.vel = vec(1, 0).rotate(self.angle).normalize() * self.speed
        self.vel[1] = - self.vel[1]
        self.rect.move_ip(self.vel)

        c_x = self.rect.center[0]
        c_y = self.rect.center[1]

        if c_x > WIDTH or c_x < 0:
            c_x = abs(c_x % WIDTH)
        if c_y > HEIGHT or c_y < 0:
            c_y = abs(c_y % HEIGHT)

        self.rect.center = (c_x, c_y)

    def avoid(self, other, screen):
        """
        try to avoid other boids
        """
        # vector pointing to the center of the current boid
        other_vector = vec(other.rect.center)
        # vector pointing to the center of the other boid
        self_vector = vec(self.rect.center)
        # distance between the above two vector, i.e. distance between the current boid_object
        # the other boid
        dist = other_vector.distance_to(self_vector)
        # the code below has been hacked together and i fully don't understand it. I will understand
        # it and then comment :(
        diff_vector = self_vector - other_vector
        self_heading_vector = vec(self.vel)
        angle_from_source = diff_vector.angle_to(-self_heading_vector)

        if dist < 50 and abs(angle_from_source) < 90 :
            if self.debug:
                pygame.draw.line(screen, RED, other.rect.center, self.rect.center)

flock = pygame.sprite.Group()

for _ in range(100):
    b1 = Boid()
    flock.add(b1)

# for debugging
b_bug = Boid(debug = True)
flock.add(b_bug)

running = True

while running:
    screen.fill(BLACK)

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for boid_object in flock:
        screen.blit(boid_object.image, boid_object.rect)
        boid_object.update()
        rest_of_flock = flock.copy()
        rest_of_flock.remove(boid_object)
        for other_obj in rest_of_flock:
            boid_object.avoid(other_obj, screen)

    clock.tick(FPS)
    pygame.display.update()
