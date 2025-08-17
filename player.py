import pygame
from circleshape import CircleShape
from constants import *
from shots import *

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0.0

    def triangle(self):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)  # -1 for upward facing
        right = forward.rotate(90) * self.radius / 1.5

        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right

        return [a, b, c]

    def draw(self, surface):
        pygame.draw.polygon(surface, (255, 255, 255), self.triangle())

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt


    def shoot(self):

        if self.shoot_timer > 0:
            return None  # Kein Schuss, Cooldown aktiv

     # Richtung berechnen (nach vorne, relativ zur Rotation)
        direction = pygame.Vector2(0, -1).rotate(self.rotation)

        # Geschwindigkeit skalieren
        velocity = direction * PLAYER_SHOOT_SPEED

        # Position leicht nach vorne versetzen, damit der Schuss aus der Spitze kommt
        offset = direction * self.radius
        shot_position = self.position + offset
        #Cooldown, damit die Waffe nicht overpowered ist
        if self.shoot_timer <= 0:
            self.shoot_timer = PLAYER_SHOOT_COOLDOWN

        # Shot erzeugen
        shot = Shot(shot_position.x, shot_position.y, velocity)
        return shot
            
    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(-dt)
        if keys[pygame.K_s]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            #self.shoot()
            shot = self.shoot()
            if shot:
                shot.add(*Shot.containers) 
        if self.shoot_timer > 0:
            self.shoot_timer -= dt