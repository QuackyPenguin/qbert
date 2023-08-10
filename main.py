import pygame
from game_logic import initialize_game, draw

# Constants
GAME_WINDOW_WIDTH = 1024
GAME_WINDOW_HEIGHT = 768

# Initialize pygame and game elements
pygame.init()
game_window = pygame.display.set_mode((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT), 0, 32)
caption = 'Q*bert'
pygame.display.set_caption(caption)
initialize_game(game_window)

# Game loop
running = True
while running:
    pygame.time.delay(25)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    draw()
    pygame.display.update()
    if level_completed:
        player.x, player.y, player.image = x_center - CUBE_SIZE * 3 // 8, y_center - CUBE_SIZE * 3 // 8, imagePlayerLeftDown
        level_completed = False
    if player.lives == 0:
        initialize_game(game_window)
pygame.quit()