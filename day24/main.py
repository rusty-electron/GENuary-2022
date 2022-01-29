import pygame

from prng_function import prng

pygame.init()

size = width, height = 800, 800

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

class randomWalker(pygame.sprite.Sprite):
    def __init__(self, start_loc=(width//2, height//2)):
        super().__init__()
        self.current_loc = start_loc
        self.trail = []
        self.color = WHITE
        self.trail.append(start_loc)
        self.step = 5

    def move(self):
        direction = prng(num_range=4)
        if direction == 0:
            x, y = 0, 1
        elif direction == 1:
            x, y = 1, 0
        elif direction == 2:
            x, y = 0, -1
        else:
            x, y = -1, 0

        x_coord = self.current_loc[0] + x * self.step
        y_coord = self.current_loc[1] + y * self.step

        # wrap around!!
        if x_coord > width or y_coord > height or x_coord < 0 or y_coord < 0:
            if x_coord > width:
                new_loc = [width - 1, y_coord]
                self.trail.append(new_loc)
                self.trail.append(None)

                new_loc = [0, y_coord]
                self.trail.append(new_loc)
                new_loc = [abs(x_coord % width), y_coord]
                self.trail.append(new_loc)
            if x_coord < 0:
                new_loc = [0, y_coord]
                self.trail.append(new_loc)
                self.trail.append(None)

                new_loc = [width - 1, y_coord]
                self.trail.append(new_loc)
                new_loc = [abs(x_coord % width), y_coord]
                self.trail.append(new_loc)

            if y_coord > height:
                new_loc = [x_coord, height - 1]
                self.trail.append(new_loc)
                self.trail.append(None)

                new_loc = [x_coord, 0]
                self.trail.append(new_loc)
                new_loc = [x_coord, abs(y_coord % height)]
                self.trail.append(new_loc)
            if y_coord < 0:
                new_loc = [x_coord, 0]
                self.trail.append(new_loc)
                self.trail.append(None)

                new_loc = [x_coord, height - 1]
                self.trail.append(new_loc)
                new_loc = [x_coord, abs(y_coord % height)]
                self.trail.append(new_loc)
        else:
            new_loc = [x_coord, y_coord]
            self.trail.append(new_loc)

        self.current_loc = new_loc

    def draw(self, screen):
        size_of_trail = len(self.trail)
        if size_of_trail > 0:
            for i in range(1, size_of_trail):
                if self.trail[i - 1] != None and self.trail[i] != None:
                    pygame.draw.line(screen, self.color, self.trail[i - 1], self.trail[i])

walker1 = randomWalker((width, height//2))
walkerGroup = pygame.sprite.Group()

walkerGroup.add(walker1)

while running:
    screen.fill(BLACK)

    # handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for walker in walkerGroup:
        walker.move()
        walker.draw(screen)

    clock.tick(FPS)
    pygame.display.update()
