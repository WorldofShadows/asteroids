import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        #self.image = pygame.Surface((radius * 2, radius * 2))
        #self.rect = self.image.get_rect(center=(x, y))
        #self.radius = radius
        self.position = pygame.Vector2(x, y)
        self.image = pygame.Surface((radius * 2, radius * 2))  
        self.rect = self.image.get_rect(center=self.position)
        self.radius = radius
        self.alive = True
        
    
    def draw(self, surface):
        pygame.draw.circle(surface, (200, 200, 200), self.rect.center, self.radius, 2)

    def kill(self):
        self.alive = False
    
    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(20, 50)

        # Erzeuge eine zufällige Basisgeschwindigkeit
        base_speed = 100
        direction = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))

        vel1 = direction.rotate(random_angle) * base_speed
        vel2 = direction.rotate(-random_angle) * base_speed

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        x, y = self.position

        asteroid1 = Asteroid(x, y, new_radius)
        asteroid1.velocity = vel1

        asteroid2 = Asteroid(x, y, new_radius)
        asteroid2.velocity = vel2

        return [asteroid1, asteroid2]


    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = self.position