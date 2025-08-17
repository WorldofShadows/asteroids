import pygame
import sys
from constants import *
from player import *
from asteroid import *
from asteroidsfield import *

def main():
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (drawable,updatable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (updatable,drawable, shots)
    AsteroidField.containers = (updatable)  # Nur updatable!

     # Instantiate the player once, outside the loop
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroid_field = AsteroidField()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
         # Alle Objekte updaten
        for obj in updatable:
            obj.update(dt)


        # Clear the screen
        screen.fill((0, 0, 0))

        for asteroid in asteroids:
            if player.collides_with(asteroid):
                print("Game over!")
                pygame.quit()
                sys.exit()
        
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    new_asteroids = asteroid.split()
                    shot.kill()
                    if new_asteroids:
                        for new in new_asteroids:
                            for container in Asteroid.containers:
                                container.add(new)
            
        # Alle Objekte zeichnen
        for obj in drawable:
            obj.draw(screen)


 
        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        dt = clock.tick(60) / 1000
       


if __name__ == "__main__":
    main()
