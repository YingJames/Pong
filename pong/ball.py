import pygame

class Ball:
    RADIUS = 7
    INIT_VEL = 5
    MAX_VEL = 13
    COLOR = (255, 255, 255)

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.INIT_VEL
        self.y_vel = 0

    def draw(self, window):
        pygame.draw.circle(window, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def flip(self, x_vel) -> int:
        flipped_x_vel = -self.MAX_VEL if x_vel > 0 else self.MAX_VEL
        return flipped_x_vel

    def reset(self, final_x):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel = self.INIT_VEL if final_x > 0 else -self.INIT_VEL