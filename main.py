import pygame
import random
# Initialize Pygame
pygame.init()
# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("GET_CODE_ARYAN")
# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
gray = (50, 50, 50)
# Game variables
clock = pygame.time.Clock()
game_speed = 3
# Player truck properties
truck_width = 50
truck_height = 100
player_truck_speed = 7
# Opponent car properties
opponent_width = 50
opponent_height = 100
def draw_truck(x, y):
    """Draws the player's truck."""
    pygame.draw.rect(screen, white, [x, y, truck_width, truck_height])
def draw_opponent(opponent):
    """Draws an opponent car."""
    pygame.draw.rect(screen, red, opponent)
def display_score(count):
    """Displays the current score on the screen."""
    font = pygame.font.Font(None, 35)
    text = font.render("Score: " + str(count), True, white)
    screen.blit(text, (10, 10))
def show_game_over_screen(score):
    """Displays Game Over message and restart/quit options."""
    screen.fill(gray)
    font_large = pygame.font.Font(None, 80)
    font_small = pygame.font.Font(None, 40)
    game_over_text = font_large.render("GAME OVER", True, red)
    score_text = font_small.render(f"Final Score: {score}", True, white)
    restart_text = font_small.render("Press R to Restart or Q to Quit", True, white)
    # Center texts
    screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, 200))
    screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2, 320))
    screen.blit(restart_text, (screen_width / 2 - restart_text.get_width() / 2, 400))
    pygame.display.update()
    # Wait for user choice
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    game_loop()  # restart
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
def game_loop():
    """Main game loop."""
    score = 0
    game_exit = False
    player_truck_x = (screen_width / 2) - (truck_width / 2)
    player_truck_y = screen_height - truck_height - 20
    player_truck_x_change = 0
    opponents = []
    opponent_spawn_timer = 0
    opponent_spawn_rate = 60  # spawn every 60 frames
    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # Handle player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_truck_x_change = -player_truck_speed
                elif event.key == pygame.K_RIGHT:
                    player_truck_x_change = player_truck_speed
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player_truck_x_change = 0
        # Update player position
        player_truck_x += player_truck_x_change
        # Boundary check for player truck
        if player_truck_x < 0:
            player_truck_x = 0
        elif player_truck_x > screen_width - truck_width:
            player_truck_x = screen_width - truck_width
        # Spawn new opponent cars
        opponent_spawn_timer += 1
        if opponent_spawn_timer >= opponent_spawn_rate:
            opponent_spawn_timer = 0
            opponent_x = random.randrange(0, screen_width - opponent_width)
            opponent_y = -opponent_height  # start above the screen
            opponents.append(pygame.Rect(opponent_x, opponent_y, opponent_width, opponent_height))
        # Update opponent positions and remove off-screen opponents
        for opponent in list(opponents):
            opponent.y += game_speed
            if opponent.y > screen_height:
                opponents.remove(opponent)
                score += 1     
        # Check for collisions
        player_rect = pygame.Rect(player_truck_x, player_truck_y, truck_width, truck_height)
        for opponent in opponents:
            if player_rect.colliderect(opponent):
                show_game_over_screen(score)
                return  # stop current loop
        # Drawing everything
        screen.fill(black)
        draw_truck(player_truck_x, player_truck_y)
        for opponent in opponents:
            draw_opponent(opponent)
        display_score(score)
        pygame.display.update()
        clock.tick(120)  # 60 FPS

# Start the game
if __name__ == "__main__":
    game_loop()
