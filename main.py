import sys
import pygame
import time
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags = pygame.SCALED)
    background_image = pygame.image.load("images/background.jpg").convert()
    background_image = pygame.transform.scale(background_image, (1280, 720))
    clock = pygame.time.Clock()
    dt = 0
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    asteroids = pygame.sprite.Group()
    Asteroid.containers = (asteroids, updatable, drawable)

    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    shots = pygame.sprite.Group()
    Shot.containers = (shots, updatable, drawable)

    game_over = False
    game_over_time = 0
    countdown_time = 3
    countdown_started = False
    countdown_start_time = 0
    countdown_running = True
    show_game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.blit(background_image, (0, 0))

        if countdown_running:
            if not countdown_started:
                countdown_start_time = pygame.time.get_ticks()
                countdown_started = True

            elapsed_time = (pygame.time.get_ticks() - countdown_start_time) / 1000

            if elapsed_time < 1:
                display_text = "3"
            elif elapsed_time < 2:
                display_text = "2"
            elif elapsed_time < 3:
                display_text = "1"
            elif elapsed_time < 4:
                display_text = "START"
            else:
                countdown_running = False

            font = pygame.font.Font(None, 74)
            text = font.render(display_text, True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2))
        
        elif game_over:
            if not show_game_over:
                game_over_time = pygame.time.get_ticks()
                show_game_over = True

            elapsed_game_over = (pygame.time.get_ticks() - game_over_time) / 1000
            
            if elapsed_game_over < 3:
                font = pygame.font.Font(None, 74)
                text = font.render("GAME OVER", True, (255, 0, 0))
                screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2))
            else:
                running = False
        
        else:
            updatable.update(dt)
            
            for asteroid in asteroids:
                if player.collides_with(asteroid):
                    print("Game over!")
                    game_over = True
                    game_over_time = time.time()
                    break

                for bullet in shots:
                    if asteroid.collides_with(bullet):
                        bullet.kill()
                        asteroid.split()
            
            for drawable_object in drawable:
                drawable_object.draw(screen)

        pygame.display.flip()
        dt = clock.tick(120) / 1000

if __name__ == "__main__":
    main()