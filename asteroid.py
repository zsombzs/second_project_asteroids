import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        self.image = pygame.image.load("asteroid.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (radius * 2, radius * 2))

    def draw(self, screen):
        screen.blit(self.image, self.position - pygame.Vector2(self.radius, self.radius))

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            random_angle = random.uniform(20, 50)
            a = self.velocity.rotate(random_angle)
            b = self.velocity.rotate(-random_angle)

            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid.velocity = a * 1.8
            asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid.velocity = b * 1.8


