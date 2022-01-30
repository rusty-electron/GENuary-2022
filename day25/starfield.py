import pygame
import random

GRAY = (108, 111, 125)
class Star(pygame.sprite.Sprite):
    def __init__(self, s_width, s_height, color):
        super().__init__()
        self.color = color
        self.s_width = s_width
        self.s_height = s_height

        self.x = random.randint(-self.s_width//2, self.s_width//2)
        self.y = random.randint(-self.s_height//2, self.s_height//2)
        self.z = random.randint(0, s_width)
        self.step = 15
        self.prev_z = None

    def update(self):
        self.prev_z = self.z
        self.z -= self.step
        if self.z < 1:
            self.x = random.randint(-self.s_width//2, self.s_width//2)
            self.y = random.randint(-self.s_height//2, self.s_height//2)
            self.z = self.s_width
            self.prev_z = None

    def translate(self, x, y):
        """
        emulate the shifting of origin to the center of the screen
        """
        return (x + self.s_width // 2, y + self.s_height // 2)

    def draw(self, screen):
        scaled_x = (self.x / self.z) * self.s_width
        scaled_y = (self.y / self.z) * self.s_height

        radius = (1 - self.z/self.s_width) * 6

        if self.prev_z is not None:
            scaled_x_p = (self.x / self.prev_z) * self.s_width
            scaled_y_p = (self.y / self.prev_z) * self.s_height
            pygame.draw.line(screen, GRAY, self.translate(scaled_x, scaled_y), self.translate(scaled_x_p, scaled_y_p), 2)

        pygame.draw.circle(screen, self.color, self.translate(scaled_x, scaled_y), radius)
