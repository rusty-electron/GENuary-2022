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

FISH_IMG_PATHS = ["./assets/fish_scaled.png",
                  "./assets/fish_scaled_light.png",
                  "./assets/fish_scaled_dark.png"]
PERCEPTION_RADIUS = 40
PERCEPTION_ANGLE = 90 # note that this is half of the actual percetion angle

MAX_VEL = 15

class Boid(pygame.sprite.Sprite):
    def __init__(self, position = None, size = (12, 12), debug = False):
        super().__init__()
        # if no position argument is provided, assign a random position to it
        if position == None:
            self.position = vec(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        else:
            self.position = vec(position)

        # for debugging
        self.debug = debug
        # randomly initialize and then turn it into a unit vector
        self.vel = (vec(random.randint(-1, 1), random.randint(-1, 1)) + vec(0.001, 0.001)).normalize()

        self.vel_magnitude = random.randint(3, MAX_VEL)
        self.vel.scale_to_length(self.vel_magnitude)

        # a vector for storing the acceleration
        self.acc = vec()

        # sprite's rotation vector is determined from the velocity vector
        self.angle = self.vel.angle_to([1, 0])

        self.saved_image = pygame.image.load(random.choice(FISH_IMG_PATHS))
        self.saved_image = pygame.transform.scale(self.saved_image, size)
        self.image = pygame.transform.rotate(self.saved_image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def rot_center(self):
        """
        bug free rotation code
        """
        self.image = pygame.transform.rotate(self.saved_image, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

    def update(self):
        self.vel += self.acc
        self.vel = clamp_vector(self.vel, MAX_VEL)
        self.rot_center() # damn, figuring this out took a lot of time! T_T

        if self.debug:
            self.image.fill((190, 0, 0, 100), special_flags=pygame.BLEND_ADD)
        self.rect.move_ip(self.vel)
        self.angle = self.vel.angle_to([1, 0])
        self.position = vec(self.rect.center) # update the position vector

        # screen wrapping
        c_x = self.rect.center[0]
        c_y = self.rect.center[1]

        if c_x > WIDTH or c_x < 0:
            c_x = abs(c_x % WIDTH)
        if c_y > HEIGHT or c_y < 0:
            c_y = abs(c_y % HEIGHT)

        self.rect.center = (c_x, c_y)
        self.acc *= 0

    def is_boid_in_range(self, other, radius = PERCEPTION_RADIUS):
        """
        check if the other boid is within perception
        """
        withinRange = False
        # vector pointing to the center of the current boid
        other_vector = vec(other.rect.center)
        # vector pointing to the center of the other boid
        self_vector = vec(self.rect.center)
        # distance between the above two vector, i.e. distance between the current boid_object
        # the other boid
        dist = other_vector.distance_to(self_vector)
        # diff_vector is a vector than points from self to the other boid's position vector
        diff_vector = ((other_vector - self_vector) + vec(0.001, 0.001)).normalize()
        self_heading_vector = self.vel.normalize() # self's heading vector

        angle_from_source = diff_vector.angle_to(self_heading_vector)

        if dist < radius and abs(angle_from_source) < PERCEPTION_ANGLE:
            withinRange = True
        return withinRange

    def separate(self, rest):
        steering = vec() # to store the sum of the velocity vector of other nearby boids
        total = 0 # keep count of such boids
        for other_boid in rest:
            if self.is_boid_in_range(other_boid, radius = 60):
                dist = self.position.distance_to(other_boid.position) + 0.0001
                dir_diff = self.position - other_boid.position
                dir_diff = dir_diff / (dist * dist)
                steering += dir_diff
                total+=1
        if total > 0:
            steering = steering/total
            if steering.length() != 0:
                steering.scale_to_length(MAX_VEL) # fixes stuck flocks
            steering = steering - self.vel
            steering = clamp_vector(steering, 1)
        return steering

    def align(self, rest):
        steering = vec() # to store the sum of the velocity vector of other nearby boids
        total = 0 # keep count of such boids
        for other_boid in rest:
            if self.is_boid_in_range(other_boid):
                steering += other_boid.vel
                total+=1
        if total > 0:
            steering = steering/total
            if steering.length() != 0:
                steering.scale_to_length(MAX_VEL) # fixes stuck flocks
            steering = steering - self.vel
            steering = clamp_vector(steering, 1)
        return steering

    def cohesion(self, rest):
        steering = vec() # to store the sum of the position vectors of other nearby boids
        total = 0 # keep count of such boids
        for other_boid in rest:
            if self.is_boid_in_range(other_boid, radius = 150):
                steering += other_boid.position
                total+=1
        if total > 0:
            steering = steering/total
            steering -= self.position
            if steering.length() != 0:
                steering.scale_to_length(MAX_VEL)
            steering = steering - self.vel
            steering = clamp_vector(steering, 1)
        return steering

def clamp_vector(in_vector, max_len):
    """
    clamps a vector's magnitude at a maximum value
    """
    magnitude = in_vector.length()
    if magnitude > max_len:
        unit_vector = in_vector.normalize()
        unit_vector.scale_to_length(max_len)
        return unit_vector
    return in_vector

flock = pygame.sprite.Group()

for _ in range(100):
    b1 = Boid()
    flock.add(b1)

# for debugging
# b_bug = Boid(debug = True)
# flock.add(b_bug)

# GAME LOOP
running = True
MULTIPLIERS = [1, 0.40, 0.95]
while running:
    screen.fill(BLACK)

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for boid_object in flock:
        rest_of_flock = flock.copy()
        rest_of_flock.remove(boid_object)

        align_acc = boid_object.align(rest_of_flock)
        cohesion_acc = boid_object.cohesion(rest_of_flock)
        separate_acc = boid_object.separate(rest_of_flock)

        boid_object.acc += align_acc * MULTIPLIERS[0]
        boid_object.acc += cohesion_acc * MULTIPLIERS[1]
        boid_object.acc += separate_acc * MULTIPLIERS[2]

        boid_object.update()
        screen.blit(boid_object.image, boid_object.rect)

    clock.tick(FPS)
    pygame.display.update()
