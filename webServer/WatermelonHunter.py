import pygame
import random

# Initialize Pygame
pygame.init()

# Set the screen size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title
pygame.display.set_caption("Super Mario Clone")

# Define the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load the images
player_image = pygame.image.load("mario.png")
player_rect = player_image.get_rect()

# Set the player's initial position
player_rect.x = 50
player_rect.y = 50

# Define the game loop
game_running = True
while game_running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Clear the screen
    screen.fill(WHITE)

    # Draw the player
    screen.blit(player_image, player_rect)

    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()